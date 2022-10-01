from pymem import Pymem
from pymem.exception import ProcessNotFound

import src.offsets as offsets

from models.game import Game
from models.chat import Chat
from models.entity import Entity
from models.entitymanager import EntityManager


def format_time(seconds):
    min, sec = divmod(seconds, 60)
    return '%02d:%02d' % (min, sec)


if __name__ == '__main__':

    pm = Pymem('League of Legends.exe')

    game = Game(pm)
    chat = Chat(pm)

    local_player = Entity(pm, pm.read_int(pm.base_address + offsets.local_player))

    minion_manager = EntityManager(pm, offsets.minion_manager)
    champion_manager = EntityManager(pm, offsets.champion_manager)
    turret_manager = EntityManager(pm, offsets.turret_manager)

    if True:
        print('GAME')
        print('Game time:', format_time(game.time.seconds))
        print()

    if True:
        print('CHAT')
        print('Is open?', chat.is_open)
        print('Current message:', chat.message_current)
        print('Number of messages sent:', chat.messages_sent_count)
        print('Messages sent:')
        for n, message in enumerate(chat.messages_sent):
            print(f' · Message {str(n + 1).zfill(2)}:', message)
        print()

    if True:
        print('PLAYER')
        print('Memory addresss:', hex(local_player.address))
        print('Memory name:', local_player.name_memory)
        print('Position:', local_player.position)
        print('Health:', f'{round(local_player.health, 2)}/{round(local_player.health_max, 2)} ({round(local_player.health_ratio, 2)})')
        print()

    if False:
        print('MINIONS & MONSTERS')
        for entity in minion_manager.entities:
            print('MINION')
            print('Memory addresss:', hex(entity.address))
            print('Category:', entity.category)
            print('Memory name:', entity.name_memory)
            print('Name:', entity.name)
            print('Position:', entity.position)
            print('Health:', f'{round(entity.health, 2)}/{round(entity.health_max, 2)} ({round(entity.health_ratio, 2)})')
            print()

    if False:
        print('CHAMPIONS')
        for entity in champion_manager.entities:
            print('CHAMPION')
            print('Memory addresss:', hex(entity.address))
            print('Memory name:', entity.name_memory)
            print('Position:', entity.position)
            print('Health:', f'{round(entity.health, 2)}/{round(entity.health_max, 2)} ({round(entity.health_ratio, 2)})')
            print()

    if False:
        print('TURRETS')
        for entity in turret_manager.entities:
            print('TURRET')
            print('Memory addresss:', hex(entity.address))
            print('Memory name:', entity.name_memory)
            print('Position:', entity.position)
            print('Health:', f'{round(entity.health, 2)}/{round(entity.health_max, 2)} ({round(entity.health_ratio, 2)})')
            print()
