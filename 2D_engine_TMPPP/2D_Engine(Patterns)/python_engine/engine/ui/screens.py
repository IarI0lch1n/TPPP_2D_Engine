import pygame

from python_engine.engine.ui.factory import AbstractUIFactory
from python_engine.engine.ui.creators import ButtonCreator, LabelCreator
from python_engine.engine.prefabs.catalog import PrefabCatalog
from python_engine.engine.ecs.world import World

from python_engine.engine.structural.decorator import BorderDecorator, TooltipDecorator


class MenuScreen:

    def __init__(self, ui_factory: AbstractUIFactory, world: World, prefabs: PrefabCatalog, is_dark: bool):
        self.factory = ui_factory
        self.world = world
        self.prefabs = prefabs
        self.is_dark = is_dark

        self.root = None
        self.status = None

        self.tooltip_font = pygame.font.SysFont("Consolas", 14)

        self._build_ui()


    def _build_ui(self):
        self.root = self.factory.create_panel(20, 20, 860, 520)

        LabelCreator(40, 40, "UI Patterns Demo (Abstract Factory + Factory Method)", 24).render(self.root, self.factory)
        LabelCreator(40, 80, "Entities are created via Builder (Director + ConcreteBuilder).", 20).render(self.root, self.factory)

        self.status = self.factory.create_label(40, 120, "World entities: 0", 20)
        self.root.add(self.status)

        def refresh():
            self.status.set_text(f"World entities: {len(self.world.entities)}")

    def handle_event(self, event: pygame.event.Event):
        self.root.handle_event(event)

    def update(self, dt: float):
        self.root.update(dt)
        if self.status:
            self.status.set_text(f"World entities: {len(self.world.entities)}")

    def draw(self, surface: pygame.Surface):
        self.root.draw(surface)

        name_color = (220, 220, 220) if self.is_dark else (30, 30, 30)
        font = pygame.font.SysFont("Consolas", 14)

        for e in self.world.entities:
            color = e.components.get("color", (200, 120, 120))
            x = int(520 + e.x)  
            y = int(200 + e.y)   
            pygame.draw.rect(surface, color, pygame.Rect(x, y, 14, 14), border_radius=4)

            txt = font.render(e.name, True, name_color)
            surface.blit(txt, (x + 18, y - 2))