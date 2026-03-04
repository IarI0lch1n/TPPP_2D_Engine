from __future__ import annotations
from abc import ABC, abstractmethod

from python_engine.engine.ecs.entity import Entity
from python_engine.engine.core.resources import ResourceManager


class EntityBuilder(ABC):
    """
    GoF Builder: интерфейс шагов построения.
    """
    def __init__(self):
        self._entity: Entity | None = None

    def get_result(self) -> Entity:
        return self._entity

    @abstractmethod
    def reset(self): ...

    @abstractmethod
    def build_identity(self): ...

    @abstractmethod
    def build_transform(self, x: float, y: float): ...

    @abstractmethod
    def build_visual(self): ...

    @abstractmethod
    def build_stats(self): ...


class PlayerBuilder(EntityBuilder):
    def reset(self):
        self._entity = Entity("Player")

    def build_identity(self):
        self._entity.components["tag"] = "actor"

    def build_transform(self, x: float, y: float):
        self._entity.x = x
        self._entity.y = y

    def build_visual(self):
        self._entity.components["sprite"] = ResourceManager().texture("player.png")
        self._entity.components["color"] = (210, 90, 90)

    def build_stats(self):
        self._entity.components["hp"] = 100
        self._entity.components["speed"] = 4.5


class NPCMerchantBuilder(EntityBuilder):
    def reset(self):
        self._entity = Entity("NPC:merchant")

    def build_identity(self):
        self._entity.components["tag"] = "actor"

    def build_transform(self, x: float, y: float):
        self._entity.x = x
        self._entity.y = y

    def build_visual(self):
        self._entity.components["sprite"] = ResourceManager().texture("npc.png")
        self._entity.components["color"] = (90, 170, 220)

    def build_stats(self):
        self._entity.components["hp"] = 60
        self._entity.components["speed"] = 2.2


class SlimeEnemyBuilder(EntityBuilder):
    def reset(self):
        self._entity = Entity("Enemy:slime")

    def build_identity(self):
        self._entity.components["tag"] = "enemy"

    def build_transform(self, x: float, y: float):
        self._entity.x = x
        self._entity.y = y

    def build_visual(self):
        self._entity.components["sprite"] = ResourceManager().texture("slime.png")
        self._entity.components["color"] = (110, 220, 140)

    def build_stats(self):
        self._entity.components["hp"] = 30
        self._entity.components["speed"] = 1.2