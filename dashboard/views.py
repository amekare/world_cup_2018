from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.db.models import Q
from operator import itemgetter
from collections import OrderedDict
from django.urls import reverse_lazy
from django.db.models import F
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from dashboard.models import Team, Player, Round, Bet, Gambler, Match


class TeamListView(ListView):
    model = Team


class TeamDetailView(DetailView):
    model = Team


class TeamCreateView(CreateView):
    model = Team
    fields = '__all__'
    success_url = reverse_lazy('team-list')


class TeamUpdateView(UpdateView):
    model = Team
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('team-detail', kwargs={'pk': self.kwargs.get('pk')})


class TeamDeleteView(DeleteView):
    model = Team
    success_url = reverse_lazy('team-list')


class PlayerListView(ListView):
    model = Player
    fields = '__all__'
    paginate_by = 20

    def get_success_url(self):
        return reverse_lazy('team-detail', kwargs={'pk': self.kwargs.get('pk')})


class PlayerCreateView(CreateView):
    model = Player
    fields = '__all__'
    success_url = reverse_lazy('player-list')


class PlayerUpdateView(UpdateView):
    model = Player
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('player-detail', kwargs={'pk': self.kwargs.get('pk')})


class PlayerDetailView(DetailView):
    model = Player

    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('player-detail', kwargs={'pk': self.kwargs.get('pk')})


class PlayerDeleteView(DeleteView):
    model = Player
    success_url = reverse_lazy('player-list')


class RoundListView(ListView):
    model = Round

    def get_queryset(self):
        queryset = super(RoundListView, self).get_queryset()
        return queryset.filter(source__name="Oficial", stage="1").order_by("team__group")


class Round8voListView(ListView):
    model = Round
    template_name = "dashboard/round8vo_list.html"

    def get_queryset(self):
        queryset = super(Round8voListView, self).get_queryset()
        return queryset.filter(source__name="Oficial", stage="2").order_by("team__group")


class RoundDetailView(DetailView):
    model = Round


class RoundCreateView(CreateView):
    model = Round
    fields = '__all__'
    success_url = reverse_lazy('round-list')


class RoundUpdateView(UpdateView):
    model = Round
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('round-detail', kwargs={'pk': self.kwargs.get('pk')})


class RoundDeleteView(DeleteView):
    model = Team
    success_url = reverse_lazy('round-list')


class BetListView(ListView):
    model = Bet

    def get_queryset(self):
        queryset = super(BetListView, self).get_queryset()
        return queryset.filter(source__name="Oficial", match__stage="1").order_by("team1__group")


class Bet8voListView(ListView):
    model = Bet
    template_name = "dashboard/bet8vo_list.html"

    def get_queryset(self):
        queryset = super(Bet8voListView, self).get_queryset()
        return queryset.filter(source__name="Oficial", match__stage="2")


class Bet4voListView(ListView):
    model = Bet
    template_name = "dashboard/bet4vo_list.html"

    def get_queryset(self):
        queryset = super(Bet4voListView, self).get_queryset()
        return queryset.filter(source__name="Oficial", match__stage="3")


class BetDetailView(DetailView):
    model = Bet


class SecondBetDetailView(DetailView):
    model = Bet
    template_name = "dashboard/second_bet_detail.html"


class BetCreateView(CreateView):
    model = Bet
    fields = ('source', 'match', 'goals_team1', 'goals_team2', 'type')
    # form_class = BetForm
    success_url = reverse_lazy('gambler-list')


class BetUpdateView(UpdateView):
    model = Bet
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('bet-detail', kwargs={'pk': self.kwargs.get('pk')})


class BetDeleteView(DeleteView):
    model = Bet
    success_url = reverse_lazy('bet-list')


class GamblerListView(ListView):
    model = Gambler

    def get_queryset(self):
        queryset = super(GamblerListView, self).get_queryset()
        return queryset.all().exclude(pk=1).annotate(
            points=(F('points_score') + (F('points_result')) + (F('points_8vo')) + (F('points_4vo')))).order_by(
            '-points')


