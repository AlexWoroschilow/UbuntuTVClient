import time
from vendor import vlc
import subprocess, threading


class Player(object):
    def __init__(self):
        self.__instance = vlc.Instance('--fullscreen', '--no-xlib')
        self.__player = self.__instance.media_player_new()
        self.__thread = None
        pass

    def play(self, stream):
        self.__thread = threading.Thread(target=lambda x=stream: self.play_thread(x))
        self.__thread.daemon = True
        self.__thread.start()
        pass

    def play_thread(self, stream):
        self.__player.set_media(self.__instance.media_new(stream))
        self.__player.set_fullscreen(True)
        self.__player.play()
        while self.__player.is_playing():
            pass
        pass

    def pause(self):
        self.__player.pause()

    def stop(self):
        self.__player.stop()
        pass


if __name__ == "__main__":
    player = Player()
    player.play('file:///home/sensey/DIS-1-234843-01112014.webm')
