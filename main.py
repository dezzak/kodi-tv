#!/usr/bin/env python3

import Database
import Media
from Entity import Show
import fixers

db = Database.db()


def fix():
    shows = db.get_shows(350)
    for show in shows:
        fix_show(show)


def fix_show(show: Show):
    # print(f'Checking [{show.id}] {show.name}')
    paths = db.get_show_paths(show.id)
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
        fixers.remove_path(path, 1)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    fix()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
