from collections import OrderedDict
from django import template
from django.core import serializers
from htmllaundry import sanitize
from htmllaundry.cleaners import CommentCleaner

register = template.Library()

@register.filter
def htmlify(value):
    replacements = OrderedDict([
        ('&amp;', '&'),
        ('&lt;', '<'),
        ('&gt;', '>'),
        ('&quot;', '"'),
        ('""', '"')
        ])
    for k,v in replacements.items():
        value = value.replace(k, v)
    return sanitize(value, CommentCleaner)
