import pygame
from python_engine.engine.structural.facade import EngineFacade


def main():
    pygame.init()

    engine = EngineFacade()
    screen = pygame.display.set_mode(engine.cfg.get("resolution", (900, 560)))
    pygame.display.set_caption("2D Engine (GoF Structural + Creational)")
    clock = pygame.time.Clock()

    menu = engine.build_menu_screen()

    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                engine.toggle_theme()
                menu = engine.build_menu_screen()

            menu.handle_event(event)

        menu.update(dt)

        bg = (12, 12, 14) if engine.cfg.get("ui_theme") == "dark" else (240, 240, 240)
        screen.fill(bg)
        menu.draw(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()