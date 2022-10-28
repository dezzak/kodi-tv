from os import path

from Entity import Path
from datetime import datetime
from .smb_mapping import convert_to_local


def is_directory(kodi_path: Path):
    local_path = convert_to_local(kodi_path.path)
    return path.isdir(local_path)


def is_link(kodi_path):
    local_path = path.normpath(convert_to_local(kodi_path.path))
    return path.islink(local_path)


def is_present(kodi_path: Path):
    local_path = path.normpath(convert_to_local(kodi_path.path))
    return path.exists(local_path)


def file_exists(kodi_path: Path, filename: str) -> bool:
    local_path = path.normpath(convert_to_local(kodi_path.path) + '/' + filename)
    return path.exists(local_path)


def get_created_time(kodi_path: Path, filename:str) -> str:
    local_path = path.normpath(convert_to_local(kodi_path.path) + '/' + filename)
    ctime = path.getctime(local_path)
    return datetime.utcfromtimestamp(ctime).strftime('%Y-%m-%d %H:%M:%S')
