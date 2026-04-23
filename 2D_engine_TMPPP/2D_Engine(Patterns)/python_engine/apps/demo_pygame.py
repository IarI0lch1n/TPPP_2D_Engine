import math
import pygame

from python_engine.engine.structural.facade import EngineFacade

from python_engine.engine.behavioral.observer import EventBus, HealthChanged, EntitySpawned, EntityDied
from python_engine.engine.behavioral.command import (
    InputInvoker,
    MoveUpCommand, MoveDownCommand, MoveLeftCommand, MoveRightCommand,
    StopUpCommand, StopDownCommand, StopLeftCommand, StopRightCommand,
    FaceUpCommand, FaceDownCommand, FaceLeftCommand, FaceRightCommand,
    AttackCommand, ClearAttackCommand
)
from python_engine.engine.behavioral.memento import Caretaker
from python_engine.engine.behavioral.strategy import AggressiveStrategy, PatrolStrategy, NeutralStrategy

from python_engine.engine.gameplay.actors import InputContext, PlayerController, WorldContext
from python_engine.engine.gameplay.combat import CombatSystem
from python_engine.engine.gameplay.waves_manager import WaveManager
from python_engine.engine.gameplay.session import GameSession


def main():
    pygame.init()

    engine = EngineFacade()
    screen = pygame.display.set_mode(engine.cfg.get("resolution", (900, 560)))
    pygame.display.set_caption("2D Engine (GoF Behavioral: State+Strategy+Observer+Command+Memento)")
    clock = pygame.time.Clock()

    menu = engine.build_menu_screen()
    menu.world = engine.world
    menu.prefabs = engine.prefabs

    
    bus = EventBus()

    class DebugObserver:
        def on_event(self, event):
            print("[EVENT]", event)

    dbg = DebugObserver()
    bus.subscribe(EntitySpawned, dbg)
    bus.subscribe(HealthChanged, dbg)
    bus.subscribe(EntityDied, dbg)

    class GameOverObserver:
        def __init__(self):
            self.is_over = False

        def on_event(self, e):
            if e.name == "Player":
                self.is_over = True

    game_over_observer = GameOverObserver()
    bus.subscribe(EntityDied, game_over_observer)

    input_ctx = InputContext()
    invoker = InputInvoker()

    invoker.bind_press(pygame.K_w, MoveUpCommand(input_ctx))
    invoker.bind_press(pygame.K_w, FaceUpCommand(input_ctx))
    invoker.bind_release(pygame.K_w, StopUpCommand(input_ctx))

    invoker.bind_press(pygame.K_s, MoveDownCommand(input_ctx))
    invoker.bind_press(pygame.K_s, FaceDownCommand(input_ctx))
    invoker.bind_release(pygame.K_s, StopDownCommand(input_ctx))

    invoker.bind_press(pygame.K_a, MoveLeftCommand(input_ctx))
    invoker.bind_press(pygame.K_a, FaceLeftCommand(input_ctx))
    invoker.bind_release(pygame.K_a, StopLeftCommand(input_ctx))

    invoker.bind_press(pygame.K_d, MoveRightCommand(input_ctx))
    invoker.bind_press(pygame.K_d, FaceRightCommand(input_ctx))
    invoker.bind_release(pygame.K_d, StopRightCommand(input_ctx))

    invoker.bind_press(pygame.K_SPACE, AttackCommand(input_ctx))
    invoker.bind_release(pygame.K_SPACE, ClearAttackCommand(input_ctx))

    world_ctx = WorldContext()

    player_entity = engine.prefabs.player(40, 40)
    engine.world.add(player_entity)

    player = PlayerController(player_entity, input_ctx, bus)
    world_ctx.player = player

    caretaker = Caretaker()

    combat = CombatSystem()
    waves = WaveManager(engine, bus, world_ctx)

    session = GameSession(engine, bus, world_ctx, player, waves)

    game_over = False

    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                engine.toggle_theme()
                menu = engine.build_menu_screen()
                menu.world = engine.world
                menu.prefabs = engine.prefabs

            if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                for e in world_ctx.enemies:
                    e.set_strategy(NeutralStrategy())
                print("[STRATEGY] All -> Neutral")

            if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                for e in world_ctx.enemies:
                    e.set_strategy(PatrolStrategy(left=120, right=240))
                print("[STRATEGY] All -> Patrol")

            if event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                for e in world_ctx.enemies:
                    e.set_strategy(AggressiveStrategy())
                print("[STRATEGY] All -> Aggressive")

            if event.type == pygame.KEYDOWN and event.key == pygame.K_F5:
                caretaker.save(session.create_memento())
                print("[MEMENTO] FULL Saved")

            if event.type == pygame.KEYDOWN and event.key == pygame.K_F9:
                m = caretaker.load()
                if m:
                    session.restore(m)
                    print("[MEMENTO] FULL Restored")

            if not game_over:
                if event.type == pygame.KEYDOWN:
                    invoker.handle_press(event.key)
                if event.type == pygame.KEYUP:
                    invoker.handle_release(event.key)

            menu.handle_event(event)

        if game_over_observer.is_over:
            game_over = True

        if not game_over:
            menu.update(dt)

            player.update(dt)

            waves.update(dt)

            for e in world_ctx.enemies:
                e.update(world_ctx, dt)

            combat.update(world_ctx, dt)

            world_ctx.enemies = [e for e in world_ctx.enemies if e.hp() > 0]
            engine.world.entities = [
                ent for ent in engine.world.entities
                if ("Player" in ent.name) or (int(ent.components.get("hp", 1)) > 0)
            ]
        else:
            engine.world.entities = [ent for ent in engine.world.entities if "Player" not in ent.name]

        bg = (12, 12, 14) if engine.cfg.get("ui_theme") == "dark" else (240, 240, 240)
        screen.fill(bg)

        menu.draw(screen)

        def draw_entity(ent, color):
            x = int(520 + ent.x)
            y = int(200 + ent.y)
            pygame.draw.rect(screen, color, pygame.Rect(x, y, 14, 14), border_radius=4)

        for ent in engine.world.entities:
            if "Enemy:" in ent.name:
                draw_entity(ent, (110, 220, 140))

        if not game_over:
            draw_entity(player_entity, (210, 90, 90))

            attack_range = int(getattr(player, "attack_range", 48.0))
            fov_deg = float(getattr(player, "attack_fov_deg", 90.0))

            fx, fy = input_ctx.facing
            if fx == 0 and fy == 0:
                fx, fy = 0, 1

            cx = int(520 + player_entity.x) + 7
            cy = int(200 + player_entity.y) + 7

            base_angle = math.atan2(fy, fx)
            half = math.radians(fov_deg) / 2.0

            steps = 22
            points = [(cx, cy)]
            for i in range(steps + 1):
                a = base_angle - half + (2 * half) * (i / steps)
                px = cx + int(math.cos(a) * attack_range)
                py = cy + int(math.sin(a) * attack_range)
                points.append((px, py))

            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            cone_fill = (255, 200, 80, 60)
            cone_border = (255, 200, 80, 130)
            pygame.draw.polygon(overlay, cone_fill, points)
            pygame.draw.lines(overlay, cone_border, False, points, 2)
            screen.blit(overlay, (0, 0))

        if game_over:
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))

            font = pygame.font.SysFont("Consolas", 56, bold=True)
            text = font.render("ИГРА ОКОНЧЕНА", True, (255, 80, 80))
            x = screen.get_width() // 2 - text.get_width() // 2
            y = screen.get_height() // 2 - text.get_height() // 2
            screen.blit(text, (x, y))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()