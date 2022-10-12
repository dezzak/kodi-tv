import fixers.path
from Database import db
from Entity import Show, Path
import Media
from . import remove_path


def fix_show(show: Show):
    paths = db().get_show_paths(show.id)
    remaining_paths = len(paths)
    paths_to_remove = []
    for path in paths:
        is_dir = Media.is_directory(path)
        is_link = Media.is_link(path)
        if not is_dir:
            paths_to_remove.append(path)
            remaining_paths -= 1
            print(f'IRREGULARITY - Path "{path.path}" [{path.id}] is not a directory')
            continue
        if is_link:
            paths_to_remove.append(path)
            remaining_paths -= 1
            print(f'IRREGULARITY - Path "{path.path}" [{path.id}] is a link')
            continue
    if remaining_paths != 1:
        print(f'IRREGULARITY - Show "{show.name}" [{show.id}] has {remaining_paths} good paths')
    for path in paths_to_remove:
        remove_path(path, 1)
    episodes = db().get_episodes_for_show(show.id)
    for episode in episodes:
        expected_show = fixers.path.get_show_for_file_path(episode.filename)
        if not expected_show:
            print(f'Could not get expected show for [{episode.id}] "{episode.filename}"')
            continue
        expected_path = db().get_path_for_file_path(episode.filename.rsplit('/', 1)[0] + '/')
        if not expected_path:
            print(f'Could not get expected path for [{episode.id}] "{episode.filename}"')
            continue
        print(f'Episode [{episode.id}] "{episode.filename}" has path: {episode.path_id} and file: {episode.file_id}')
        if expected_show != show.id:
            print(
                f'IRREGULARITY - Episode [{episode.id}] "{episode.filename}" is on show {show.id} but expected {expected_show}')
        if int(expected_path.id) != int(episode.path_id):
            print(
                f'IRREGULARITY - Episode [{episode.id}] "{episode.filename}" is on path {episode.path_id} but expected {expected_path.id}')
