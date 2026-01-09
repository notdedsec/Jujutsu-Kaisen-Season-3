import subprocess
from pathlib import Path

from muxtools import GlobSearch

from project_module.config import config
from project_module.constants import SEASON_EPISODE_MAP

source_folder = Path(__file__).parent.parent / 'sources'


def get_season(ep: str) -> str:
    for season, episodes in SEASON_EPISODE_MAP.items():
        if int(ep) in episodes:
            return str(season).zfill(2)


def get_season_offset(ep: str) -> int:
    season = get_season(ep)
    offset = int(min(SEASON_EPISODE_MAP[int(season)])) - 1
    return offset


def absolute_to_seasonal(ep: str) -> str:
    offset = get_season_offset(ep)
    seasonal = str(int(ep) - offset).zfill(2)
    return seasonal


def get_source(ep: str, folder: str | None = None, release: str = '') -> Path:
    season = get_season(ep)
    episode = absolute_to_seasonal(ep)
    show = config.show_name.replace(' ', '*')
    search_folder = source_folder if folder is None else source_folder / Path(folder)

    search_a = GlobSearch(f'{show}*S{season}E{episode}*{release}*mkv', dir=search_folder)
    search_b = GlobSearch(f'*{release}*{show}*{ep}*mkv', dir=search_folder)

    results = search_a.paths or search_b.paths
    if not results:
        raise FileNotFoundError(f'No results found for episode {ep} in {search_folder.resolve()}')

    return results[0]


def get_release(ep: str) -> Path:
    group_tag = config.group_tag
    show_name = config.show_name.replace(' ', '*')

    results = GlobSearch(f'*{group_tag}*{show_name}*{ep}*.mkv', dir='.', recursive=False).paths
    if not results:
        raise FileNotFoundError(f'No results found for episode {ep} in {Path(".").resolve()}')

    return results[0]


def parse_episode_arg(episode_arg: str) -> list[str]:
    episode_arg = episode_arg.strip()
    episodes = []

    parts = [part.strip() for part in episode_arg.split(',')]

    for part in parts:
        if '-' in part:
            try:
                start, end = part.split('-', 1)
                start_ep = int(start.strip())
                end_ep = int(end.strip())
                episodes.extend([f'{ep:02d}' for ep in range(start_ep, end_ep + 1)])
            except ValueError:
                raise ValueError(f'Invalid range format: {part}. Use format like "48-60".')
        else:
            if part.isdigit():
                episodes.append(f'{int(part):02d}')
            else:
                episodes.append(part)

    return episodes


def set_mkv_title(path: str | Path, title: str):
    cmd = ['mkvpropedit', '--quiet', str(path), '--edit', 'info', '--set', f'title={title}']
    subprocess.run(cmd, check=True)
