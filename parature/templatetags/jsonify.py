from django import template
from django.core import serializers
import json

register = template.Library()

@register.filter
def jsonify(value):
    data = json.loads(serializers.serialize('json', [value]))
    return json.dumps(data, indent=2)
