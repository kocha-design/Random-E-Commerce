from django import template

register = template.Library()


@register.filter
def tsh(value):
    """Format price as TSh 38,000 (no decimals)."""
    try:
        return f"TSh {int(float(value)):,}"
    except (ValueError, TypeError):
        return f"TSh {value}"