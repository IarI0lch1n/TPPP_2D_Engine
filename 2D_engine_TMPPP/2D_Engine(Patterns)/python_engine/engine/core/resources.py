class ResourceManager:
    """
    Singleton: кэш ресурсов (текстуры/шрифты и т.п.)
    В демо мы кэшируем просто "строки", чтобы показать принцип.
    """
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if ResourceManager._initialized:
            return
        self._textures = {}
        ResourceManager._initialized = True

    def texture(self, path: str):
        if path not in self._textures:
            self._textures[path] = f"<Texture:{path}>"
        return self._textures[path] 