class SecondGamblerListView(ListView):
    model = Gambler
    template_name = "dashboard/second_gambler_list.html"

    def get_queryset(self):
        queryset = super(SecondGamblerListView, self).get_queryset()
        return queryset.all().exclude(pk=1).annotate(
            points=(F('points_score2') + (F('points_result2')) + (F('points_4vo2')))).order_by(
            '-points')


class GamblerDetailView(DetailView):
    model = Gambler


class SecondGamblerDetailView(DetailView):
    model = Gambler
    template_name = "dashboard/second_gambler_detail.html"


def update_first_round(stage):
    source = Gambler.objects.get(name='Oficial')
    results = Bet.objects.filter(source=source, checked=False, type="Original")
    print(results)
    for result in results:
        print(result.checked)
        round1 = Round.objects.get(team=result.team1, stage=stage)
        round2 = Round.objects.get(team=result.team2, stage=stage)
        print(round1.source.name)
        print(round2.source.name)
        round1.played_matches += 1
        round2.played_matches += 1
        if result.goals_team1 > result.goals_team2:
            round1.won += 1
            round2.lose += 1
        if result.goals_team1 == result.goals_team2:
            round1.draw += 1
            round2.draw += 1
        if result.goals_team1 < result.goals_team2:
            round1.lose += 1
            round2.won += 1
        round1.goals_for += result.goals_team1
        round1.goals_against += result.goals_team2
        round1.goals_difference = round1.goals_for - round1.goals_against
        round2.goals_for += result.goals_team2
        round2.goals_against += result.goals_team1
        round2.goals_difference = round2.goals_for - round2.goals_against
        round1.save()
        round2.save()
        result.checked = True
        result.save()
    update_scores(stage)
    print("Actualizados: " + str(len(results)))
    update_gamblers()
    update_gamblers2()
    if stage == '1':
        get_first_round_position()


# 1 = 1st stage, 2 = 8th
def update_scores(stage):
    rounds = Round.objects.filter(stage=stage)
    for r in rounds:
        r.points = r.won * 3 + r.draw * 1
        r.save()


def update_gamblers():
    oficial_results = Bet.objects.filter(source__name='Oficial', type="Original")
    gamblers_updated = []
    for oficial in oficial_results:
        bets = Bet.objects.filter(match=oficial.match, checked=False, type="Original")
        for bet in bets:
            gambler = Gambler.objects.get(name=bet.source.name)
            if oficial.goals_team1 == bet.goals_team1 and oficial.goals_team2 == bet.goals_team2:
                gambler.points_score += 1
            if result_match(oficial.source.name, oficial.match, "") == result_match(bet.source.name, bet.match,
                                                                                    bet.type):
                gambler.points_result += 1
                gamblers_updated.append(gambler)
            gambler.save()
            bet.checked = True
            bet.save()
    print("Gamblers updated: " + str(len(gamblers_updated)))
    print(gamblers_updated)


def update_gamblers2():
    oficial_results = Bet.objects.filter(source__name='Oficial')
    gamblers_updated = []
    for oficial in oficial_results:
        bets = Bet.objects.filter(match=oficial.match, checked=False, type="Consolación")
        for bet in bets:
            gambler = Gambler.objects.get(name=bet.source.name)
            if oficial.goals_team1 == bet.goals_team1 and oficial.goals_team2 == bet.goals_team2:
                gambler.points_score2 += 1
            if result_match(oficial.source.name, oficial.match, "") == result_match(bet.source.name, bet.match,
                                                                                    bet.type):
                gambler.points_result2 += 1
                gamblers_updated.append(gambler)
            gambler.save()
            bet.checked = True
            bet.save()
    print("Gamblers in second quiniela updated: " + str(len(gamblers_updated)))
    print(gamblers_updated)


def result_match(source, match, type):
    if len(type) == 0:
        bet = Bet.objects.get(source__name=source, match=match)
    else:
        bet = Bet.objects.get(source__name=source, match=match, type=type)
    if bet.goals_team1 > bet.goals_team2:
        return 'Team 1 won'
    if bet.goals_team1 == bet.goals_team2:
        return 'Draw'
    if bet.goals_team1 < bet.goals_team2:
        return 'Team 2 won'


