from __future__ import annotations
from dataclasses import dataclass

from python_engine.engine.behavioral.state import PlayerStateMachine
from python_engine.engine.behavioral.strategy import EnemyStrategy, NeutralStrategy
from python_engine.engine.behavioral.observer import (
    EventBus,
    EntitySpawned,
    HealthChanged,
    EntityDied
)
from python_engine.engine.behavioral.memento import GameMemento, Originator


@dataclass
class InputContext:
    up: bool = False
    down: bool = False
    left: bool = False
    right: bool = False

    attack: bool = False
    facing: tuple[int, int] = (0, 1)


class WorldContext:
    def __init__(self):
        self.player: PlayerController | None = None
        self.enemies: list[EnemyController] = []

    def get_player(self):
        return self.player


class PlayerController(Originator):
    def __init__(self, entity, input_ctx: InputContext, bus: EventBus):
        self.entity = entity
        self.input = input_ctx
        self.bus = bus
        self.sm = PlayerStateMachine(entity, input_ctx)
        self.entity_id = id(entity)

        self.attack_range = 48.0
        self.attack_fov_deg = 90.0
        self.sword_damage = 50
        self._attack_cooldown = 0.0  

        self.bus.notify(EntitySpawned(self.entity_id, self.entity.name))

    def update(self, dt: float):
        if self._attack_cooldown > 0.0:
            self._attack_cooldown = max(0.0, self._attack_cooldown - dt)

        self.sm.handle_input()
        self.sm.update(dt)

    def can_attack(self) -> bool:
        return self._attack_cooldown <= 0.0

    def start_attack_cd(self) -> None:
        self._attack_cooldown = 0.25

    def damage(self, amount: int):
        hp = int(self.entity.components.get("hp", 100))
        hp = max(0, hp - amount)
        self.entity.components["hp"] = hp

        self.bus.notify(HealthChanged(self.entity_id, hp))

        if hp <= 0:
            self.bus.notify(EntityDied(self.entity_id, self.entity.name))

    def create_memento(self) -> GameMemento:
        return GameMemento({
            "x": float(self.entity.x),
            "y": float(self.entity.y),
            "hp": int(self.entity.components.get("hp", 100)),
            "facing": tuple(self.input.facing),
        })

    def restore(self, memento: GameMemento) -> None:
        st = memento.state
        self.entity.x = float(st["x"])
        self.entity.y = float(st["y"])
        self.entity.components["hp"] = int(st["hp"])
        self.input.facing = tuple(st.get("facing", (0, 1)))


class EnemyController:
    def __init__(self, entity, bus: EventBus, strategy: EnemyStrategy | None = None):
        self.entity = entity
        self.bus = bus
        self.strategy = strategy or NeutralStrategy()
        self.entity_id = id(entity)

        self.bus.notify(EntitySpawned(self.entity_id, self.entity.name))

    def set_strategy(self, strategy: EnemyStrategy):
        self.strategy = strategy

    def update(self, world_ctx: WorldContext, dt: float):
        self.strategy.update(self, world_ctx, dt)

    def hp(self) -> int:
        return int(self.entity.components.get("hp", 1))

    def damage(self, amount: int):
        hp = self.hp()
        hp = max(0, hp - amount)
        self.entity.components["hp"] = hp

        if hp <= 0:
            self.bus.notify(EntityDied(self.entity_id, self.entity.name))