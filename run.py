import sys
from pathlib import Path

project_root = Path(__file__).parent.resolve()
sys.path.insert(0, str(project_root))

import typer
from rich.console import Console

from project_module.config import config

app = typer.Typer(
    name=f'{config.shorthand}-cli',
    help=f'{config.show_name} Automations',
    rich_markup_mode='rich',
    add_completion=False,
)

console = Console()

episode_help = 'Episode number or range (e.g., "50" or "48-60")'


def process_episodes(episode_arg: str, process_func, operation: str, *args, **kwargs):
    """Helper function to process episodes with consistent logging and error handling."""
    from project_module.helpers import parse_episode_arg

    try:
        episodes = parse_episode_arg(episode_arg)
        is_batch = len(episodes) > 1

        if is_batch:
            console.print(f'[bold cyan]Processing {operation} for {len(episodes)} episodes from {episode_arg}[/bold cyan]')
        else:
            console.print(f'[bold cyan]Processing {operation} for {episode_arg}[/bold cyan]')

        for ep in episodes:
            if is_batch:
                console.print(f'[blue]Processing episode {ep}...[/blue]')
            _ = process_func(ep, *args, **kwargs)
            if is_batch:
                console.print(f'[green]✓ Completed episode {ep}[/green]')

        if is_batch:
            console.print(f'[green]Successfully processed {operation} for all {len(episodes)} episodes[/green]')
        else:
            console.print(f'[green]Successfully processed {operation} for {episode_arg}[/green]')
    except Exception as e:
        console.print_exception()
        console.print(f'[red]Error during {operation}: {e}[/red]')
        raise typer.Exit(1)


@app.command()
def encode(episode: str = typer.Argument(..., help=episode_help)):
    """Encode episode using VapourSynth script."""
    from project_module.workflows import run_encode

    process_episodes(episode, run_encode, 'encoding')


@app.command()
def preview(episode: str = typer.Argument(..., help=episode_help)):
    """Preview episode script in vspreview."""
    from project_module.workflows import run_preview

    process_episodes(episode, run_preview, 'preview')


@app.command()
def keyframes(episode: str = typer.Argument(..., help=episode_help)):
    """Generate keyframes for episode premux files."""
    from project_module.workflows import run_keyframes

    process_episodes(episode, run_keyframes, 'keyframe generation')


@app.command()
def demux(episode: str = typer.Argument(..., help=episode_help)):
    """Demux episode subtitles into dialogue and typesets files."""
    from project_module.workflows import run_demux

    process_episodes(episode, run_demux, 'demuxing')


@app.command()
def mux(episode: str = typer.Argument(..., help=episode_help)):
    """Mux episode with processed subtitles and create final output."""
    from project_module.workflows import run_mux

    process_episodes(episode, run_mux, 'muxing')


@app.command()
def sub_replace(
    episode: str = typer.Argument(..., help=episode_help),
    find: str = typer.Option(..., '--find', '-f', help='Text to find'),
    replace: str = typer.Option(..., '--replace', '-r', help='Text to replace with'),
    style: str = typer.Option('default,alt', '--style', '-s', help='Style name to apply replacement to'),
):
    """Process episode subtitles to find and replace text in specific styles."""
    from project_module.workflows import sub_replace as run_sub_replace

    process_episodes(episode, run_sub_replace, 'find/replace', find, replace, style)


@app.command()
def sub_cleanup(
    episode: str = typer.Argument(..., help=episode_help),
    actions: str = typer.Option(..., '--actions', '-a', help='Comma-separated list of cleanup actions (e.g., "breaks,dashes,spaces")'),
    style: str = typer.Option('default,alt', '--style', '-s', help='Style name to apply cleanup to'),
):
    """Process episode subtitles with predefined cleanup actions."""
    from project_module.workflows import sub_cleanup as run_sub_cleanup

    process_episodes(episode, run_sub_cleanup, 'cleanup', actions, style)


@app.command()
def torrent(episode: str = typer.Argument(..., help=episode_help)):
    """Create torrent file for episode."""
    from project_module.workflows import run_torrent

    process_episodes(episode, run_torrent, 'torrent creation')


@app.command()
def nyaa(episode: str = typer.Argument(..., help=episode_help)):
    """Create torrent and upload to nyaa."""
    from project_module.workflows import run_nyaa

    process_episodes(episode, run_nyaa, 'nyaa upload')


if __name__ == '__main__':
    app()
