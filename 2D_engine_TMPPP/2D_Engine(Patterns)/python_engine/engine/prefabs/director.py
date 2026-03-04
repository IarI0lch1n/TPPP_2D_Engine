from __future__ import annotations
from python_engine.engine.prefabs.builders import EntityBuilder


class PrefabDirector:
    """
    GoF Director: задаёт порядок шагов построения.
    """
    def construct(self, builder: EntityBuilder, x: float, y: float):
        builder.reset()
        builder.build_identity()
        builder.build_transform(x, y)
        builder.build_visual()
        builder.build_stats()
        return builder.get_result()