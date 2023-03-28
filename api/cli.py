import click
from core import core_obj


@click.group()
def service_cli():
    ...


@service_cli.command()
def service_start():
    core_obj.socket_instance.send({"hola": "te quiero"}, str, lambda data: data["hola"])


if __name__ == "__main__":
    service_cli()
