from __future__ import annotations
import math

from python_engine.engine.gameplay.actors import PlayerController, EnemyController, WorldContext
from python_engine.engine.behavioral.observer import EntityDied


def _len(x, y):
    return math.sqrt(x*x + y*y)


class CombatSystem:
    """
    SRP: вся боёвка отдельно.
    - враг наносит урон игроку при близком расстоянии (с кулдауном)
    - игрок бьёт мечом по Space в секторе (range + fov) перед собой
    """
    def __init__(self):
        self.enemy_hit_range = 22.0
        self.enemy_damage = 10
        self.enemy_hit_cd = 0.6
        self._enemy_cd = {}  

    def update(self, world_ctx: WorldContext, dt: float):
        for k in list(self._enemy_cd.keys()):
            self._enemy_cd[k] = max(0.0, self._enemy_cd[k] - dt)

        player = world_ctx.get_player()
        if not player:
            return

        for enemy in list(world_ctx.enemies):
            if enemy.hp() <= 0:
                continue
            dx = player.entity.x - enemy.entity.x
            dy = player.entity.y - enemy.entity.y
            dist = _len(dx, dy)

            cd = self._enemy_cd.get(enemy.entity_id, 0.0)
            if dist <= self.enemy_hit_range and cd <= 0.0:
                player.damage(self.enemy_damage)
                self._enemy_cd[enemy.entity_id] = self.enemy_hit_cd

        if player.input.attack and player.can_attack():
            self._player_sword_hit(player, world_ctx)
            player.start_attack_cd()

    def _player_sword_hit(self, player: PlayerController, world_ctx: WorldContext):
        fx, fy = player.input.facing
        if fx == 0 and fy == 0:
            fx, fy = 0, 1

        fov_cos = math.cos(math.radians(player.attack_fov_deg) / 2.0)

        for enemy in list(world_ctx.enemies):
            if enemy.hp() <= 0:
                continue

            dx = enemy.entity.x - player.entity.x
            dy = enemy.entity.y - player.entity.y
            dist = math.sqrt(dx*dx + dy*dy)

            if dist > player.attack_range:
                continue

            close_radius = 18.0
            if dist <= close_radius:
                enemy.damage(player.sword_damage)
                continue

            nx = dx / dist
            ny = dy / dist

            fl = math.sqrt(fx*fx + fy*fy)
            fdx = fx / fl
            fdy = fy / fl

            dot = nx * fdx + ny * fdy
            if dot >= fov_cos:
                enemy.damage(player.sword_damage)