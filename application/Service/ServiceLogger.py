import inspect
from  logging import *


class ServiceLogger():
    """
    Initialize a main power manager object
    set up all power switchers
    """
    def __init__(self, container):
        basicConfig(level=DEBUG, filename='./powermanager.log')
        self._logger = getLogger("power_manager")
        pass


    def on_loaded(self, event, dispatcher):
        print("ServiceLogger.on_loaded")
        pass


    def on_started(self, event, dispatcher):
        print("ServiceLogger.on_started")
        pass

