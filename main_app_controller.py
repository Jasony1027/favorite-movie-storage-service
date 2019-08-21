import tkinter as tk
from top_navbar_view import TopNavbarView
from page1_view import Page1View
from page2_view import Page2View
from bottom_navbar_view import BottomNavbarView
from popup_view import PopupView
from update_popup_view import UpdatePopupView
import requests
import json


class MainAppController(tk.Frame):
    """ Main Application for GUI """
    def __init__(self, parent):
        """ Initialize Main Application """
        tk.Frame.__init__(self, parent)

        self._top_navbar = TopNavbarView(self, self._page_callback, self._page_popup_callback)
        self._page1 = Page1View(self, self._page1_refresh_callback, self._page1_delete_callback, self._update_page_popup_callback, self._page1_detail_callback)
        self._page2 = Page2View(self, self._page2_refresh_callback, self._page2_delete_callback, self._update_page_popup_callback, self._page2_detail_callback)
        self._bottom_navbar = BottomNavbarView(self, self._quit_callback)

        self._top_navbar.grid(row=0, columnspan=5, pady=10)
        self._page1.grid(row=1, columnspan=5, pady=10)
        self._curr_page = TopNavbarView.PAGE1
        # Hide Page 2 by default
        self._bottom_navbar.grid(row=2, columnspan=5, pady=10)

        self._data_1 = self._get_data('Movie')
        self._page1.set_form_data(self._data_1)
        self._data_2 = self._get_data('TV series')
        self._page2.set_form_data(self._data_2)

    def _page_callback(self):
        """ Handle Switching Between Pages """

        curr_page = self._top_navbar.curr_page.get()
        if self._curr_page != curr_page and self._curr_page == TopNavbarView.PAGE1:
            self._page1.grid_forget()
            self._page2.grid(row=1, columnspan=5)
            self._curr_page = TopNavbarView.PAGE2
        elif self._curr_page != curr_page and self._curr_page == TopNavbarView.PAGE2:
            self._page2.grid_forget()
            self._page1.grid(row=1, columnspan=5)
            self._curr_page = TopNavbarView.PAGE1

    def _page_popup_callback(self):
        self._popup_win = tk.Toplevel()
        self._popup = PopupView(self._popup_win, self._close_popup_callback, self._submit_popup_callback)

    def _update_page_popup_callback(self):
        try:
            type = self._get_type()
            ent = self._get_cur_item(type)
            self._update_popup_win = tk.Toplevel()
            self.__update_popup = UpdatePopupView(self._update_popup_win, self._close_update_popup_callback, self._submit_update_popup_callback, ent)
        except:
            print("missing info")

    def _close_popup_callback(self):
        self._popup_win.destroy()

    def _close_update_popup_callback(self):
        self._update_popup_win.destroy()

    def _submit_popup_callback(self):
        type = self._get_type()
        try:
            id = self._popup.make_id(self._data_1+self._data_2)
            dict = self._popup.submit_ent(id, type)
            print(requests.post(url="http://127.0.0.1:5000/streamingservice/entertainment", json=dict))
        except:
            print("missing info")

    def _submit_update_popup_callback(self):
        try:
            dict = self.__update_popup.submit_update()
            print(requests.put(url="http://127.0.0.1:5000/streamingservice/entertainment/" + str(dict["id"]), json=dict))
        except:
            print("missing info")

    def _page1_refresh_callback(self):
        self._page1.set_form_data(self._get_data("Movie"))

    def _page1_delete_callback(self):
        try:
            type = self._get_type()
            ent = self._get_cur_item(type)
            id = self._page1.delete_id(self._page1.get_id())
            headers = {'content-type': 'application/json'}
            url = "http://127.0.0.1:5000/streamingservice/entertainment/"+id
            req = requests.delete(url=url, data=json.dumps(ent), headers=headers)
            print(req)
            if req.status_code == 200:
                print("Deleted successfully")
            else:
                print("error")
        except:
            print("missing info")

    def _page1_detail_callback(self):
        try:
            type = self._get_type()
            ent = self._get_cur_item(type)
            self._page1.get_detail(ent)
        except:
            print("midding info")

    def _page2_delete_callback(self):
        try:
            type = self._get_type()
            ent = self._get_cur_item(type)
            id = self._page2.delete_id(self._page2.get_id())
            headers = {'content-type': 'application/json'}
            url = "http://127.0.0.1:5000/streamingservice/entertainment/"+id
            req = requests.delete(url=url, data=json.dumps(ent), headers=headers)
            print(req)
            if req.status_code == 200:
                print("Deleted successfully")
            else:
                print("error")
        except:
            print("missing info")

    def _page2_refresh_callback(self):
        self._page2.set_form_data(self._get_data("TV series"))

    def _page2_detail_callback(self):
        try:
            type = self._get_type()
            ent = self._get_cur_item(type)
            self._page2.get_detail(ent)
        except:
            print("missing info")

    def _quit_callback(self):
        self.quit()

    def _get_type(self):
        if self._curr_page == TopNavbarView.PAGE2:
            return "TV series"
        elif self._curr_page == TopNavbarView.PAGE1:
            return "Movie"

    def _get_data(self, type):
        req = requests.get("http://127.0.0.1:5000/streamingservice/entertainment/all/" + type)
        print(req)
        if req.status_code == 200:
            return req.json()

    def _get_cur_item(self, type):
        if type == "Movie":
            return self._page1.get_selected(self._get_data('Movie'))
        else:
            return self._page2.get_selected(self._get_data('TV series'))


if __name__ == "__main__":
    root = tk.Tk()
    MainAppController(root).pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    root.mainloop()

