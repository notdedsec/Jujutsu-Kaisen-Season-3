import base64
from pathlib import Path
from typing import Any

import requests

from project_module.config import config


def upload_to_nekobt(
    torrent_file: Path | str,
    name: str | None = None,
    description: str | Path = '',
    mediainfo: str = '',
    hidden: bool = True,
    anonymous: bool = False,
    batch: bool = False,
    ignore_warnings: bool = False,
    video_type: int = 8,
    video_codec: int = 2,
    level: int = 3,
    audio_langs: str = 'ja',
    fansub_langs: str = 'en,enm',
    api_key: str | None = config.nekobt_api_key,
    group_id: str | None = config.nekobt_group_id,
    group_members: list[dict] = config.nekobt_group_members,
) -> dict[str, Any]:

    torrent_path = Path(torrent_file)

    if not torrent_path.exists():
        raise FileNotFoundError(f'Torrent file not found: {torrent_path}')

    if not api_key:
        raise ValueError('NekoBT API key not provided.')

    if not name:
        name = torrent_path.stem

    if description and Path(description).exists():
        with open(description, 'r', encoding='utf-8') as f:
            description = f.read()

    with open(torrent_path, 'rb') as f:
        torrent_b64 = base64.b64encode(f.read()).decode('utf-8')

    url = 'https://nekobt.to/api/v1/upload'

    payload = {
        'torrent': torrent_b64,
        'title': name,
        'movie': False,
        'category': '1',
        'video_type': str(video_type),
        'video_codec': video_codec,
        'level': str(level),
        'mtl': False,
        'otl': False,
        'hardsub': False,
        'batch': batch,
        'anonymous': anonymous,
        'hidden': hidden,
        'audio_langs': audio_langs,
        'sub_langs': '',
        'fansub_langs': fansub_langs,
        'description': description,
        'mediainfo': mediainfo,
        'secondary_groups': [],
        'ignore_warnings': ignore_warnings,
    }

    if group_id:
        payload['primary_group'] = {
            'id': group_id,
            'members': group_members,
        }

    response = requests.post(
        url,
        json=payload,
        cookies={'ssid': api_key},
    )

    if response.status_code != 200:
        raise Exception(f'Upload failed: {response.text}')

    result = response.json()
    if result.get('error'):
        raise Exception(f'Upload failed: {result.get("message", response.text)}')

    return result
