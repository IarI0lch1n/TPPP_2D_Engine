class World:
    def __init__(self):
        self.entities = []

    def add(self, e):
        self.entities.append(e)

    def remove(self, e):
        if e in self.entities:
            self.entities.remove(e)

    def clear(self):
        self.entities.clear()