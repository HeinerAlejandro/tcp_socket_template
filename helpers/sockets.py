import json
import socket
from functools import wraps


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


def get_string_request(http_options: dict, url_type: str):
    return "{http_verb}+{url_type}+{path}+{query_params}".format(
        **http_options,
        url_type=url_type
    )


def get_format_data(data_bytes: bytes):
    data_str = data_bytes.decode()

    parts = data_str.split("+")
    _type = parts[0]
    url_type = parts[1]
    data = parts[2]
    return json.loads(data)
