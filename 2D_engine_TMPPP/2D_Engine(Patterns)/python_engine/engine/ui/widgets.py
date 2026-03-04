from __future__ import annotations
import pygame
from python_engine.engine.ui.products import AbstractButton, AbstractLabel, AbstractPanel, AbstractWidget


# -----------------------
# Base implementations
# -----------------------
class _BaseLabel(AbstractLabel):
    def __init__(self, x, y, text, font: pygame.font.Font, color):
        self.x = x
        self.y = y
        self.text = text
        self.font = font
        self.color = color

    def set_text(self, text: str):
        self.text = text

    def handle_event(self, event):  # label doesn't react
        pass

    def update(self, dt: float):
        pass

    def draw(self, surface):
        img = self.font.render(self.text, True, self.color)
        surface.blit(img, (self.x, self.y))


class _BaseButton(AbstractButton):
    def __init__(self, rect: pygame.Rect, text: str, font: pygame.font.Font, colors: dict, on_click=None):
        self.rect = rect
        self.text = text
        self.font = font
        self.colors = colors  # bg, bg_hover, text, border
        self.on_click = on_click
        self._hover = False

    def set_on_click(self, callback):
        self.on_click = callback

    def set_text(self, text: str):
        self.text = text

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self._hover = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.on_click:
                    self.on_click()

    def update(self, dt: float):
        pass

    def draw(self, surface):
        bg = self.colors["bg_hover"] if self._hover else self.colors["bg"]
        pygame.draw.rect(surface, bg, self.rect, border_radius=10)
        pygame.draw.rect(surface, self.colors["border"], self.rect, width=2, border_radius=10)

        img = self.font.render(self.text, True, self.colors["text"])
        x = self.rect.centerx - img.get_width() // 2
        y = self.rect.centery - img.get_height() // 2
        surface.blit(img, (x, y))


class _BasePanel(AbstractPanel):
    def __init__(self, rect: pygame.Rect, bg_color, border_color):
        self.rect = rect
        self.bg_color = bg_color
        self.border_color = border_color
        self.children: list[AbstractWidget] = []

    def add(self, widget: AbstractWidget) -> AbstractWidget:
        self.children.append(widget)
        return widget

    def handle_event(self, event):
        for c in self.children:
            c.handle_event(event)

    def update(self, dt: float):
        for c in self.children:
            c.update(dt)

    def draw(self, surface):
        pygame.draw.rect(surface, self.bg_color, self.rect, border_radius=14)
        pygame.draw.rect(surface, self.border_color, self.rect, width=2, border_radius=14)
        for c in self.children:
            c.draw(surface)


# -----------------------
# Concrete Products - DARK family
# -----------------------
class DarkButton(_BaseButton):
    pass

class DarkLabel(_BaseLabel):
    pass

class DarkPanel(_BasePanel):
    pass


# -----------------------
# Concrete Products - LIGHT family
# -----------------------
class LightButton(_BaseButton):
    pass

class LightLabel(_BaseLabel):
    pass

class LightPanel(_BasePanel):
    pass