from ass import Style
from muxtools import default_style_args, get_complimenting_styles

main_style = Style(
    name="Default",
    fontname="Cabin F",
    fontsize=75.0,
    outline=3.6,
    shadow=1.8,
    margin_l=128,
    margin_r=128,
    margin_v=60,
    **default_style_args,
)

styles = [main_style, *get_complimenting_styles(main_style)]
