from Database import db
from Entity import Show
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