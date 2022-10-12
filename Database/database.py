import sqlite3

from Entity import Show, Path, File


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
        for row in cur.execute("SELECT p.idPath, p.strPath, p.noUpdate, p.exclude FROM path p INNER JOIN tvshowlinkpath t ON p.idPath = t.idPath WHERE t.idShow = :show_id", {"show_id": show_id}):
            result.append(Path(row[0], row[1], row[2], row[3]))
        return result

    def get_files_for_path(self, path_id: int) -> list[File]:
        cur = self.con.cursor()
        result = []
        for row in cur.execute("SELECT idFile, strFilename FROM files WHERE idPath = :path", {"path": path_id}):
            result.append(File(row[0], row[1]))
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


def db() -> Database:
    if Database.instance:
        return Database.instance
    return Database()
