import socket

from ipaddress import (
    IPv4Address,
    IPv6Address
)

from adapters.interfaces.sockets import SocketClientAbstract
from helpers import sockets
from core import exceptions, data_types


class SocketClient(SocketClientAbstract):
    """Socket TCP/IP"""

    def __init__(
        self,
        address: IPv4Address | IPv6Address | str,
        port: int,
        logger
    ):
        # TCP Socket Creation
        self.socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        self.logger = logger

        self.address = address
        self.port = port

    #@sockets.raise_socket_error_dec(
    #    custom_exc=exceptions.ConnectionErrorException,
    #    msg="Ups...error has occurred while connecting to the server"
    #)
    def connect(self):
        self.socket.connect(
            (self.address, self.port)
        )
        self.logger.info(f"Socket connected to the Server: {self.address}:{self.port}")

    #@sockets.raise_socket_error_dec(
    #    custom_exc=exceptions.DataSendingErrorException,
    #    msg="Ups...error has occurred while the data sending"
    #)
    def send(
        self,
        http_options: dict,
        url_type: str,
    ) -> int:

        if not self.socket.getpeername():
            raise exceptions.ConnectionErrorException("Socket is not connected")

        request_str = sockets.get_string_request(
            http_options,
            url_type
        )

        #self.logger.info("Fetching in course...")
        #self.logger.info(request_str)

        self.socket.sendall(request_str.encode())

    #@sockets.raise_socket_error_dec(
    #    custom_exc=exceptions.DataRecvErrorException,
    #    msg="Ups...error has occurred while the data receiving"
    #)
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