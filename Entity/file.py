class File:
    def __init__(self, file_id: int, filename: str, path_id: int, play_count: int):
        self.id = file_id
        self.filename = filename
        self.path_id = path_id
        self.playCount = play_count
