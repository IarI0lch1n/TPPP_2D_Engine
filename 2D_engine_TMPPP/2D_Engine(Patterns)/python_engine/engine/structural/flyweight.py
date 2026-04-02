from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Protocol
import pygame


class ITexture(Protocol):
    def get_surface(self) -> pygame.Surface:
        ...


@dataclass(frozen=True)
class TextureFlyweight:
    path: str
    surface: pygame.Surface

    def get_surface(self) -> pygame.Surface:
        return self.surface


class TextureFlyweightFactory:
    def __init__(self):
        self._pool: Dict[str, TextureFlyweight] = {}

    def get(self, path: str) -> TextureFlyweight:
        if path not in self._pool:
            surf = pygame.image.load(path).convert_alpha()
            self._pool[path] = TextureFlyweight(path=path, surface=surf)
        return self._pool[path]

    def count(self) -> int:
        return len(self._pool)