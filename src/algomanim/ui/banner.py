import manim as mn
import numpy as np
from manim import ManimColor

from ..core.code_block_base import CodeBlockBase


class CloseBanner(mn.VGroup):
    """
    ...
    """

    def __init__(
        self,
        # --- code block ---
        code_block: CodeBlockBase,
        # --- text ---
        *text_lines: str,
        # --- font ---
        font: str = "",
        font_size: float = 50,
        font_sizes: tuple[int, ...] = (),
        text_color: ManimColor | str = mn.WHITE,
        text_inter_buff: float = 0.8,
        # --- rectangle ---
        bg_color: ManimColor | str = mn.PINK,
    ):
        super().__init__()

        if font_sizes and len(font_sizes) != len(text_lines):
            raise ValueError("font_sizes: number different than text_lines")

        # create rectangle
        self._rect_mob = mn.RoundedRectangle(
            corner_radius=code_block._rect_corner_radius,
            width=code_block.width,
            height=code_block.height,
            fill_color=bg_color,
            fill_opacity=1,
            stroke_width=0,
        )
        self._rect_mob.move_to(code_block)
        self.add(self._rect_mob)

        self._text_mobs = mn.VGroup(
            mn.Text(
                line,
                font=font,
                weight="BOLD",
                font_size=font_size if not font_sizes else font_sizes[i],
                color=text_color,
            )
            for i, line in enumerate(text_lines)
        )
        self._text_mobs.arrange(mn.DOWN, buff=text_inter_buff)
        self._text_mobs.move_to(self._rect_mob)
        self.add(self._text_mobs)
