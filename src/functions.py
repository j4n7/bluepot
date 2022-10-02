import requests
import json
import urllib3

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


def format_time(seconds):
    min, sec = divmod(seconds, 60)
    return '%02d:%02d' % (min, sec)
