from django import template
from menu.models import Menu

register = template.Library()


@register.inclusion_tag('menu/menu.html', takes_context=True)
def show_menu(context):
    elements = Menu.objects.filter(sort__gt=0, level__exact=0).order_by('sort')
    return {
        'menu': elements,
        'user': context['user']
    }
