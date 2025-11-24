from typing import (
    List,
    Literal,
)

import numpy as np
import manim as mn
from manim import ManimColor

from algomanim.core.base import AlgoManimBase


class CodeBlock(AlgoManimBase):
    """Code block visualization with syntax highlighting capabilities.

    Args:
        code_lines: List of code lines to display.
        vector: Position vector to place the code block.
        pre_code_lines: Lines to display before the main code.
        font_size: Font size for the code text.
        font: Font for the code text.
        font_color_regular: Color for regular text.
        font_color_highlight: Color for highlighted text.
        bg_highlight_color: Background color for highlighted lines.
        inter_block_buff: Buffer between pre-code and code blocks.
        pre_code_buff: Buffer between pre-code lines.
        code_buff: Buffer between code lines.
        mob_center: Center object for positioning.
        align_edge: Edge to align with reference mobject. If None,
            centers at mobject center.
    """

    def __init__(
        self,
        code_lines: List[str],
        pre_code_lines: List[str] = [],
        # --- position ---
        vector: np.ndarray = mn.ORIGIN,
        mob_center: mn.Mobject = mn.Dot(mn.ORIGIN),
        align_edge: Literal["up", "down", "left", "right"] | None = None,
        # --- font ---
        font_size=20,
        font="",
        font_color_regular: ManimColor | str = "WHITE",
        font_color_highlight: ManimColor | str = "YELLOW",
        # --- buffs ---
        inter_block_buff=0.5,
        pre_code_buff=0.15,
        code_buff=0.05,
        # --- other ---
        bg_highlight_color: ManimColor | str = "BLUE",
    ):
        super().__init__()
        self._code_lines = code_lines
        self._pre_code_lines = pre_code_lines
        self._vector = vector
        self._mob_center = mob_center
        self._align_edge = align_edge
        self._font_size = font_size
        self._font = font
        self._font_color_regular = font_color_regular
        self._font_color_highlight = font_color_highlight
        self._inter_block_buff = inter_block_buff
        self._pre_code_buff = pre_code_buff
        self._code_buff = code_buff
        self._bg_highlight_color = bg_highlight_color

        self._code_mobs = [
            mn.Text(
                line,
                font=self._font,
                font_size=self._font_size,
                color=self._font_color_regular,
            )
            for line in self._code_lines
        ]
        self._bg_rects: List[mn.Rectangle | None] = [None] * len(
            self._code_lines
        )  # list to save links on all possible rectangles and to manage=delete them

        code_vgroup = mn.VGroup(*self._code_mobs).arrange(
            mn.DOWN,
            aligned_edge=mn.LEFT,
            buff=self._code_buff,
        )

        if self._pre_code_lines:
            self._pre_code_mobs = [
                mn.Text(
                    line,
                    font=self._font,
                    font_size=self._font_size,
                    color=self._font_color_regular,
                )
                for line in self._pre_code_lines
            ]
            self._pre_code_vgroup = mn.VGroup(*self._pre_code_mobs).arrange(
                mn.DOWN,
                aligned_edge=mn.LEFT,
                buff=self._pre_code_buff,
            )
            self._code_block_vgroup = mn.VGroup(
                self._pre_code_vgroup, code_vgroup
            ).arrange(
                mn.DOWN,
                aligned_edge=mn.LEFT,
                buff=inter_block_buff,
            )
        else:
            self._code_block_vgroup = code_vgroup

        self._position(self._code_block_vgroup, self._code_block_vgroup)

        self.add(self._code_block_vgroup)

    def highlight_line(self, i: int):
        """Highlights a single line of code with background and text color.

        Args:
            i: Index of the line to highlight.
        """

        for k, mob in enumerate(self._code_mobs):
            if k == i:
                # change font color
                mob.set_color(self._font_color_highlight)
                # create bg rectangle
                if self._bg_rects[k] is None:
                    bg_rect = mn.Rectangle(
                        width=mob.width + 0.2,
                        height=mob.height + 0.1,
                        fill_color=self._bg_highlight_color,
                        fill_opacity=0.3,
                        stroke_width=0,
                    )
                    bg_rect.move_to(mob.get_center())
                    self.add(bg_rect)
                    bg_rect.z_index = -1  # send background to back
                    self._bg_rects[k] = bg_rect
            else:
                # normal line: regular font color
                mob.set_color(self._font_color_regular)
                # remove rect
                bg_rect = self._bg_rects[k]
                if bg_rect:
                    self.remove(bg_rect)
                    self._bg_rects[k] = None
