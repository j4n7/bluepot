from pymem import Pymem

from src.models.game import Game
from src.functions import is_game_live, format_time


# Package structure as suggested by:
# https://medium.com/analytics-vidhya/explicit-understanding-of-python-package-building-structuring-4ac7054c0749


if __name__ == '__main__':
    pm = None
    game = None
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
            if waiting_message:
                print('\nWaiting for game...')
            waiting_message = False

        if pm and not game:
            game = Game(pm)

        if game:

            print('GAME')
            print('Game time:', format_time(game.time.seconds))
            print()

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
            # print('Memory name:', game.local_player.name_memory)
            # print('Position:', game.local_player.position)
            # print('Health:', f'{round(game.local_player.health, 2)}/{round(game.local_player.health_max, 2)} ({round(game.local_player.health_ratio, 2)})')
            # print()

            # print('MINIONS & MONSTERS')
            # for entity in game.minion_manager.entities:
            #     print('MINION')
            #     print('Memory addresss:', hex(entity.address))
            #     print('Category:', entity.category)
            #     print('Memory name:', entity.name_memory)
            #     print('Name:', entity.name)
            #     print('Position:', entity.position)
            #     print('Health:', f'{round(entity.health, 2)}/{round(entity.health_max, 2)} ({round(entity.health_ratio, 2)})')
            #     print()

            # print('CHAMPIONS')
            # for entity in game.minion_manager.entities:
            #     print('CHAMPION')
            #     print('Memory addresss:', hex(entity.address))
            #     print('Memory name:', entity.name_memory)
            #     print('Position:', entity.position)
            #     print('Health:', f'{round(entity.health, 2)}/{round(entity.health_max, 2)} ({round(entity.health_ratio, 2)})')
            #     print()

            # print('TOWERS')
            # for entity in game.tower_manager.entities:
            #     print('TOWER')
            #     print('Memory addresss:', hex(entity.address))
            #     print('Memory name:', entity.name_memory)
            #     print('Position:', entity.position)
            #     print('Health:', f'{round(entity.health, 2)}/{round(entity.health_max, 2)} ({round(entity.health_ratio, 2)})')
            #     print()