def update_goals_first_stage():
    rounds = Round.objects.filter(stage='1')
    for r in rounds:
        team = Team.objects.get(name=r.team.name)
        # home team
        bets1 = Bet.objects.filter(source__name='Oficial', team1=team)
        # away team
        bets2 = Bet.objects.filter(source__name='Oficial', team2=team)
        for bet in bets1:
            r.goals_against += bet.goals_team2
            r.goals_for += bet.goals_team1
            r.save()
        for bet in bets2:
            r.goals_against += bet.goals_team1
            r.goals_for += bet.goals_team2
            r.save()
        r.goals_difference = r.goals_for - r.goals_against
        r.save()


def qualified_eight(request):
    qualified_list = Round.objects.filter(
        Q(position__startswith="Primero", source__name__startswith="OFicial") | Q(position__startswith="Segundo",
                                                                                  source__name__startswith="OFicial")).order_by(
        "team__group", "position")
    template = loader.get_template('dashboard/qualified_oficial.html')
    context = {
        'qualified_list': qualified_list,
    }
    return HttpResponse(template.render(context, request))


def qualified_first_round_gamblers(request):
    qualified_list = Round.objects.filter(
        Q(position__startswith="Primero") | Q(position__startswith="Segundo")).order_by("source__name", "team__group",
                                                                                        "position")
    template = loader.get_template('dashboard/qualified_gamblers.html')
    print(len(qualified_list))
    context = {
        'qualified_list': qualified_list,
    }
    return HttpResponse(template.render(context, request))


# update oficial rounds
def get_first_round_position():
    groups = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    for group in groups:
        rounds = Round.objects.filter(team__group=group, stage=1, source__name='Oficial').order_by("-points")
        positions = {}
        for round in rounds:
            score = round.points * 1000000 + (round.goals_difference + 50) * 1000 + round.goals_for
            positions[round.team] = score
        sorted_by_value = OrderedDict(sorted(positions.items(), key=itemgetter(1)))
        first = list(sorted_by_value.items())[3]
        second = list(sorted_by_value.items())[2]
        third = list(sorted_by_value.items())[1]
        fourth = list(sorted_by_value.items())[0]
        r = Round.objects.get(team__name=first[0], source__name='Oficial', stage=1)
        r1 = Round.objects.get(team__name=second[0], source__name='Oficial', stage=1)
        r2 = Round.objects.get(team__name=third[0], source__name='Oficial', stage=1)
        r3 = Round.objects.get(team__name=fourth[0], source__name='Oficial', stage=1)
        if first[1] > second[1]:
            r.position = "Primero"
            r.save()
            r1.position = "Segundo"
            r1.save()
            if second[1] == third[1]:
                r2.position = "Segundo"
                r2.save()
            else:
                r2.position = "Tercero"
                r2.save()
                if third[1] == fourth[1]:
                    r3.position = "Tercero"
                    r3.save()
                else:
                    r3.position = "Cuarto"
                    r3.save()
        if first[1] == second[1]:
            r.position = "Primero"
            r.save()
            r1.position = "Primero"
            r1.save()
            r2.position = "Segundo"
            r2.save()
            r3.position = "Tercero"
            r3.save()

        r3.position = "Cuarto"
        r3.save()


def update_played_matches():
    groups = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    for group in groups:
        teams = Round.objects.filter(team__group=group, stage=1)
        for team in teams:
            if team.played_matches == 3:
                team.done = True
                team.save()


