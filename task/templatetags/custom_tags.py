from django import template

register = template.Library()

@register.filter
def make_list(value):
    return range(value)
