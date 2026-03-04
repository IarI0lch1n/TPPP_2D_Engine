class Entity:
    def __init__(self, name: str):
        self.name = name
        self.x = 0.0
        self.y = 0.0
        self.components = {}

    def __repr__(self):
        return f"Entity({self.name}, pos=({self.x},{self.y}), comps={list(self.components)})"