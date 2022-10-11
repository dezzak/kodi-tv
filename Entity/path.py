class Path:
    def __init__(self, path_id: int, path: str, no_update: bool, exclude: bool):
        self.id = path_id
        self.path = path
        self.no_update = no_update
        self.exclude = exclude
