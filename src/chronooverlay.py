import tkinter as tk
# from PIL import Image, ImageTk
from infi.systray import SysTrayIcon

import win32gui
# import win32con
# import win32api

from pathlib import PurePath
from pymem.exception import ProcessError, MemoryReadError


# https://stackoverflow.com/questions/63047053/how-to-replace-a-background-image-in-tkinter
# https://stackoverflow.com/questions/59334733/resize-photoimage-using-zoom-or-subsample
# https://stackoverflow.com/questions/29641616/drag-window-when-using-overrideredirect


path_img = PurePath(PurePath(__file__).parent, 'img')


class CustomFrame(tk.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # def RBGAImage(path):
        #     return Image.open(path).convert('RGBA')

        # frame = RBGAImage('bluepot.png')
        # frame = ImageTk.PhotoImage(frame)

        image = tk.PhotoImage(file=PurePath(path_img, 'window.png'))

        self.background_image = image.zoom(2).subsample(3)
        self.background = tk.Label(self, border=0, bg='grey15', image=self.background_image)
        self.background.pack(fill=tk.BOTH, expand=True)


class ChronoOverlay(tk.Tk):

    def __init__(self, game, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.game = game

        self.overrideredirect(True)  # Deletes Windows' default title bar

        self.wm_attributes('-alpha', 0.75)
        self.wm_attributes('-transparentcolor', 'grey15')  # str_a_ange color to avoid jagged borders
        self.wm_attributes("-topmost", True)

        frame = CustomFrame(self)
        frame.pack(side='top', fill='both', expand='True')

        self._offsetx = 0
        self._offsety = 0

        self.bind('<Escape>', self.close)
        self.bind('<Button-1>', self.click)
        self.bind('<B1-Motion>', self.drag)

        if not hasattr(self.game, 'mockup'):
            self.set_geometry()
        else:
            self.geometry("213x320")

        self.set_title_bar()
        self.set_headers()
        self.set_labels()

    def show(self, event):
        self.deiconify()

    def hide(self, event):
        self.withdraw()

    def close(self, event):
        self.quit()

    def drag(self, event):
        x = self.winfo_pointerx() - self._offsetx
        y = self.winfo_pointery() - self._offsety
        self.geometry('+{x}+{y}'.format(x=x, y=y))

    def click(self, event):
        self._offsetx = event.x
        self._offsety = event.y

    def set_geometry(self):
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
        game_resolution = {'width': client_properties['width'], 'height': client_properties['height']}
        is_borderless = True if window_resolution == game_resolution else False

        # self.geometry('320x480')
        self.geometry(f"213x320+{window_properties['margin_left'] + window_properties['width'] - 228}+146")
        # self.geometry('160x240')

    def create_label(self, text, size, color):
        return tk.Label(self,
                        textvariable=text,
                        font=('Tahoma', size),
                        fg=color,
                        bg='#1F1F1F',  # Color from image
                        bd=0,  # Important to adjust borders
                        padx=0,
                        pady=0)

    def set_title_bar(self):
        def reset_jungle_chrono():
            for widget in self.winfo_children():
                if isinstance(widget, tk.Label) or isinstance(widget, tk.Button):
                    try:
                        value = self.getvar(widget['textvariable'])
                        if value not in ['BLUEPOT', '', 'Start', 'End', 'Clear']:
                            # widget.place_forget()
                            widget.config(fg='#1F1F1F')
                    except tk.TclError:
                        pass

            self.game.reset_jungle()

        # LOGO
        image = tk.PhotoImage(file=PurePath(path_img, 'potion.png'))
        image_logo = image.subsample(9)

        self.logo = tk.Label(self, border=0, bg='#1F1F1F', image=image_logo)
        self.logo.image = image_logo  # * Otherwise this won't work
        self.logo.place(x=11, y=13)

        self.logo_label = tk.Label(self, text='Bluepot', font=('Tahoma', 10, 'bold'), fg='#72A7E8', bg='#1F1F1F', bd=0, pady=0)
        self.logo_label.place(x=37, y=13)

        # BUTTONS
        self.button_reset = tk.Button(self, text='Reset', font=('Tahoma', 10, 'bold'), fg='white', bg='#1F1F1F', bd=0, pady=0, command=reset_jungle_chrono)
        self.button_reset.place(x=156, y=10)

        self.button_export = tk.Button(self, text='Export', font=('Tahoma', 10, 'bold'), fg='white', bg='#1F1F1F', bd=0, pady=0)
        self.button_export.place(x=106, y=10)

    def set_headers(self):
        # START
        self.header_total_text = tk.StringVar()
        self.header_total_text.set('Start')

        self.header_total_label = self.create_label(self.header_total_text, 10, 'yellow')
        self.header_total_label.place(x=66, y=19 + 21)

        # END
        self.header_end_text = tk.StringVar()
        self.header_end_text.set('End')

        self.header_end_label = self.create_label(self.header_end_text, 10, 'yellow')
        self.header_end_label.place(x=114, y=19 + 21)

        # TOTAL
        self.header_total_text = tk.StringVar()
        self.header_total_text.set('Clear')

        self.header_total_label = self.create_label(self.header_total_text, 10, 'yellow')
        self.header_total_label.place(x=162, y=19 + 21)

    def set_mockup(self):
        jungle_chrono = {
            'gromp_blue': {'name': 'Gromp', 'color': '#72a7e8', 'start': '4:23.5', 'end': '5:23.5', 'total': '7:23.5'},
            'moving_1': {'name': '..........', 'color': 'white', 'start': '0:00:0', 'end': '0:00:0', 'total': '0:00:0'},
            'blue_blue': {'name': 'Blue', 'color': '#72a7e8', 'start': '0:00:0', 'end': '0:00:0', 'total': '0:00:0'},
            'moving_2': {'name': '..........', 'color': 'white', 'start': '0:00:0', 'end': '0:00:0', 'total': '0:00:0'},
            'wolves_blue': {'name': 'Wolves', 'color': '#72a7e8', 'start': '0:00:0', 'end': '0:00:0', 'total': '0:00:0'},
            'moving_3': {'name': '..........', 'color': 'white', 'start': '0:00:0', 'end': '0:00:0', 'total': '0:00:0'},
            'gromp_red': {'name': 'Raptors', 'color': '#e87272', 'start': '0:00:0', 'end': '0:00:0', 'total': '0:00:0'},
            'moving_4': {'name': '..........', 'color': 'white', 'start': '0:00:0', 'end': '0:00:0', 'total': '0:00:0'},
            'blue_red': {'name': 'Red', 'color': '#e87272', 'start': '0:00:0', 'end': '0:00:0', 'total': '0:00:0'},
            'moving_5': {'name': '..........', 'color': 'white', 'start': '0:00:0', 'end': '0:00:0', 'total': '0:00:0'},
            'wolves_red': {'name': 'Krugs', 'color': '#e87272', 'start': '0:00:0', 'end': '0:00:0', 'total': '0:00:0'},
            'total': {'name': 'TOTAL', 'color': 'yellow', 'start': '6camp', 'end': '0:00:0--', 'total': '0:00:0'},
        }

        self.geometry("213x320")

        # LABELS
        n_row = 2
        spacing = 21

        for step_name, step_info in jungle_chrono.items():
            # NAME
            setattr(self, f'{n_row}_name_text', tk.StringVar())
            text = getattr(self, f'{n_row}_name_text')
            text.set(step_info['name'])

            setattr(self, f'{n_row}_name_label', self.create_label(text, 10, step_info['color']))
            label = getattr(self, f'{n_row}_name_label')

            label.place(x=13, y=18 + n_row * spacing)

            # START
            setattr(self, f'{n_row}_start_text', tk.StringVar())
            text = getattr(self, f'{n_row}_start_text')
            text.set(step_info['start'])

            setattr(self, f'{n_row}_start_label', self.create_label(text, 10, 'white'))
            label = getattr(self, f'{n_row}_start_label')

            label.place(x=66, y=19 + n_row * spacing)

            # END
            setattr(self, f'{n_row}_end_text', tk.StringVar())
            text = getattr(self, f'{n_row}_end_text')
            text.set(step_info['end'])

            setattr(self, f'{n_row}_end_label', self.create_label(text, 10, 'green'))
            label = getattr(self, f'{n_row}_end_label')

            label.place(x=114, y=19 + n_row * spacing)

            # CLEAR
            setattr(self, f'{n_row}_clear_text', tk.StringVar())
            text = getattr(self, f'{n_row}_clear_text')
            text.set(step_info['total'])

            setattr(self, f'{n_row}_clear_label', self.create_label(text, 10, 'yellow'))
            label = getattr(self, f'{n_row}_clear_label')

            label.place(x=162, y=19 + n_row * spacing)

            n_row += 1

    def set_labels(self):
        spacing = 21
        for n in range(2, 14):  # 0 = nav, 1 = headers
            # NAME
            setattr(self, f'{n}_name_text', tk.StringVar())
            text = getattr(self, f'{n}_name_text')

            setattr(self, f'{n}_name_label', self.create_label(text, 10, 'white'))
            label = getattr(self, f'{n}_name_label')
            label.place(x=13, y=18 + n * spacing)

            # START
            setattr(self, f'{n}_start_text', tk.StringVar())
            text = getattr(self, f'{n}_start_text')

            setattr(self, f'{n}_start_label', self.create_label(text, 10, 'white'))
            label = getattr(self, f'{n}_start_label')
            label.place(x=66, y=19 + n * spacing)

            # END
            setattr(self, f'{n}_end_text', tk.StringVar())
            text = getattr(self, f'{n}_end_text')

            setattr(self, f'{n}_end_label', self.create_label(text, 10, 'green'))
            label = getattr(self, f'{n}_end_label')
            label.place(x=114, y=19 + n * spacing)

            # CLEAR
            setattr(self, f'{n}_clear_text', tk.StringVar())
            text = getattr(self, f'{n}_clear_text')

            setattr(self, f'{n}_clear_label', self.create_label(text, 10, 'yellow'))
            label = getattr(self, f'{n}_clear_label')
            label.place(x=162, y=19 + n * spacing)

    def update_labels(self):
        try:
            if self.game.get_jungle_chrono():
                # FIRST ERASE CURRENT TEXT
                for n in range(2, 14):
                    # NAME
                    text = getattr(self, f'{n}_name_text')
                    text.set('')

                    # START
                    text = getattr(self, f'{n}_start_text')
                    text.set('')

                    # END
                    text = getattr(self, f'{n}_end_text')
                    text.set('')

                    # CLEAR
                    text = getattr(self, f'{n}_clear_text')
                    text.set('')

                n = 2
                for step_name, step_info in self.game.get_jungle_chrono().items():
                    # NAME
                    label = getattr(self, f'{n}_name_label')
                    label.config(fg=step_info['color'])

                    text = getattr(self, f'{n}_name_text')
                    text.set(step_info['name'])

                    # START
                    label = getattr(self, f'{n}_start_label')
                    label.config(fg='white')

                    text = getattr(self, f'{n}_start_text')
                    text.set(step_info['start'])

                    # END
                    label = getattr(self, f'{n}_end_label')
                    label.config(fg='green')

                    text = getattr(self, f'{n}_end_text')
                    text.set(step_info['end'])

                    # CLEAR
                    label = getattr(self, f'{n}_clear_label')
                    label.config(fg='yellow')

                    text = getattr(self, f'{n}_clear_text')
                    text.set(step_info['total'])

                    n += 1

        except ProcessError or MemoryReadError:
            '''Game finished!'''
            self.quit()

        self.after(1, self.update_labels)

    def run(self):
        self.after(1, self.update_labels)
        self.mainloop()

    def create(self):
        '''Set system tray icon'''
        menu_options = (('Show', None, self.show),
                        ('Hide', None, self.hide),
                        )

        path = str(PurePath(path_img, 'potion.ico'))
        systray = SysTrayIcon(path, 'Bluepot', menu_options, on_quit=self.close)
        systray.start()

        self.run()


if __name__ == '__main__':

    class Game():
        def __init__(self):
            self.mockup = True

        def get_jungle_chrono(self):
            return

        def reset_jungle(self):
            return

    game = Game()

    overlay = ChronoOverlay(game)
    overlay.set_mockup()
    overlay.create()
