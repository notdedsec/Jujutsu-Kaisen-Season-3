import re

from muxtools.subtitle.basesub import _Line

from project_module.constants import CHARACTER_NAMES, HONORIFIC_REPLACEMENTS, TERMINOLOGY_REPLACEMENTS


def remove_unwanted_lines(lines: list[_Line]):
    for line in lines:

        if line.style.startswith('OP') or line.style.startswith('ED'):
            line.TYPE = 'DELETE'

        if line.text.startswith('Subtitle translation by'):
            line.TYPE = 'DELETE'

    return [line for line in lines if line.TYPE != 'DELETE']


def swap_honorifics(lines: list[_Line]):
    for line in lines:

        if not any(honorific in line.text for honorific in HONORIFIC_REPLACEMENTS.keys()):
            continue

        for honorific, replacement in HONORIFIC_REPLACEMENTS.items():
            line.text = re.sub(honorific + r'\b', replacement, line.text)

    return lines


def reverse_name_order(lines: list[_Line]):
    for line in lines:

        if not any(name in line.text for name in CHARACTER_NAMES):
            continue

        for name in CHARACTER_NAMES:
            first, last = name.split(' ')
            line.text = re.sub(r'\b' + re.escape(f'{first} {last}') + r'\b', f'{last} {first}', line.text)

    return lines


def update_terminology(lines: list[_Line]):
    for line in lines:

        if not any(term in line.text for term in TERMINOLOGY_REPLACEMENTS.keys()):
            continue

        for term, replacement in TERMINOLOGY_REPLACEMENTS.items():
            use_word_boundary = '{' not in term
            pattern = r'\b' + re.escape(term) + r'\b' if use_word_boundary else re.escape(term)
            line.text = re.sub(pattern, replacement, line.text)

    return lines


def add_placeholder_chapters(lines: list[_Line]):
    ...
