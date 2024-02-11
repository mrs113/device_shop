from django.utils.http import urlencode
from products.models import Product
from django import template

register = template.Library()


@register.simple_tag()
def products_list_tags():
    return Product.objects.filter(is_have=True)


@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)
