from pymem import Pymem

from src.models.game import Game
from src.minimapoverlay import MinimapOverlay
from src.functions import is_game_live, format_time


# Package structure as suggested by:
# https://medium.com/analytics-vidhya/explicit-understanding-of-python-package-building-structuring-4ac7054c0749


if __name__ == '__main__':
    n = 0
    n_iterations = 0

    pm = None
    game = None
    minimap_overlay = None
    waiting_message = True
    while True:
        if is_game_live():
            if not pm:
                pm = Pymem('League of Legends.exe')
                print('\nGame live!')
                waiting_message = True
        else:
            pm = None
            game = None
            if minimap_overlay:
                minimap_overlay.root.destroy()
            minimap_overlay = None
            if waiting_message:
                print('\nWaiting for game...')
            waiting_message = False
        if pm and not game:
            game = Game(pm)
            n = 0

        if game:
            n += 1

            minimap_overlay = MinimapOverlay(game.minimap_resolution, game.get_jungle_camps)
            minimap_overlay.run()

            # if n <= n_iterations or not n_iterations:

                # print('GAME')
                # print('Game time:', format_time(game.time))

                # print('CHAT')
                # print('Is open?', game.chat.is_open)
                # print('Current message:', game.chat.message_current)
                # print('Number of messages sent:', game.chat.messages_sent_count)
                # print('Messages sent:')
                # for n, message in enumerate(game.chat.messages_sent):
                #     print(f' · Message {str(n + 1).zfill(2)}:', message)
                # print()

                # print('PLAYER')
                # print('Memory addresss:', hex(game.local_player.address))         
                # print('Name (short):', game.local_player.name_short)
                # print('Position:', game.local_player.position)
                # print('Is visible?', hex(game.local_player.address))
                # print('Health:', f'{round(game.local_player.health, 2)}/{round(game.local_player.health_max, 2)} ({round(game.local_player.health_ratio, 2)})')
                # print('Is dead?', game.local_player.is_dead)
                # print()

                # print('MINIONS & JUNGLE MONSTERS')
                # for entity in game.minion_manager.entities:
                #     print('MINION')
                #     print('Memory addresss:', hex(entity.address))
                #     print('Category:', entity.category)
                #     print('Name (short):', entity.name_short)
                #     print('Name:', entity.name)
                #     print('Position:', entity.position)
                #     print('Health:', f'{round(entity.health, 2)}/{round(entity.health_max, 2)} ({round(entity.health_ratio, 2)})')
                #     print()

                # print('JUNGLE MONSTERS')
                # for entity in game.jungle_monsters:
                #     print('MONSTER')
                #     print('Memory addresss:', hex(entity.address))
                #     print('Category:', entity.category)
                #     print('Name (short):', entity.name_short)
                #     print('Name:', entity.name)
                #     print('Name (verbose)', entity.name_verbose)
                #     print('Position:', entity.position)
                #     print('Is visible?', entity.is_visible)
                #     print('Health:', f'{round(entity.health, 2)}/{round(entity.health_max, 2)} ({round(entity.health_ratio, 2)})')
                #     print('Is dead?', entity.is_dead)
                #     print()

                # print('JUNGLE CAMP RESPAWNS')
                # for entity in game.jungle_camp_respawns:
                #     print('RESPAWN MARKER')
                #     print('Memory addresss:', hex(entity.address))
                #     print('Category:', entity.category)
                #     print('Name (short):', entity.name_short)
                #     print('Name:', entity.name)
                #     print('Position:', entity.position)
                #     print('Health:', f'{round(entity.health, 2)}/{round(entity.health_max, 2)} ({round(entity.health_ratio, 2)})')
                #     print('Is dead?', entity.is_dead)
                #     print()

                # print('CHAMPIONS')
                # for entity in game.minion_manager.entities:
                #     print('CHAMPION')
                #     print('Memory addresss:', hex(entity.address))
                #     print('Name (short):', entity.name_short)
                #     print('Position:', entity.position)
                #     print('Health:', f'{round(entity.health, 2)}/{round(entity.health_max, 2)} ({round(entity.health_ratio, 2)})')
                #     print()

                # print('TOWERS')
                # for entity in game.tower_manager.entities:
                #     print('TOWER')
                #     print('Memory addresss:', hex(entity.address))
                #     print('Name (short):', entity.name_short)
                #     print('Position:', entity.position)
                #     print('Health:', f'{round(entity.health, 2)}/{round(entity.health_max, 2)} ({round(entity.health_ratio, 2)})')
                #     print()
