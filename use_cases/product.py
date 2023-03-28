import json

from dependency_injector.wiring import inject, Provide

from adapters.interfaces import sockets

from core import CoreContainer
from use_cases import container


@inject
def get_products(
    socket_client: sockets.SocketClientAbstract = Provide[CoreContainer.socket_instance],
    default_logging=Provide[CoreContainer.default_logging]
) -> list[dict]:

    socket_client.connect()

    socket_client.send(
        {
            "http_verb": "GET",
            "path": {},
            "query_params": ""
        },
        url_type="PRODUCTS"
    )

    return socket_client.recv()


@inject
def get_product(
    code: str,
    socket_client: sockets.SocketClientAbstract = Provide[CoreContainer.socket_instance],
    default_logging=Provide[CoreContainer.default_logging],
) -> dict:

    try:
        socket_client.socket.getpeername()
    except OSError:
        socket_client.connect()

    socket_client.send(
        {
            "http_verb": "GET",
            "path": json.dumps({"code": code}),
            "query_params": ""
        },
        url_type="PRODUCT"
    )

    response = socket_client.recv(until_complete=False)

    return response


container.wire(modules=[__name__])
