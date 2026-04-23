from __future__ import annotations
from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass


# ---- Movement flags ----
class MoveUpCommand(Command):
    def __init__(self, input_ctx): self.input = input_ctx
    def execute(self) -> None: self.input.up = True


class MoveDownCommand(Command):
    def __init__(self, input_ctx): self.input = input_ctx
    def execute(self) -> None: self.input.down = True


class MoveLeftCommand(Command):
    def __init__(self, input_ctx): self.input = input_ctx
    def execute(self) -> None: self.input.left = True


class MoveRightCommand(Command):
    def __init__(self, input_ctx): self.input = input_ctx
    def execute(self) -> None: self.input.right = True


class StopUpCommand(Command):
    def __init__(self, input_ctx): self.input = input_ctx
    def execute(self) -> None: self.input.up = False


class StopDownCommand(Command):
    def __init__(self, input_ctx): self.input = input_ctx
    def execute(self) -> None: self.input.down = False


class StopLeftCommand(Command):
    def __init__(self, input_ctx): self.input = input_ctx
    def execute(self) -> None: self.input.left = False


class StopRightCommand(Command):
    def __init__(self, input_ctx): self.input = input_ctx
    def execute(self) -> None: self.input.right = False


# ---- Facing (куда смотрит игрок) ----
class FaceUpCommand(Command):
    def __init__(self, input_ctx): self.input = input_ctx
    def execute(self) -> None: self.input.facing = (0, -1)


class FaceDownCommand(Command):
    def __init__(self, input_ctx): self.input = input_ctx
    def execute(self) -> None: self.input.facing = (0, 1)


class FaceLeftCommand(Command):
    def __init__(self, input_ctx): self.input = input_ctx
    def execute(self) -> None: self.input.facing = (-1, 0)


class FaceRightCommand(Command):
    def __init__(self, input_ctx): self.input = input_ctx
    def execute(self) -> None: self.input.facing = (1, 0)


# ---- Attack flag ----
class AttackCommand(Command):
    def __init__(self, input_ctx): self.input = input_ctx
    def execute(self) -> None: self.input.attack = True


class ClearAttackCommand(Command):
    def __init__(self, input_ctx): self.input = input_ctx
    def execute(self) -> None: self.input.attack = False


class InputInvoker:
    """Invoker (GoF): вызывает набор команд, привязанных к событию."""
    def __init__(self):
        self.on_press = {}  
        self.on_release = {}  

    def bind_press(self, key, cmd: Command):
        self.on_press.setdefault(key, []).append(cmd)

    def bind_release(self, key, cmd: Command):
        self.on_release.setdefault(key, []).append(cmd)

    def handle_press(self, key):
        for cmd in self.on_press.get(key, []):
            cmd.execute()

    def handle_release(self, key):
        for cmd in self.on_release.get(key, []):
            cmd.execute()