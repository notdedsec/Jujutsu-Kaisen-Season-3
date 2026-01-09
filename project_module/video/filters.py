from vsaa import based_aa
from vsdeband import Grainer, deband_detail_mask, f3k_deband
from vsdehalo import fine_dehalo
from vsdenoise import MVToolsPreset, Prefilter, bm3d, frequency_merge, mc_degrain, nl_means
from vskernels import Bilinear, Hermite
from vsmasktools import Morpho
from vsmuxtools import FileInfo
from vspreview import is_preview
from vsscale import ArtCNN, Rescale
from vstools import core, replace_ranges, set_output, vs

from project_module.source.models import Episode

FrameRanges = list[tuple[int, int]] | None
SceneRanges = dict[tuple[int, int], dict] | None


def merge(episode: Episode) -> vs.VideoNode:
    cr = FileInfo(episode.CR).init_cut()
    az = FileInfo(episode.AZ).init_cut()
    dp = FileInfo(episode.DP, trim=(24, None)).init_cut()
    nf = FileInfo(episode.NF, trim=(24, None)).init_cut()

    def lowpass(clip):
        return core.std.BoxBlur(
            clip,
            hradius=3, vradius=3,
            hpasses=2, vpasses=2,
        )

    out = frequency_merge(cr, dp, nf, lowpass=lowpass)

    if is_preview():
        set_output(cr, 'crunchyroll')
        # set_output(az, 'amazon')
        set_output(dp, 'disney+')
        set_output(nf, 'netflix')
        set_output(out, 'merge')

    return out


def rescale(clip: vs.VideoNode, skip_ranges: FrameRanges = None) -> vs.VideoNode:
    r = Rescale(
        clip,
        height=843.75,
        kernel=Bilinear,
        upscaler=ArtCNN,
        downscaler=Hermite,
    )

    r.doubled = fine_dehalo(
        r.doubled,
        ss=1,
        darkstr=0.25,
        brightstr=0.75,
        thmi=40,
        thlimi=16,
        exclude=False,
    )

    r.line_mask = Morpho.expand(
        r.default_line_mask(),
        sw=1,
    )

    r.credit_mask = Morpho.inflate(
        r.default_credit_mask(),
        radius=2,
        iterations=2,
    )

    out = r.upscale

    if skip_ranges:
        out = replace_ranges(out, clip, skip_ranges)

    if is_preview():
        set_output(out, 'rescale')

    return out


def denoise(clip: vs.VideoNode, skip_ranges: FrameRanges = None, scene_filter: SceneRanges = None) -> vs.VideoNode:
    def _denoise(thsad: int = 100, sigma: float = 0.75, h: float = 0.25) -> vs.VideoNode:
        ref = mc_degrain(
            clip,
            prefilter=Prefilter.DFTTEST,
            preset=MVToolsPreset.HQ_SAD,
            thsad=thsad,
        )

        out = bm3d(
            clip,
            sigma=sigma,
            tr=2,
            profile=bm3d.Profile.HIGH,
            ref=ref,
            planes=[0],
        )

        out = nl_means(
            out,
            h=h,
            tr=2,
            ref=ref,
            planes=[1, 2],
        )

        return out

    out = _denoise()

    if scene_filter:
        for ranges, args in scene_filter.items():
            out = replace_ranges(out, _denoise(**args), [ranges])

    if skip_ranges:
        out = replace_ranges(out, clip, skip_ranges)

    if is_preview():
        set_output(out, 'denoise')

    return out


def antialias(clip: vs.VideoNode, skip_ranges: FrameRanges = None) -> vs.VideoNode:
    out = based_aa(
        clip,
        rfactor=1.6,
    )

    if skip_ranges:
        out = replace_ranges(out, clip, skip_ranges)

    if is_preview():
        set_output(out, 'aa')

    return out


def deband(clip: vs.VideoNode, skip_ranges: FrameRanges = None, scene_filter: SceneRanges = None) -> vs.VideoNode:
    mask = deband_detail_mask(
        clip,
        brz=(0.01, 0.025),
    )

    def _deband(radius: int = 16, thr: int = 96) -> vs.VideoNode:
        out = f3k_deband(
            clip,
            radius=radius,
            thr=thr,
        )

        return core.std.MaskedMerge(out, clip, mask)

    out = _deband()

    if scene_filter:
        for ranges, args in scene_filter.items():
            out = replace_ranges(out, _deband(**args), [ranges])

    if skip_ranges:
        out = replace_ranges(out, clip, skip_ranges)

    if is_preview():
        set_output(out, 'deband')

    return out


def grain(clip: vs.VideoNode) -> vs.VideoNode:
    out = Grainer.FBM_SIMPLEX(
        clip,
        strength=[2.5, 0],
    )

    if is_preview():
        set_output(out, 'grain')

    return out
