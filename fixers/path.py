from typing import Optional

import Media
from Entity import Path, File
from Database import db

dry_run = False


def remove_path(path: Path, expected_shows: int = 0):
    linked_show_count = db().count_shows_for_path(path.id)
    if linked_show_count > expected_shows:
        print(f'IRREGULARITY - There are {linked_show_count} shows for path [{path.id}], but we expected {expected_shows}')
        return
    for sub_path in db().get_sub_paths(path.id):
        remove_path(sub_path, 0)
    files_to_remove = db().get_files_for_path(path.id)
    for file in files_to_remove:
        if dry_run:
            print(f'Would remove file "{path.path}{file.filename}" [{file.id}]')
        else:
            print(f'Removing file "{path.path}{file.filename}" [{file.id}]')
        remove_file(file)
    if not dry_run:
        if not Media.is_present(path):
            db().remove_path(path.id)
        else:
            db().mark_path_as_excluded(path.id)
        if linked_show_count > 0:
            db().unlink_path_from_tvshows(path.id)


def remove_file(file: File):
    if not dry_run:
        db().remove_bookmarks_by_file(file.id)
        db().remove_episodes_by_file(file.id)
        db().remove_settings_by_file(file.id)
        db().remove_stacktimes_by_file(file.id)
        db().remove_streamdetails_by_file(file.id)
        db().remove_file(file.id)


def get_show_for_file_path(file_path: str) -> Optional[int]:
    paths = db().get_all_show_paths()
    for path in paths.keys():
        if file_path.startswith(path):
            return paths[path]
    return None


def normalise_paths(paths: list[Path]):
    for path in paths:
        normalise_path(path)


def normalise_path(path: Path):
    if not path.parent_path_id:
        return
    parent = db().get_path(path.parent_path_id)
    if not parent:
        print(f'IRREGULARITY - path [{path.id}] {path.path} which has parent id [{path.parent_path_id}] - parent not found')
        fix_missing_parent_path(path)
        return
    if not path.path.startswith(parent.path):
        print(f'IRREGULARITY - path [{path.id}] {path.path} which has parent id [{path.parent_path_id}] is not aligned ({parent.path})')
        return
    normalise_path(parent)


def fix_missing_parent_path(path: Path):
    parent_str_path = path.path.rsplit('/', 2 if path.path.endswith('/') else 1)[0] + '/'
    found_parent = db().get_path_for_file_path(parent_str_path)
    if found_parent:
        if dry_run:
            print(f'Would update path [{path.id}] to have parent {found_parent.id} ({found_parent.path})')
        else:
            db().update_parent_path(path.id, found_parent.id)
            print(f'Updated path [{path.id}] to have parent {found_parent.id} ({found_parent.path})')
    else:
        print(f'Could not find parent with path {parent_str_path}')
