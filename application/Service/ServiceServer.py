import netifaces, threading, time
from vendor import socketserver
from vendor.EventDispatcher import Event
from vendor.TransportProtocol.ProtocolJson import ProtocolJson
from application.Service.ContainerAware import ContainerAware


class ServiceServer(ContainerAware):
    def __init__(self, container):
        super().__init__(container)
        self.__servers = []
        self.__protocol = ProtocolJson()
        pass

    @property
    def ports(self):
        return [i for i in range(8880, 8890)]

    @property
    def ips(self):
        for devices in netifaces.interfaces():
            collection = netifaces.ifaddresses(devices)
            if collection is not None and netifaces.AF_INET in collection.keys():
                for interface in collection[netifaces.AF_INET]:
                    if 'addr' in interface.keys():
                        yield interface['addr']

    def on_loaded(self, event, dispatcher):
        service_event_dispatcher = self.get("event_dispatcher")
        service_event_dispatcher.addListener('app.on_ping', self.on_ping)
        service_event_dispatcher.addListener('app.on_shutdown', self.on_shutdown)
        pass

    def on_ping(self, event, dispatcher):
        service_logger = self.get("logger")
        service_logger.info('[ServiceServer] ping')
        pass

    def on_started(self, event, dispatcher):
        for host in self.ips:
            thread = threading.Thread(target=self.on_server_started, args=[self, host])
            thread.daemon = True
            thread.start()
        while True:
            time.sleep(1000)
        pass

    def on_server_started(self, server, host):
        service_logger = self.get("logger")

        class ServiceServerTCPHandler(socketserver.BaseRequestHandler):
            def handle(self):
                data = self.request.recv(1024).strip()
                self.request.sendall(server.process(data))

        for port in self.ports:
            try:
                service_logger.info('[ServiceServer] start on %s:%s' % (host, port))
                server_socket = socketserver.TCPServer((host, port), ServiceServerTCPHandler)
                service_logger.info('[ServiceServer] started on %s:%s' % (host, port))
                self.__servers.append(server_socket)
                server_socket.serve_forever()
                return
            except OSError as error:
                service_logger.error("[ServiceServer] error: %s" % error)
                continue
        pass

    def process(self, data):
        service_logger = self.get("logger")
        service_event_dispatcher = self.get("event_dispatcher")

        (task, event_data) = self.__protocol.translate(data)

        service_logger.debug('[ServiceServer] process: %s' % task)

        service_event_dispatcher.dispatch(({
            "ping": "app.on_ping",
            "play": "app.on_play",
            "stop": "app.on_stop",
            "pause": "app.on_pause"
        }).get(task, lambda: None), Event(event_data))

        return data

    def on_shutdown(self, event, dispatcher):
        service_logger = self.get("logger")
        service_logger.debug('[ServiceServer] on_shutdown')

        if self.__servers is not None:
            for server_socket in self.__servers:
                server_socket.shutdown()
        pass


if __name__ == "__main__":
    server = ServiceServer({})
    print([ip for ip in server.ips])
    print(server.ports)
    # print(server.process(bytes('{"version":"0.1","task":"ping","data":{}}', 'utf-8')))
    # print(server.process(bytes('{"version":"0.1","task":"ping","data":{}}', 'utf-8')))
    # print(server.process(bytes('{"version":"0.1","task":"play","data":{"stream": "file:///home/sensey/DIS-1-234843-01112014.webm"}}', 'utf-8')))
    # print(server.process(bytes('{"version":"0.1","task":"stop","data":{}}', 'utf-8')))
    # print(server.process(bytes('{"version":"0.1","task":"pause","data":{}}', 'utf-8')))
    # print(server.process(bytes('{"version":"0.1","task":"unknown","data":{}}', 'utf-8')))
    # print(server.process(bytes('asdfasdfadfs', 'utf-8')))
