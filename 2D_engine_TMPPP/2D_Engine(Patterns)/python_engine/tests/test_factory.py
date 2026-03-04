from python_engine.engine.entities.creators import PlayerCreator

def test_factory():
    p = PlayerCreator().spawn(1, 2)
    assert p.name == "Player"
    assert p.x == 1 and p.y == 2
