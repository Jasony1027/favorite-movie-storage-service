import tkinter as tk


class BottomNavbarView(tk.Frame):
    """ Navigation Bar """

    def __init__(self, parent, quit_callback):
        """ Initialize the nav bar """
        tk.Frame.__init__(self, parent)
        self._parent = parent

        self._quit_callback = quit_callback
        self._create_widgets()

    def _create_widgets(self):
        self._button = tk.Button(self,
                           text="QUIT",
                           fg="red",
                           command=self._quit_callback)
        self._button.grid(column=1)
