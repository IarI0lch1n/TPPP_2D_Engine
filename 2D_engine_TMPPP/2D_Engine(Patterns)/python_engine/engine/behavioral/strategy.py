from __future__ import annotations
from abc import ABC, abstractmethod


class EnemyStrategy(ABC):
    """Strategy interface (GoF)."""
    @abstractmethod
    def update(self, enemy_ctx, world_ctx, dt: float) -> None:
        pass


class AggressiveStrategy(EnemyStrategy):
    """ConcreteStrategy: агрессивное поведение."""
    def update(self, enemy_ctx, world_ctx, dt: float) -> None:
        player = world_ctx.get_player()
        if not player:
            return
        dx = player.entity.x - enemy_ctx.entity.x
        dy = player.entity.y - enemy_ctx.entity.y
        speed = enemy_ctx.entity.components.get("speed", 1.0)
        enemy_ctx.entity.x += (1 if dx > 0 else -1 if dx < 0 else 0) * speed * dt * 60
        enemy_ctx.entity.y += (1 if dy > 0 else -1 if dy < 0 else 0) * speed * dt * 60


class PatrolStrategy(EnemyStrategy):
    """ConcreteStrategy: патруль."""
    def __init__(self, left: float, right: float):
        self.left = left
        self.right = right
        self.dir = 1

    def update(self, enemy_ctx, world_ctx, dt: float) -> None:
        speed = enemy_ctx.entity.components.get("speed", 1.0)
        enemy_ctx.entity.x += self.dir * speed * dt * 60
        if enemy_ctx.entity.x < self.left:
            enemy_ctx.entity.x = self.left
            self.dir = 1
        elif enemy_ctx.entity.x > self.right:
            enemy_ctx.entity.x = self.right
            self.dir = -1


class NeutralStrategy(EnemyStrategy):
    """ConcreteStrategy: нейтральное (стоит/минимально двигается)."""
    def update(self, enemy_ctx, world_ctx, dt: float) -> None:
        return