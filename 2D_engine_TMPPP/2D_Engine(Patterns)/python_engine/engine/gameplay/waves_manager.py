from __future__ import annotations
import random

from python_engine.engine.behavioral.strategy import AggressiveStrategy
from python_engine.engine.gameplay.actors import EnemyController, WorldContext
from python_engine.engine.behavioral.observer import EventBus
from python_engine.engine.behavioral.observer import EntityDied


class WaveManager:
    """
    Простая система волн:
    - каждые N секунд спавнит врага
    - увеличивает кол-во врагов в волне со временем
    """
    def __init__(self, engine_facade, bus: EventBus, world_ctx: WorldContext):
        self.engine = engine_facade
        self.bus = bus
        self.world_ctx = world_ctx

        self.wave = 1
        self.to_spawn = 3
        self.spawned = 0

        self.spawn_interval = 1.0
        self._timer = 0.0

        self.killed = 0
        self.bus.subscribe(EntityDied, self._DeathObserver(self))

    class _DeathObserver:
        def __init__(self, wm): self.wm = wm
        def on_event(self, e):
            if "Enemy:" in e.name:
                self.wm.killed += 1

    def update(self, dt: float):
        if self.killed >= self.to_spawn and self.spawned >= self.to_spawn:
            self.wave += 1
            self.to_spawn = 3 + (self.wave - 1) * 2
            self.spawned = 0
            self.killed = 0
            self.spawn_interval = max(0.4, self.spawn_interval * 0.92)

        self._timer += dt
        if self.spawned < self.to_spawn and self._timer >= self.spawn_interval:
            self._timer = 0.0
            self._spawn_enemy()
            self.spawned += 1

    def _spawn_enemy(self):
        x = random.randint(0, 560)
        y = random.randint(0, 900)  

        enemy_entity = self.engine.prefabs.enemy_slime(x, y)
        self.engine.world.add(enemy_entity)

        enemy = EnemyController(enemy_entity, self.bus, strategy=AggressiveStrategy())
        self.world_ctx.enemies.append(enemy)