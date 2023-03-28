from abc import ABC, abstractmethod
import socket
from typing import Any
from dataclasses import field
from ipaddress import IPv4Address, IPv6Address


class SocketClientAbstract(ABC):
    @abstractmethod
    def connect(self):
        ...

    @abstractmethod
    def close(self):
        ...

    @abstractmethod
    def send(
        self,
        http_options: dict,
        url_type: str,
    ) -> int:
        ...

    @abstractmethod
    def recv(self, until_complete: bool):
        ...


__all__ = ["SocketClientAbstract"]
