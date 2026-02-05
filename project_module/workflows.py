import runpy
import subprocess
import sys

from muxtools import Chapters, Premux, Setup, SubFile, mux
from muxtools.subtitle import _Line
from vsmuxtools.utils.source import FileInfo, generate_keyframes

from project_module.config import config
from project_module.helpers import get_release, set_mkv_title
from project_module.release.nyaa import upload_to_nyaa
from project_module.release.torrent import create_torrent
from project_module.source.getter import get_episode
from project_module.subtitles.cleanup import get_cleanup_actions
from project_module.subtitles.process_dialogue import remove_unwanted_lines, reverse_name_order, swap_honorifics, update_terminology
from project_module.subtitles.process_typesets import style_title_signs
from project_module.subtitles.styling import styles
from project_module.subtitles.utils import rename_styles, save_subs, set_garbage, set_headers


def run_encode(ep: str):
    Setup(ep)
    episode = get_episode(ep)
    runpy.run_path(str(episode.script), run_name='__main__')


def run_preview(ep: str):
    Setup(ep)
    episode = get_episode(ep)
    subprocess.run([sys.executable, '-m', 'vspreview', str(episode.script)])


def run_keyframes(ep: str):
    episode = get_episode(ep)

    clip = FileInfo(episode.encode).init()
    keyframes = generate_keyframes(clip)

    text = f'# keyframe format v1\nfps {clip.fps}\n'
    text += ''.join(f'{f}\n' for f in keyframes)

    episode.keyframes.write_text(text)


def run_demux(ep: str):
    Setup(ep)
    episode = get_episode(ep)

    subs = SubFile.from_mkv(episode.CR) \
        .shift_0(timesource=episode.encode, timescale=1000) \
        .resample() \
        .clean_extradata() \
        .manipulate_lines(remove_unwanted_lines) \
        .manipulate_lines(swap_honorifics) \
        .manipulate_lines(reverse_name_order) \
        .manipulate_lines(update_terminology) \
        .manipulate_lines(style_title_signs)

    set_headers(subs, title=f'{config.show_name} - {episode.number} - {episode.title}')
    set_garbage(subs, filename=episode.encode.name)

    rename_styles(subs, 'Ep_Title', 'Signs')

    subs.unfuck_cr(
        dialogue_styles=['default', 'main', 'narration', 'flashback'],
        italics_styles=['italics'],
        keep_flashback=False,
        alt_styles=None,
        top_styles=None,
    )

    subs.restyle(styles, clean_after=False)

    dialogue = subs.copy().separate_signs(inverse=True)
    typesets = subs.copy().separate_signs()

    save_subs(dialogue, episode.subs_dialogue)
    save_subs(typesets, episode.subs_typesets)


def run_mux(ep: str):
    Setup(ep)
    episode = get_episode(ep)

    main_subs = SubFile(sorted(episode.folder.glob(f'{config.show}_{episode.number}_subs*.ass')))

    main_subs.change_layers()

    if episode.OP:
        main_subs.merge(episode.OP.subs, 'opsync', 'sync', episode.OP.encode, 1000)

    if episode.ED:
        main_subs.merge(episode.ED.subs, 'edsync', 'sync', episode.ED.encode, 1000)

    # if episode.EC:
    #     main_subs.merge(episode.EC.subs, 'ecsync')

    weeb_subs = main_subs.copy().autoswapper()

    fonts = main_subs.collect_fonts()

    chapters = Chapters.from_sub(main_subs, episode.encode, 1000, use_actor_field=True, _print=False)

    muxfile = mux(
        Premux(episode.encode),
        main_subs.to_track(f'{config.group_tag}', 'en', args=["--compression", f"0:zlib"]),
        weeb_subs.to_track(f'{config.group_tag} (Honorifics)', 'enm', args=["--compression", f"0:zlib"]),
        *fonts,
        chapters,
    )

    set_mkv_title(muxfile, title=f'{config.show_name} - {episode.number} - {episode.title}')


def sub_replace(ep: str, find: str, repl: str, style: str = 'default,alt'):
    Setup(ep)
    episode = get_episode(ep)

    def apply_find_replace(lines: list[_Line]):
        for line in lines:
            if line.style.lower() in style.lower():
                line.text = line.text.replace(find, repl)
        return lines

    subs = SubFile(episode.subs_dialogue)
    subs.manipulate_lines(apply_find_replace)
    save_subs(subs)


def sub_cleanup(ep: str, actions: str, style: str = 'default,alt'):
    Setup(ep)
    episode = get_episode(ep)

    cleanup_actions = get_cleanup_actions(actions)

    if not cleanup_actions:
        print('No valid cleanup actions found.')
        return

    def apply_cleanup_actions(lines: list[_Line]):
        for line in lines:
            if line.style.lower() in style.lower():
                for action in cleanup_actions:
                    for replacement in action['replacements']:
                        line.text = line.text.replace(replacement['find'], replacement['repl'])
        return lines

    subs = SubFile(episode.subs_dialogue)
    subs.manipulate_lines(apply_cleanup_actions)
    save_subs(subs)


def run_torrent(ep: str):
    muxfile = get_release(ep)
    torrent_file = create_torrent(muxfile)
    return torrent_file


def run_nyaa(ep: str):
    episode = get_episode(ep)
    torrent_file = run_torrent(ep)
    upload_to_nyaa(
        torrent_file=torrent_file,
        information=config.information,
        description=episode.folder / config.description
    )
