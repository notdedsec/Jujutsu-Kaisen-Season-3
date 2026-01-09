from muxtools.subtitle.basesub import _Line


def style_title_signs(lines: list[_Line]):
    for line in lines:
        if line.style != 'Ep_Title':
            continue

        line.text = line.text
        # TODO: implement styling logic here

    return lines
