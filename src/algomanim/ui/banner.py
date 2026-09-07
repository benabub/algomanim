from __future__ import annotations

import manim as mn
import numpy as np
from manim import ManimColor

from ..core.base import AlgoManimBase
from ..core.code_block_base import CodeBlockBase


class CloseBanner(AlgoManimBase):
    """Banner that overlays a code block with text and a background rectangle.

    Args:
        code_block: The code block to overlay.
        *text_lines: Text lines to display on the banner.
        font: Font family for the text.
        font_size: Base font size for all text lines.
        font_sizes: Optional tuple of font sizes for each line individually.
            Must match the number of text_lines. Overrides font_size for those lines.
        text_color: Color of the text.
        text_inter_buff: Vertical spacing between text lines.
        bg_color: Background color of the banner rectangle.
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
        text_shift: np.ndarray | None = mn.DOWN * 1.2,
        # --- rectangle ---
        bg_color: ManimColor | str = mn.PINK,
        # --- svg ---
        svg_path: str | None = None,
        svg_shift: np.ndarray = mn.UP * 2,
        svg_height: float = 1.5,
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
        if text_shift is not None:
            self._text_mobs.shift(text_shift)
        self.add(self._text_mobs)

        if not svg_path:
            self._svg_mob = None
            return
        self._svg_mob = mn.SVGMobject(svg_path, height=svg_height)
        self._svg_mob.move_to(self._rect_mob)
        self._svg_mob.shift(svg_shift)
        self.add(self._svg_mob)

