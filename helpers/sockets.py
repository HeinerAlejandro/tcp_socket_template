import json
import socket
from functools import wraps

from core.data_types import RequestTuple


def raise_socket_error_dec(custom_exc: Exception, msg: str):
    def raise_socket_error(func: callable) -> callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except socket.error:
                raise custom_exc(msg)
        return wrapper
    return raise_socket_error


def resolve_request_type(request_str: str) -> RequestTuple:
    """Destructure request string from client

    Request String is made of 4 sections separated by '+' symbol:
    - HTTP Verb
    - URL Type
    - Path Data
    - Query Params

    :param self:
    :param request_str: request string from socket client
    :return:
        :RequestTuple: Return a destructure form by + separator
    """

    request_parts = request_str.split("+")

    return RequestTuple(
        http_verb=request_parts[0],
        url_type=request_parts[1],
        path=json.loads(request_parts[2]),
        query_params=request_parts[3]
    )
