# In your app, create a templatetags directory:
# aiml_app/templatetags/custom_filters.py
{% load custom_filters %}

import base64
from django import template

register = template.Library()

@register.filter
def b64encode(value):
    return base64.b64encode(value).decode()
