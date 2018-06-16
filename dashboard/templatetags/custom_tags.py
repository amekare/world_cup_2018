from dashboard.models import Gambler
from django.template.defaultfilters import stringfilter
from django import template

register = template.Library()


@register.filter()
def total_points(value, arg):
    gambler = Gambler.objects.get(name=arg)
    points = gambler.points_semi + gambler.points_score + gambler.points_final + gambler.points_8vo+gambler.points_4vo + gambler.points_3er + gambler.points_result
    return str(points)


