import tkinter as tk

import requests

class UpdatePopupView(tk.Frame):
    """ Popup Window """
    def __init__(self, parent, close_update_popup_callback, submit_update_popup_callback, ent):
        """ Initialize the nav bar """
        tk.Frame.__init__(self, parent, width=1200, height=1200)
        self._parent = parent
        self.grid(rowspan=5, columnspan=10)
        self._close_update_popup_callback = close_update_popup_callback
        self._submit_update_popup_callback = submit_update_popup_callback

        self._id = 0
        self._type = ""
        self._name = ""
        self._year_released = 0
        self._rating = 0
        self._director = ""
        self._length = 0
        self._msg = ""
        self._ent = ent
        self._create_widgets()

    def _create_widgets(self):
        """ Creates the widgets for the nav bar """
        self._label1 = tk.Label(self, text="Name:")
        self._label1.grid(row=1, column=0, padx=20)

        self._entry_1 = tk.Entry(self)
        self._entry_1.grid(row=1, column=1)

        self._label2 = tk.Label(self, text="Year Released:")
        self._label2.grid(row=2, column=0, padx=20)

        self._entry_2 = tk.Entry(self)
        self._entry_2.grid(row=2, column=1)

        self._label3 = tk.Label(self, text="Director:")
        self._label3.grid(row=3, column=0, padx=20)

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

        self._label6 = tk.Label(self, text="", fg="red")
        self._label6.grid(row=6, column=1, padx=0)
        self._label_success = tk.Label(self, text="", fg="green")
        self._label_success.grid(row=7, column=1, padx=0)

        self._id = self._ent["id"]
        self._name =self._ent["name"]
        self._year_released = self._ent["year_released"]
        self._type = self._ent["type"]
        self._director = self._ent["director"]
        self._rating = self._ent["rating"]
        self._entry_1.insert(0, self._name)
        self._entry_2.insert(0, self._year_released)
        self._entry_3.insert(0, self._director)
        self._entry_4.insert(0, self._rating)

        if self._type == "Movie":
            self._length = self._ent["length"]
            self._entry_5.insert(0, self._length)
        else:
            self._entry_5.insert(0, "-")


        self._button = tk.Button(self,
                                 text="Submit",
                                 command=self._submit_update_popup_callback).grid(row=8, column=1, pady=2)

        self._button = tk.Button(self,
                                 text="Close",
                                 command=self._close_update_popup_callback).grid(row=8, column=2, pady=2)

    def initialize_ent(self, ent):
        self._ent = ent

    def submit_update(self):

        self._validate_input("Name", self._entry_1.get())

        self._validate_input("Year Released", self._entry_2.get())
        self._validate_float("Year Released", self._entry_2.get())
        self._validate_input("Director", self._entry_3.get())
        self._validate_input("Rating", self._entry_4.get())
        self._validate_float("Rating", self._entry_4.get())
        if self._type == "Movie":
            self._validate_input("Length", self._entry_5.get())
            self._validate_float("Length", self._entry_5.get())

        self._name = self._entry_1.get()
        self._year_released = self._entry_2.get()
        self._director = self._entry_3.get()
        self._rating = self._entry_4.get()
        self._length = self._entry_5.get()
        if self._type == "TV series":
            self._length = 0

        if self._msg == "":
            dict = {
                "id": int(self._id),
                "name": self._name,
                "year_released": float(self._year_released),
                "director": self._director,
                "rating": float(self._rating),
                "type": self._type,
                "length": float(self._length)
            }

            success_msg = "{} {} updated!".format(self._type, self._name)
            self._msg = success_msg
            self._label_success .config(text=success_msg)
            return dict


    def _validate_input(self, input, value):
        msg = input + " is empty"
        if value == "":
            self._label6.config(text=msg)
            raise ValueError

    def _validate_type(self, value):
        if value != "Movie" and value != "TV series":
            self._label6.config(text="Type can only be Movie or TV series")
            raise ValueError

    def _validate_float(self, input, value):
        msg = input + " should be a number"
        try:
            val = float(value)
        except ValueError:
            self._label6.config(text=msg)
            raise ValueError

