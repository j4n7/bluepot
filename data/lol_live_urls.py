# Live Client Data API
# https://developer.riotgames.com/docs/lol#league-client-api


lol_live_url = 'https://127.0.0.1:2999/liveclientdata'

lol_live_game_data_url = f'{lol_live_url}/allgamedata'
lol_live_game_stats_url = f'{lol_live_url}/gamestats'
lol_live_game_events_url = f'{lol_live_url}/eventdata'


lol_live_player_url = f'{lol_live_url}/activeplayer'
lol_live_player_name_url = f'{lol_live_url}/activeplayername'
lol_live_player_abilities_url = f'{lol_live_url}/activeplayerabilities'
lol_live_player_runes_url = f'{lol_live_url}/activeplayerrunes'

lol_live_players_url = f'{lol_live_url}/playerlist'

lol_live_get_player_scores_url = f'{lol_live_url}/playerscores?summonerName='
lol_live_get_player_summoner_spells_url = f'{lol_live_url}/playersummonerspells?summonerName='
lol_live_get_player_runes_url = f'{lol_live_url}/playermainrunes?summonerName='
lol_live_get_player_items_url = f'{lol_live_url}/playeritems?summonerName='
