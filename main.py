from dependency_injector.wiring import Provide, inject

from core import CoreContainer

from adapters.interfaces.sockets import SocketServerAbstract

from settigs import BASE_DIR


@inject
def start_server(
    socket_server: SocketServerAbstract = Provide[CoreContainer.socket_server],
    default_logging=Provide[CoreContainer.default_logging]
):
    default_logging.info("RUNNING SERVER")
    socket_server.server.serve_forever()


if __name__ == "__main__":

    container = CoreContainer()

    container.config.from_yaml(BASE_DIR / "config.yaml")

    container.wire(modules=[__name__])

    start_server()
