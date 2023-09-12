from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def str_cut(value: str, length: int):
    if len(value) > length:
        return value[:length] + ' ...'
    return value
