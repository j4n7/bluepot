import sys
import wmi
import json
import urllib3
import requests
import pythoncom

from pathlib import Path
from datetime import datetime, timedelta


# FIX RELATIVE IMPORTS
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    pass
else:
    sys.path.append('.')
from data.lol_live_urls import lol_live_game_stats_url, lol_live_game_events_url, lol_live_players_url


# Disable insecure https warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_base_dir():
    '''Get absolute path to base directory, works for dev and for PyInstaller'''
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        base_dir = Path(sys._MEIPASS)
    else:
        base_dir = Path(__file__).parent.parent
    return base_dir


def get_offset(entry):
    def hex_to_int(str_):
        return int(str_, 16)
    return hex_to_int(entry['value'])


def offsets_need_update(remote, local):
    remote = [int(n) for n in remote['version'].split('.')]
    local = [int(n) for n in local['version'].split('.')]
    if remote[0] > local[0] or remote[1] > local[1]:
        return True
    return False


def get_game_info():
    pythoncom.CoInitialize()  # Run in thread

    c = wmi.WMI()

    for process in c.Win32_Process(name='League of Legends.exe'):
        command_line = process.CommandLine.replace('"', '')

    arguments = ['-' + str_ for n, str_ in enumerate(command_line.split(' -')) if n != 0]

    for argument in arguments:
        if argument.startswith('-GameID='):
            game_id = argument.replace('-GameID=', '')
        elif argument.startswith('-Region='):
            region = argument.replace('-Region=', '')

    return game_id, region


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
    format = '%M:%S.%f' if time[-3] == '.' else '%M:%S'
    time = datetime.strptime(time, format)
    delta = timedelta(minutes=time.minute, seconds=time.second, microseconds=time.microsecond)
    return delta


def format_time(delta, mode='min'):
    if delta:
        min, sec = divmod(delta.seconds, 60)
        if mode == 'min':
            return '%02d:%02d' % (min, sec)

        elif mode.startswith('sec'):
            micro_to_sec = delta.microseconds / 10 ** 6
            if mode == 'sec1':
                micro_to_sec_d1 = round(micro_to_sec, 1)
                micro_parsed = str(int(micro_to_sec_d1 * 10))[0]
            elif mode == 'sec2':
                micro_to_sec_d2 = round(micro_to_sec, 2)
                micro_parsed = str(int(micro_to_sec_d2 * 100))[:2].zfill(2)
            return f'{min}:{str(sec).zfill(2)}.{micro_parsed}'
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
