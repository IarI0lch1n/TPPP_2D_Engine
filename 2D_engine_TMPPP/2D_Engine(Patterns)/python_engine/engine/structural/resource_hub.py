from __future__ import annotations
import pygame

from python_engine.engine.structural.adapter import LegacyTextureLoader, TextureProviderAdapter
from python_engine.engine.structural.flyweight import TextureFlyweightFactory
from python_engine.engine.structural.proxy import TextureProxy


class ResourceHub:
    def __init__(self):
        self._adapter = TextureProviderAdapter(LegacyTextureLoader())
        self._flyweights = TextureFlyweightFactory()

    def get_surface_shared(self, path: str) -> pygame.Surface:
        return self._flyweights.get(path).get_surface()

    def get_surface_lazy(self, path: str) -> TextureProxy:
        return TextureProxy(lambda: self._adapter.load(path))

    def flyweight_count(self) -> int:
        return self._flyweights.count()