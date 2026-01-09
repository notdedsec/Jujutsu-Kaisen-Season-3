from pathlib import Path

from torf import Torrent

from project_module.config import config


def create_torrent(file_path: Path | str, trackers: list[str] = config.trackers) -> Path:
    file_path = Path(file_path)
    torrent_path = file_path.with_suffix('.torrent')

    if not torrent_path.exists():
        torrent = Torrent(
            path=file_path,
            trackers=trackers,
        )
        torrent.generate()
        torrent.write(torrent_path)

    return torrent_path
