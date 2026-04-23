from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, DefaultDict, Dict, List, Protocol, Type, TypeVar
from collections import defaultdict


@dataclass(frozen=True)
class Event:
    """Base event type."""
    pass

@dataclass(frozen=True)
class HealthChanged(Event):
    entity_id: int
    hp: int

@dataclass(frozen=True)
class EntitySpawned(Event):
    entity_id: int
    name: str

@dataclass(frozen=True)
class EntityDied(Event):
    entity_id: int
    name: str

TEvent = TypeVar("TEvent", bound=Event)


class Observer(Protocol[TEvent]):
    """Observer interface (GoF)."""
    def on_event(self, event: TEvent) -> None: ...


class Subject:
    """Subject interface (GoF)."""
    def subscribe(self, event_type: Type[TEvent], observer: Observer[TEvent]) -> None: ...
    def unsubscribe(self, event_type: Type[TEvent], observer: Observer[TEvent]) -> None: ...
    def notify(self, event: Event) -> None: ...


class EventBus(Subject):
    """
    ConcreteSubject: EventBus.
    SOLID: не Singleton, а передаётся зависимостью туда, где нужно (DIP).
    """
    def __init__(self):
        self._observers: DefaultDict[Type[Event], List[Observer]] = defaultdict(list)

    def subscribe(self, event_type: Type[TEvent], observer: Observer[TEvent]) -> None:
        if observer not in self._observers[event_type]:
            self._observers[event_type].append(observer)

    def unsubscribe(self, event_type: Type[TEvent], observer: Observer[TEvent]) -> None:
        if observer in self._observers[event_type]:
            self._observers[event_type].remove(observer)

    def notify(self, event: Event) -> None:
        for obs in list(self._observers[type(event)]):
            obs.on_event(event)