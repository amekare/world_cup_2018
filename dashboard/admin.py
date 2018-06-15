from django.contrib import admin
from dashboard.models import Team, Player, Position, Bet, Round, Match, Gambler


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'finals', 'cups')
    search_fields = ('name', 'code')


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'team')
    search_fields = ('name', 'team__name')


class RoundAdmin(admin.ModelAdmin):
    list_display = ('group', 'stage', 'team', 'played_matches', 'won', 'draw', 'lose', 'points')
    search_fields = ('group', 'team__name')


class MatchAdmin(admin.ModelAdmin):
    list_display = ('team1', 'team2')
    search_fields = ('team1__name', 'team2__name')


class BetAdmin(admin.ModelAdmin):
    list_display = ('source', 'match', 'team1', 'team2', 'goals_team1', 'goals_team2', 'checked')
    search_fields = ('source__name', 'team1__name', 'team2__name')


admin.site.register(Team, TeamAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Position)
admin.site.register(Gambler)
admin.site.register(Bet, BetAdmin)
admin.site.register(Round, RoundAdmin)
admin.site.register(Match, MatchAdmin)
