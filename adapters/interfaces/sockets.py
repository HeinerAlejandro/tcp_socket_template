from abc import ABC, abstractmethod
from typing import Callable
from socketserver import TCPServer, BaseRequestHandler
from typing import Any
from dataclasses import dataclass, field
from ipaddress import (
    IPv4Address,
    IPv6Address
)

from adapters.interfaces import FetchAbstract


class SocketServerHandlerPeriodicAbstract(ABC):

    @abstractmethod
    def fetch_product_by_interval(self, interval: int, fetch_handler: Callable):
        ...


class SocketServerAbstract(ABC):

    @abstractmethod
    def _connect(self):
        ...


__all__ = [
    "SocketServerHandlerPeriodicAbstract",
    "SocketServerAbstract",
]
