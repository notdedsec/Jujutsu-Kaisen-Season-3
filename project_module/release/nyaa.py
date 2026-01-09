import json
from enum import Enum
from pathlib import Path
from typing import Any, Dict

import requests

from project_module.config import config


class NyaaCategory(str, Enum):
    ANIME_AMV = "1_1"
    ANIME_ENGLISH = "1_2"
    ANIME_NON_ENGLISH = "1_3"
    ANIME_RAW = "1_4"

    AUDIO_LOSSLESS = "2_1"
    AUDIO_LOSSY = "2_2"

    LITERATURE_ENGLISH = "3_1"
    LITERATURE_NON_ENGLISH = "3_2"
    LITERATURE_RAW = "3_3"

    LIVE_ACTION_ENGLISH = "4_1"
    LIVE_ACTION_IDOL = "4_2"
    LIVE_ACTION_NON_ENGLISH = "4_3"
    LIVE_ACTION_RAW = "4_4"

    PICTURES_GRAPHICS = "5_1"
    PICTURES_PHOTOS = "5_2"

    SOFTWARE_APPLICATIONS = "6_1"
    SOFTWARE_GAMES = "6_2"


def upload_to_nyaa(
    torrent_file: Path | str,
    username: str | None = config.nyaa_username,
    password: str | None = config.nyaa_password,
    name: str | None = None,
    category: NyaaCategory = NyaaCategory.ANIME_ENGLISH,
    information: str = '',
    description: str | Path = '',
    anonymous: bool = False,
    hidden: bool = True,
    complete: bool = False,
    remake: bool = False,
    trusted: bool = True,
) -> Dict[str, Any]:

    torrent_path = Path(torrent_file)

    if not torrent_path.exists():
        raise FileNotFoundError(f'Torrent file not found: {torrent_path}')

    if not name:
        name = torrent_path.stem

    if not username or not password:
        raise ValueError('Nyaa username and password not provided.')

    if description and Path(description).exists():
        with open(description, 'r', encoding='utf-8') as f:
            description = f.read()

    url = 'https://nyaa.si/api/upload'

    fields = {
        'name': name,
        'category': category.value,
        'information': information,
        'description': description,
        'anonymous': anonymous,
        'hidden': hidden,
        'complete': complete,
        'remake': remake,
        'trusted': trusted,
    }

    with open(torrent_path, 'rb') as f:
        files = {
            'torrent_data': (None, json.dumps(fields)),
            'torrent': (torrent_path.name, f)
        }

        response = requests.post(
            url,
            files=files,
            auth=(username, password)
        )

    if response.status_code != 200:
        raise Exception(f'Upload failed: {response.text}')

    return response.json()
