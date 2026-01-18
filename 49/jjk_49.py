from vsmuxtools import FileInfo
from vstools import match_clip, replace_ranges

from project_module.source.getter import get_episode
from project_module.video.encoder import run_encode
from project_module.video.filters import antialias, deband, denoise, grain, merge, rescale

episode = get_episode('49')

src = merge(episode)

MASK = FileInfo('49\\jjk_49_22010_clean.png')
mask = match_clip(MASK.init(), src, length=True)
src = replace_ranges(src, mask, ranges=[(22010, 22119), (22139, 22143), (22162, 22184), (22208, 22224), (22243, 22271), (22288, 22310), (22325, 22336), (22349, 22489)])

rsc = rescale(src)
dns = denoise(rsc)
aaa = antialias(dns)
dbn = deband(aaa)
grn = grain(dbn)


if __name__ == '__main__':
    run_encode(episode, grn)
