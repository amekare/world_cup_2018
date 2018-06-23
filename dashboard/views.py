from django.urls import reverse_lazy
from django.db.models import F
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from dashboard.models import Team, Player, Round, Bet, Gambler


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
        return queryset.filter(source__name="Oficial").order_by("team1__group")


class BetDetailView(DetailView):
    model = Bet


class BetCreateView(CreateView):
    model = Bet
    fields = ('source', 'match', 'goals_team1', 'goals_team2')
    #form_class = BetForm
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
        return queryset.all().exclude(pk=1).annotate(points=(F('points_score')+(F('points_result')))).order_by('-points')


class GamblerDetailView(DetailView):
    model = Gambler


def update_first_round():
    source = Gambler.objects.get(name='Oficial')
    results = Bet.objects.filter(source=source, checked=False)
    print(results)
    for result in results:
        print(result.checked)
        round1 = Round.objects.get(team=result.team1, stage='1')
        round2 = Round.objects.get(team=result.team2, stage='1')
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
        round1.save()
        round2.save()
        result.checked = True
        result.save()
    stage = '1'
    update_scores(stage)
    print("first")
    print("Actualizados: " + str(len(results)))
    print("second")
    update_gamblers()
    print("third")


# 1 = 1st stage, 2 = 8th
def update_scores(stage):
    rounds = Round.objects.filter(stage=stage)
    for r in rounds:
        r.points = r.won * 3 + r.draw * 1
        r.save()



def update_gamblers():
    oficial_results = Bet.objects.filter(source__name='Oficial')
    gamblers_updated = []
    for oficial in oficial_results:
        bets = Bet.objects.filter(match=oficial.match, checked=False)
        for bet in bets:
            gambler = Gambler.objects.get(name=bet.source.name)
            if oficial.goals_team1 == bet.goals_team1 and oficial.goals_team2 == bet.goals_team2:
                gambler.points_score += 1
            if result_match(oficial.source.name, oficial.match) == result_match(bet.source.name, bet.match):
                gambler.points_result += 1
                gamblers_updated.append(gambler)
            gambler.save()
            bet.checked = True
            bet.save()
    print("Gamblers updated: " + str(len(gamblers_updated)))
    print(gamblers_updated)


def result_match(source, match):
    bet = Bet.objects.get(source__name=source, match=match)
    if bet.goals_team1 > bet.goals_team2:
        return 'Team 1 won'
    if bet.goals_team1 == bet.goals_team2:
        return 'Draw'
    if bet.goals_team1 < bet.goals_team2:
        return 'Team 2 won'
