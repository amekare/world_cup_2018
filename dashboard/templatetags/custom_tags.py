from dashboard.models import Gambler, Bet, Round
from dashboard.views import result_match
from django import template

register = template.Library()


@register.filter()
def total_points(value, arg):
    gambler = Gambler.objects.get(name=arg)
    points = gambler.points_semi + gambler.points_score + gambler.points_final + gambler.points_8vo+gambler.points_4vo + gambler.points_3er + gambler.points_result
    return str(points)


@register.filter()
def total_points2(value, arg):
    gambler = Gambler.objects.get(name=arg)
    points = gambler.points_semi2 + gambler.points_score2 + gambler.points_final2 + gambler.points_4vo2 + gambler.points_3er2 + gambler.points_result2
    return str(points)


@register.filter()
def total_percentage(value, arg):
    gambler = Gambler.objects.get(name=arg)
    oficial_g = Gambler.objects.get(name="Oficial")
    bets = Bet.objects.filter(source=oficial_g)
    total_points_matches = len(bets) * 2
    points = 0
    for bet in bets:
        try:
            b = Bet.objects.get(match=bet.match, source=gambler)
            if bet.goals_team1 == b.goals_team1 and bet.goals_team2 == b.goals_team2:
                points += 1
            if result_match(bet.source.name, bet.match) == result_match(b.source.name, b.match):
                points += 1
        except Bet.DoesNotExist:
            print(gambler)
            print(str(bet) + " Sin partido")
    return "{0:.2f}".format((points * 100)/total_points_matches)


@register.filter()
def result(value, arg):
    try:
        bet = Bet.objects.get(match=arg, source__name="Oficial", type="Original")
    except Bet.DoesNotExist:
        return 'Sin jugar'

    return str(bet.goals_team1) + " - " + str(bet.goals_team2)


@register.filter()
def result2(value, arg):
    try:
        bet = Bet.objects.get(match=arg, source__name="Oficial", type="Consolación")
    except Bet.DoesNotExist:
        return 'Sin jugar'

    return str(bet.goals_team1) + " - " + str(bet.goals_team2)


@register.filter()
def played_points(value, arg):
    matches = len(Bet.objects.filter(source__name='Oficial'))
    return matches * 2


@register.simple_tag(name='qualified_matched')
def qualified_matched_gambler(*args):
    try:
        round_player = Round.objects.get(team__name=args[0], source__name=args[1], stage=args[2])
        round_Oficial = Round.objects.get(team__name=args[0], source__name="Oficial", stage=args[2])
        if round_Oficial.position == round_player.position:
            return "Sí"
        else:
            return "No"
    except Round.DoesNotExist:
        return "No"

