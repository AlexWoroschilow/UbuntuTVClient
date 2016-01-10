import sys
from gi.repository import Gtk as gtk

from vendor.IndicatorPlugins.Common import Common


class History(Common):
    def __init__(self, app):
        self.__app = app
        self.__history = []

    @property
    def order(self):
        return 50

    def on_play(self, name, media):
        print("History::on_play")
        self.__history.append({
            "name": name,
            "stream": media
        })
        pass

    def menu(self, menu):
        for element in self.__history:
            name = element["name"]
            callback = lambda x: self.__app.on_indicator_history(element)
            menu.append(self._menu_element(name, callback))
            pass
