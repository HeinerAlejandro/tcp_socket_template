import socket

from ipaddress import IPv4Address, IPv6Address

from adapters.interfaces.sockets import SocketClientAbstract
from helpers import sockets
from core import exceptions, data_types


class SocketClient(SocketClientAbstract):
    """Socket TCP/IP"""

    def __init__(self, address: IPv4Address | IPv6Address | str, port: int, logger):
        # TCP Socket Creation
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.logger = logger

        self.address = address
        self.port = port

    def connect(self):
        self.socket.connect((self.address, self.port))

    def send(
        self,
        http_options: dict,
        url_type: str,
    ) -> int:
        if not self.socket.getpeername():
            raise exceptions.ConnectionErrorException("Socket is not connected")

        request_str = sockets.get_string_request(http_options, url_type)

        self.socket.sendall(request_str.encode())

    def recv(self, until_complete=True) -> bytes:
        if not self.socket.getpeername():
            raise exceptions.ConnectionErrorException("Socket is not connected")

        received_data = b""

        if until_complete:
            while True:
                chunk = self.socket.recv(1024)
                print(chunk)
                if not chunk:
                    break

                received_data += chunk
        else:
            received_data = self.socket.recv(1024)

        return sockets.get_format_data(received_data)

    def close(self):
        self.socket.close()
