from django import template


register = template.Library()


@register.filter(name='multiply')
def multiply(value, arg):
    try:
        return value * arg
    except (ValueError, TypeError):
        return ''
    

@register.filter(name='sum_values')
def sum_values(items):
    try:
        return sum(item.quantity * item.product.price for item in items)
    except (ValueError, TypeError):
        return ''
    
@register.filter
def sum_total_price(items):
    return sum(item.get_total_price() for item in items)