def qualified_per_gambler():
    gamblers = Gambler.objects.all().exclude(name="Oficial")
    for gambler in gamblers:
        print(gambler)
        # creation of round per gambler
        # get rounds from oficial and stage 1
        rounds_oficial = Round.objects.filter(source__name="Oficial", stage="1")
        for r in rounds_oficial:
            if r.played_matches == 3:
                try:
                    exist = Round.objects.get(stage=1, source=gambler, team=r.team)
                except Round.DoesNotExist:
                    ro = Round()
                    ro.source = gambler
                    ro.played_matches = 3
                    ro.stage = '1'
                    ro.team = r.team
                    ro.save()
        rounds = Round.objects.filter(stage='1', source=gambler)
        for r in rounds:
            if not r.done:
                team = Team.objects.get(name=r.team.name)
                # home team
                bets1 = Bet.objects.filter(source=gambler, team1=team)
                # away team
                bets2 = Bet.objects.filter(source=gambler, team2=team)

                for bet in bets1:
                    r.goals_against += bet.goals_team2
                    r.goals_for += bet.goals_team1
                    if bet.goals_team1 > bet.goals_team2:
                        r.won += 1
                    if bet.goals_team1 == bet.goals_team2:
                        r.draw += 1
                    if bet.goals_team1 < bet.goals_team2:
                        r.lose += 1
                    r.save()
                for bet in bets2:
                    r.goals_against += bet.goals_team1
                    r.goals_for += bet.goals_team2
                    if bet.goals_team1 > bet.goals_team2:
                        r.lose += 1
                    if bet.goals_team1 == bet.goals_team2:
                        r.draw += 1
                    if bet.goals_team1 < bet.goals_team2:
                        r.won += 1
                    r.save()
                r.goals_difference = r.goals_for - r.goals_against
                r.done = True
                r.save()
                print(r)
    update_scores(1)


def update_first_round_oficial():
    g = Gambler.objects.get(name="Oficial")
    rounds = Round.objects.all()
    for r in rounds:
        r.source = g
        r.save()


# update oficial rounds
def first_round_position_gamblers():
    groups = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    gamblers = Gambler.objects.all().exclude(name='Oficial')
    for gambler in gamblers:
        for group in groups:
            rounds = Round.objects.filter(source=gambler, stage=1, team__group=group).order_by("-points")
            positions = {}
            if len(rounds) == 4:
                for round in rounds:
                    score = round.points * 1000000 + (round.goals_difference + 50) * 1000 + round.goals_for
                    positions[round.team] = score
                sorted_by_value = OrderedDict(sorted(positions.items(), key=itemgetter(1)))
                first = list(sorted_by_value.items())[3]
                second = list(sorted_by_value.items())[2]
                third = list(sorted_by_value.items())[1]
                fourth = list(sorted_by_value.items())[0]
                r = Round.objects.get(team__name=first[0], source=gambler, stage=1)
                r1 = Round.objects.get(team__name=second[0], source=gambler, stage=1)
                r2 = Round.objects.get(team__name=third[0], source=gambler, stage=1)
                r3 = Round.objects.get(team__name=fourth[0], source=gambler, stage=1)
                if not r.qualified_revision:
                    if first[1] > second[1]:
                        r.position = "Primero"
                        r.qualified_revision = True
                        r.save()
                        r1.position = "Segundo"
                        r1.qualified_revision = True
                        r1.save()
                        if second[1] == third[1]:
                            r2.position = "Segundo"
                            r2.qualified_revision = True
                            r2.save()
                        else:
                            r2.position = "Tercero"
                            r2.qualified_revision = True
                            r2.save()
                            if third[1] == fourth[1]:
                                r3.position = "Tercero"
                                r3.qualified_revision = True
                                r3.save()
                            else:
                                r3.position = "Cuarto"
                                r3.qualified_revision = True
                                r3.save()
                    if first[1] == second[1]:
                        r.position = "Primero"
                        r.qualified_revision = True
                        r.save()
                        r1.position = "Primero"
                        r1.qualified_revision = True
                        r1.save()
                        r2.position = "Tercero"
                        r2.qualified_revision = True
                        r2.save()
                        r3.position = "Cuarto"
                        r3.qualified_revision = True
                        r3.save()


def qualified_gambler(request, pk):
    gambler = Gambler.objects.get(pk=pk)
    qualified_list = Round.objects.filter(
        Q(position__startswith="Primero", source__name__startswith=gambler.name) | Q(position__startswith="Segundo",
                                                                                     source__name__startswith=gambler.name)).order_by(
        "team__group", "position")
    template = loader.get_template('dashboard/gambler_detail_qualified.html')
    context = {
        'qualified_list': qualified_list,
        'gambler': gambler,
    }
    return HttpResponse(template.render(context, request))


