from python_engine.engine.gameplay.prototypes import REGISTRY


class WaveSpawner:
    def spawn_wave(self, ids: list[str]):
        return [REGISTRY.clone(i) for i in ids]