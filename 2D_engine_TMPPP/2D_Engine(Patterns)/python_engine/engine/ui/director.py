from __future__ import annotations
from abc import ABC, abstractmethod
import pygame


class AbstractWidget(ABC):
    @abstractmethod
    def handle_event(self, event: pygame.event.Event): ...

    @abstractmethod
    def update(self, dt: float): ...

    @abstractmethod
    def draw(self, surface: pygame.Surface): ...


class AbstractButton(AbstractWidget, ABC):
    @abstractmethod
    def set_on_click(self, callback): ...

    @abstractmethod
    def set_text(self, text: str): ...


class AbstractLabel(AbstractWidget, ABC):
    @abstractmethod
    def set_text(self, text: str): ...


class AbstractPanel(AbstractWidget, ABC):
    @abstractmethod
    def add(self, widget: AbstractWidget) -> AbstractWidget: ...