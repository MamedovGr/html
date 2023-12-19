from django import template
from datetime import datetime
from django.conf import settings
from main.models import Store

register = template.Library()

@register.filter(name='times')
def times(number):
    return range(number)

@register.filter(name='expiration')
def expiration(expiration_date):
    delta = expiration_date - datetime.now()
    return delta.days

@register.filter(name='expiration_m')
def expiration_m(expiration_date):
    delta = expiration_date - datetime.now()
    return delta.total_seconds() // 60

@register.filter(name='get_list')
def get_list(value):
    splited = value.strip('][').split(', ')
    trimed = [ v.replace("'", '') for v in splited ]
    return trimed

@register.filter(name='count')
def count(array):
    if type(array) is list:
        return len(array)

@register.filter(name='get_store_with_id')
def get_store_with_id(id):
    try:
        store = Store.objects.get(id=id).title
    except ValueError:
        store = 'Hemmesi'
    return store

@register.filter(name='number_to_text')
def number_to_text(number):
    number_text_dict = {
        1: 'bir',
        2: 'iki',
        3: 'üç',
        4: 'dört',
        5: 'bäş',
        6: 'alty',
        7: 'ýedi',
        8: 'sekiz',
        9: 'dokuz',
        10: 'on',
        12: 'on bir',
        12: 'on iki',
    }
    return number_text_dict[number]

@register.filter(name='transF')
def transF(month):
    return settings.TRANSLATED_MONTHS[month]

@register.filter(name='startswith')
def startswith(text, starts):
    if isinstance(text, str):
        return text.startswith(starts)
    return False

@register.filter(name='lor')
def lor(value, arg):
    return value if value else arg
