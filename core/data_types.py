from typing import NamedTuple


class RequestTuple(NamedTuple):
    http_verb: str
    url_type: str
    path: dict
    query_params: str
