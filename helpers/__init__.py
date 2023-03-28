from yaml import safe_load

from settigs import BASE_DIR


def get_config_from_yaml(key: str | None = None):
    full_path = BASE_DIR / "config.yaml"
    config = None

    with open(full_path, "r") as _stream:
        config = safe_load(_stream).get(key, None)

    if not config:
        raise ValueError(f"There is not config for key: {key}")

    return config
