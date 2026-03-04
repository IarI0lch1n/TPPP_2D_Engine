from __future__ import annotations

from abc import ABC, abstractmethod
import pygame


class AbstractWidget(ABC):
    """
    Product (общий базовый продукт для UI)
    """

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        pass

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        pass


class AbstractButton(AbstractWidget, ABC):
    """
    AbstractProductA (пример: Button)
    """

    @abstractmethod
    def set_on_click(self, callback) -> None:
        pass

    @abstractmethod
    def set_text(self, text: str) -> None:
        pass


class AbstractLabel(AbstractWidget, ABC):
    """
    AbstractProductB (пример: Label)
    """

    @abstractmethod
    def set_text(self, text: str) -> None:
        pass


class AbstractPanel(AbstractWidget, ABC):
    """
    AbstractProductC (пример: Panel / Container)
    """

    @abstractmethod
    def add(self, widget: AbstractWidget) -> AbstractWidget:
        pass