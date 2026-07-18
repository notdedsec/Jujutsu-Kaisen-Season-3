from pathlib import Path

from muxtools import GlobSearch
from muxtools.utils.types import Trim

from project_module.config import config
from project_module.constants import BD_TRIMS, SEASON_EPISODE_MAP

source_folder = Path(__file__).parent.parent / 'sources'


def if_exists(path: Path) -> Path | None:
    return path if path.exists() else None


def get_trim(ep: str) -> Trim | None:
    if config.format != 'BD':
        return None

    return BD_TRIMS.get(ep)


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


def get_source(ep: str, folder: str) -> Path:
    show = config.show_name.replace(' ', '*')
    season = get_season(ep)
    episode = absolute_to_seasonal(ep)

    search_dir = source_folder / Path(folder)
    search_a = GlobSearch(f'*{show}*S{season}E{episode}*.mkv', dir=search_dir)
    search_b = GlobSearch(f'*{show}*{ep}*.mkv', dir=search_dir)

    results = search_a.paths or search_b.paths
    if not results:
        raise FileNotFoundError(f'No results found for episode {ep} in {search_dir.resolve()}')

    return results[0]


def get_release(ep: str) -> Path:
    from project_module.source.resolve import get_episode

    episode = get_episode(ep)
    results = GlobSearch(episode.release_glob, allow_multiple=True, dir='.', recursive=False).paths

    if not results:
        raise FileNotFoundError(f'No results found for episode {ep} in {Path(".").resolve()}')

    if len(results) > 1:
        raise ValueError(f'Multiple release files found for episode {ep}: {", ".join(path.name for path in results)}')

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
                raise ValueError(f'Invalid range format: {part}. Use format like "48-50"')
        else:
            if part.isdigit():
                episodes.append(f'{int(part):02d}')
            else:
                episodes.append(part)

    return episodes
