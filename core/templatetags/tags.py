from django import template
register = template.Library()

def mod(value):
    return int(value) % 10

register.filter('mod', mod)