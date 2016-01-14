from vendor.player import Player
from application.Service.ContainerAware import ContainerAware


class ServicePlayer(ContainerAware):
    def __init__(self, container):
        super().__init__(container)
        self.__player = Player()

    def on_loaded(self, event, dispatcher):
        service_event_dispatcher = self.get("event_dispatcher")
        service_event_dispatcher.addListener('app.on_ping', self.on_ping)
        service_event_dispatcher.addListener('app.on_play', self.on_play)
        service_event_dispatcher.addListener('app.on_stop', self.on_stop)
        service_event_dispatcher.addListener('app.on_pause', self.on_pause)
        service_event_dispatcher.addListener('app.on_shutdown', self.on_shutdown)
        pass

    def on_started(self, event, dispatcher):
        pass

    def on_ping(self, event, dispatcher):
        service_logger = self.get("logger")
        service_logger.debug('[ServicePlayer] ping')
        pass

    def on_play(self, event, dispatcher):
        assert 'stream' in event.data.keys()

        name = event.data['stream']
        stream = event.data['stream']

        service_logger = self.get("logger")
        service_logger.debug('[ServicePlayer] play: %s<%s>' % (name, stream))

        self.__player.play(stream)
        pass

    def on_stop(self, event, dispatcher):
        service_logger = self.get("logger")
        service_logger.debug('[ServicePlayer] stop')
        self.__player.stop()
        pass

    def on_pause(self, event, dispatcher):
        service_logger = self.get("logger")
        service_logger.debug('[ServicePlayer] pause')
        self.__player.pause()
        pass

    def on_shutdown(self, event, dispatcher):
        service_logger = self.get("logger")
        service_logger.debug('[ServicePlayer] shutdown')
        pass
