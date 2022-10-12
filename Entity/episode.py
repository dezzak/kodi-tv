class Episode:
    def __init__(self, episode_id: int, filename: str, file_id: int, path_id: int, show_id: int):
        self.id = episode_id
        self.filename = filename
        self.file_id = file_id
        self.path_id = path_id
        self.show_id = show_id
