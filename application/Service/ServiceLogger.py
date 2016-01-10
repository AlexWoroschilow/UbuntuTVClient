from logging import *

class ServiceLogger(object):
    def __init__(self):
        basicConfig(level=DEBUG, filename='./ubuntu_tv_client.log')
        self.__logger = getLogger("ubuntu_tv_client")
        pass

    def on_loaded(self, event, dispatcher):
        self.__logger.debug("on_loaded action")
        pass

    def on_started(self, event, dispatcher):
        self.__logger.debug("on_started action")
        pass

    def debug(self, message):
        self.__logger.debug(message)
        pass

    def info(self, message):
        self.__logger.debug(message)
        pass

    def warning(self, message):
        self.__logger.warning(message)
        pass

    def error(self, message):
        self.__logger.error(message)
        pass

    def fatal(self, message):
        self.__logger.fatal(message)
        pass
