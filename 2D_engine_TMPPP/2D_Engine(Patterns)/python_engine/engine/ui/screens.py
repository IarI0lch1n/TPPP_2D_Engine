import pygame

from python_engine.engine.ui.factory import AbstractUIFactory
from python_engine.engine.ui.creators import ButtonCreator, LabelCreator
from python_engine.engine.prefabs.catalog import PrefabCatalog
from python_engine.engine.ecs.world import World


class MenuScreen:
    """
    Client в терминах GoF:
    - получает AbstractUIFactory
    - создаёт UI через Creator’ы (Factory Method)
    - сущности строит через Director+Builder (PrefabCatalog)
    """

    def __init__(self, ui_factory: AbstractUIFactory, world: World, prefabs: PrefabCatalog, is_dark: bool):
        self.factory = ui_factory
        self.world = world
        self.prefabs = prefabs
        self.is_dark = is_dark

        self.root = None
        self.status = None
        self._build_ui()

    def _build_ui(self):
        self.root = self.factory.create_panel(20, 20, 860, 520)

        LabelCreator(40, 40, "UI Patterns Demo (Abstract Factory + Factory Method)", 24).render(self.root, self.factory)
        LabelCreator(40, 80, "Entities are created via Builder (Director + ConcreteBuilder).", 20).render(self.root, self.factory)

        self.status = self.factory.create_label(40, 120, "World entities: 0", 20)
        self.root.add(self.status)

        def refresh():
            self.status.set_text(f"World entities: {len(self.world.entities)}")

        def spawn_player():
            e = self.prefabs.player(120, 260)
            self.world.add(e)
            refresh()

        def spawn_npc():
            e = self.prefabs.npc_merchant(240, 260)
            self.world.add(e)
            refresh()

        def spawn_enemy():
            e = self.prefabs.enemy_slime(200, 220)
            self.world.add(e)
            refresh()

        def clear_world():
            self.world.clear()
            refresh()

        ButtonCreator(40, 170, 240, 52, "Spawn Player", spawn_player).render(self.root, self.factory)
        ButtonCreator(40, 235, 240, 52, "Spawn NPC", spawn_npc).render(self.root, self.factory)
        ButtonCreator(40, 300, 240, 52, "Spawn Enemy", spawn_enemy).render(self.root, self.factory)
        ButtonCreator(40, 365, 240, 52, "Clear World", clear_world).render(self.root, self.factory)

        refresh()

    def handle_event(self, event: pygame.event.Event):
        self.root.handle_event(event)

    def update(self, dt: float):
        self.root.update(dt)

    def draw(self, surface: pygame.Surface):
        self.root.draw(surface)

        # рисуем сущности (простая "игровая сцена")
        name_color = (220, 220, 220) if self.is_dark else (30, 30, 30)
        font = pygame.font.SysFont("Consolas", 14)

        for e in self.world.entities:
            color = e.components.get("color", (200, 120, 120))
            x = int(520 + e.x)
            y = int(200 + e.y)
            pygame.draw.rect(surface, color, pygame.Rect(x, y, 14, 14), border_radius=4)

            txt = font.render(e.name, True, name_color)
            surface.blit(txt, (x + 18, y - 2))