from django import template

register = template.Library()

@register.filter
def subtract(value, arg):
    "Subtracts the arg from the value"
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return ''

@register.filter
def multiply(value, arg):
    "Multiplies the value by the arg"
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''

@register.filter
def divide(value, arg):
    "Divides the value by the arg"
    try:
        if float(arg) == 0:
            return 0
        return float(value) / float(arg)
    except (ValueError, TypeError):
        return ''

# Register them for the template
register.filter('sub', subtract)
register.filter('mul', multiply)
register.filter('div', divide)