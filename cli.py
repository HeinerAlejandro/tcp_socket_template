import os
import threading
import time

import click
from rich.console import Console
from rich.prompt import Prompt

from settigs import BASE_DIR
from core import CoreContainer

from use_cases import product

from helpers.cli import (
    create_table,
    isin_table
)

container = CoreContainer()
container.config.from_yaml(BASE_DIR / "config.yaml")


@click.group()
def service_cli():
    ...


@service_cli.command()
def start():
    container.socket_instance().connect()


@service_cli.command()
def get_products():

    products = product.get_products()

    cols = [
        "code",
        "buying_price",
        "selling_price",
        "description"
    ]

    table = create_table(
        name="Products",
        cols=cols,
        rows=products
    )

    console = Console()
    console.print(table)

    container.socket_instance().close()


@service_cli.command()
@click.option('--code', required=True, type=str)
def get_product(code):

    cols = [
        "code",
        "buying_price",
        "selling_price",
        "description",
        "created_at",
        "updated_at"
    ]

    table = create_table(
        name=f"Product: {code}",
        cols=cols
    )

    console = Console()

    def proc_func(_code: str):
        data = []
        while True:

            product_data = product.get_product(code=_code)

            isin_data = isin_table(product_data, data)

            if not isin_data:
                if os.name == "posix":
                    os.system("clear")
                elif os.name == "ce" or os.name == "nt" or os.name == "dos":
                    os.system("cls")

                table.add_row(*list(product_data.values()))
                data.append(product_data)

                console.print(table)
                console.print("Waiting for updates ...")

    get_data_product_job = threading.Thread(target=proc_func, args=(code, ), daemon=True)

    continue_pipe = True

    get_data_product_job.start()

    while continue_pipe:

        option = Prompt.ask(
            "Do you want to close the Data Flow?",
            choices=["yes", "no"]
        )

        opt_lowercase = option.lower()

        if opt_lowercase == "yes":
            continue_pipe = False

    container.socket_instance().close()


if __name__ == '__main__':
    service_cli()
