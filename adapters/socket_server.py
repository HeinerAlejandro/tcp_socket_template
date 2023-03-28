from socketserver import (
    ThreadingTCPServer,
    BaseRequestHandler
)

from typing import Callable

from ipaddress import (
    IPv4Address,
    IPv6Address
)

import time

from adapters.interfaces.sockets import (
    SocketServerHandlerPeriodicAbstract,
    SocketServerAbstract
)

from helpers import (
    sockets,
    s3_http,
    get_config_from_yaml
)

from core import exceptions
from core.data_types import RequestTuple


class SocketServerRequestHandler(
    SocketServerHandlerPeriodicAbstract,
    BaseRequestHandler
):

    def fetch_product_by_interval(self, interval: int, fetch_handler: Callable):
        while True:
            product_str_data: str = fetch_handler()
            self.request.sendall(product_str_data.encode())
            print(interval)
            time.sleep(interval)

    def handle(self):

        request_type = self.request.recv(1024).decode()

        request_tuple: RequestTuple = sockets.resolve_request_type(request_type)

        s3_http_config = get_config_from_yaml("s3_server")

        s3_url = s3_http.get_url_by_request_type(s3_http_config, request_tuple)

        if request_tuple.url_type == "PRODUCT":
            self.request.setblocking(False)
            handler_option_config = get_config_from_yaml("handler_options")

            self.fetch_product_by_interval(
                handler_option_config["interval"],
                lambda: s3_http.do_s3_fetch(request_tuple.url_type, s3_url)
            )
        else:
            data_str = s3_http.do_s3_fetch(request_tuple.url_type, s3_url)
            self.request.sendall(data_str.encode())


class SocketServer(SocketServerAbstract):
    """Socket TCP/IP"""

    def __init__(
        self,
        address: IPv4Address | IPv6Address | str,
        port: int,
        request_handler: BaseRequestHandler
    ):

        self.address = address
        self.port = port
        self.request_handler = request_handler

        # TCP Socket Server Creation
        self.server = None
        self._connect()

    @sockets.raise_socket_error_dec(
        custom_exc=exceptions.ConnectionErrorException,
        msg="Ups...error has occurred while connecting to the server"
    )
    def _connect(self):
        self.server = ThreadingTCPServer(
            (self.address, int(self.port)),
            self.request_handler
        )
