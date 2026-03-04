class GameConfig:
    """
    Singleton: единый конфиг движка.
    """
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if GameConfig._initialized:
            return

        self.settings = {
            "resolution": (900, 560),
            "ui_theme": "dark",  # dark | light
        }
        GameConfig._initialized = True

    def get(self, key, default=None):
        return self.settings.get(key, default)

    def set(self, key, value):
        self.settings[key] = value