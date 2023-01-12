import json
import warnings
import requests
import keyboard

from pathlib import Path
from threading import Thread
from pymem import Pymem
from bs4 import MarkupResemblesLocatorWarning

from src.models.game import Game
from src.functions import get_base_dir, is_game_live
from src.trayicon import TrayIcon
from src.newreleasewindow import NewReleaseWindow
from src.chronooverlay import ChronoOverlay
# from src.minimapoverlay import MinimapOverlay


# Ignore bs4 warning
warnings.filterwarnings('ignore', category=MarkupResemblesLocatorWarning, module='bs4')

base_dir = get_base_dir()
data_dir = base_dir / 'data'


class BluePot():
    version = '1.2.0'

    def __init__(self, use_chrono_overlay=False, use_chrono_overlay_hotkeys=False):
        self._check_new_release()

        self._use_chrono_overlay = True if use_chrono_overlay else False
        self._use_hotkeys = True if use_chrono_overlay_hotkeys else False

        self._pm = None
        self._game = None

        self._chrono_overlay_thread = None
        self._hotkey_stop_thread = None
        self._hotkey_reset_thread = None

        self._chrono_overlay = None

        if self._use_hotkeys:
            self.hotkey_stop = 69  # Pause key <event.scan_code>
            self.hotkey_reset = 14  # Backspace key
            self._game_hotkeys_settings_init()

    def _check_new_release(self):
        request = requests.get('https://api.github.com/repos/j4n7/bluepot/releases/latest')
        version_remote = [int(n) for n in request.json()['name'][1:].split('.')]
        version_local = [int(n) for n in BluePot.version.split('.')]

        new_release_available = False
        if version_remote[0] > version_local[0]:
            new_release_available = True
        elif version_remote[1] > version_local[1]:
            new_release_available = True
        elif version_remote[2] > version_local[2]:
            new_release_available = True

        if new_release_available:
            new_release_window = NewReleaseWindow()
            new_release_window.mainloop()

    def _game_tray_icon_init(self):
        TrayIcon()

    def _game_listener_init(self):
        '''
        Executes an infinite loop in a thread.
        It checks if a game is live and connects
        or disconnects to it accordingly.
        It also starts or stops any other related
        functionalities (overlays and hotkeys) that
        are using sub-threads.
        '''
        def set_game_listener():
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

                    if self._chrono_overlay_thread:
                        if self._chrono_overlay:
                            self._chrono_overlay.terminate()
                            print('\nChrono overlay destroyed')

                        self._chrono_overlay_thread = None
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

                if self._use_chrono_overlay:
                    self._game_chrono_overlay_init()

                if self._use_hotkeys:
                    self._game_hotkeys_init()

        thread = Thread(name='game_listener', target=set_game_listener)
        thread.start()

    def _game_chrono_overlay_init(self):
        '''Sub-thread - Tkinter is not thread safe!'''
        if self._game and not self._chrono_overlay_thread:
            def set_chrono_overlay(game):
                self._chrono_overlay = ChronoOverlay(game)
                self._chrono_overlay.run()

            print('\nOverlay started')

            # * Daemon arg is important for being able to abruptly reset thread
            self._chrono_overlay_thread = Thread(name='chrono_overlay', target=set_chrono_overlay, args=(self._game,), daemon=True)
            self._chrono_overlay_thread.start()

    def _game_hotkeys_init(self):
        '''Sub-thread'''
        if self._game and self._chrono_overlay and not self._hotkey_stop_thread:
            def set_hotkey_stop():
                keyboard.add_hotkey(self.hotkey_stop, lambda: self._chrono_overlay.stop())
                keyboard.wait()

            print('\nStop hotkey started')

            self._hotkey_stop_thread = Thread(name='hotkey_stop', target=set_hotkey_stop, daemon=True)
            self._hotkey_stop_thread.start()

        if self._game and self._chrono_overlay and not self._hotkey_reset_thread:
            def set_hotkey_reset():
                keyboard.add_hotkey(self.hotkey_reset, lambda: self._chrono_overlay.reset())
                keyboard.wait()

            print('\nReset hotkey started')

            self._hotkey_reset_thread = Thread(name='hotkey_reset', target=set_hotkey_reset, daemon=True)
            self._hotkey_reset_thread.start()

    def _game_hotkeys_settings_init(self):
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

    def get_game(self):
        while True:
            if self._game:
                return self._game

    def get_champion_local(self):
        while True:
            if self._game and self._game.champion_local:
                return self._game.champion_local

    def start(self):
        '''The order of execution of these methods is non trivial.'''
        self._game_tray_icon_init()
        self._game_listener_init()


if __name__ == '__main__':

    bluepot = BluePot(use_chrono_overlay=True)
    bluepot.start()

    game = bluepot.get_game()
    chat = game.chat
    champion_local = game.champion_local
    champion_name = game.champion_local.name
