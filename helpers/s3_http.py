import json

import requests

from core.data_types import RequestTuple


def get_url_by_request_type(http_options: dict, request_tuple: RequestTuple) -> str:

    types = {
        "PRODUCTS": "/api/products/",
        "PRODUCT": "/api/products/{code}"
    }

    _type = types.get(request_tuple.url_type)

    url_with_path = _type.format(**request_tuple.path)
    url_init = f"{http_options['schema']}://{http_options['address']}:{http_options['port']}"
    url = f"{url_init}{url_with_path}?{request_tuple.query_params}"

    return url


def do_s3_fetch(url_type: str, url: str):

    response = requests.get(url)

    if response.status_code == 200:

        data_type = "LIST"

        data = response.json()

        if "results" not in data:
            data_type = "JSON"
        else:
            data = data["results"]

    return "{data_type}+{url_type}+{data}".format(
        data_type=data_type,
        url_type=url_type,
        data=json.dumps(data)
    )
