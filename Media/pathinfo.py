from os import path

from Entity import Path


def convert_to_local(smb_path):
    conversions = [
        ("smb://henrietta.internal.dezzanet.co.uk/media/", "/home/dezza/src/kodi-tv/mediahen/")
    ]
    for conversion in conversions:
        if smb_path.startswith(conversion[0]):
            return smb_path.replace(conversions[0][0], conversions[0][1])


def is_directory(kodi_path: Path):
    local_path = convert_to_local(kodi_path.path)
    return path.isdir(local_path)


def is_link(kodi_path):
    local_path = path.normpath(convert_to_local(kodi_path.path))
    return path.islink(local_path)


def is_present(kodi_path: Path):
    local_path = path.normpath(convert_to_local(kodi_path.path))
    return path.exists(local_path)
