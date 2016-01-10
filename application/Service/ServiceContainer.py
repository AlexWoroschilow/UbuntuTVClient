'''
Created on 03.01.2016

@author: sensey
'''
from vendor import Inject
from vendor.EventDispatcher import EventDispatcher

from application.Service.ServiceServer import ServiceServer
from application.Service.ServicePlayer import ServicePlayer
from application.Service.ServiceIndicator import ServiceIndicator
from application.Service.ServiceLogger import ServiceLogger


class ServiceContainer(object):
    def __init__(self):
        Inject.configure_once(self.__load_services)
        service_event_dispatcher = self.get("event_dispatcher")
        service_event_dispatcher.addListener('app.on_loaded', self.__on_loaded)
        service_event_dispatcher.addListener('app.on_started', self.__on_started)
        pass

    def __load_services(self, binder):
        binder.bind("logger", ServiceLogger())
        binder.bind("event_dispatcher", EventDispatcher())
        binder.bind("server", ServiceServer(self))
        binder.bind("indicator", ServiceIndicator(self))
        binder.bind("player", ServicePlayer(self))
        pass

    def __on_loaded(self, event, dispatcher):
        service_server = self.get("server")
        service_indicator = self.get("indicator")
        service_player = self.get("player")
        service_event_dispatcher = self.get("event_dispatcher")

        service_event_dispatcher.addListener('app.on_loaded', service_server.on_loaded)
        service_event_dispatcher.addListener('app.on_loaded', service_player.on_loaded)
        service_event_dispatcher.addListener('app.on_loaded', service_indicator.on_loaded)
        pass

    def __on_started(self, event, dispatcher):
        service_server = self.get("server")
        service_indicator = self.get("indicator")
        service_player = self.get("player")
        service_event_dispatcher = self.get("event_dispatcher")

        service_event_dispatcher.addListener('app.on_started', service_player.on_started)
        service_event_dispatcher.addListener('app.on_started', service_indicator.on_started)
        service_event_dispatcher.addListener('app.on_started', service_server.on_started)
        pass

    def get(self, name):
        return Inject.instance(name)
