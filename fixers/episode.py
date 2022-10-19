from Entity import Episode, Show
from Database import db
from Media import file_exists, get_created_time
from . import path

dry_run = False


def fix_episode(episode: Episode, show: Show):
    expected_show = path.get_show_for_file_path(episode.filename)
    # print(f'Episode [{episode.id}] "{episode.filename}" has path: {episode.path_id} and file: {episode.file_id}')
    if not expected_show:
        irregularity(episode, 'Could not get expected show')
        return
    expected_path = db().get_path_for_file_path(episode.get_file_path() + '/')
    if not expected_path:
        irregularity(episode, 'could not get expected path')
        return
    expected_file = db().get_file_in_path(expected_path.id, episode.get_file_name())
    if not expected_file:
        irregularity(episode, f'could not get file (expected file id {episode.file_id})')
        if not file_exists(expected_path, episode.get_file_name()):
            irregularity(episode, f'file does not exist [{episode.file_id}]')
            return
        created_time = get_created_time(expected_path, episode.get_file_name())
        if dry_run:
            print(f'Would create file entry to replace {episode.get_file_name()}')
            return
        new_file_id = db().create_file(expected_path.id, episode.get_file_name(), created_time)
        expected_file = db().get_file_by_id(new_file_id)
        if not expected_file:
            irregularity(episode, f'created replacement file [{new_file_id}] but unable to get it back')
            return
        print(f'Created file {episode.get_file_name()} [{new_file_id}] with created time {created_time}')
    try:
        expected_season = db().get_season(expected_show, episode.season_number)
    except Exception as e:
        irregularity(episode, f'could not get season')
        if dry_run:
            return
        else:
            db().create_season(expected_show, episode.season_number)
            expected_season = db().get_season(expected_show, episode.season_number)
    needs_update = False
    if expected_show != show.id:
        irregularity(episode, f'is on show {show.id} but expected {expected_show}')
        needs_update = True
    if int(expected_path.id) != int(episode.path_id):
        irregularity(episode, f'is on path {episode.path_id} but expected {expected_path.id}')
        needs_update = True
    if int(expected_file.id) != int(episode.file_id):
        irregularity(episode, f'is on file {episode.file_id} but expected {expected_file.id}')
        needs_update = True
    if int(expected_season.id) != int(episode.season_id):
        irregularity(episode, f'is on season id {episode.season_id} but expected {expected_season.id}')
        needs_update = True
    if needs_update:
        desired_episode = Episode(episode.id, episode.filename, expected_file.id, expected_path.id, expected_show,
                                  expected_season.id, episode.season_number, episode.unique_id, episode.rating_id)
        if dry_run:
            print(
                f'Would update episode {desired_episode.id} to have show {desired_episode.show_id}, path {desired_episode.path_id}, file {desired_episode.file_id} and season {desired_episode.season_id}')
        else:
            db().update_episode(desired_episode)


def irregularity(episode: Episode, message: str):
    print(
        f'IRREGULARITY - Episode [{episode.id}] "{episode.filename}" {message}')


def deduplicate_for_show(episodes_for_show: dict[int, list[Episode]]):
    for file_id, episodes in episodes_for_show.items():
        deduplicate_for_file(file_id, episodes)


def deduplicate_for_file(file_id: int, episodes: list[Episode]):
    if len(episodes) == 1:
        return
    path_id = None
    season_id = None
    unique_ids = []
    for episode in episodes:
        if not path_id:
            path_id = episode.path_id
        if not season_id:
            season_id = episode.season_id
        if path_id != episode.path_id:
            irregularity(episodes[0], f'file {file_id} has duplicate episode entries but different path IDs')
            return
        if season_id != episode.season_id:
            irregularity(episodes[0], f'file {file_id} has duplicate episode entries but different season IDs')
            return
        unique_ids.append(episode.unique_id)
    irregularity(episodes[0], f'file {file_id} has duplicate episode entries')
    desired_unique_id = db().get_unique_id_for_type(unique_ids, 'tvdb')
    if not desired_unique_id:
        irregularity(episodes[0], f'unable to work out which episode to dedupe with')
        return
    for episode in episodes:
        if int(episode.unique_id) == int(desired_unique_id):
            continue
        if dry_run:
            print(f'Would remove episode [{episode.id}]')
        else:
            db().remove_episode_by_id(episode.id)
