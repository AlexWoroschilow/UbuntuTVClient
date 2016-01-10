'''
Created on 03.01.2016

@author: sensey
'''

from collections import OrderedDict


class Event(object):
    def __init__(self, data=None):
        self.__name = None
        self.__data = data

    def setName(self, name):
        self.__name = name

    def getName(self):
        return self.__name

    @property
    def data(self):
        return self.__data
        pass


class EventSubscriberInterface(object):
    def getSubscribedEvents(self):
        raise NotImplementedError()


class EventListenerItem():
    def __init__(self, listener, priority):
        self.__listener = listener
        self.__priority = priority
        pass

    @property
    def listener(self):
        return self.__listener

    @property
    def priority(self):
        return self.__priority


class EventDispatcher(object):
    def __init__(self):
        self._listeners = {}

    def dispatch(self, eventName, event=None):
        if event is None:
            event = Event()
        elif not isinstance(event, Event):
            raise ValueError('Unexpected event type given')
        event.setName(eventName)
        if eventName not in self._listeners:
            return event
        for listener_item in self._listeners[eventName]:
            listener_item.listener(event, self)
        return event

    def addListener(self, eventName, listener, priority=0):
        if eventName not in self._listeners:
            self._listeners[eventName] = []
        self._listeners[eventName].append(EventListenerItem(listener, priority))
        self._listeners[eventName].sort(key=lambda item: item.priority)

    def removeListener(self, eventName, listener=None):
        if eventName not in self._listeners:
            return
        if not listener:
            del self._listeners[eventName]
        else:
            for p, l in self._listeners[eventName].items():
                if l is listener:
                    self._listeners[eventName].pop(p)
                    return

    def addSubscriber(self, subscriber):
        if not isinstance(subscriber, EventSubscriberInterface):
            raise ValueError('Unexpected subscriber type given')
        for eventName, params in subscriber.getSubscribedEvents().items():
            if isinstance(params, str):
                self.addListener(eventName, getattr(subscriber, params))
            elif isinstance(params, list):
                if not params:
                    raise ValueError('Invalid params "%r" for event "%s"' % (params, eventName))
                if len(params) <= 2 and isinstance(params[0], str):
                    priority = params[1] if len(params) > 1 else 0
                    self.addListener(eventName, getattr(subscriber, params[0]), priority)
                else:
                    for listener in params:
                        priority = listener[1] if len(listener) > 1 else 0
                        self.addListener(eventName, getattr(subscriber, listener[0]), priority)
            else:
                raise ValueError('Invalid params for event "%s"' % eventName)


if __name__ == "__main__":
    dispatcher = EventDispatcher()
    dispatcher.addListener('app.on_shutdown', lambda e, d: print("func_2"), 1)
    dispatcher.addListener('app.on_shutdown', lambda e, d: print("func_1"), 0)
    dispatcher.addListener('app.on_shutdown', lambda e, d: print("func_3"), 2)
    dispatcher.addListener('app.on_shutdown', lambda e, d: print("func_4"), 3)

    dispatcher.dispatch('app.on_shutdown', Event())
