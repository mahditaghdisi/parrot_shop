from django import template

register = template.Library()


@register.filter
def comma(value):
    """Format a number with standard ',' thousand separators (locale-independent)."""
    try:
        value = int(value)
    except (TypeError, ValueError):
        return value
    return f"{value:,}"
