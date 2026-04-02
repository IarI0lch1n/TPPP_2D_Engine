from __future__ import annotations
from abc import ABC, abstractmethod

from python_engine.engine.ui.products import AbstractPanel, AbstractWidget
from python_engine.engine.ui.factory import AbstractUIFactory


class UIElementCreator(ABC):
    """
    GoF Creator:
    - render(panel) = operation()
    - factory_method(factory) = creates Product
    """
    def render(self, panel: AbstractPanel, factory: AbstractUIFactory) -> AbstractWidget:
        widget = self.factory_method(factory)   
        panel.add(widget)
        return widget

    @abstractmethod
    def factory_method(self, factory: AbstractUIFactory) -> AbstractWidget:
        pass


class ButtonCreator(UIElementCreator):
    def __init__(self, x, y, w, h, text, on_click=None):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.text = text
        self.on_click = on_click

    def factory_method(self, factory: AbstractUIFactory) -> AbstractWidget:
        return factory.create_button(self.x, self.y, self.w, self.h, self.text, self.on_click)


class LabelCreator(UIElementCreator):
    def __init__(self, x, y, text, size=24):
        self.x, self.y = x, y
        self.text = text
        self.size = size

    def factory_method(self, factory: AbstractUIFactory) -> AbstractWidget:
        return factory.create_label(self.x, self.y, self.text, self.size)