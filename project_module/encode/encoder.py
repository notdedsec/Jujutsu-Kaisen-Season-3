from vsmuxtools import FFV1, IntermediaryEncoder, LosslessPreset, SVTAV1, do_audio, mux, settings_builder_5fish_svt_av1_psy, settings_builder_x265, src_file, x265
from vstools import finalize_clip, vs

from project_module.config import config
from project_module.encode.filters import grain
from project_module.source.models import Episode

settings_x265 = settings_builder_x265(
    crf=14,
    qcomp=0.72,
    preset='slower',
)

settings_av1 = settings_builder_5fish_svt_av1_psy(
    preset=2,
    crf=24.0,
    lineart_psy_bias=4,
    texture_psy_bias=3,
)


def run_encode(episode: Episode, clip: vs.VideoNode, zones=None):
    clip = finalize_clip(clip)

    if config.vcodec == 'HEVC':
        video = x265(settings_x265, zones).encode(grain(clip))
    elif config.vcodec == 'AV1':
        video = SVTAV1(src_file(episode.CR), **settings_av1).encode(clip)
    else:
        raise ValueError(f'Unsupported video codec: {config.vcodec}')

    audio = do_audio(episode.AZ)

    mux(
        video.to_track(f'{config.format} 1080p {config.vcodec} [dedsec]'),
        audio.to_track(f'Japanese 2.0 {config.acodec}', 'ja'),
        outfile=episode.encode,
    )


def run_encodes(episode: Episode, clip: vs.VideoNode, zones=None):
    outfile_main = episode.folder / f'{config.show}_{episode.number}_premux.mkv'
    outfile_mini = episode.folder / f'{config.show}_{episode.number}_premux_mini.mkv'

    video_main, video_mini = IntermediaryEncoder(
        FFV1(LosslessPreset.SPEED),
        [
            (x265(settings_x265, zones), grain),
            SVTAV1(src_file(episode.CR), **settings_av1),
        ],
    ).encode(finalize_clip(clip))

    audio = do_audio(episode.AZ)

    mux(
        video_main.to_track(f'{config.format} 1080p HEVC [dedsec]'),
        audio.to_track(f'Japanese 2.0 {config.acodec}', 'ja'),
        outfile=outfile_main,
    )

    mux(
        video_mini.to_track(f'{config.format} 1080p AV1 [dedsec]'),
        audio.to_track(f'Japanese 2.0 {config.acodec}', 'ja'),
        outfile=outfile_mini,
    )
