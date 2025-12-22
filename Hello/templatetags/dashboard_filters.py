from django import template
from itertools import groupby
from operator import itemgetter

register = template.Library()

@register.filter
def groupby(queryset, key):
    """
    Groups a queryset by a given key.
    Usage: {% for date, activities in daily_activities|groupby:"date" %}
    """
    return [(k, list(g)) for k, g in groupby(queryset, key=itemgetter(key))] 