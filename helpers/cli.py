from rich.table import Table
from rich.console import Console


def create_table(name: str, cols: list[str], rows: list[dict] = []) -> Table:
    table = Table(title=name)

    for col in cols:
        table.add_column(col)

    for row in rows:
        values = []
        for col in cols:
            values.append(row[col])

        table.add_row(*values)

    return table


def wrapper_with_handler(func: callable, handler: callable):
    def new_func():
        data = func()
        new_obj = handler([data])
        console = Console()
        console.print(new_obj)

    return new_func


def isin_table(data: dict, table: list[dict]):
    records = [item for item in table if item["update_at"] == data["update_at"]]
    return len(records) > 0
