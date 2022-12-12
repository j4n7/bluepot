from pathlib import Path
from threading import Thread
from pymem import Pymem
from pymem.exception import MemoryReadError

import json
import keyboard

from src.models.game import Game
from src.functions import get_base_dir, is_game_live
from src.trayicon import TrayIcon
from src.chronooverlay import ChronoOverlay
# from src.minimapoverlay import MinimapOverlay


base_dir = get_base_dir()
data_dir = base_dir / 'data'


class BluePot():
    def __init__(self):
        self._pm = None
        self._game = None

        self._chrono_thread = None
        self._hotkey_stop_thread = None
        self._hotkey_reset_thread = None

        self._chrono_overlay = None
        self._draw_overlay = False

        self.hotkey_stop = 69  # Pause key <event.scan_code>
        self.hotkey_reset = 14  # Backspace key

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

                    if self._hotkey_stop_thread:
                        self._hotkey_stop_thread = None
                        print('\nStop key thread destroyed')

                    if self._hotkey_reset_thread:
                        self._hotkey_reset_thread = None
                        print('\nReset key thread destroyed')

                    if waiting_message:
                        print('\nWaiting for game...')
                    waiting_message = False

                if self._pm and not self._game:
                    self._game = Game(self._pm)

                if self._draw_overlay:
                    self._game_chrono_overlay()
                    self._game_hotkeys_init()

        game_thread = Thread(name='game_connect', target=set_game_connect)
        game_thread.start()

    def _game_chrono_overlay(self):
        if self._game and not self._chrono_thread:
            def set_chrono_overlay(game):
                self._chrono_overlay = ChronoOverlay(game)
                self._chrono_overlay.run()

            # * Daemon arg is important for being able to abruptly reset thread
            self._chrono_thread = Thread(name='chrono_overlay', target=set_chrono_overlay, args=(self._game,), daemon=True)
            self._chrono_thread.start()

    def _game_hotkeys_set(self):
        txt_file = Path('hotkeys_settings.txt')
        if not txt_file.is_file():
            return

        with open('hotkeys_settings.txt') as txt_file:
            hotkeys_user = [line.rstrip() for line in txt_file]
    
        with open(data_dir / 'hotkeys.json') as json_file:
            hotkeys = json.load(json_file)
        
        hotkeys_stop = [hotkey for hotkey in hotkeys_user[8:18] if not hotkey.startswith('#')]
        hotkeys_reset = [hotkey for hotkey in hotkeys_user[21:31] if not hotkey.startswith('#')]

        if hotkeys_stop and len(hotkeys_stop) == 1 and hotkeys_stop[0] in hotkeys:
            self.hotkey_stop = hotkeys[hotkeys_stop[0]]

        if hotkeys_reset and len(hotkeys_reset) == 1 and hotkeys_reset[0] in hotkeys:
            self.hotkey_reset = hotkeys[hotkeys_reset[0]]

    def _game_hotkeys_init(self):
        if self._game and self._chrono_overlay and not self._hotkey_stop_thread:
            def set_hotkey_stop():
                keyboard.add_hotkey(self.hotkey_stop, lambda: self._chrono_overlay.stop())
                keyboard.wait()

            self._hotkey_stop_thread = Thread(name='hotkey_stop', target=set_hotkey_stop, daemon=True)
            self._hotkey_stop_thread.start()

        if self._game and self._chrono_overlay and not self._hotkey_reset_thread:
            def set_hotkey_reset():
                keyboard.add_hotkey(self.hotkey_reset, lambda: self._chrono_overlay.reset())
                keyboard.wait()

            self._hotkey_reset_thread = Thread(name='hotkey_reset', target=set_hotkey_reset, daemon=True)
            self._hotkey_reset_thread.start()

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
        '''The order of execution of these methods is non trivial.'''
        self._game_hotkeys_set()
        self._game_tray_icon()
        self._game_connect()


if __name__ == '__main__':

    bluepot = BluePot()
    bluepot.chrono_overlay()
    bluepot.start()

    game = bluepot.get_game()
    chat = game.chat
    local_player = game.local_player
    champion_name = game.local_player.name
