from django import template
from store.models import category

register=template.Library()
@register.inclusion_tag('coreapp/menu.html')
def menu():
    categories = category.objects.all()
    return {"categories":categories}