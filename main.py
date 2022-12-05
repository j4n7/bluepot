from threading import Thread
from pymem import Pymem
from pymem.exception import MemoryReadError

from src.models.game import Game
from src.functions import is_game_live
from src.trayicon import TrayIcon
from src.chronooverlay import ChronoOverlay
# from src.minimapoverlay import MinimapOverlay


class BluePot():
    def __init__(self):
        self._pm = None
        self._game = None
        self._chrono_thread = None

        self._draw_overlay = False

    def _game_tray_icon(self):
        TrayIcon()

    def _game_connect(self):
        def set_game_connect():
            waiting_message = True
            while True:
                if is_game_live():
                    if not self._pm:
                        self._pm = Pymem('League of Legends.exe')
                        print('\nGame live!')
                        waiting_message = True
                else:
                    self._pm = None
                    self._game = None

                    if self._chrono_thread:
                        self._chrono_thread = None
                        print('\nChrono thread destroyed')

                    if waiting_message:
                        print('\nWaiting for game...')
                    waiting_message = False

                if self._pm and not self._game:
                    self._game = Game(self._pm)

                if self._draw_overlay:
                    self._game_chrono_overlay()

        game_thread = Thread(name='game_connect', target=set_game_connect)
        game_thread.start()

    def _game_chrono_overlay(self):
        if self._game and not self._chrono_thread:
            def set_chrono_overlay(game):
                chrono_overlay = ChronoOverlay(game)
                chrono_overlay.run()

            # * Daemon arg is important for being able to abruptly stop thread
            self._chrono_thread = Thread(name='chrono_overlay', target=set_chrono_overlay, args=(self._game,), daemon=True)
            self._chrono_thread.start()

    def chrono_overlay(self):
        self._draw_overlay = True

    def get_game(self):
        while True:
            if self._game:
                return self._game

    def get_local_player(self):
        while True:
            if self._game and self._game.local_player:
                return self._game.local_player

    def start(self):
        self._game_tray_icon()
        self._game_connect()


if __name__ == '__main__':

    bluepot = BluePot()
    bluepot.chrono_overlay()
    bluepot.start()

    game = bluepot.get_game()
    local_player = game.local_player
    champion_name = game.local_player.name_short

    while True:
        print(f'Local player position: {local_player.position}')
