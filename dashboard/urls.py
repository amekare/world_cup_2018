from django.conf.urls import url
from dashboard import views

urlpatterns = [
    url(r'^teams$', views.TeamListView.as_view(), name='team-list'),
    url(r'^teams/(?P<pk>\d+)$', views.TeamDetailView.as_view(), name='team-detail'),
    url(r'^teams/new$', views.TeamCreateView.as_view(), name='team-create'),
    url(r'^teams/(?P<pk>\d+)/edit$', views.TeamUpdateView.as_view(), name='team-update'),
    url(r'^teams/(?P<pk>\d+)/delete$', views.TeamDeleteView.as_view(), name='team-delete'),

    url(r'^players$', views.PlayerListView.as_view(), name='player-list'),
    url(r'^players/(?P<pk>\d+)$', views.PlayerDetailView.as_view(), name='player-detail'),
    url(r'^players/(?P<pk>\d+)/edit$', views.PlayerUpdateView.as_view(), name='player-update'),
    url(r'^players/(?P<pk>\d+)/delete$', views.PlayerDeleteView.as_view(), name='player-delete'),

    url(r'^rounds$', views.RoundListView.as_view(), name='round-list'),
    url(r'^rounds/(?P<pk>\d+)$', views.RoundDetailView.as_view(), name='round-detail'),
    url(r'^rounds/new$', views.RoundCreateView.as_view(), name='round-create'),
    url(r'^rounds/(?P<pk>\d+)/edit$', views.RoundUpdateView.as_view(), name='round-update'),
    url(r'^rounds/(?P<pk>\d+)/delete$', views.RoundDeleteView.as_view(), name='round-delete'),

    url(r'^bets$', views.BetListView.as_view(), name='bet-list'),
    url(r'^bets/(?P<pk>\d+)$', views.BetDetailView.as_view(), name='bet-detail'),
    url(r'^bets/new$', views.BetCreateView.as_view(), name='bet-create'),
    url(r'^bets/(?P<pk>\d+)/edit$', views.BetUpdateView.as_view(), name='bet-update'),
    url(r'^bets/(?P<pk>\d+)/delete$', views.BetDeleteView.as_view(), name='bet-delete'),


]