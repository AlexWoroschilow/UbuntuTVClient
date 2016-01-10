import sys
from gi.repository import Gtk as gtk


class Common(object):
    def __init__(self, app):
        self.__app = app

    @property
    def order(self):
        return 100

    def menu(self, menu):
        callback = lambda x: self.__app.on_indicator_shutdown(None)
        menu.append(self._menu_element("Exit", callback))

    def _menu_element(self, name=None, callback=None):
        element = gtk.MenuItem(name)
        element.connect("activate", callback)
        element.show()
        return element

    def on_play(self, name, media):
        pass

    def __lt__(self, other):
        return self.order < other.order

    def __gt__(self, other):
        return self.order > other.order

    def __eq__(self, other):
        return self.order == other.order

    def __le__(self, other):
        return self.order <= other.order

    def __ge__(self, other):
        return self.order >= other.order

    def __ne__(self, other):
        return self.order != other.order
