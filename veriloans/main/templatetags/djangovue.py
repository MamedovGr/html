from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def vue(var_name):
    return "{{%s}}" % var_name

@register.simple_tag
def method(value):
    return mark_safe("<input type=\"hidden\" name=\"_method\" value=\"%s\">" % value)

@register.simple_tag
def get_dict(key, value):
    context = {}

    # convert to list of keys
    splited_key = key.strip('][').split(', ')
    trimed_key = [ v.replace("'", '') for v in splited_key ]

    # convert to list of values
    splited_value = value.strip('][').split(', ')
    trimed_value = [ v.replace("'", '') for v in splited_value ]

    for i in range(len(trimed_key)):
        context[trimed_key[i]] = trimed_value[i]

    return context.items()

@register.simple_tag
def D_M_Y():
    return '([0-2][0-9]|[3][01])-([0][1-9]|[1][0-2])-[12][09]\d{2}'
