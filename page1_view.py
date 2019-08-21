import tkinter as tk
from tkinter import messagebox as tkMessageBox
import requests

class Page1View(tk.Frame):
    """ Page 1 """

    def __init__(self, parent, submit_callback, delete_callback, update_callback, detail_callback):
        """ Initialize Page 1 """
        tk.Frame.__init__(self, parent, width=1200, height=1200, padx=20)
        self._parent = parent
        self._submit_callback = submit_callback
        self._delete_callback = delete_callback
        self._update_callback = update_callback
        self._detail_callback = detail_callback
        self._create_widgets()

    def _create_widgets(self):
        """ Creates the widgets for Page 1 """
        self._label = tk.Label(self, text="Movie")
        self._label.grid(row=1, column=2, padx=50)

        self._scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)

        self._listbox = tk.Listbox(self, yscrollcommand=self._scrollbar.set)
        self._scrollbar.config(command=self._listbox.yview)
        self._listbox.grid(row=2, columnspan=5, ipadx=100, ipady=20)
        self._scrollbar.grid(row=2, column=6, sticky=tk.N+tk.S+tk.E)

        self._button1 = tk.Button(self,
                                  text="Refresh",
                                  command=self._submit_callback)
        self._button1.grid(row=3, column=1, pady=5)

        self._button1 = tk.Button(self,
                                  text="Update",
                                  command=self._update_callback)
        self._button1.grid(row=3, column=2, pady=5)

        self._button1 = tk.Button(self,
                                  text="Delete",
                                  command=self._delete_callback)
        self._button1.grid(row=3, column=3, pady=5)

        self._button1 = tk.Button(self,
                                  text="Details",
                                  command=self._detail_callback)
        self._button1.grid(row=3, column=4, pady=5)

    def set_form_data(self, data):
        self._listbox.delete(0, tk.END)
        if data is None:
            self._listbox.insert(tk.END, "")
            return
        for m in data:
            self._listbox.insert(tk.END, "{}--{}".format(m["name"], m["id"]))

    def get_id(self):
        if len(self._listbox.curselection()) != 0:
            index = self._listbox.curselection()[0]
            id = int(self._listbox.get(0, tk.END)[index].split("--")[1])
            return str(id)

        else:
            tkMessageBox.showerror("Error", "No item is selected.")
            raise ValueError

    def delete_id(self, id):
        index = self._listbox.curselection()[0]
        name = str(self._listbox.get(0, tk.END)[index].split("--")[0])
        if tkMessageBox.askyesno('Verify', 'Delete ' + name + "?"):
            return id

    def get_detail(self, ent):
        tkMessageBox.showinfo("Details", "Name: {}\nYear Released: {}\nDirector: {}\nRating: {}\nLength: {}"
                .format(ent['name'], ent['year_released'], ent['director'], ent['rating'], ent['length']))

    def get_selected(self, data):
        if self.get_id() is not None:
            for m in data:
                if m["id"] == int(self.get_id()):
                    return m



