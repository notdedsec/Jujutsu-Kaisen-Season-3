from project_module.source.resolve import get_episode
from project_module.encode.encoder import run_encode
from project_module.encode.filters import antialias, deband, denoise, get_src, grain, rescale

episode = get_episode('51')

src = get_src(episode)

rsc = rescale(src)
dns = denoise(rsc)
aaa = antialias(dns)
dbn = deband(aaa)
grn = grain(dbn)


if __name__ == '__main__':
    run_encode(episode, dbn)
