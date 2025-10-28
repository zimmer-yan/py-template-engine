from abc import ABC, abstractmethod
from typing import Any


class TemplaterInterface(ABC):
    def __init__(self, raise_on_error: bool = False):
        self.raise_on_error = raise_on_error

    @abstractmethod
    def render(self, template: str, **kwargs: dict[str, Any]) -> str:
        raise NotImplementedError
