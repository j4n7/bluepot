import tkinter as tk

import win32gui
import win32con
import win32api

from pymem.exception import ProcessError, MemoryReadError

from src.functions import format_time, format_timer


# https://stackoverflow.com/questions/16726050/how-do-we-get-the-border-size-of-a-window
# https://stackoverflow.com/questions/67544105/click-through-tkinter-windows
# https://stackoverflow.com/questions/70149724/tkinter-canvas-without-white-background-make-it-transparent
# https://stackoverflow.com/questions/214359/converting-hex-color-to-rgb-and-vice-versa


class MinimapOverlay:
    def __init__(self, minimap_resolution, get_new_text_callback):

        self.get_new_text_callback = get_new_text_callback
        self.game_resolution = {'width': None, 'height': None}

        self.minimap_resolution = minimap_resolution
        self.minimap_font_size = ''
        self.minimap_camps_positions = {}

        self.transparent_color = '#000000'

        self.root = tk.Tk()
        self.get_geometry()
        self.set_proportions()

        self.root.title("Blue Pot")
        self.root.config(bg=self.transparent_color)

        self.root.overrideredirect(True)  # Deletes border from window
        # self.root.lift()
        self.root.attributes("-transparentcolor", self.transparent_color)
        self.root.attributes("-topmost", True)

        self.set_labels()
        self.set_not_interactive(self.root)

    def get_geometry(self):
        # WINDOW RECT
        # Origin (x = 0, y = 0) is left top corner of full screen
        # Margin left: distance from x = 0 to left side
        # Margin right: distance from x = 0 to right side
        # Margin top: distance from y = 0 to top side
        # Margin bottom: distance from y = 0 to bottom side

        window_name = 'League of Legends (TM) Client'  # 'League of Legends (TM) Client'
        window_handle = win32gui.FindWindow(None, window_name)
        window_rect = win32gui.GetWindowRect(window_handle)
        client_rect = win32gui.GetClientRect(window_handle)

        window_properties = {
            'margin_left': window_rect[0],
            'margin_top': window_rect[1],
            'margin_right': window_rect[2],
            'margin_bottom': window_rect[3],
            'width': window_rect[2] - window_rect[0],
            'height': window_rect[3] - window_rect[1],
        }

        # In relation to window
        client_properties = {
            'margin_left': client_rect[0],
            'margin_top': client_rect[1],
            'margin_right': client_rect[2],
            'margin_bottom': client_rect[3],
            'width': client_rect[2] - client_rect[0],
            'height': client_rect[3] - client_rect[1],
        }

        window_resolution = {'width': window_properties['width'], 'height': window_properties['height']}
        self.game_resolution = {'width': client_properties['width'], 'height': client_properties['height']}
        is_borderless = True if window_resolution == self.game_resolution else False

        minimap_offset = 6
        minimap_resolution = {'width': self.minimap_resolution['width'] + minimap_offset, 'height': self.minimap_resolution['height'] + minimap_offset}
        minimap_margin_x = window_properties['margin_left'] + window_properties['width'] - minimap_resolution['width'] - minimap_offset
        minimap_margin_y = window_properties['margin_top'] + window_properties['height'] - minimap_resolution['height'] - minimap_offset
        self.root.geometry(f"{int(minimap_resolution['width'])}x{int(minimap_resolution['height'])}+{int(minimap_margin_x)}+{int(minimap_margin_y)}")

    def set_not_interactive(self, tk_object):
        if not tk_object['bg'].startswith('#'):
            raise ValueError('Tkinter object needs background color to be set in hex format.')

        def hex_to_rgb(value):
            """Return (red, green, blue) for the color given as #rrggbb."""
            value = value.lstrip('#')
            lv = len(value)
            return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

        bg = hex_to_rgb(tk_object['bg'])
        colorkey = win32api.RGB(bg[0], bg[1], bg[2])
        hwnd = tk_object.winfo_id()
        wnd_exstyle = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        wnd_exstyle |= win32con.WS_EX_LAYERED  # | win32con.WS_EX_TRANSPARENT (seems to be unnecesary)
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, wnd_exstyle)
        win32gui.SetLayeredWindowAttributes(hwnd, colorkey, 255, win32con.LWA_COLORKEY)

    def set_proportions(self):
        # ! This shouldn't be hard coded
        # game_resolution == '1280x1024', map_resolution = 242x242 (33 = ingame)
        self.minimap_font_size = '8'
        self.minimap_camps_positions = {
            'gromp_blue': {'x': 0.15, 'y': 0.43},
            'blue_blue': {'x': 0.265, 'y': 0.47},
            'wolves_blue': {'x': 0.261, 'y': 0.57},
            'raptors_blue': {'x': 0.46, 'y': 0.63},
            'red_blue': {'x': 0.527, 'y': 0.73},
            'krugs_blue': {'x': 0.58, 'y': 0.817},
            'gromp_red': {'x': 1.01 - 0.15, 'y': 1 - 0.43},
            'blue_red': {'x': 1.01 - 0.265, 'y': 1 - 0.47},
            'wolves_red': {'x': 1.01 - 0.261, 'y': 1 - 0.57},
            'raptors_red': {'x': 1.01 - 0.46, 'y': 0.99 - 0.63},
            'red_red': {'x': 1.01 - 0.527, 'y': 1 - 0.73},
            'krugs_red': {'x': 1.01 - 0.58, 'y': 1 - 0.817}
        }

    def set_camp_position(self, ratio):
        return ratio * self.minimap_resolution['width']

    def create_label(self, text):
        return tk.Label(self.root,
                        textvariable=text,
                        font=('Tahoma', self.minimap_font_size),
                        fg='yellow',
                        bg=self.transparent_color,
                        bd=0,  # Important do adjust borders
                        padx=0,
                        pady=0)

    def set_labels(self):
        for camp_name, position in self.minimap_camps_positions.items():

            setattr(self, f"{camp_name}_text", tk.StringVar())
            text = getattr(self, f"{camp_name}_text")

            setattr(self, f"{camp_name}_label", self.create_label(text))
            label = getattr(self, f"{camp_name}_label")

            label.place(x=self.set_camp_position(position['x']), y=self.set_camp_position(position['y']), anchor='center')

    def update_labels(self):
        try:
            for camp_name, camp_stored_info in self.get_new_text_callback().items():
                if camp_name in self.minimap_camps_positions:
                    text = getattr(self, f"{camp_name}_text")
                    text.set('')
                    if camp_stored_info['timer']:
                        time = format_timer(format_time(camp_stored_info['timer']))
                        if len(time) <= 5:  # ! Patching some errors (e.g., 1349:00)
                            if time != '0':  # Exclude 0 seconds
                                text.set(time)
        except ProcessError or MemoryReadError:
            '''Game finished!'''
            self.root.quit()

        self.root.after(1, self.update_labels)

    def run(self):
        self.root.after(1, self.update_labels)
        self.root.mainloop()
