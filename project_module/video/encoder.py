from vsmuxtools import do_audio, mux, settings_builder_x265, x265
from vstools import finalize_clip, vs

from project_module.source.models import Episode


def run_encode(episode: Episode, clip: vs.VideoNode, zones=None):
    clip = finalize_clip(clip)

    settings = settings_builder_x265(
        crf=14,
        qcomp=0.72,
        preset='slower',
    )

    video = x265(settings, zones).encode(clip)
    audio = do_audio(episode.AZ)

    mux(
        video.to_track('WEB 1080p HEVC [dedsec]'),
        audio.to_track('Japanese 2.0 EAC-3', 'ja'),
        outfile=episode.encode,
    )
