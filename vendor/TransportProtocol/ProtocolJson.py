import json


class ProtocolJson(object):
    def __init__(self):
        self.__accepted = ["ping", "play", "stop", "pause"]
        pass

    def translate(self, bytestring):
        parsed = self.__parse(bytestring)
        task = parsed['task']
        data = parsed['data']
        if task not in self.__accepted:
            return ("ping", {})
        return (task, data)

    def __parse(self, byte_string):
        try:
            return json.loads(self.__bytes_utf8_to(byte_string))
        except ValueError as error:
            return {"task": "ping", "data": {}}

    def __utf8_to_bytes(self, data):
        return bytes(data, 'utf-8')

    def __bytes_utf8_to(self, data):
        if type(data) is not str:
            return data.decode('utf-8').strip()
        return None


if __name__ == "__main__":
    protocol = ProtocolJson()
    print(protocol.translate(bytes('{"version":"0.1","task":"ping","data":{}}', 'utf-8')))
    print(protocol.translate(bytes('{"version":"0.1","task":"play","data":{"stream": "file:///home/sensey/DIS-1-234843-01112014.webm"}}','utf-8')))
    print(protocol.translate(bytes('{"version":"0.1","task":"stop","data":{}}', 'utf-8')))
    print(protocol.translate(bytes('{"version":"0.1","task":"pause","data":{}}', 'utf-8')))
    print(protocol.translate(bytes('{"version":"0.1","task":"unknown","data":{}}', 'utf-8')))
    print(protocol.translate(bytes('asdfasdfadfs', 'utf-8')))
