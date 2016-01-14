import threading
from vendor.Indicator import IndicatorUbuntuTV
from vendor.EventDispatcher import Event
from application.Service.ContainerAware import ContainerAware


class ServiceIndicator(ContainerAware):
    def __init__(self, container):
        super().__init__(container)
        self.__thread = None
        self.__indicator = IndicatorUbuntuTV(self)
        pass

    def on_loaded(self, event, dispatcher):
        service_event_dispatcher = self.get("event_dispatcher")
        service_event_dispatcher.addListener('app.on_ping', self.on_ping)
        service_event_dispatcher.addListener('app.on_play', self.on_play)
        service_event_dispatcher.addListener('app.on_stop', self.on_stop)
        service_event_dispatcher.addListener('app.on_pause', self.on_pause)
        service_event_dispatcher.addListener('app.on_shutdown', self.on_shutdown)
        pass

    def on_ping(self, event, dispatcher):
        service_logger = self.get("logger")
        service_logger.debug('[ServiceIndicator] ping')
        pass

    def on_play(self, event, dispatcher):
        assert 'stream' in event.data.keys()

        name = event.data['stream']
        stream = event.data['stream']

        service_logger = self.get("logger")
        service_logger.debug("[ServiceIndicator] play: %s<%s>" % (name, stream))

        self.__indicator.on_play(name, stream)
        pass

    def on_stop(self, event, dispatcher):
        service_logger = self.get("logger")
        service_logger.debug('[ServiceIndicator] stop')
        pass

    def on_pause(self, event, dispatcher):
        service_logger = self.get("logger")
        service_logger.debug('[ServiceIndicator] pause')
        pass

    def on_started(self, event, dispatcher):
        self.on_shutdown(event, dispatcher)
        service_logger = self.get("logger")
        service_logger.debug('[ServiceIndicator] started')
        self.__thread = threading.Thread(target=self.on_started_target)
        self.__thread.daemon = True
        self.__thread.start()
        pass

    def on_started_target(self):
        self.__indicator.main()

    def on_shutdown(self, event, dispatcher):
        service_logger = self.get("logger")
        service_logger.debug('[ServiceIndicator] shutdown')
        pass

    def on_indicator_play(self, item=None):
        service_logger = self.get("logger")
        service_logger.debug('[ServiceIndicator] indicator menu play selected')

        service_event_dispatcher = self.get("event_dispatcher")
        service_event_dispatcher.dispatch('app.on_play', Event(item))
        pass

    def on_indicator_pause(self, item=None):
        service_logger = self.get("logger")
        service_logger.debug('[ServiceIndicator] indicator menu pause selected')

        service_event_dispatcher = self.get("event_dispatcher")
        service_event_dispatcher.dispatch('app.on_pause', Event(item))
        pass

    def on_indicator_stop(self, item=None):
        service_logger = self.get("logger")
        service_logger.debug('[ServiceIndicator] indicator menu stop selected')

        service_event_dispatcher = self.get("event_dispatcher")
        service_event_dispatcher.dispatch('app.on_stop', Event(item))
        pass

    def on_indicator_history(self, item=None):
        service_logger = self.get("logger")
        service_logger.debug('[ServiceIndicator] indicator menu history selected')

        service_event_dispatcher = self.get("event_dispatcher")
        service_event_dispatcher.dispatch('app.on_play', Event(item))
        print("on_indicator_history", item)
        pass

    def on_indicator_shutdown(self, item=None):
        service_logger = self.get("logger")
        service_logger.debug('[ServiceIndicator] indicator menu shutdown selected')

        service_event_dispatcher = self.get("event_dispatcher")
        service_event_dispatcher.dispatch('app.on_shutdown', Event(item))
        pass
