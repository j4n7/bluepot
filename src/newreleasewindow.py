import webbrowser
import tkinter as tk

from pathlib import PurePath
from src.functions import get_base_dir


class NewReleaseWindow(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title('BluePot')
        self.geometry('250x90')
        self.resizable(False, False)
        self.eval('tk::PlaceWindow . center')

        base_dir = get_base_dir()
        path_img = PurePath(base_dir, 'src', 'img')

        self.iconbitmap(PurePath(path_img, 'potion.ico'))

        label = tk.Label(self, text='There is a new version available.')
        label.place(x=40, y=14)

        button = tk.Button(self, text='Download', command=lambda: webbrowser.open('https://github.com/j4n7/bluepot/releases'))
        button.place(x=94, y=44)


if __name__ == '__main__':
    new_release_window = NewReleaseWindow()
    new_release_window.mainloop()
