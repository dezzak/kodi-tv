from Database import db
from Entity import Show, Path, File
from Media.unwatched import get_all_unwatched

dry_run = True


def fix_unwatched_for_show(show: Show):
    paths = db().get_show_paths(show.id)
    for path in paths:
        fix_unwatched_for_path(path)


def fix_unwatched_for_path(path: Path):
    sub_paths = db().get_sub_paths(path.id)
    for sub_path in sub_paths:
        fix_unwatched_for_path(sub_path)
    files = db().get_files_for_path(path.id)
    for file in files:
        fix_unwatched_for_file(file, path)


def fix_unwatched_for_file(file: File, path: Path):
    full_path = path.path + file.filename
    unwatched_files = get_all_unwatched()
    if full_path not in unwatched_files:
        mark_file_as_watched(file)


def mark_file_as_watched(file: File):
    if dry_run:
        print(f'Would mark file [{file.id}] ({file.filename}) as watched')
        return
