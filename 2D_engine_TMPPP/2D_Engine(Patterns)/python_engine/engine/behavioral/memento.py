from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass(frozen=True)
class GameMemento:
    """Memento (GoF): хранит снимок состояния."""
    state: Dict[str, Any]


class Originator:
    """Originator (GoF): умеет сохранять и восстанавливать."""
    def create_memento(self) -> GameMemento: ...
    def restore(self, memento: GameMemento) -> None: ...


class Caretaker:
    """Caretaker (GoF): хранит memento, не лезет внутрь."""
    def __init__(self):
        self._last: GameMemento | None = None

    def save(self, m: GameMemento) -> None:
        self._last = m

    def load(self) -> GameMemento | None:
        return self._last