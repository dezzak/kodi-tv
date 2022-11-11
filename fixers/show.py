import fixers
from Database import db
from Entity import Show
import Media
from . import remove_path, fix_episode, normalise_paths
from .unwatched import fix_unwatched_for_show


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
        fix_episode(episode, show)
    # Now get the episodes again to find duplicates
    episodes = db().get_episodes_for_show(show.id)
    episodes_by_file = {}
    for episode in episodes:
        if episode.file_id in episodes_by_file:
            episodes_by_file[episode.file_id].append(episode)
        else:
            episodes_by_file[episode.file_id] = [episode]
    fixers.deduplicate_for_show(episodes_by_file)
    fix_unwatched_for_show(show)
    # Now try the paths
    episode_paths = db().get_paths_of_episodes_for_show(show.id)
    normalise_paths(episode_paths)
