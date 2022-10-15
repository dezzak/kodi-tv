from Entity import Episode, Show
from Database import db
from . import path

dry_run = True


def fix_episode(episode: Episode, show: Show):
    expected_show = path.get_show_for_file_path(episode.filename)
    # print(f'Episode [{episode.id}] "{episode.filename}" has path: {episode.path_id} and file: {episode.file_id}')
    if not expected_show:
        irregularity(episode, 'Could not get expected show')
        return
    expected_path = db().get_path_for_file_path(episode.filename.rsplit('/', 1)[0] + '/')
    if not expected_path:
        irregularity(episode, 'could not get expected path')
        return
    expected_file = db().get_file_in_path(expected_path.id, episode.filename.rsplit('/', 1)[1])
    if not expected_file:
        irregularity(episode, f'could not get file (expected file id {episode.file_id})')
        return
    expected_season = db().get_season(expected_show, episode.season_number)
    if not expected_season:
        irregularity(episode, f'could not get season')
        return
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
                                  expected_season.id, episode.season_number)
        if dry_run:
            print(
                f'Would update episode {desired_episode.id} to have show {desired_episode.show_id}, path {desired_episode.path_id}, file {desired_episode.file_id} and season {desired_episode.season_id}')
        else:
            db().update_episode(desired_episode)


def irregularity(episode: Episode, message: str):
    print(
        f'IRREGULARITY - Episode [{episode.id}] "{episode.filename}" {message}')
