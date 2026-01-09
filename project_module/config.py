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
    trackers: list[str] = [
        "http://nyaa.tracker.wf:7777/announce"
    ]
    
    @property
    def show(self) -> str:
        return self.shorthand


config = SetupConfig()
