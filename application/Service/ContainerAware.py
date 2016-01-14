from logging import *


class ContainerAware(object):
    def __init__(self, container):
        self._container = container
        pass

    def get(self, name):
        return self._container.get(name)
