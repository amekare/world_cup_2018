from dashboard.models import Gambler, Bet
from dashboard.views import result_match
from django import template

register = template.Library()


@register.filter()
def total_points(value, arg):
    gambler = Gambler.objects.get(name=arg)
    points = gambler.points_semi + gambler.points_score + gambler.points_final + gambler.points_8vo+gambler.points_4vo + gambler.points_3er + gambler.points_result
    return str(points)


@register.filter()
def total_percentage(value, arg):
    gambler = Gambler.objects.get(name=arg)
    oficial_g = Gambler.objects.get(name="Oficial")
    bets = Bet.objects.filter(source=oficial_g)
    total_points = len(bets) * 2
    print(total_points)
    points = 0
    for bet in bets:
        b = Bet.objects.get(match=bet.match, source=gambler)
        if bet.goals_team1 == b.goals_team1 and bet.goals_team2 == b.goals_team2:
            points += 1
        if result_match(bet.source.name, bet.match) == result_match(b.source.name, b.match):
            points += 1
    print(points)
    print(str((points * 100)/total_points))
    return "{0:.2f}".format((points * 100)/total_points)



@register.filter()
def result(value, arg):
    try:
        bet = Bet.objects.get(match=arg, source__name="Oficial")
    except Bet.DoesNotExist:
        return 'Sin jugar'

    return str(bet.goals_team1) + " - " + str(bet.goals_team2)


