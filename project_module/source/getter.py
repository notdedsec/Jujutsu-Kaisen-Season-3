from project_module.source import mapping
from project_module.source.models import Bonus, Episode


def get_stream(name: str) -> Episode | Bonus:
    return getattr(mapping, name, None)


def get_episode(ep: str) -> Episode:
    episode = get_stream(f'E{ep}')
    if not episode:
        raise ValueError(f'Episode {ep} not found in mapping.')
    return episode
