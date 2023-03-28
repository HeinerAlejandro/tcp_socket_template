from abc import ABC, abstractmethod


class FetchAbstract(ABC):
    @abstractmethod
    def get_data(self, url: str):
        ...
