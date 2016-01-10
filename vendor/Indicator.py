import sys
import dbus
import inspect

from gi.repository.AppIndicator3 import Indicator, IndicatorCategory, IndicatorStatus
from gi.repository import Gtk as gtk

from vendor.IndicatorPlugins import *
import vendor.IndicatorPlugins as Plugins


class IndicatorUbuntuTV(object):
    def __init__(self, service):
        self.__service = service

        self.__pligins = []
        for (name, module) in inspect.getmembers(Plugins, inspect.ismodule):
            if hasattr(module, name):
                identifier = getattr(module, name)
                self.__pligins.append(identifier(self))
        self.__pligins.sort(key=None, reverse=False)

        self.__indicator = Indicator.new(
                "Indicator Ubuntu TV",
                "/usr/share/power-manager-indicator/share/icons/1x50px.png",
                IndicatorCategory.SYSTEM_SERVICES
        )
        self.__indicator.set_status(IndicatorStatus.ACTIVE)
        self.__indicator.set_label(u"\U0001F4FA client", "Indicator Ubuntu TV")
        self.__indicator.set_menu(self.menu)

    @property
    def menu(self):
        menu = gtk.Menu()
        for plugin in self.plugins:
            plugin.menu(menu)
        return menu

    @property
    def indicator(self):
        return self.__indicator

    @property
    def plugins(self):
        return self.__pligins

    def on_play(self, name, media):
        for plugin in self.plugins:
            plugin.on_play(name, media)
        self.refresh()
        pass

    def on_indicator_play(self, item=None):
        self.__service.on_indicator_play(item)
        pass

    def on_indicator_pause(self, item=None):
        self.__service.on_indicator_pause(item)
        pass

    def on_indicator_stop(self, item=None):
        self.__service.on_indicator_stop(item)
        pass

    def on_indicator_history(self, item=None):
        self.__service.on_indicator_history(item)
        pass

    def on_indicator_shutdown(self, item=None):
        self.__service.on_indicator_shutdown(item)
        pass

    def label(self, label, description):
        self.indicator.set_label(label, description)

    def refresh(self):
        self.indicator.set_menu(self.menu)
        pass

    def main(self):
        gtk.main()
