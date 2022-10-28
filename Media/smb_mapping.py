base_dir = "/home/dezza/src/kodi-tv/mediahen/"
smb_dir = "smb://henrietta.internal.dezzanet.co.uk/media/"


def convert_to_local(smb_path):
    conversions = [
        (smb_dir, base_dir)
    ]
    for conversion in conversions:
        if smb_path.startswith(conversion[0]):
            return smb_path.replace(conversions[0][0], conversions[0][1])


def convert_to_smb(local_path):
    conversions = [
        (base_dir, smb_dir)
    ]
    for conversion in conversions:
        if local_path.startswith(conversion[0]):
            return local_path.replace(conversions[0][0], conversions[0][1])
