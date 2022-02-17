from django import template
from importlib_metadata import pass_none

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)