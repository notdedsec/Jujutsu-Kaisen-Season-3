from pathlib import Path

from ass import FieldSection, ScriptInfoSection
from muxtools import SubFile
from muxtools.subtitle.basesub import _Line


def save_subs(subs: SubFile, filename: Path | None = None):
    if not filename:
        filename = subs.source

    if filename.exists():
        filename.unlink()

    subs.file.rename(filename)


def rename_styles(subs: SubFile, old_name: str, new_name: str):
    doc = subs._read_doc()

    for style in doc.styles:
        if style.name == old_name:
            style.name = new_name

    subs._update_doc(doc)

    def rename_line_styles(lines: list[_Line]):
        for line in lines:
            if line.style == old_name:
                line.style = new_name
        return lines

    subs.manipulate_lines(rename_line_styles)


def set_headers(subs: SubFile, title: str):
    doc = subs._read_doc()

    doc.sections['Script Info'] = ScriptInfoSection(
        name='Script Info',
        fields={
            'Title': title,
            'ScriptType': 'v4.00+',
            'WrapStyle': 0,
            'PlayResX': 1920,
            'PlayResY': 1080,
            'LayoutResX': 1920,
            'LayoutResY': 1080,
            'YCbCr Matrix': 'TV.709',
            'ScaledBorderAndShadow': 'yes',
        },
    )

    subs._update_doc(doc)


def set_garbage(subs: SubFile, filename: str):
    doc = subs._read_doc()

    doc.sections['Aegisub Project Garbage'] = FieldSection(
        name='Aegisub Project Garbage',
        fields={
            'Video File': filename,
            'Audio File': filename,
            'Keyframes File': filename.replace('premux.mkv', 'keyframes.txt'),
        },
    )

    subs._update_doc(doc)
