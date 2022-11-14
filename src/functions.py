import requests
import json
import urllib3
from datetime import datetime, timedelta

from data.lol_live_urls import lol_live_game_stats_url, lol_live_game_events_url, lol_live_players_url


# Disable insecure https warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_game_stats():
    game_stats_request = requests.get(lol_live_game_stats_url, verify=False)
    game_stats = json.loads(game_stats_request.text)
    return game_stats


def get_game_events():
    game_events_request = requests.get(lol_live_game_events_url, verify=False)
    events = json.loads(game_events_request.text)['Events']
    return events


def get_players():
    players_request = requests.get(lol_live_players_url, verify=False)
    players = json.loads(players_request.text)
    return players


def get_drake_death_count():
    drake_killers = [event['KillerName'] for event in get_game_events() if event['EventName'] == 'DragonKill']
    blue_team_players = [player['summonerName'] for player in get_players() if player['team'] == 'ORDER']
    red_team_players = [player['summonerName'] for player in get_players() if player['team'] == 'CHAOS']
    drakes = {'blue': 0, 'red': 0}
    for player in drake_killers:
        if player in blue_team_players:
            drakes['blue'] += 1
        if player in red_team_players:
            drakes['red'] += 1
    return drakes


def get_death_time(monster_name):
    if monster_name.startswith('drake'):
        event_name = 'DragonKill'
    elif monster_name == 'herald':
        event_name = 'HeraldKill'
    elif monster_name == 'baron':
        event_name = 'BaronKill'
    death_time = max([event['EventTime'] for event in get_game_events() if event['EventName'] == event_name], default=0)

    return timedelta(seconds=death_time)


def is_game_live():
    game_started = False
    try:
        game_stats_request = requests.get(lol_live_game_stats_url, verify=False)
        status_code = game_stats_request.status_code
        if status_code == 200:
            events = get_game_events()
            game_started = True if events and 'GameStart' in [event['EventName'] for event in events] else False
    except requests.exceptions.ConnectionError:
        pass
    return game_started


def parse_time(time):
    time = datetime.strptime(time, '%M:%S')
    delta = timedelta(minutes=time.minute, seconds=time.second)
    return delta


def format_time(delta):
    if delta:
        min, sec = divmod(delta.seconds, 60)
        return '%02d:%02d' % (min, sec)
    return None


def format_timer(time_string):
    if time_string:
        min, sec = time_string.split(':')
        min = int(min)
        if min:
            return str(min) + ':' + sec
        else:
            return str(int(sec))
    return None
