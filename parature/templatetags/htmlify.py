from django import template
from django.core import serializers
import json

register = template.Library()

@register.filter
def htmlify(value):
    replacements = {
            '\n': '<br>',
            '&lt;': '<',
            '&gt;': '>',
            '&amp;': '&',
            '&quot;': '"',
            '&#8217;': '\''
        }
    for val, replacement in replacements.items():
        value = value.replace(val, replacement)
    return value
