from pathlib import Path

import dotenv
from pydantic_settings import BaseSettings

dotenv.load_dotenv()


class SetupConfig(BaseSettings):
    group_tag: str = 'Kaizoku'
    show_name: str = 'Jujutsu Kaisen'
    shorthand: str = 'jjk'

    information: str = 'https://github.com/notdedsec/Jujutsu-Kaisen-Season-3'
    description: Path = Path('description.vm')

    nyaa_username: str | None = None
    nyaa_password: str | None = None

    nekobt_api_key: str | None = None

    nekobt_group_id: str = '8438338633525'
    nekobt_group_members: list[dict] = [
        {'id': '8437619399442', 'role': 'Encoding, Editing, Timing', 'display_name': ''},
        {'id': '8164177537557', 'role': 'Typesetting', 'display_name': ''},
        {'id': '8883999249942', 'role': 'Quality Control', 'display_name': ''},
    ]

    trackers: list[str] = [
        'http://nyaa.tracker.wf:7777/announce',
        'https://tracker.nekobt.to/api/tracker/public/announce',
        'udp://open.stealth.si:80/announce',
        'udp://tracker.opentrackr.org:1337/announce',
        'udp://exodus.desync.com:6969/announce',
        'udp://tracker.torrent.eu.org:451/announce',
        'udp://open.demonii.com:1337/announce',
    ]
    
    @property
    def show(self) -> str:
        return self.shorthand


config = SetupConfig()
