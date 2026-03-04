import copy
from dataclasses import dataclass


@dataclass
class Enemy:
    kind: str
    hp: int
    speed: float

    def clone(self):
        return copy.deepcopy(self)


class PrototypeRegistry:
    def __init__(self):
        self._items = {}

    def register(self, key: str, proto):
        self._items[key] = proto

    def clone(self, key: str):
        return self._items[key].clone()

    def keys(self):
        return list(self._items.keys())


REGISTRY = PrototypeRegistry()
REGISTRY.register("slime", Enemy("slime", 30, 1.2))
REGISTRY.register("treant", Enemy("treant", 120, 0.8))