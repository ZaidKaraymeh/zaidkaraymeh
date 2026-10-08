from django.core.management.base import BaseCommand

from core.models import MediaClick, PageVisit
from core.tracking import _lookup


class Command(BaseCommand):
    help = 'Fill in country and city for logged visits and clicks that are missing them.'

    def handle(self, *args, **options):
        models = (PageVisit, MediaClick)
        ips = set()
        for model in models:
            ips.update(
                model.objects.filter(country='').exclude(ip=None).values_list('ip', flat=True)
            )

        filled = missing = 0
        for ip in sorted(ips):
            geo = _lookup(ip)
            if not geo or not geo[0]:
                missing += 1
                continue
            country, code, city = geo
            for model in models:
                model.objects.filter(ip=ip, country='').update(
                    country=country, country_code=code, city=city
                )
            filled += 1

        self.stdout.write(f'{filled} IPs filled, {missing} still unknown, out of {len(ips)}.')
