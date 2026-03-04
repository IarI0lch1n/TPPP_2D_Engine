from python_engine.engine.ecs.world import World
from python_engine.engine.prefabs.catalog import PrefabCatalog
from python_engine.engine.gameplay.waves import WaveSpawner


def main():
    world = World()
    prefabs = PrefabCatalog()

    prefabs.player().spawn(world)
    prefabs.npc_merchant().spawn(world)

    wave = WaveSpawner().spawn_wave(["slime", "treant"])

    print("World:")
    for e in world.entities:
        print(" -", e)

    print("\nWave (Prototype):")
    for w in wave:
        print(" -", w)


if __name__ == "__main__":
    main()