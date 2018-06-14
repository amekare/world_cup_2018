from django.shortcuts import render
import http.client
import json
import requests
from dashboard.models import Team, Player, Position


# connection = http.client.HTTPConnection('api.football-data.org')
# headers = {'X-Auth-Token': '6403e75cc2824d6ab4c6dfc26d832718', 'X-Response-Control': 'minified'}
# connection.request('GET', '/v1/competitions', None, headers)
# response = json.loads(connection.getresponse().read().decode())
#
# print(response)


def get_teams():
    response = requests.get('http://api.football-data.org/v1/competitions/467/teams')
    teams = response.json()
    equipos = teams.get("teams")
    for t in equipos:
        team = Team()
        team.name = t.get("name")
        team.code = t.get("code")
        team.save()
        play = t.get("_links")
        players = get_players(play.get("players").get("href"), team)
        print(team.name + '-------- ' + str(players))
##agregar algo para no repetir

print("Total de equipos: " + str(Team.objects.all().count()))


def get_players(url, team):
    response = requests.get(url)
    j = response.json()
    players = j.get("players")
    for player in players:
        p = Player()
        p.name = player.get("name")
        p.birth_date = player.get("dateOfBirth")
        p.jerseyNumber = player.get("jerseyNumber")
        p.team = team
        p.save()
        if Position.objects.filter(name=player.get("position")).exists():
            pos = Position.objects.filter(name=player.get("position")).first()
            p.positions.add(pos)
        else:
            pos = Position()
            pos.name = player.get("position")
            pos.save()
            p.positions.add(pos)
        print(p)

    return Player.objects.filter(team=team).count()
