class ConfigResponse:
    def __init__(self, dictionary):
        self._dict = dictionary

    def __getattr__(self, key):
        if key in self._dict:
            return self._dict[key]
        else:
            raise AttributeError(f"Config Response object has no attribute '{key}'")
        
    def all(self):
        return self._dict