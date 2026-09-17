import ipaddress
import json
import logging
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

from django.db import connection

from .models import PageVisit

logger = logging.getLogger(__name__)

SKIP_PREFIXES = ('/static/', '/media/', '/admin/', '/favicon.ico')
GEO_ENDPOINT = 'https://ipwho.is/{ip}?fields=success,country,country_code,city'

_executor = ThreadPoolExecutor(max_workers=2, thread_name_prefix='geo')
_geo_cache = {}


def client_ip(request):
    """First public-looking address in the proxy chain Railway hands us."""
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR', '')
    candidates = [part.strip() for part in forwarded.split(',') if part.strip()]
    candidates.append(request.META.get('REMOTE_ADDR', '') or '')
    for candidate in candidates:
        try:
            ipaddress.ip_address(candidate)
        except ValueError:
            continue
        return candidate
    return None


def _is_private(ip):
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        return True


def _lookup(ip):
    if ip in _geo_cache:
        return _geo_cache[ip]

    if _is_private(ip):
        geo = ('Local network', '', '')
    else:
        try:
            with urllib.request.urlopen(GEO_ENDPOINT.format(ip=ip), timeout=4) as response:
                payload = json.load(response)
        except (urllib.error.URLError, OSError, ValueError, TimeoutError):
            # A failed lookup is not cached so the next visit can retry.
            return None
        if not payload.get('success'):
            return None
        geo = (
            payload.get('country') or '',
            (payload.get('country_code') or '')[:2],
            payload.get('city') or '',
        )

    if len(_geo_cache) > 1000:
        _geo_cache.clear()
    _geo_cache[ip] = geo
    return geo


def cached_geo(ip):
    """Country already known for this IP, if we have looked it up before."""
    return _geo_cache.get(ip) if ip else None


def _resolve(model, obj_id, ip):
    try:
        geo = _lookup(ip)
        if not geo or not geo[0]:
            return
        country, code, city = geo
        # Backfill every earlier row from this IP that is still missing a country.
        model.objects.filter(ip=ip, country='').update(
            country=country, country_code=code, city=city
        )
        model.objects.filter(pk=obj_id).update(
            country=country, country_code=code, city=city
        )
    except Exception:
        logger.debug('geo lookup failed for %s', ip, exc_info=True)
    finally:
        connection.close()


def resolve_geo_later(model, obj_id, ip):
    """Fill in the country off the request thread so nobody waits on it."""
    if ip:
        _executor.submit(_resolve, model, obj_id, ip)


class VisitLogMiddleware:
    """Records page views. Never alters the response the visitor gets."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        try:
            self._record(request, response)
        except Exception:
            logger.debug('visit tracking failed', exc_info=True)
        return response

    def _record(self, request, response):
        if request.method != 'GET' or response.status_code >= 400:
            return
        if request.path.startswith(SKIP_PREFIXES):
            return
        if 'text/html' not in response.get('Content-Type', ''):
            return

        ip = client_ip(request)
        geo = cached_geo(ip)
        visit = PageVisit.objects.create(
            path=request.path[:500],
            ip=ip,
            country=geo[0] if geo else '',
            country_code=geo[1] if geo else '',
            city=geo[2] if geo else '',
            referrer=request.META.get('HTTP_REFERER', '')[:500],
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:400],
        )
        if not geo:
            resolve_geo_later(PageVisit, visit.pk, ip)
