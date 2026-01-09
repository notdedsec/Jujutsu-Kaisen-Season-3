from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path

from project_module.config import config
from project_module.helpers import get_source

show = config.shorthand


@dataclass
class Stream:
    id: str
    title: str
    folder: Path = field(init=False)
    script: Path = field(init=False)
    encode: Path = field(init=False)
    keyframes: Path = field(init=False)

    @property
    def number(self) -> str:
        return self.id

    def __post_init__(self):
        self.folder = Path(self.id)
        self.script = self.folder / f'{show}_{self.id}.py'
        self.encode = self.folder / f'{show}_{self.id}_premux.mkv'
        self.keyframes = self.folder / f'{show}_{self.id}_keyframes.txt'


@dataclass
class Bonus(Stream):
    subs: Path = field(init=False)

    def __post_init__(self):
        super().__post_init__()

        self.subs = self.folder / f'{show}_{self.id}_subs.ass'

        if self.id[-1] in ['A', 'B', 'C', 'D', 'E']:
            base_id = self.id[:-1]

            if not self.subs.exists():
                self.subs = Path(f"{base_id}/{show}_{base_id}_subs.ass")


@dataclass
class Episode(Stream):
    OP: Bonus | None = None
    ED: Bonus | None = None
    # EC: Path | None = None
    subs_dialogue: Path = field(init=False)
    subs_typesets: Path = field(init=False)

    def __post_init__(self):
        super().__post_init__()

        self.subs_dialogue = self.folder / f'{show}_{self.id}_subs_dialogue.ass'
        self.subs_typesets = self.folder / f'{show}_{self.id}_subs_typesets.ass'

    @cached_property
    def CR(self) -> Path | None:
        try:
            return get_source(self.id, 'Crunchyroll')
        except FileNotFoundError:
            return None

    @cached_property
    def AZ(self) -> Path | None:
        try:
            return get_source(self.id, 'Amazon')
        except FileNotFoundError:
            return None

    @cached_property
    def DP(self) -> Path | None:
        try:
            return get_source(self.id, 'Disney+')
        except FileNotFoundError:
            return None

    @cached_property
    def NF(self) -> Path | None:
        try:
            return get_source(self.id, 'Netflix')
        except FileNotFoundError:
            return None
