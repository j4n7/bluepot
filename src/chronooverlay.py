import tkinter as tk
# from PIL import Image, ImageTk

import sys
import csv
import datetime
import requests

import win32gui
# import win32con
# import win32api

from pathlib import PurePath
from pymem.exception import ProcessError


# FIX RELATIVE IMPORTS
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    from src.functions import get_base_dir, parse_time, format_time
    from src.chronoexporter import ChronoExporter
else:
    sys.path.append('./src')
    from functions import get_base_dir, parse_time, format_time
    from chronoexporter import ChronoExporter


# https://stackoverflow.com/questions/63047053/how-to-replace-a-background-image-in-tkinter
# https://stackoverflow.com/questions/59334733/resize-photoimage-using-zoom-or-subsample
# https://stackoverflow.com/questions/29641616/drag-window-when-using-overrideredirect


base_dir = get_base_dir()
path_img = PurePath(base_dir, 'src', 'img')


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

        self.frame = CustomFrame(self)
        self.frame.pack(side='top', fill='both', expand='True')

        self._padx = -6

        self._offsetx = 0
        self._offsety = 0

        self._terminate = False

        self.bind('<Button-1>', self.click)
        self.bind('<B1-Motion>', self.drag)

        if hasattr(self.game, 'mockup'):
            self.bind('<Escape>', self._close)
            self.geometry("213x320")
            self.eval('tk::PlaceWindow . center')
        else:
            self.set_geometry()

        self.set_title_bar()
        self.set_headers()
        self.set_labels()

        self.get_clears_optimized(check_updates=True)
        self.chrono_exporter = ChronoExporter(self.game)

    def terminate(self):
        self._terminate = True

    def stop(self):
        self.stop_jungle_chrono()

    def reset(self):
        # ! Not working properly
        self.reset_jungle_chrono()

    def _show(self, event):
        self.deiconify()

    def _hide(self, event):
        self.withdraw()

    def _close(self, event):
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

    def create_button(self, text, size, color, n):
        def set_is_smited(n):
            button = getattr(self, f'{n}_name_button')
            name = button.cget('text')
            if name not in ['..........', 'TOTAL']:
                name = name.lower()
                color = 'blue' if button.cget('fg') == '#72A7E8' else 'red'
                jungle_camp = f'{name}_{color}'
                self.game._jungle_path[jungle_camp]['is_smited'] = not self.game._jungle_path[jungle_camp]['is_smited']
                if self.game._jungle_path[jungle_camp]['is_smited']:
                    button.config(font=('Tahoma', 10, 'underline'))
                else:
                    button.config(font=('Tahoma', 10,))

        return tk.Button(self,
                         textvariable=text,
                         font=('Tahoma', size),
                         fg=color,
                         bg='#1F1F1F',  # Color from image
                         bd=0,  # Important to adjust borders
                         padx=0,
                         pady=0,
                         command=lambda: set_is_smited(n))

    def set_title_bar(self):
        def export_jungle_chrono():
            jungle_chrono = self.format_jungle_chrono(self.get_jungle_chrono(), format_color=False)
            self.chrono_exporter.export(jungle_chrono)

        # LOGO
        image = tk.PhotoImage(file=PurePath(path_img, 'potion.png'))
        image_logo = image.subsample(9)

        self.logo = tk.Label(self, border=0, bg='#1F1F1F', image=image_logo)
        self.logo.image = image_logo  # * Otherwise this won't work
        self.logo.place(x=11, y=13)

        self.logo_label = tk.Label(self, text='BluePot', font=('Tahoma', 10, 'bold'), fg='#72A7E8', bg='#1F1F1F', bd=0, pady=0)
        self.logo_label.place(x=37, y=13)

        # BUTTONS
        self.button_export = tk.Button(self, text='Export', font=('Tahoma', 10, 'bold'), fg='white', bg='#1F1F1F', bd=0, pady=0, command=export_jungle_chrono)
        self.button_export.place(x=106, y=10)

        self.button_reset = tk.Button(self, text='Reset', font=('Tahoma', 10, 'bold'), fg='white', bg='#1F1F1F', bd=0, pady=0, command=self.reset_jungle_chrono)
        self.button_reset.place(x=156, y=10)

    def set_headers(self):
        # PATH TIME
        self.header_path_time_text = tk.StringVar()
        self.header_path_time_text.set('')

        self.header_path_time_label = self.create_label(self.header_path_time_text, 10, 'white')
        self.header_path_time_label.place(x=13, y=19 + 21)

        # START
        self.header_start_text = tk.StringVar()
        self.header_start_text.set('Start')

        self.header_start_label = self.create_label(self.header_start_text, 10, 'yellow')
        self.header_start_label.place(x=self._padx + 66, y=19 + 21)

        # END
        self.header_end_text = tk.StringVar()
        self.header_end_text.set('End')

        self.header_end_label = self.create_label(self.header_end_text, 10, 'yellow')
        self.header_end_label.place(x=self._padx + 114, y=19 + 21)

        # TOTAL
        self.header_total_text = tk.StringVar()
        self.header_total_text.set('Clear')

        self.header_total_label = self.create_label(self.header_total_text, 10, 'yellow')
        self.header_total_label.place(x=self._padx + 162, y=19 + 21)

    def get_clears_optimized(self, check_updates=False):
        csv_path = base_dir / 'data' / 'clears_optimized.csv'

        if check_updates:
            with requests.Session() as session:
                request = session.get('https://raw.githubusercontent.com/j4n7/bluepot/develop/data/clears_optimized.csv')
                decoded_content = request.content.decode('utf-8')
                reader = csv.reader(decoded_content.splitlines())
                remote = [row for row in reader]
                version_remote = int(remote[0][0].split(' ')[0])

            with open(csv_path) as csv_file:
                reader = csv.reader(csv_file)
                version_local = int(next(reader)[0].split(' ')[0])

            if version_remote > version_local:
                with open(csv_path, 'w', newline='', encoding='utf-8') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerows(remote)

        with open(csv_path) as csv_file:
            dict_reader = csv.DictReader(csv_file)
            clears_optimized = list(dict_reader)

        self.clears_optimized = [clear for clear in clears_optimized if clear['Champ'] == self.game.champion_local.name]

    def get_jungle_chrono(self):

        def get_name_and_color(step_name):
            name, color = step_name.split('_')
            if name == 'moving':
                name = '..........'
                color = None
            # if color == 'blue':
            #     color = '#72A7E8'
            # elif color == 'red':
            #     color = '#E87272'
            return name.capitalize(), color

        jungle_chrono = {}
        n_step = 0
        n_camps = 0
        n_camp = 0
        end_current = datetime.timedelta(seconds=0)
        for step_name, step_info in self.game._jungle_path.items():
            if self.game.path_start and n_step <= 10 and n_camps <= 5:  # * Max overlay space

                end_current = step_info['end'] if step_info['end'] and step_info['end'] > end_current and step_info['total'] else end_current
                clear_current = self.game.time - self.game.path_start + self.game.offset_start

                start = step_info['start'] if step_info['start'] else datetime.timedelta(seconds=0)
                end = step_info['end'] if step_info['end'] else (clear_current if clear_current else datetime.timedelta(seconds=0))
                total = step_info['total'] if step_info['end'] else clear_current - step_info['start']

                name, color = get_name_and_color(step_name)

                n_camps = n_camps + 1 if not step_name.startswith('moving') and step_info['end'] else n_camps
                n_step += 1

                jungle_chrono[step_name] = {'name': name, 'color': color, 'is_smited': step_info['is_smited'],
                                            'start': start, 'end': end, 'total': total,
                                            'start_optimized': None, 'end_optimized': None, 'total_optimized': None}

                clears_optimized_coincidences = []
                if not step_name.startswith('moving'):
                    n_camp += 1
                    for clear in self.clears_optimized:
                        if clear[f'C{n_camp} Name'] == name and clear[f'C{n_camp} Color'] == color.capitalize():
                            clears_optimized_coincidences.append(clear)

                            start_optimized = parse_time(clear[f'C{n_camp} Start'])
                            end_optimized = parse_time(clear[f'C{n_camp} End'])
                            total_optimized = parse_time(clear[f'C{n_camp} Total'])

                            if step_info['start']:
                                if start - start_optimized > datetime.timedelta(seconds=2):
                                    jungle_chrono[step_name]['start_optimized'] = 'red'
                                elif start - start_optimized <= datetime.timedelta(seconds=2) and start - start_optimized > datetime.timedelta(seconds=0):
                                    jungle_chrono[step_name]['start_optimized'] = 'yellow'
                                else:
                                    jungle_chrono[step_name]['start_optimized'] = 'green'

                            if step_info['end']:
                                if end - end_optimized > datetime.timedelta(seconds=2):
                                    jungle_chrono[step_name]['end_optimized'] = 'red'
                                elif end - end_optimized <= datetime.timedelta(seconds=2) and end - end_optimized > datetime.timedelta(seconds=0):
                                    jungle_chrono[step_name]['end_optimized'] = 'yellow'
                                else:
                                    jungle_chrono[step_name]['end_optimized'] = 'green'

                                if total - total_optimized > datetime.timedelta(seconds=2):
                                    jungle_chrono[step_name]['total_optimized'] = 'red'
                                elif total - total_optimized <= datetime.timedelta(seconds=2) and total - total_optimized > datetime.timedelta(seconds=0):
                                    jungle_chrono[step_name]['total_optimized'] = 'yellow'
                                else:
                                    jungle_chrono[step_name]['total_optimized'] = 'green'
                            else:
                                jungle_chrono[step_name]['end_optimized'] = '#B372E8'
                                jungle_chrono[step_name]['end'] = total_optimized

                    self.clears_optimized = clears_optimized_coincidences if clears_optimized_coincidences else self.clears_optimized

        if jungle_chrono:
            jungle_chrono['total'] = {'name': 'TOTAL',
                                      'color': None,
                                      'is_smited': None,
                                      'start': f'{n_camps}camps',
                                      'end': end_current if end_current else '',
                                      'total': end_current - self.game.offset_start if end_current else '',
                                      'start_optimized': None, 'end_optimized': None, 'total_optimized': None}

        return jungle_chrono

    def stop_jungle_chrono(self):
        last_step_name = list(self.game._jungle_path)[-1] if self.game._jungle_path else None
        if last_step_name and not last_step_name.startswith('moving'):
            self.game._jungle_camps_stopped.append(last_step_name)

    def reset_jungle_chrono(self):
        self.game.reset_jungle()
        self.game.reset = True
        for widget in self.winfo_children():
            if isinstance(widget, tk.Label) or isinstance(widget, tk.Button):
                try:
                    value = self.getvar(widget['textvariable'])
                    if value not in ['', 'Start', 'End', 'Clear']:
                        # widget.place_forget()
                        widget.config(fg='#1F1F1F')
                except tk.TclError:
                    pass

    def format_jungle_chrono(self, jungle_chrono, format_color=True):
        if not jungle_chrono:
            return None

        for step_name, step_info in jungle_chrono.items():
            if format_color:
                step_info['color'] = '#72A7E8' if step_info['color'] == 'blue' else '#E87272' if step_info['color'] == 'red' else 'yellow' if step_name == 'total' else 'white'
            step_info['start'] = format_time(step_info['start'], mode='sec2') if type(step_info['start']) is not str else step_info['start']
            step_info['end'] = format_time(step_info['end'], mode='sec2') if step_info['end'] else ''
            step_info['total'] = format_time(step_info['total'], mode='sec2') if step_info['total'] else ''

            if not step_info['start']:
                # For first camp
                step_info['start'] = '0:00.00'

            # if step_name == 'total' and step_info['end']:
            #     step_info['end'] += '-'

        return jungle_chrono

    def set_labels(self):
        spacing = 21
        for n in range(2, 14):  # 0 = nav, 1 = headers
            # NAME
            setattr(self, f'{n}_name_text', tk.StringVar())
            text = getattr(self, f'{n}_name_text')

            setattr(self, f'{n}_name_button', self.create_button(text, 10, 'white', n))
            button = getattr(self, f'{n}_name_button')
            button.config(font=('Tahoma', 10,)) if self.game.reset else None
            button.place(x=13, y=16 + n * spacing)

            # START
            setattr(self, f'{n}_start_text', tk.StringVar())
            text = getattr(self, f'{n}_start_text')

            setattr(self, f'{n}_start_label', self.create_label(text, 10, 'white'))
            label = getattr(self, f'{n}_start_label')
            label.place(x=self._padx + 66, y=19 + n * spacing)

            # END
            setattr(self, f'{n}_end_text', tk.StringVar())
            text = getattr(self, f'{n}_end_text')

            setattr(self, f'{n}_end_label', self.create_label(text, 10, 'green'))
            label = getattr(self, f'{n}_end_label')
            label.place(x=self._padx + 114, y=19 + n * spacing)

            # CLEAR
            setattr(self, f'{n}_clear_text', tk.StringVar())
            text = getattr(self, f'{n}_clear_text')

            setattr(self, f'{n}_clear_label', self.create_label(text, 10, 'yellow'))
            label = getattr(self, f'{n}_clear_label')
            label.place(x=self._padx + 162, y=19 + n * spacing)

    def update_labels(self):
        if hasattr(self.game, 'mockup'):
            return

        if self._terminate:
            '''Game finished'''
            self.destroy()

        # RESET
        if self.game.reset:
            for n in range(2, 14):
                button = getattr(self, f'{n}_name_button')
                button.config(font=('Tahoma', 10,))
                label = getattr(self, f'{n}_start_label')
                label.config(fg='white')
                label = getattr(self, f'{n}_end_label')
                label.config(fg='green')
                label = getattr(self, f'{n}_clear_label')
                label.config(fg='yellow')
            self.game.reset = False
            self.chrono_exporter.saves_n = 0
            self.get_clears_optimized()

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

        try:
            # PATH TIME
            if self.game.time_jungle_path.total_seconds() > 180:
                # 3:00: Second charge of Smite is ready
                self.header_path_time_label.config(fg='green')
            else:
                self.header_path_time_label.config(fg='white')
            self.header_path_time_text.set(format_time(self.game.time_jungle_path))
        except TypeError:
            '''Can happen while restarting game (Practice Tool)'''
        except (ProcessError, tk.TclError):
            '''Process is not avaliable - Game has ended'''

        try:
            jungle_chrono = self.format_jungle_chrono(self.get_jungle_chrono())
        except (RecursionError, RuntimeError):
            # Dictionary changed size during iteration
            jungle_chrono = None

        if jungle_chrono:
            try:
                if self.game._smite_invalid:

                    button_2 = getattr(self, '2_name_button')
                    button_2.config(font=('Tahoma', 10), fg='#E87272')

                    text_2 = getattr(self, '2_name_text')
                    text_2.set('INVALID SMITE')

                    button_3 = getattr(self, '3_name_button')
                    button_3.config(font=('Tahoma', 10), fg='#E87272')

                    text_3 = getattr(self, '3_name_text')
                    text_3.set('RESTART GAME')
                else:
                    n = 2
                    for step_name, step_info in jungle_chrono.items():
                        # NAME
                        button = getattr(self, f'{n}_name_button')
                        button.config(fg=step_info['color'])

                        text = getattr(self, f'{n}_name_text')
                        text.set(step_info['name'])

                        # START
                        label = getattr(self, f'{n}_start_label')
                        if not step_info['start_optimized']:
                            label.config(fg='white')
                        else:
                            color = step_info['start_optimized'] if step_info['start_optimized'] != 'red' else '#E87272'
                            label.config(fg=color)

                        text = getattr(self, f'{n}_start_text')
                        text.set(step_info['start'])

                        # END
                        label = getattr(self, f'{n}_end_label')
                        if not step_info['end_optimized']:
                            if self.clears_optimized:
                                label.config(fg='white')
                            else:
                                label.config(fg='green')
                        else:
                            color = step_info['end_optimized'] if step_info['end_optimized'] != 'red' else '#E87272'
                            label.config(fg=color)

                        text = getattr(self, f'{n}_end_text')
                        text.set(step_info['end'])

                        # CLEAR
                        label = getattr(self, f'{n}_clear_label')
                        if not step_info['total_optimized']:
                            if self.clears_optimized:
                                label.config(fg='white')
                            else:
                                label.config(fg='yellow')
                        else:
                            color = step_info['total_optimized'] if step_info['total_optimized'] != 'red' else '#E87272'
                            label.config(fg=color)

                        text = getattr(self, f'{n}_clear_text')
                        text.set(step_info['total'])

                        n += 1
            except tk.TclError:
                '''Game has ended'''

        self.after(1, self.update_labels)

    def run(self):
        self.after(1, self.update_labels)
        self.mainloop()

    def set_mockup(self):
        def set_timedelta(seconds):
            return datetime.timedelta(seconds=seconds)

        jungle_chrono = {
            'gromp_blue': {'name': 'Gromp', 'color': 'blue', 'start': set_timedelta(90), 'end': set_timedelta(103), 'total': set_timedelta(25)},
            'moving_1': {'name': '..........', 'color': None, 'start': set_timedelta(103), 'end': set_timedelta(105), 'total': set_timedelta(2)},
            'blue_blue': {'name': 'Blue', 'color': 'blue', 'start': set_timedelta(105), 'end': set_timedelta(123), 'total': set_timedelta(18)},
            'moving_2': {'name': '..........', 'color': None, 'start': set_timedelta(123), 'end': set_timedelta(129), 'total': set_timedelta(6)},
            'wolves_blue': {'name': 'Wolves', 'color': 'blue', 'start': set_timedelta(129), 'end': set_timedelta(142), 'total': set_timedelta(13)},
            'moving_3': {'name': '..........', 'color': None, 'start': set_timedelta(142), 'end': set_timedelta(154), 'total': set_timedelta(12)},
            'raptors_blue': {'name': 'Raptors', 'color': 'blue', 'start': set_timedelta(154), 'end': set_timedelta(166), 'total': set_timedelta(12)},
            'moving_4': {'name': '..........', 'color': None, 'start': set_timedelta(166), 'end': set_timedelta(169), 'total': set_timedelta(3)},
            'red_blue': {'name': 'Red', 'color': 'blue', 'start': set_timedelta(169), 'end': set_timedelta(187), 'total': set_timedelta(18)},
            'moving_5': {'name': '..........', 'color': None, 'start': set_timedelta(187), 'end': set_timedelta(191), 'total': set_timedelta(4)},
            'krugs_blue': {'name': 'Krugs', 'color': 'blue', 'start': set_timedelta(191), 'end': set_timedelta(200), 'total': set_timedelta(9)},
            'total': {'name': 'TOTAL', 'color': 'yellow', 'start': '6camps', 'end': set_timedelta(200), 'total': set_timedelta(110)},
        }

        jungle_chrono = self.format_jungle_chrono(jungle_chrono)

        # LABELS
        n_row = 2
        spacing = 21

        for step_name, step_info in jungle_chrono.items():
            # NAME
            setattr(self, f'{n_row}_name_text', tk.StringVar())
            text = getattr(self, f'{n_row}_name_text')
            text.set(step_info['name'])

            setattr(self, f'{n_row}_name_button', self.create_button(text, 10, step_info['color'], n_row))
            button = getattr(self, f'{n_row}_name_button')
            button.place(x=13, y=16 + n_row * spacing)

            # START
            setattr(self, f'{n_row}_start_text', tk.StringVar())
            text = getattr(self, f'{n_row}_start_text')
            text.set(step_info['start'])

            setattr(self, f'{n_row}_start_label', self.create_label(text, 10, 'white'))
            label = getattr(self, f'{n_row}_start_label')
            label.place(x=self._padx + 66, y=19 + n_row * spacing)

            # END
            setattr(self, f'{n_row}_end_text', tk.StringVar())
            text = getattr(self, f'{n_row}_end_text')
            text.set(step_info['end'])

            setattr(self, f'{n_row}_end_label', self.create_label(text, 10, 'green'))
            label = getattr(self, f'{n_row}_end_label')
            label.place(x=self._padx + 114, y=19 + n_row * spacing)

            # CLEAR
            setattr(self, f'{n_row}_clear_text', tk.StringVar())
            text = getattr(self, f'{n_row}_clear_text')
            text.set(step_info['total'])

            setattr(self, f'{n_row}_clear_label', self.create_label(text, 10, 'yellow'))
            label = getattr(self, f'{n_row}_clear_label')
            label.place(x=self._padx + 162, y=19 + n_row * spacing)

            n_row += 1


if __name__ == '__main__':

    class Game():
        def __init__(self):
            self.mockup = True
            self.reset = False

            self.champion_local = lambda: None
            self.champion_local.name = ''

        def reset_jungle(self):
            return

    game = Game()

    overlay = ChronoOverlay(game)
    overlay.set_mockup()
    overlay.run()
