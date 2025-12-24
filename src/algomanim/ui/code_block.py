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
        between_blocks_buff: Buffer between pre-code and code blocks.
        pre_code_buff: Buffer between pre-code lines.
        code_buff: Buffer between code lines.
        mob_center: Center object for positioning.
        # align_edge: Edge to align with reference mobject. If None,
            centers at mobject center.
    """

    def __init__(
        self,
        code_lines: List[str],
        pre_code_lines: List[str] = [],
        # --- position ---
        vector: np.ndarray = mn.ORIGIN,
        mob_center: mn.Mobject = mn.Dot(mn.ORIGIN),
        # align_edge: Literal["up", "down", "left", "right"] | None = None,
        # --- font ---
        font_size=20,
        font="",
        font_color_regular: ManimColor | str = "WHITE",
        font_color_highlight: ManimColor | str = "YELLOW",
        # --- buffs ---
        between_blocks_buff=0.5,
        pre_code_buff=0.15,
        code_buff=0.05,
        # --- other ---
        bg_highlight_color: ManimColor | str = mn.BLACK,
        **kwargs,
    ):
        super().__init__(
            vector=vector,
            mob_center=mob_center,
            # align_edge=align_edge,
            **kwargs,
        )

        self._code_lines = code_lines
        self._pre_code_lines = pre_code_lines
        self._font_size = font_size
        self._font = font
        self._font_color_regular = font_color_regular
        self._font_color_highlight = font_color_highlight
        self._between_blocks_buff = between_blocks_buff
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
        self._bg_rects_code: List[mn.Rectangle | None] = [None] * len(
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
            self._bg_rects_precode: List[mn.Rectangle | None] = [None] * len(
                self._code_lines
            )  # list to save links on all possible rectangles and to manage=delete them
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
                buff=between_blocks_buff,
            )
        else:
            self._code_block_vgroup = code_vgroup

        self.add(self._code_block_vgroup)
        self._position()

    def _highlight_block(
        self,
        code_mobs_list: List[mn.Text],
        rects_list: List[mn.Rectangle | None],
        indices: tuple[int, ...],
    ) -> None:
        """Helper method to highlight lines in a code block.

        Args:
            code_mobs_list: List of text mobjects to highlight.
            rects_list: List of background rectangles (parallel to code_mobs_list).
            indices: Tuple of line indices to highlight.
        """
        for k, mob in enumerate(code_mobs_list):
            if k in indices:
                # change font color
                mob.set_color(self._font_color_highlight)
                # create bg rectangle
                if rects_list[k] is None:
                    bg_rect = mn.Rectangle(
                        width=mob.width + 0.2,
                        height=mob.height + 0.1,
                        fill_color=self._bg_highlight_color,
                        fill_opacity=1,
                        stroke_width=0,
                    )
                    bg_rect.move_to(mob.get_center())
                    self.add(bg_rect)
                    bg_rect.z_index = -1  # send background to back
                    rects_list[k] = bg_rect
            else:
                # normal line: regular font color
                mob.set_color(self._font_color_regular)
                # remove rect
                bg_rect = rects_list[k]
                if bg_rect:
                    self.remove(bg_rect)
                    rects_list[k] = None

    def _clear_block_highlights(
        self,
        code_mobs_list: List[mn.Text],
        rects_list: List[mn.Rectangle | None],
    ) -> None:
        """Clear all highlights from a code block.

        Args:
            code_mobs_list: List of text mobjects in the block.
            rects_list: List of background rectangles (parallel to code_mobs_list).
        """

        for k, mob in enumerate(code_mobs_list):
            # normal line: regular font color
            mob.set_color(self._font_color_regular)
            # remove rect
            bg_rect = rects_list[k]
            if bg_rect:
                self.remove(bg_rect)
                rects_list[k] = None

    @staticmethod
    def format_code_lines(code: str) -> list[str]:
        """Format code string into indented lines with tree markers.

        Args:
            code: Multiline code string.

        Returns:
            list[str]: Lines formatted with '│   ' prefixes
              for indentation levels.
        """
        lines = code.strip().split("\n")
        res = []
        for line in lines:
            indent = len(line) - len(line.lstrip())
            prefix = "│   " * (indent // 4)
            res.append(prefix + line.lstrip())
        return res

    def highlight(
        self,
        *code_indices: int,
        precode_indices: tuple[int, ...] | None = None,
    ):
        """Highlights one or more lines with background and text color.

        Args:
            *i: Tuple of code line indices to highlight.
            pre_code: Tuple of pre-code line indices to highlight, or None.
        """

        self._highlight_block(self._code_mobs, self._bg_rects_code, code_indices)

        if hasattr(self, "_pre_code_mobs"):
            if precode_indices is not None:
                self._highlight_block(
                    self._pre_code_mobs, self._bg_rects_precode, precode_indices
                )
            else:
                self._clear_block_highlights(
                    self._pre_code_mobs, self._bg_rects_precode
                )

    def highlight_line(self, i: int):
        """Deprecated: use highlight_lines() instead"""

        import warnings

        warnings.warn(
            "highlight_line() is deprecated, use highlight()",
            DeprecationWarning,
            stacklevel=2,
        )
        self.highlight(i)
