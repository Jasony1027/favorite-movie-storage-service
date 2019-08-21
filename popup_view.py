import tkinter as tk

import requests

class PopupView(tk.Frame):
    """ Popup Window """
    def __init__(self, parent, close_popup_callback, submit_popup_callback):
        """ Initialize the nav bar """
        tk.Frame.__init__(self, parent, width=1200, height=1200)

        self._parent = parent
        self.grid(rowspan=5, columnspan=10)
        self._close_popup_callback = close_popup_callback
        self._submit_popup_callback = submit_popup_callback
        self._create_widgets()
        self._msg = ""

    def _create_widgets(self):
        """ Creates the widgets for the nav bar """

        self._label1 = tk.Label(self, text="Name:")
        self._label1.grid(row=1, column=0,padx=20)

        self._entry_1 = tk.Entry(self)
        self._entry_1.grid(row=1, column=1)

        self._label2 = tk.Label(self, text="Year Released:")
        self._label2.grid(row=2, column=0, padx=20)

        self._entry_2 = tk.Entry(self)
        self._entry_2.grid(row=2, column=1)

        self._label3 = tk.Label(self, text="Director:")
        self._label3.grid(row=3, column=0,padx=20)

        self._entry_3 = tk.Entry(self)
        self._entry_3.grid(row=3, column=1)

        self._label4 = tk.Label(self, text="Rating:")
        self._label4.grid(row=4, column=0, padx=20)

        self._entry_4 = tk.Entry(self)
        self._entry_4.grid(row=4, column=1)

        self._label5 = tk.Label(self, text="Length:")
        self._label5.grid(row=5, column=0, padx=20)

        self._entry_5 = tk.Entry(self)
        self._entry_5.grid(row=5, column=1)

        self._label6 = tk.Label(self, text="",fg="red")
        self._label6.grid(row=6, column=1, padx=0)
        self._label_success = tk.Label(self, text="", fg="green")
        self._label_success.grid(row=7, column=1, padx=0)

        self._button = tk.Button(self,
                                 text="Submit",
                                 command=self._submit_popup_callback).grid(row=8, column=1, pady=2)

        self._button = tk.Button(self,
                                 text="Close",
                                 command=self._close_popup_callback).grid(row=8, column=2, pady=2)

    def make_id(self, data):
        max = 0
        if len(data) == 0:
            return 1
        for e in data:
            if e["id"] > max:
                max = e["id"]
        return max + 1

    def submit_ent(self, id, type):
        self._validate_input("Name", self._entry_1.get())

        self._validate_input("Year Released", self._entry_2.get())
        self._validate_float("Year Released", self._entry_2.get())

        self._validate_input("Director", self._entry_3.get())

        self._validate_input("Rating", self._entry_4.get())
        self._validate_float("Rating", self._entry_4.get())

        if type == "Movie":
            self._validate_input("Length", self._entry_5.get())
            self._validate_float("Length", self._entry_5.get())

        if self._msg == "":
            if type == "TV series":
                length = 0
            else:
                length = float(self._entry_5.get())

            dict = {
                "id": id,
                "name": self._entry_1.get(),
                "year_released": float(self._entry_2.get()),
                "director": self._entry_3.get(),
                "rating": float(self._entry_4.get()),
                "type": type,
                "length": length
            }
            success_msg = "{} {} added!".format(type, self._entry_1.get())
            self._msg = success_msg
            self._label_success .config(text=success_msg)
            return dict

    def _validate_input(self, input, value):
        msg = input + " is empty"
        if value == "":
            self._label6.config(text=msg)
            raise ValueError

    def _validate_float(self, input, value):
        msg = input + " should be a number"
        try:
            val = float(value)
            print(type(val))
        except ValueError:
            self._label6.config(text=msg)
            raise ValueError

