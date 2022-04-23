import json
import socket
from _socket import timeout

import settings


class SocketClient:

    def __init__(self):
        self.target_host = settings.APP_HOST
        self.target_port = int(settings.APP_PORT)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(0.1)
        self.client.connect((self.target_host, self.target_port))

    def get(self, endpoint, params=None):
        return self._send(endpoint, params=params)

    def post(self, endpoint, params=None):
        return self._send(endpoint, params=params, method="POST")

    def put(self, endpoint, params=None):
        return self._send(endpoint, params=params, method="PUT")

    def delete(self, endpoint, params=None):
        return self._send(endpoint, params=params, method="DELETE")

    def _send(self, endpoint, params=None, method="GET"):
        request = f'{method} {endpoint} HTTP/1.1\r\nHost: {self.target_host}:{self.target_port}\r\n'
        if params:
            request += 'Content-Type: application/json\r\n'
            content = json.dumps(params)
            request += f'Content-Length: {len(content)}\r\n\r\n'
            request += content
        else:
            request += '\r\n'
        self.client.sendall(request.encode('utf-8'))
        return self.get_response()

    def get_response(self):
        total_data = b""
        try:
            while True:
                data = self.client.recv(4096)
                if data:
                    total_data += data
                else:
                    break
        except timeout:
            pass
        return total_data.decode().splitlines()

    def close(self):
        self.client.close()
