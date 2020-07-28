from django import template
register = template.Library()

@register.filter("index")
def index(indexable, i):
    return indexable[i]
