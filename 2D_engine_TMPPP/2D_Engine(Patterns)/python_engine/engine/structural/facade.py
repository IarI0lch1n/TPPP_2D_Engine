from __future__ import annotations

import pygame
from python_engine.engine.core.config import GameConfig
from python_engine.engine.ecs.world import World
from python_engine.engine.prefabs.catalog import PrefabCatalog
from python_engine.engine.ui.factory import DarkUIFactory, LightUIFactory
from python_engine.engine.ui.screens import MenuScreen
from python_engine.engine.structural.resource_hub import ResourceHub


class EngineFacade:
    def __init__(self):
        self.cfg = GameConfig()
        self.world = World()
        self.prefabs = PrefabCatalog()
        self.resources = ResourceHub()  

    def make_ui_factory(self):
        theme = self.cfg.get("ui_theme", "dark")
        return DarkUIFactory() if theme == "dark" else LightUIFactory()

    def build_menu_screen(self) -> MenuScreen:
        theme = self.cfg.get("ui_theme", "dark")
        is_dark = (theme == "dark")
        return MenuScreen(self.make_ui_factory(), self.world, self.prefabs, is_dark)

    def toggle_theme(self):
        if self.cfg.get("ui_theme") == "dark":
            self.cfg.set("ui_theme", "light")
        else:
            self.cfg.set("ui_theme", "dark")

    def clear_world(self):
        self.world.clear()