import sys
import socket
import json
from time import sleep
from vendor import socketserver
from vendor.EventDispatcher import Event
from vendor.TransportProtocol.ProtocolJson import ProtocolJson


class ServiceServer(object):
    def __init__(self, container):
        self.__host = "arbeiter.fritz.box"
        self.__port = [i for i in range(8880, 8890)]
        self.__protocol = ProtocolJson()
        self.__server = None
        self.__container = container

        pass

    def on_loaded(self, event, dispatcher):
        service_event_dispatcher = self.__container.get("event_dispatcher")
        service_event_dispatcher.addListener('app.on_ping', self.on_ping)
        service_event_dispatcher.addListener('app.on_play', self.on_play)
        service_event_dispatcher.addListener('app.on_stop', self.on_stop)
        service_event_dispatcher.addListener('app.on_shutdown', self.on_shutdown)
        pass

    def on_ping(self, event, dispatcher):
        pass

    def on_play(self, event, dispatcher):
        pass

    def on_stop(self, event, dispatcher):
        pass

    def on_started(self, event, dispatcher):
        service_server = self

        class ServiceServerTCPHandler(socketserver.BaseRequestHandler):
            def handle(self):
                data = self.request.recv(1024).strip()
                self.request.sendall(service_server.process(data))

        for port in self.__port:
            try:
                print("port", port)
                self.__server = socketserver.TCPServer((self.__host, port), ServiceServerTCPHandler)
                self.__server.serve_forever()
                break
            except OSError as error:
                print(error)
                continue
        pass

    def process(self, data):
        service_event_dispatcher = self.__container.get("event_dispatcher")

        (task, event_data) = self.__protocol.translate(data)

        service_event_dispatcher.dispatch(({
            "ping": "app.on_ping",
            "play": "app.on_play",
            "stop": "app.on_stop",
            "pause": "app.on_pause"
        }).get(task, lambda: None), Event(event_data))

        return data

    def on_shutdown(self, event, dispatcher):
        print("ServiceServer::on_shutdown")
        if self.__server is not None:
            self.__server.shutdown()
        pass

    def __del__(self):
        if self.__server is not None:
            self.__server.shutdown()
        pass


if __name__ == "__main__":
    server = ServiceServer({})
    server.process(bytes('{"version":"0.1","task":"ping","data":{}}', 'utf-8'))
    print(server.process(bytes('{"version":"0.1","task":"ping","data":{}}', 'utf-8')))
    print(server.process(bytes('{"version":"0.1","task":"play","data":{"stream": "file:///home/sensey/DIS-1-234843-01112014.webm"}}','utf-8')))
    print(server.process(bytes('{"version":"0.1","task":"stop","data":{}}', 'utf-8')))
    print(server.process(bytes('{"version":"0.1","task":"pause","data":{}}', 'utf-8')))
    print(server.process(bytes('{"version":"0.1","task":"unknown","data":{}}', 'utf-8')))
    print(server.process(bytes('asdfasdfadfs', 'utf-8')))
