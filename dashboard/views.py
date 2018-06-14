from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from dashboard.models import Team, Player, Round, Bet


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


class BetDetailView(DetailView):
    model = Bet


class BetCreateView(CreateView):
    model = Bet
    fields = '__all__'
    success_url = reverse_lazy('bet-list')


class BetUpdateView(UpdateView):
    model = Bet
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('bet-detail', kwargs={'pk': self.kwargs.get('pk')})


class BetDeleteView(DeleteView):
    model = Bet
    success_url = reverse_lazy('bet-list')
