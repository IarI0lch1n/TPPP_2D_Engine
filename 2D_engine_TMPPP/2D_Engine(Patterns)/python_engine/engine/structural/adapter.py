from __future__ import annotations
from typing import Protocol
import pygame


class ITextureProvider(Protocol):
    def load(self, path: str) -> pygame.Surface:
        ...

class LegacyTextureLoader:
    def load_texture(self, filename: str) -> pygame.Surface:
        return pygame.image.load(filename).convert_alpha()


class TextureProviderAdapter(ITextureProvider):
    def __init__(self, adaptee: LegacyTextureLoader):
        self.adaptee = adaptee

    def load(self, path: str) -> pygame.Surface:
        return self.adaptee.load_texture(path)