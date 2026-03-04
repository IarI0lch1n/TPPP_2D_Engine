from python_engine.engine.prefabs.director import PrefabDirector
from python_engine.engine.prefabs.builders import PlayerBuilder, NPCMerchantBuilder, SlimeEnemyBuilder


class PrefabCatalog:
    """
    Удобная обёртка: выбирает нужный ConcreteBuilder,
    а Director строит Product.
    """
    def __init__(self):
        self.director = PrefabDirector()

    def player(self, x=100, y=260):
        return self.director.construct(PlayerBuilder(), x, y)

    def npc_merchant(self, x=240, y=260):
        return self.director.construct(NPCMerchantBuilder(), x, y)

    def enemy_slime(self, x=360, y=260):
        return self.director.construct(SlimeEnemyBuilder(), x, y)