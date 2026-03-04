from python_engine.engine.core.config import GameConfig

def test_singleton():
    a = GameConfig()
    b = GameConfig()
    assert a is b
