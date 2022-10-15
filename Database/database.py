import sqlite3
from typing import Optional

from Entity import Show, Path, File, Episode, Season
from functools import lru_cache


def get_connection():
    con = sqlite3.connect("remote/userdata/Database/MyVideos116.db")
    return con


class Database:
    instance = None

    def __init__(self):
        self.con = get_connection()
        Database.instance = self

    def get_shows(self, limit: int = 10) -> list[Show]:
        cur = self.con.cursor()
        result = []
        for row in cur.execute("SELECT idShow, c00 FROM tvshow LIMIT :limit", {"limit": limit}):
            result.append(Show(row[0], row[1]))
        return result

    def get_show_paths(self, show_id: int) -> list[Path]:
        cur = self.con.cursor()
        result = []
        for row in cur.execute(
                "SELECT p.idPath, p.strPath, p.noUpdate, p.exclude FROM path p INNER JOIN tvshowlinkpath t ON p.idPath = t.idPath WHERE t.idShow = :show_id",
                {"show_id": show_id}):
            result.append(Path(row[0], row[1], row[2], row[3]))
        return result

    def get_files_for_path(self, path_id: int) -> list[File]:
        cur = self.con.cursor()
        result = []
        for row in cur.execute("SELECT idFile, strFilename, idPath FROM files WHERE idPath = :path", {"path": path_id}):
            result.append(File(row[0], row[1], row[2]))
        return result

    def count_shows_for_path(self, path_id: int) -> int:
        cur = self.con.cursor()
        cur.execute("SELECT count(idShow) FROM tvshowlinkpath WHERE idPath = :path", {"path": path_id})
        return cur.fetchone()[0]

    def get_sub_paths(self, path_id: int) -> list[Path]:
        cur = self.con.cursor()
        result = []
        for row in cur.execute(
                "SELECT idPath, strPath, noUpdate, exclude FROM path WHERE idParentPath = :path_id",
                {"path_id": path_id}):
            result.append(Path(row[0], row[1], row[2], row[3]))
        return result

    def get_path(self, path_id: int) -> Path:
        cur = self.con.cursor()
        cur.execute(
            "SELECT idPath, strPath, noUpdate, exclude FROM path WHERE idPath = :path_id",
            {"path_id": path_id})
        row = cur.fetchone()
        return Path(row[0], row[1], row[2], row[3])

    def remove_bookmarks_by_file(self, file_id: int):
        cur = self.con.cursor()
        cur.execute("DELETE FROM bookmark WHERE idFile = :file_id", {"file_id": file_id})
        self.con.commit()
        print(f'Removed bookmark for file [{file_id}]')

    def remove_settings_by_file(self, file_id: int):
        cur = self.con.cursor()
        cur.execute("DELETE FROM settings WHERE idFile = :file_id", {"file_id": file_id})
        self.con.commit()
        print(f'Removed settings for file [{file_id}]')

    def remove_episodes_by_file(self, file_id: int):
        cur = self.con.cursor()
        cur.execute("DELETE FROM episode WHERE idFile = :file_id", {"file_id": file_id})
        self.con.commit()
        print(f'Removed episodes for file [{file_id}]')

    def remove_stacktimes_by_file(self, file_id: int):
        cur = self.con.cursor()
        cur.execute("DELETE FROM stacktimes WHERE idFile = :file_id", {"file_id": file_id})
        self.con.commit()
        print(f'Removed stacktimes for file [{file_id}]')

    def remove_streamdetails_by_file(self, file_id: int):
        cur = self.con.cursor()
        cur.execute("DELETE FROM streamdetails WHERE idFile = :file_id", {"file_id": file_id})
        self.con.commit()
        print(f'Removed streamdetails for file [{file_id}]')

    def remove_file(self, file_id: int):
        cur = self.con.cursor()
        cur.execute("DELETE FROM files WHERE idFile = :file_id", {"file_id": file_id})
        self.con.commit()
        print(f'Removed file [{file_id}]')

    def remove_path(self, path_id: int):
        cur = self.con.cursor()
        cur.execute("DELETE FROM path WHERE idPath = :path_id", {"path_id": path_id})
        self.con.commit()
        print(f'Removed path [{path_id}]')

    def mark_path_as_excluded(self, path_id: int):
        cur = self.con.cursor()
        cur.execute("UPDATE path SET noUpdate=0, exclude=1 WHERE idPath = :path_id", {"path_id": path_id})
        self.con.commit()
        print(f'Marked path [{path_id}] as excluded from library updates')

    def unlink_path_from_tvshows(self, path_id: int):
        cur = self.con.cursor()
        cur.execute("DELETE FROM tvshowlinkpath WHERE idPath = :path_id", {"path_id": path_id})
        self.con.commit()
        print(f'Unlinked path [{path_id}] from all shows')

    @lru_cache
    def get_all_show_paths(self) -> dict:
        cur = self.con.cursor()
        result = []
        for row in cur.execute(
                "SELECT p.strPath, t.idShow FROM path p INNER JOIN tvshowlinkpath t on p.idPath = t.idPath"):
            result.append(row)
        return dict(result)

    def get_episodes_for_show(self, show_id: int) -> list[Episode]:
        cur = self.con.cursor()
        result = []
        for row in cur.execute(
                "SELECT idEpisode, c18, idFile, c19, idShow, idSeason, c12, c20, c03 FROM episode WHERE idShow = :show_id",
                {"show_id": show_id}):
            result.append(Episode(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))
        return result

    @lru_cache
    def get_path_for_file_path(self, file_path: str) -> Optional[Path]:
        cur = self.con.cursor()
        cur.execute(
            "SELECT idPath, strPath, noUpdate, exclude FROM path WHERE strPath = :file_path",
            {"file_path": file_path})
        row = cur.fetchone()
        if not row:
            return None
        return Path(row[0], row[1], row[2], row[3])

    def get_file_by_id(self, file_id: int) -> Optional[File]:
        cur = self.con.cursor()
        cur.execute("SELECT idFile, strFilename, idPath FROM files WHERE idFile = :file_id", {"file_id": file_id})
        row = cur.fetchone()
        if not row:
            return None
        return File(row[0], row[1], row[2])

    def get_file_in_path(self, path_id: int, file_name: str) -> Optional[File]:
        cur = self.con.cursor()
        cur.execute(
            "SELECT idFile, strFilename, idPath FROM files WHERE idPath = :path_id AND strFilename = :file_name",
            {"path_id": path_id, "file_name": file_name})
        row = cur.fetchone()
        if not row:
            return None
        return File(row[0], row[1], row[2])

    def update_episode(self, episode: Episode):
        cur = self.con.cursor()
        cur.execute(
            "UPDATE episode SET idShow = :show_id, c19 = :path_id, idFile = :file_id, idSeason = :season_id WHERE idEpisode = :episode_id",
            {"episode_id": episode.id, "path_id": episode.path_id, "file_id": episode.file_id,
             "show_id": episode.show_id, "season_id": episode.season_id})
        self.con.commit()
        print(f'Updated episode [{episode.id}]')

    @lru_cache
    def get_season(self, show_id: int, season_number: int) -> Optional[Season]:
        cur = self.con.cursor()
        cur.execute(
            "SELECT idSeason, idShow, season FROM seasons WHERE idShow = :show_id AND season = :season_number",
            {"show_id": show_id, "season_number": season_number})
        row = cur.fetchone()
        if not row:
            return None
        return Season(row[0], row[1], row[2])

    def get_unique_id_for_type(self, ids_to_search: list[int], desired_type: str) -> int:
        params: list = ids_to_search.copy()
        params.append(desired_type)
        cur = self.con.cursor()
        cur.execute("SELECT uniqueid_id FROM uniqueid WHERE uniqueid_id IN (%s) AND type = ?" % ','.join(
            '?' * (len(ids_to_search))),
                    params)
        row = cur.fetchone()
        return row[0]

    def remove_episode_by_id(self, episode_id: int):
        cur = self.con.cursor()
        cur.execute("DELETE FROM episode WHERE idEpisode = :id", {"id": episode_id})
        self.con.commit()
        print(f'Removed episode [{episode_id}]')


def db() -> Database:
    if Database.instance:
        return Database.instance
    return Database()
