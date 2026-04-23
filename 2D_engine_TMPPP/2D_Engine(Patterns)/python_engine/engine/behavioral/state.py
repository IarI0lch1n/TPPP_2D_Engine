from __future__ import annotations
from abc import ABC, abstractmethod


class PlayerState(ABC):
    @abstractmethod
    def enter(self, ctx) -> None: ...
    @abstractmethod
    def handle_input(self, ctx, input_ctx) -> None: ...
    @abstractmethod
    def update(self, ctx, dt: float) -> None: ...


class IdleState(PlayerState):
    def enter(self, ctx) -> None:
        ctx.entity.components["anim"] = "idle"

    def handle_input(self, ctx, input_ctx) -> None:
        if input_ctx.attack:
            ctx.change_state(AttackState())
            return
        if input_ctx.up or input_ctx.down or input_ctx.left or input_ctx.right:
            ctx.change_state(MoveState())

    def update(self, ctx, dt: float) -> None:
        pass


class MoveState(PlayerState):
    def enter(self, ctx) -> None:
        ctx.entity.components["anim"] = "run"

    def handle_input(self, ctx, input_ctx) -> None:
        if input_ctx.attack:
            ctx.change_state(AttackState())
            return
        if not (input_ctx.up or input_ctx.down or input_ctx.left or input_ctx.right):
            ctx.change_state(IdleState())

    def update(self, ctx, dt: float) -> None:
        speed = float(ctx.entity.components.get("speed", 4.0))

        dx = 0.0
        dy = 0.0
        if ctx.input.left:  dx -= 1.0
        if ctx.input.right: dx += 1.0
        if ctx.input.up:    dy -= 1.0
        if ctx.input.down:  dy += 1.0

        if dx != 0.0 and dy != 0.0:
            dx *= 0.7071
            dy *= 0.7071

        ctx.entity.x += dx * speed * dt * 60.0
        ctx.entity.y += dy * speed * dt * 60.0


class AttackState(PlayerState):
    def enter(self, ctx) -> None:
        ctx.entity.components["anim"] = "attack"
        ctx._attack_time = 0.0

    def handle_input(self, ctx, input_ctx) -> None:
        pass

    def update(self, ctx, dt: float) -> None:
        ctx._attack_time += dt
        if ctx._attack_time >= 0.15:
            ctx.input.attack = False
            if ctx.input.up or ctx.input.down or ctx.input.left or ctx.input.right:
                ctx.change_state(MoveState())
            else:
                ctx.change_state(IdleState())


class PlayerStateMachine:
    def __init__(self, entity, input_ctx):
        self.entity = entity
        self.input = input_ctx
        self.state: PlayerState = IdleState()
        self._attack_time = 0.0
        self.state.enter(self)

    def change_state(self, new_state: PlayerState) -> None:
        self.state = new_state
        self.state.enter(self)

    def handle_input(self) -> None:
        self.state.handle_input(self, self.input)

    def update(self, dt: float) -> None:
        self.state.update(self, dt)