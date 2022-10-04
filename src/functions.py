import requests
import json
import urllib3
from datetime import datetime, timedelta

from data.lol_live_urls import lol_live_game_stats_url, lol_live_game_events_url


# Disable insecure https warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def is_game_live():
    game_started = False
    try:
        game_stats_request = requests.get(lol_live_game_stats_url, verify=False)
        status_code = game_stats_request.status_code
        if status_code == 200:
            game_events_request = requests.get(lol_live_game_events_url, verify=False)
            events = json.loads(game_events_request.text)['Events']
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
