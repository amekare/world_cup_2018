from django.contrib import admin
from dashboard.models import Team, Player, Position, Bet, Round, Match, Gambler


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'finals', 'cups', 'group')
    search_fields = ('name', 'code')


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'team')
    search_fields = ('name', 'team__name')


class RoundAdmin(admin.ModelAdmin):
    list_display = ('stage', 'team','position', 'source', 'won', 'draw', 'lose', 'points', 'goals_for', 'goals_against', 'goals_difference', 'done')
    search_fields = ('team__name', 'stage', 'source__name')
    ordering = ("team__group", "-points", "stage")


class MatchAdmin(admin.ModelAdmin):
    list_display = ('team1', 'team2', 'game_date', 'stage')
    search_fields = ('team1__name', 'team2__name', 'stage')


class BetAdmin(admin.ModelAdmin):
    list_display = ('source', 'match', 'team1', 'team2', 'goals_team1', 'goals_team2', 'checked', 'type')
    search_fields = ('source__name', 'team1__name', 'team2__name', 'match__stage', 'type')


class GamblerAdmin(admin.ModelAdmin):
    list_display = ('name', 'points_score', 'points_result', 'get_total_points')
    search_fields = ('name', '')

    ordering = ('name','points_score', 'points_result')


admin.site.register(Team, TeamAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Position)
admin.site.register(Gambler, GamblerAdmin)
admin.site.register(Bet, BetAdmin)
admin.site.register(Round, RoundAdmin)
admin.site.register(Match, MatchAdmin)
