from django.shortcuts import render
import http.client
import json
import requests
from dashboard.models import Team, Player, Position, Match


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


def get_matches():
    #response = requests.get('http://api.football-data.org/v1/competitions/467/teams', headers={'Authorization': '6403e75cc2824d6ab4c6dfc26d832718'})
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = {'X-Auth-Token': '6403e75cc2824d6ab4c6dfc26d832718', 'X-Response-Control': 'full'}
    connection.request('GET', '/v1/competitions/467/teams', None, headers)
    response = json.loads(connection.getresponse().read().decode())
    #print(response)
    teams = response
    equipos = teams.get("teams")
    print("----")
    print(len(equipos))

    for t in equipos:
        if t is not None:
            link = t.get("_links")
            url = link.get("fixtures").get("href")
            connection.request('GET', url, None, headers)
            response1 = json.loads(connection.getresponse().read().decode())
            matches = response1.get("fixtures")
            for match in matches:
                if match is not None:
                    #print(match)
                    home_team = recover_team_code(match.get("_links").get("homeTeam").get('href'))
                    away_team = recover_team_code(match.get("_links").get("awayTeam").get('href'))
                    if home_team is not None and away_team is not None:
                        try:
                            check_match = Match.objects.get(team1=home_team, team2=away_team)
                            if check_match.game_date is None:
                                check_match.game_date = match.get('date')
                                check_match.save()
                                print("Fecha actualizada")
                                print(home_team)
                                print(away_team)
                            else:
                                print("Ya tenía")
                                print(home_team)
                                print(away_team)
                        except Match.DoesNotExist:
                            new_match = Match()
                            new_match.team1 = home_team
                            new_match.team2 = away_team
                            new_match.game_date = match.get('date')
                            new_match.save()
                            print("Partido creado")
                            print(home_team)
                            print(away_team)

                else:
                    print('No response')


def recover_team_code(url):
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = {'X-Auth-Token': '6403e75cc2824d6ab4c6dfc26d832718', 'X-Response-Control': 'full'}
    connection.request('GET', url, None, headers)
    response = json.loads(connection.getresponse().read().decode())
    code = response.get('code')
    if code is not None:
        t = Team.objects.get(code=code)
        return t
