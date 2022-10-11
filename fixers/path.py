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
        if not Media.is_directory(path):
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
