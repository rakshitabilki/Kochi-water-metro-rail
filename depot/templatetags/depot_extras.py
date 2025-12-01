# depot/templatetags/depot_extras.py
from django import template
register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Return dictionary[key] or None (works in templates)."""
    try:
        return dictionary.get(key)
    except Exception:
        return None
