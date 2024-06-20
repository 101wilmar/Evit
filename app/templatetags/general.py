from django import template

register = template.Library()


@register.filter(name='get_value_for_key')
def get_value_for_key(data, key, default_value=''):
    value = data.get(key, default_value)
    return value
