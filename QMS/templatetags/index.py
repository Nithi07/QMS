from django import template
register = template.Library()

@register.filter
def getindex(listvalue, indexget):
    return listvalue[indexget]
