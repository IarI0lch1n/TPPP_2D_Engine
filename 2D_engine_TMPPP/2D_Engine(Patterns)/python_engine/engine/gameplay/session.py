from __future__ import annotations

from typing import Any, Dict, List

from python_engine.engine.behavioral.memento import GameMemento, Originator
from python_engine.engine.behavioral.strategy import AggressiveStrategy, PatrolStrategy, NeutralStrategy
from python_engine.engine.gameplay.actors import EnemyController, WorldContext, PlayerController
from python_engine.engine.behavioral.observer import EventBus


def _strategy_to_name(strategy) -> str:
    return strategy.__class__.__name__


def _strategy_from_data(data: Dict[str, Any]):
    name = data.get("strategy", "NeutralStrategy")

    if name == "AggressiveStrategy":
        return AggressiveStrategy()

    if name == "NeutralStrategy":
        return NeutralStrategy()

    if name == "PatrolStrategy":
        left = float(data.get("patrol_left", 0))
        right = float(data.get("patrol_right", 0))
        return PatrolStrategy(left=left, right=right)

    return NeutralStrategy()


class GameSession(Originator):
    """
    Originator (GoF Memento): сохраняет/восстанавливает полный прогресс игры:
    - player: x/y/hp/facing
    - wave manager state
    - enemies: list (name, x, y, hp, speed, strategy + patrol params)
    """

    def __init__(self, engine_facade, bus: EventBus, world_ctx: WorldContext, player: PlayerController, waves_manager):
        self.engine = engine_facade
        self.bus = bus
        self.world_ctx = world_ctx
        self.player = player
        self.waves = waves_manager

    def create_memento(self) -> GameMemento:
        p = {
            "x": float(self.player.entity.x),
            "y": float(self.player.entity.y),
            "hp": int(self.player.entity.components.get("hp", 100)),
            "facing": tuple(self.player.input.facing),
        }

        w = {
            "wave": int(getattr(self.waves, "wave", 1)),
            "to_spawn": int(getattr(self.waves, "to_spawn", 0)),
            "spawned": int(getattr(self.waves, "spawned", 0)),
            "killed": int(getattr(self.waves, "killed", 0)),
            "spawn_interval": float(getattr(self.waves, "spawn_interval", 1.0)),
            "tim    er": float(getattr(self.waves, "_timer", 0.0)),
        }

        enemies: List[Dict[str, Any]] = []
        for ec in self.world_ctx.enemies:
            ent = ec.entity
            ed = {
                "name": ent.name,
                "x": float(ent.x),
                "y": float(ent.y),
                "hp": int(ent.components.get("hp", 1)),
                "speed": float(ent.components.get("speed", 1.0)),
                "strategy": _strategy_to_name(ec.strategy),
            }

            if ed["strategy"] == "PatrolStrategy":
                ed["patrol_left"] = float(getattr(ec.strategy, "left", 0))
                ed["patrol_right"] = float(getattr(ec.strategy, "right", 0))

            enemies.append(ed)

        return GameMemento({
            "player": p,
            "waves": w,
            "enemies": enemies
        })

    def restore(self, memento: GameMemento) -> None:
        st = memento.state

        p = st["player"]
        self.player.entity.x = float(p["x"])
        self.player.entity.y = float(p["y"])
        self.player.entity.components["hp"] = int(p["hp"])
        self.player.input.facing = tuple(p.get("facing", (0, 1)))

        self.engine.world.entities = [ent for ent in self.engine.world.entities if "Enemy:" not in ent.name]
        self.world_ctx.enemies.clear()

        for ed in st["enemies"]:
            enemy_ent = self.engine.prefabs.enemy_slime(ed["x"], ed["y"])
            enemy_ent.name = ed["name"]
            enemy_ent.components["hp"] = int(ed["hp"])
            enemy_ent.components["speed"] = float(ed["speed"])

            self.engine.world.add(enemy_ent)

            ctrl = EnemyController(enemy_ent, self.bus)
            strat = _strategy_from_data(ed)
            ctrl.set_strategy(strat)
            self.world_ctx.enemies.append(ctrl)

        w = st.get("waves", {})
        if hasattr(self.waves, "wave"): self.waves.wave = int(w.get("wave", getattr(self.waves, "wave", 1)))
        if hasattr(self.waves, "to_spawn"): self.waves.to_spawn = int(w.get("to_spawn", getattr(self.waves, "to_spawn", 0)))
        if hasattr(self.waves, "spawned"): self.waves.spawned = int(w.get("spawned", getattr(self.waves, "spawned", 0)))
        if hasattr(self.waves, "killed"): self.waves.killed = int(w.get("killed", getattr(self.waves, "killed", 0)))
        if hasattr(self.waves, "spawn_interval"): self.waves.spawn_interval = float(w.get("spawn_interval", getattr(self.waves, "spawn_interval", 1.0)))
        if hasattr(self.waves, "_timer"): self.waves._timer = float(w.get("timer", getattr(self.waves, "_timer", 0.0)))