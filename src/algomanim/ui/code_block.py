from typing import (
    List,
)

import numpy as np
import manim as mn
from manim import ManimColor
import pyperclip

from algomanim.core.base import AlgoManimBase


class CodeBlock(AlgoManimBase):
    """Code block visualization with syntax highlighting capabilities.

    Args:
        code_lines: List of code lines to display.
        precode_lines: Lines to display before the main code.
        vector: Position offset from mob_center for positioning.
        mob_center: Reference mobject for positioning.
        align_left: Reference mobject to align left edge with.
        align_right: Reference mobject to align right edge with.
        align_top: Reference mobject to align top edge with.
        align_bottom: Reference mobject to align bottom edge with.
        font_size: Font size for the code text.
        font: Font family for the code text. Defaults to system default.
        text_color_regular: Color for regular (non-highlighted) text.
        text_color_highlight: Color for highlighted text.
        between_blocks_buff: Vertical buffer between pre-code and code blocks.
        precode_buff: Vertical buffer between pre-code lines.
        code_buff: Vertical buffer between code lines.
        bg_rect_fill_color: Background fill color for the code block container.
        bg_rect_stroke_width: Stroke width for the code block container.
        bg_rect_stroke_color: Stroke color for the code block container.
        bg_rect_corner_radius: Corner radius for the rounded rectangle container.
        bg_rect_buff: Padding around the code text within the background container.
        bg_highlight_color: Background color for highlighted lines.

    Note:
        The code block uses a layered z-index system:
        -2: Main background rectangle (deepest)
        -1: Line highlight rectangles
        -0: Text lines (topmost)
    """

    def __init__(
        self,
        code_lines: List[str],
        precode_lines: List[str] = [],
        # --- position ---
        vector: np.ndarray = mn.ORIGIN,
        mob_center: mn.Mobject = mn.Dot(mn.ORIGIN),
        align_left: mn.Mobject | None = None,
        align_right: mn.Mobject | None = None,
        align_top: mn.Mobject | None = None,
        align_bottom: mn.Mobject | None = None,
        # --- font ---
        font_size=20,
        font="",
        text_color_regular: ManimColor | str = "WHITE",
        text_color_highlight: ManimColor | str = "YELLOW",
        # --- buffs ---
        between_blocks_buff=0.5,
        precode_buff=0.15,
        code_buff=0.05,
        # --- bg_rect ---
        bg_rect_fill_color: ManimColor | str = "#545454",
        bg_rect_stroke_width: float = 4,
        bg_rect_stroke_color: ManimColor | str = "#151515",
        bg_rect_corner_radius: float = 0.1,
        bg_rect_buff: float = 0.5,
        # --- highlights ---
        bg_highlight_color: ManimColor | str = mn.BLACK,
    ):
        super().__init__(
            vector=vector,
            mob_center=mob_center,
            align_left=align_left,
            align_right=align_right,
            align_top=align_top,
            align_bottom=align_bottom,
        )

        self._code_lines = code_lines
        self._precode_lines = precode_lines
        # --- font ---
        self._font_size = font_size
        self._font = font
        self._text_color_regular = text_color_regular
        self._text_color_highlight = text_color_highlight
        # --- buffs ---
        self._between_blocks_buff = between_blocks_buff
        self._precode_buff = precode_buff
        self._code_buff = code_buff
        # --- colors ---
        self._bg_highlight_color = bg_highlight_color

        self._code_mobs = [
            mn.Text(
                line,
                font=self._font,
                font_size=self._font_size,
                color=self._text_color_regular,
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

        if self._precode_lines:
            self._precode_mobs = [
                mn.Text(
                    line,
                    font=self._font,
                    font_size=self._font_size,
                    color=self._text_color_regular,
                )
                for line in self._precode_lines
            ]
            self._bg_rects_precode: List[mn.Rectangle | None] = [None] * len(
                self._code_lines
            )  # list to save links on all possible rectangles and to manage=delete them
            self._precode_vgroup = mn.VGroup(*self._precode_mobs).arrange(
                mn.DOWN,
                aligned_edge=mn.LEFT,
                buff=self._precode_buff,
            )
            self._code_block_vgroup = mn.VGroup(
                self._precode_vgroup, code_vgroup
            ).arrange(
                mn.DOWN,
                aligned_edge=mn.LEFT,
                buff=between_blocks_buff,
            )
        else:
            self._code_block_vgroup = code_vgroup

        self._bg_rect = mn.RoundedRectangle(
            width=self._code_block_vgroup.width + bg_rect_buff,
            height=self._code_block_vgroup.height + bg_rect_buff,
            fill_color=bg_rect_fill_color,
            fill_opacity=1,
            stroke_width=bg_rect_stroke_width,
            stroke_color=bg_rect_stroke_color,
            corner_radius=bg_rect_corner_radius,
        )

        self._bg_rect.z_index = -2  # deepest layout

        self.add(self._bg_rect, self._code_block_vgroup)
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
                mob.set_color(self._text_color_highlight)
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
                    bg_rect.z_index = -1  # medium layout
                    rects_list[k] = bg_rect
            else:
                # normal line: regular font color
                mob.set_color(self._text_color_regular)
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
            mob.set_color(self._text_color_regular)
            # remove rect
            bg_rect = rects_list[k]
            if bg_rect:
                self.remove(bg_rect)
                rects_list[k] = None

    def highlight(
        self,
        *code_indices: int,
        precode_indices: tuple[int, ...] | None = None,
    ):
        """Highlights one or more lines with background and text color.

        Args:
            *i: Tuple of code line indices to highlight.
            precode: Tuple of precode line indices to highlight, or None.
        """

        self._highlight_block(self._code_mobs, self._bg_rects_code, code_indices)

        if hasattr(self, "_precode_mobs"):
            if precode_indices is not None:
                self._highlight_block(
                    self._precode_mobs, self._bg_rects_precode, precode_indices
                )
            else:
                self._clear_block_highlights(self._precode_mobs, self._bg_rects_precode)

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

    @staticmethod
    def create_animation_template(code: str) -> None:
        """Generate animation scaffolding from algorithm code.

        This static method converts algorithm code into a template for Manim
        animation construction. It parses the code structure and generates
        corresponding highlight calls and wait statements.

        The generated template is copied to the system clipboard for easy
        insertion into Manim scene construct() method.

        Important:
            The CodeBlock instance in the scene must be named `code_block`
            for the generated template to work correctly.

        Args:
            code: Multiline string containing the algorithm code to animate.
        """
        code_lines = code.strip().split("\n")
        res = ""
        tab = "    "
        base_tab = tab * 2
        i = 0
        for line in code_lines:
            line_lstrip = line.lstrip()
            indent = line[: len(line) - len(line_lstrip)]
            if line_lstrip.startswith("if "):
                line_1 = base_tab + indent + f"code_block.highlight({i})\n"
                line_2 = base_tab + indent + "self.wait(pause)\n"
                line_3 = base_tab + line + "\n"
                line_4 = base_tab + indent + tab + "#\n"
                add_block = line_1 + line_2 + line_3 + line_4
            elif (
                line_lstrip.startswith("for ")
                or line_lstrip.startswith("while ")
                or line_lstrip.startswith("else ")
                or line_lstrip.startswith("elif ")
            ):
                line_1 = base_tab + line + "\n"
                line_2 = base_tab + indent + tab + f"code_block.highlight({i})\n"
                line_3 = base_tab + indent + tab + "self.wait(pause)\n"
                line_4 = base_tab + indent + tab + "#\n"
                add_block = line_1 + line_2 + line_3 + line_4
            elif line_lstrip.startswith("return "):
                line_1 = base_tab + "# " + line + "\n"
                line_2 = base_tab + indent + f"code_block.highlight({i})\n"
                line_3 = base_tab + indent + "self.wait(pause)\n"
                line_4 = "\n"
                add_block = line_1 + line_2 + line_3 + line_4
            else:
                line_1 = base_tab + line + "\n"
                line_2 = base_tab + indent + f"code_block.highlight({i})\n"
                line_3 = base_tab + indent + "self.wait(pause)\n"
                line_4 = "\n"
                add_block = line_1 + line_2 + line_3 + line_4

            res += add_block
            i += 1

        pyperclip.copy(res)
