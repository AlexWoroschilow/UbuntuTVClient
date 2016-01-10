import sys
from gi.repository import Gtk as gtk

from vendor.IndicatorPlugins.Common import Common


class Stop(Common):
    def __init__(self, app):
        self.__app = app

    @property
    def order(self):
        return 3

    def menu(self, menu):
        callback = lambda x: self.__app.on_indicator_stop(None)
        menu.append(self._menu_element("Stop", callback))

    def on_play(self, name, media):
        pass
