from __future__ import annotations
from abc import ABC, abstractmethod
import pygame

from python_engine.engine.ui.products import AbstractButton, AbstractLabel, AbstractPanel
from python_engine.engine.ui.widgets import (
    DarkButton, DarkLabel, DarkPanel,
    LightButton, LightLabel, LightPanel
)


class AbstractUIFactory(ABC):
    """
    GoF Abstract Factory:
    CreateButton / CreateLabel / CreatePanel -> AbstractProducts
    """
    @abstractmethod
    def create_button(self, x, y, w, h, text: str, on_click=None) -> AbstractButton: ...

    @abstractmethod
    def create_label(self, x, y, text: str, size: int = 24) -> AbstractLabel: ...

    @abstractmethod
    def create_panel(self, x, y, w, h) -> AbstractPanel: ...


class DarkUIFactory(AbstractUIFactory):
    def _font(self, size: int):
        return pygame.font.SysFont("Consolas", size)

    def create_button(self, x, y, w, h, text: str, on_click=None) -> AbstractButton:
        colors = {
            "bg": (30, 30, 35),
            "bg_hover": (45, 45, 55),
            "text": (235, 235, 235),
            "border": (90, 90, 110),
        }
        return DarkButton(pygame.Rect(x, y, w, h), text, self._font(22), colors, on_click)

    def create_label(self, x, y, text: str, size: int = 24) -> AbstractLabel:
        return DarkLabel(x, y, text, self._font(size), (235, 235, 235))

    def create_panel(self, x, y, w, h) -> AbstractPanel:
        return DarkPanel(pygame.Rect(x, y, w, h), (20, 20, 24), (80, 80, 95))


class LightUIFactory(AbstractUIFactory):
    def _font(self, size: int):
        return pygame.font.SysFont("Consolas", size)

    def create_button(self, x, y, w, h, text: str, on_click=None) -> AbstractButton:
        colors = {
            "bg": (235, 235, 235),
            "bg_hover": (210, 210, 210),
            "text": (20, 20, 20),
            "border": (140, 140, 140),
        }
        return LightButton(pygame.Rect(x, y, w, h), text, self._font(22), colors, on_click)

    def create_label(self, x, y, text: str, size: int = 24) -> AbstractLabel:
        return LightLabel(x, y, text, self._font(size), (20, 20, 20))

    def create_panel(self, x, y, w, h) -> AbstractPanel:
        return LightPanel(pygame.Rect(x, y, w, h), (245, 245, 245), (180, 180, 180))