from core import CoreContainer
from settigs import BASE_DIR


container = CoreContainer()
container.config.from_yaml(BASE_DIR / "config.yaml")