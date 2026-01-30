from ass import Style
from ass.line import Color
from muxtools import default_style_args, edit_style

main_style = Style(
    name='Default',
    fontname='Cabin F',
    fontsize=71.0,
    outline=3.6,
    shadow=1.8,
    margin_l=128,
    margin_r=128,
    margin_v=65,
    **default_style_args,
)

alt_style = edit_style(
    style=main_style,
    name='Alt',
    outline_color=Color(r=0x00, g=0x39, b=0x3C, a=0x00)
)

styles = [main_style, alt_style]