def matches_knockout_phase():
    matches_ready = {}
    matches = Match.objects.filter(stage=2)
    gamblers = Gambler.objects.all().exclude(name="Oficial")
    for match in matches:
        #     print("OFicial")
        #     print(match)
        match_list = []
        team1 = match.team1
        team2 = match.team2
        r1 = Round.objects.get(source__name="Oficial", stage=1, team=team1)
        r2 = Round.objects.get(source__name="Oficial", stage=1, team=team2)
        # print(r1)
        # print(r1.position)
        # print(r2)
        # print(r2.position)
        for gambler in gamblers:
            rg1 = Round.objects.get(source=gambler, stage=1, team=team1)
            rg2 = Round.objects.get(source=gambler, stage=1, team=team2)
            # print(rg1)
            # print(rg1.position)
            # print(rg2)
            # print(rg2.position)
            if r1.position == rg1.position:
                if r2.position == rg2.position:
                    match_list.append(gambler.name)
        matches_ready[match] = match_list

    for k, v in matches_ready.items():
        print(k, v)


# only call after matches for 8vo are in the system
def load_8vo_stages():
    matches = Match.objects.filter(stage="2")
    gambler = Gambler.objects.get(name="Oficial")
    for match in matches:
        round = Round()
        round.stage = "2"
        round.source = gambler
        round.team = match.team1
        round.save()
        round1 = Round()
        round1.stage = "2"
        round1.source = gambler
        round1.team = match.team2
        round1.save()


def successful_matches(request, pk):
    gambler = Gambler.objects.get(pk=pk)
    matches_list = []
    bets = Bet.objects.filter(source=gambler, type="Original")
    for bet in bets:
        oficial = Bet.objects.get(match=bet.match, source__name="Oficial")
        if result_match(oficial.source.name, oficial.match, "") == result_match(bet.source.name, bet.match,
                                                                                bet.type):
            matches_list.append(bet)
    template = loader.get_template('dashboard/gambler_matches_detail.html')
    context = {
        'bet_list': matches_list,
        'gambler': gambler,
        'points': len(matches_list)

    }
    return HttpResponse(template.render(context, request))


def successful_scores(request, pk):
    gambler = Gambler.objects.get(pk=pk)
    scores_list = []
    bets = Bet.objects.filter(source=gambler, type="Original")
    for bet in bets:
        oficial = Bet.objects.get(match=bet.match, source__name="Oficial")
        if oficial.goals_team1 == bet.goals_team1 and oficial.goals_team2 == bet.goals_team2:
            scores_list.append(bet)
    template = loader.get_template('dashboard/gambler_scores_detail.html')
    context = {
        'bet_list': scores_list,
        'gambler': gambler,
        'points': len(scores_list)

    }
    return HttpResponse(template.render(context, request))


def get_errors():
    gamblers = Gambler.objects.all().exclude(name="Oficial")
    oficial = Gambler.objects.get(name="Oficial")
    errors = []
    for gambler in gamblers:
        scores_points = []
        bets_points = []
        bets_list = Bet.objects.filter(source=gambler, type="Original")
        for bet in bets_list:
            try:
                oficial_bet = Bet.objects.get(source=oficial, match=bet.match, type="Original")
                if oficial_bet.goals_team1 == bet.goals_team1 and oficial_bet.goals_team2 == bet.goals_team2:
                    scores_points.append(bet)
                if result_match(oficial_bet.source.name, oficial_bet.match, "") == result_match(bet.source.name, bet.match,
                                                                                        bet.type):
                    bets_points.append(bet)
            except Bet.DoesNotExist:
                pass
        if len(scores_points) != gambler.points_score:
            error = gambler.name + " marcadores: " + str(len(scores_points)) + " vs " + str(gambler.points_score)
            errors.append(error)
        if len(bets_points) != gambler.points_result:
            error = gambler.name + " resultados: " + str(len(bets_points)) + " vs " + str(gambler.points_result)
            errors.append(error)
    print(errors)


def data(request):
    return render(request, 'dashboard/data.html')

