import pygame

from python_engine.engine.core.config import GameConfig
from python_engine.engine.ecs.world import World
from python_engine.engine.prefabs.catalog import PrefabCatalog
from python_engine.engine.ui.factory import DarkUIFactory, LightUIFactory
from python_engine.engine.ui.screens import MenuScreen


def main():
    pygame.init()

    cfg = GameConfig()
    screen = pygame.display.set_mode(cfg.get("resolution", (900, 560)))
    pygame.display.set_caption("2D Engine (UI Patterns - GoF)")
    clock = pygame.time.Clock()

    world = World()
    prefabs = PrefabCatalog()

    theme = cfg.get("ui_theme", "dark")
    factory = DarkUIFactory() if theme == "dark" else LightUIFactory()
    is_dark = (theme == "dark")

    screen_obj = MenuScreen(factory, world, prefabs, is_dark)

    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                # переключение темы = смена ConcreteFactory (Abstract Factory)
                if cfg.get("ui_theme") == "dark":
                    cfg.set("ui_theme", "light")
                    factory = LightUIFactory()
                    is_dark = False
                else:
                    cfg.set("ui_theme", "dark")
                    factory = DarkUIFactory()
                    is_dark = True

                screen_obj = MenuScreen(factory, world, prefabs, is_dark)

            screen_obj.handle_event(event)

        screen_obj.update(dt)

        bg = (12, 12, 14) if is_dark else (240, 240, 240)
        screen.fill(bg)

        screen_obj.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()