from vendor.player import Player
import time


class ServicePlayer(object):
    def __init__(self, container):
        self.__player = Player()
        self.__container = container

    def on_loaded(self, event, dispatcher):
        service_event_dispatcher = self.__container.get("event_dispatcher")
        service_event_dispatcher.addListener('app.on_ping', self.on_ping)
        service_event_dispatcher.addListener('app.on_play', self.on_play)
        service_event_dispatcher.addListener('app.on_stop', self.on_stop)
        service_event_dispatcher.addListener('app.on_pause', self.on_pause)
        service_event_dispatcher.addListener('app.on_shutdown', self.on_shutdown)

        pass

    def on_started(self, event, dispatcher):
        print('ServicePlayer::on_started')
        pass

    def on_ping(self, event, dispatcher):
        print('ServicePlayer::on_ping')
        pass

    def on_play(self, event, dispatcher):
        assert 'stream' in event.data.keys()
        self.__player.play(event.data['stream'])
        print('ServicePlayer::on_play')
        pass

    def on_stop(self, event, dispatcher):
        print('ServicePlayer::on_stop')
        self.__player.stop()
        pass

    def on_pause(self, event, dispatcher):
        print('ServicePlayer::on_pause')
        self.__player.pause()
        pass

    def on_shutdown(self, event, dispatcher):
        print('ServicePlayer::on_shutdown')
        pass
