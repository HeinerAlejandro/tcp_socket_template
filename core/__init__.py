import logging

from dependency_injector import containers, providers

from adapters.socket_client import SocketClient


FORMAT = "%(asctime)s %(clientip)-15s %(user)-8s %(message)s"

logging.basicConfig(
    level=logging.INFO,
    format=FORMAT
)


class CoreContainer(containers.DeclarativeContainer):
    """Core Container contains all adapters you have to use
    I.E:
    - Socket Custom Class
    - Sentry Custom Class
    - UI CLI/Dash
    """

    config = providers.Configuration()

    default_logging = providers.Singleton(
        logging.getLogger,
        "socket_client"
    )

    socket_instance = providers.Singleton(
        SocketClient,
        address=config.server.address,
        port=config.server.port,
        logger=default_logging
    )
