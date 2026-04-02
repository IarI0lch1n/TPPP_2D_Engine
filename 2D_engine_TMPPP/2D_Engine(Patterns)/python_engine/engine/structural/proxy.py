from __future__ import annotations
from typing import Protocol, Callable
import pygame


class ITexture(Protocol):
    def get_surface(self) -> pygame.Surface:
        ...


class RealTexture(ITexture):
    def __init__(self, loader: Callable[[], pygame.Surface]):
        self._surface = loader()

    def get_surface(self) -> pygame.Surface:
        return self._surface


class TextureProxy(ITexture):
    def __init__(self, loader: Callable[[], pygame.Surface]):
        self._loader = loader
        self._real: RealTexture | None = None

    def get_surface(self) -> pygame.Surface:
        if self._real is None:
            self._real = RealTexture(self._loader)
        return self._real.get_surface()