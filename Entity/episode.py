class Episode:
    def __init__(self, episode_id: int, filename: str, file_id: int, path_id: int, show_id: int, season_id: int,
                 season_number: int, unique_id: int, rating_id: int):
        self.id = episode_id
        self.filename = filename
        self.file_id = file_id
        self.path_id = path_id
        self.show_id = show_id
        self.season_id = season_id
        self.season_number = season_number
        self.unique_id = unique_id
        self.rating_id = rating_id
