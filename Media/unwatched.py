import os
from functools import lru_cache

from .smb_mapping import base_dir, convert_to_smb


@lru_cache
def get_all_unwatched() -> list[str]:
    unwatched_path = get_unwatched_path()
    files = os.listdir(unwatched_path)
    unwatched_items = list()
    for file in files:
        file_path = unwatched_path + '/' + file
        is_link = os.path.islink(file_path)
        if is_link:
            real_path = os.path.realpath(file_path)
            smb_path = convert_to_smb(real_path)
            unwatched_items.append(smb_path)
    return unwatched_items


def get_unwatched_path():
    return base_dir + "unwatched"
