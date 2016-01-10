import sys

from application.Service.ServiceContainer import ServiceContainer
from vendor.EventDispatcher import Event


class UbuntuTv:
    def __init__(self):
        self.container = ServiceContainer()
        service_event_dispatcher = self.container.get("event_dispatcher")
        service_event_dispatcher.addListener('app.on_shutdown', self.on_shutdown, 9999)

        service_event_dispatcher.dispatch('app.on_loaded', Event())
        pass

    """
    Show all available and enabled modules
    for current power manager context
    """

    def start(self):
        service_event_dispatcher = self.container.get("event_dispatcher")
        service_event_dispatcher.dispatch('app.on_started', Event())
        pass

    def on_shutdown(self, event, dispatcher):
        sys.exit(0)
        pass
