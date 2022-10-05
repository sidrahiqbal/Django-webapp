import ast

from django import template

register = template.Library()


@register.filter(name='filter')
def get_string_as_list(value):
    return ast.literal_eval(value)
