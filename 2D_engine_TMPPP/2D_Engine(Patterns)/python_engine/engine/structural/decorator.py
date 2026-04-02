from __future__ import annotations
from abc import ABC, abstractmethod
import pygame
from python_engine.engine.ui.products import AbstractWidget


class WidgetDecorator(AbstractWidget, ABC):
    def __init__(self, component: AbstractWidget):
        self.component = component

    def handle_event(self, event: pygame.event.Event) -> None:
        self.component.handle_event(event)

    def update(self, dt: float) -> None:
        self.component.update(dt)

    def draw(self, surface: pygame.Surface) -> None:
        self.component.draw(surface)


class BorderDecorator(WidgetDecorator):
    def __init__(self, component: AbstractWidget, color=(255, 200, 80), width=2):
        super().__init__(component)
        self.color = color
        self.width = width

    def draw(self, surface: pygame.Surface) -> None:
        super().draw(surface)
        rect = getattr(self.component, "rect", None)
        if rect is not None:
            pygame.draw.rect(surface, self.color, rect, width=self.width, border_radius=10)


class TooltipDecorator(WidgetDecorator):
    def __init__(self, component: AbstractWidget, text: str, font: pygame.font.Font, color=(240,240,240)):
        super().__init__(component)
        self.text = text
        self.font = font
        self.color = color
        self._hover = False

    def handle_event(self, event: pygame.event.Event) -> None:
        super().handle_event(event)
        if event.type == pygame.MOUSEMOTION:
            rect = getattr(self.component, "rect", None)
            self._hover = (rect is not None and rect.collidepoint(event.pos))

    def draw(self, surface: pygame.Surface) -> None:
        super().draw(surface)
        if not self._hover:
            return
        rect = getattr(self.component, "rect", None)
        if rect is None:
            return
        img = self.font.render(self.text, True, self.color)
        surface.blit(img, (rect.right + 8, rect.top))