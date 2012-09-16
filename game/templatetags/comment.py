from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(needs_autoescape=True)
def comment(value, autoescape=None):
    if autoescape:
        value = conditional_escape(value)
    value=value.replace("\r\n","<br/>")
    value=value.replace("\n","<br/>")
    return mark_safe(value)
