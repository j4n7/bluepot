import os

from infi.systray import SysTrayIcon
from pathlib import PurePath


class TrayIcon():
    '''System tray icon'''

    def __init__(self):
        # menu_options = (('Show', None, lambda _: print('Show')),
        #                 ('Hide', None, lambda _: print('Hide')),
        #                 )

        menu_options = ()

        path_img = PurePath(PurePath(__file__).parent, 'img')
        path_icon = str(PurePath(path_img, 'potion.ico'))

        systray = SysTrayIcon(path_icon, 'BluePot', menu_options, on_quit=lambda _: os._exit(0))
        systray.start()


if __name__ == '__main__':

    TrayIcon()
