from project_module.source.getter import get_episode
from project_module.video.encoder import run_encode
from project_module.video.filters import antialias, deband, denoise, grain, merge, rescale

episode = get_episode('48')

src = merge(episode)

rsc = rescale(src)
dns = denoise(rsc)
aaa = antialias(dns)
dbn = deband(aaa)
grn = grain(dbn)


if __name__ == '__main__':
    run_encode(episode, grn)
