import threading
from vendor.Indicator import IndicatorUbuntuTV
from vendor.EventDispatcher import Event


class ServiceIndicator(object):
    """
    Initialize a main power manager object
    set up all power switchers
    """

    def __init__(self, container):
        self.__thread = None
        self.__container = container
        self.__indicator = IndicatorUbuntuTV(self)
        pass

    def on_loaded(self, event, dispatcher):
        service_event_dispatcher = self.__container.get("event_dispatcher")
        service_event_dispatcher.addListener('app.on_ping', self.on_ping)
        service_event_dispatcher.addListener('app.on_play', self.on_play)
        service_event_dispatcher.addListener('app.on_stop', self.on_stop)
        service_event_dispatcher.addListener('app.on_pause', self.on_pause)
        service_event_dispatcher.addListener('app.on_shutdown', self.on_shutdown)
        pass

    def on_ping(self, event, dispatcher):
        print('serviceindicator::on_ping')
        pass

    def on_play(self, event, dispatcher):
        assert 'stream' in event.data.keys()
        self.__indicator.on_play(event.data['stream'], event.data['stream'])
        print('ServiceIndicator::on_play')
        pass

    def on_stop(self, event, dispatcher):
        print('ServiceIndicator::on_stop')
        pass

    def on_pause(self, event, dispatcher):
        print('ServiceIndicator::on_pause')
        pass

    def on_started(self, event, dispatcher):
        self.on_shutdown(event, dispatcher)

        self.__thread = threading.Thread(target=self.on_started_target)
        self.__thread.daemon = True
        self.__thread.start()
        pass

    def on_started_target(self):
        self.__indicator.main()

    def on_shutdown(self, event, dispatcher):
        pass

    def on_indicator_play(self, item=None):
        print("on_indicator_play", item)
        service_event_dispatcher = self.__container.get("event_dispatcher")
        service_event_dispatcher.dispatch('app.on_play', Event(item))
        pass

    def on_indicator_pause(self, item=None):
        print("on_indicator_pause", item)
        service_event_dispatcher = self.__container.get("event_dispatcher")
        service_event_dispatcher.dispatch('app.on_pause', Event(item))
        pass

    def on_indicator_stop(self, item=None):
        print("on_indicator_stop", item)
        service_event_dispatcher = self.__container.get("event_dispatcher")
        service_event_dispatcher.dispatch('app.on_stop', Event(item))
        pass

    def on_indicator_history(self, item=None):
        service_event_dispatcher = self.__container.get("event_dispatcher")
        service_event_dispatcher.dispatch('app.on_play', Event(item))
        print("on_indicator_history", item)
        pass

    def on_indicator_shutdown(self, item=None):
        print("on_indicator_shutdown", item)
        service_event_dispatcher = self.__container.get("event_dispatcher")
        service_event_dispatcher.dispatch('app.on_shutdown', Event(item))
        pass

    def __del__(self):
        pass
