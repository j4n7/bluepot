from pymem import Pymem
import timeit
import time

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
        # start_time = time.perf_counter()

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

            # game.update_jungle()

            # MEASURE LOOP TIME
            # end_time = time.perf_counter()
            # elpased_time = end_time - start_time
            # time_to_sleep = max(Game.server_tick_time - elpased_time, 0)

            # print('Elapsed time:', elpased_time)
            # print('Time to sleep:', time_to_sleep)

            # time.sleep(time_to_sleep)

            # MINIMAP OVERLAY
            # ? Here loop halts till Tkinter instance ends
            # ? Nothing gets executed later
            minimap_overlay = MinimapOverlay(game.minimap_resolution, game.get_jungle_camps)
            minimap_overlay.run()

            # if n <= n_iterations or not n_iterations:

                # PERFORMANCE TIMERS
                # timer_setup = 'from __main__ import game'
                # timer_minion_manager = timeit.timeit(setup=timer_setup, stmt='game.minion_manager', number=100)
                # timer_jungle_monsters = timeit.timeit(setup=timer_setup, stmt='game.jungle_monsters', number=100)
                # timer__update_jungle_monsters = timeit.timeit(setup=timer_setup, stmt='game._update_jungle_monsters()', number=100)
                # timer__update_jungle_camps = timeit.timeit(setup=timer_setup, stmt='game._update_jungle_camps()', number=100)
                # timer_get_jungle_camps = timeit.timeit(setup=timer_setup, stmt='game.get_jungle_camps()', number=100)

                # print('Time: minion_manager', round(timer_minion_manager * 1000 * 1000, 2), 'μs')
                # print('Time: jungle_monsters', round(timer_jungle_monsters * 1000 * 1000, 2), 'μs')
                # print('Time: _update_jungle_monster', round(timer__update_jungle_monsters, 2), 's')
                # print('Time: _update_jungle_camps', round(timer__update_jungle_camps, 2), 's')
                # print('Time: get_jungle_camps()', round(timer_get_jungle_camps, 2), 's')
                # print()

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
                # print('Mana:', f'{round(game.local_player.mana, 2)}/{round(game.local_player.mana_max, 2)} ({round(game.local_player.mana_ratio, 2)})')
                # print('Is dead?', game.local_player.is_dead)
                # print('Buffs:')
                # for buff in game.local_player.buff_manager.buffs:
                #     print(f'... {buff.name}: start [{buff.start_time}] - end [{buff.end_time}] - duration [{buff.duration}]')
                # print()

                # print('OBJECTS')
                # for entity in game.object_manager.entities:
                #     if not entity.name_verbose.startswith('Audio-Emitter') and not entity.name_verbose.startswith('SRU_River') and not entity.name_verbose.startswith('sru_River'):
                #         print('OBJECT')
                #         print('Memory addresss:', hex(entity.address))
                #         print('Name (verbose):', entity.name_verbose)
                #         print()

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
                #     print('Name (verbose):', entity.name_verbose)
                #     print('Position:', entity.position)
                #     print('Is visible?', entity.is_visible)
                #     print('Health:', f'{round(entity.health, 2)}/{round(entity.health_max, 2)} ({round(entity.health_ratio, 2)})')
                #     print('Is dead?', entity.is_dead)
                #     print('Buffs:')
                #     for buff in entity.buff_manager.buffs:
                #         print(f'... {buff.name}: start [{buff.start_time}] - end [{buff.end_time}] - duration [{buff.duration}]')
                #     print()

                # print('JUNGLE CAMP RESPAWNS')
                # for entity in game.jungle_camp_respawns:
                #     print('RESPAWN MARKER')
                #     print('Memory addresss:', hex(entity.address))
                #     print('Category:', entity.category)
                #     print('Name (short):', entity.name_short)
                #     print('Name:', entity.name)
                #     print('Position:', entity.position)
                #     print('Buffs:')
                #     for buff in entity.buff_manager.buffs:
                #         print(f'... {buff.name}: start [{buff.start_time}] - end [{buff.end_time}] - duration [{buff.duration}]')
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
