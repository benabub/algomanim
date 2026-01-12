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
            rects_list: list of background rectangles (parallel to code_mobs_list).
            indices: tuple of line indices to highlight.
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

    def _separate_indices(self, *indices) -> tuple[tuple[int, ...], tuple[int, ...]]:
        """Separates indices into precode and code tuples.

        Args:
            *indices: Line indices to separate.

        Returns:
            Tuple of (precode_indices, code_indices) where:
            - precode_indices: tuple of indices referring to precode lines
            - code_indices: tuple of indices referring to main code lines (rebase to 0)
        """
        len_precode_lines = len(self._precode_lines)

        if self._precode_lines:
            precode_indices = tuple(
                idx for idx in indices if idx in range(len_precode_lines)
            )
            code_indices = tuple(
                idx - len_precode_lines for idx in indices if idx >= len_precode_lines
            )
        else:
            precode_indices = ()
            code_indices = indices
        return precode_indices, code_indices

    def highlight(
        self,
        *indices: int,
    ):
        """Highlights one or more lines with background and text color.

        Args:
            *i: Tuple of code line indices to highlight.
        """

        precode_indices, code_indices = self._separate_indices(*indices)

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
    def create_animation_template(code: str, precode_len: int = 0) -> None:
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
        i = precode_len
        for j, line in enumerate(code_lines):
            line_lstrip = line.lstrip()
            indent = line[: len(line) - len(line_lstrip)]

            if line_lstrip.startswith("if ") or (
                j != 0 and line_lstrip.startswith("while ")
            ):
                line_1 = base_tab + indent + f"code_block.highlight({i})\n"
                line_2 = base_tab + indent + "self.wait(pause)\n"
                line_3 = base_tab + line + "\n"
                line_4 = base_tab + indent + tab + "#\n"
                add_block = line_1 + line_2 + line_3 + line_4
            elif (
                line_lstrip.startswith("for ")
                or line_lstrip.startswith("else")
                or line_lstrip.startswith("elif ")
                or (j == 0 and line_lstrip.startswith("while "))
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


class CodeBlockLense(AlgoManimBase):
    """Code block visualization with syntax highlighting capabilities.

    Args:
        code_lines: List of code lines to display.
        precode_lines: Lines to display before the main code.
        limit: ...
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
        dimm_opacity: ...

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
        limit: int = 7,
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
        # bg_rect_buff: float = 0.5,
        bg_rect_buff: float = 0.3,
        # --- highlights ---
        bg_highlight_color: ManimColor | str = mn.BLACK,
        dim_opacity: float = 0.5,
    ):
        super().__init__(
            vector=vector,
            mob_center=mob_center,
            align_left=align_left,
            align_right=align_right,
            align_top=align_top,
            align_bottom=align_bottom,
        )
        # checks
        if limit < 5:
            raise ValueError("limit must be at least 5")

        # self fields
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
        # --- bg_rect ---
        self._bg_rect_fill_color = bg_rect_fill_color
        self._bg_rect_stroke_width = bg_rect_stroke_width
        self._bg_rect_stroke_color = bg_rect_stroke_color
        self._bg_rect_corner_radius = bg_rect_corner_radius
        self._bg_rect_buff = bg_rect_buff
        # --- highlight ---
        self._highlight_rect = None  # the only highlight rect possible
        self._dimm_opacity = dim_opacity
        # --- limit ---
        if limit % 2:
            self._limit = limit
        else:
            self._limit = limit - 1
        # --- lengths ---
        self._code_lines_len = len(self._code_lines)
        self._precode_lines_len = len(self._precode_lines)  # default=0

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

        self._code_mobs = [
            mn.Text(
                line,
                font=self._font,
                font_size=self._font_size,
                color=self._text_color_regular,
            )
            for line in self._code_lines
        ]

        self._bg_rect = self._bg_rect_construct()
        self._bg_rect.z_index = -2
        self.add(self._bg_rect)
        self._position()

        self._text_left_edge = self._bg_rect.get_left()[0] + (self._bg_rect_buff / 2)

        precode_indices, code_indices = self._get_initial_indices()
        self._text_vgroup = self._construct_text_vgroup(precode_indices, code_indices)

        self._position_text_vgroup()

        self._dim_lines(-1)

        self.add(self._text_vgroup)

    def _position_text_vgroup(self):
        """
        ...
        """
        self._text_vgroup.move_to(self._bg_rect)
        shift_x = self._text_left_edge - self._text_vgroup.get_left()[0]
        self._text_vgroup.shift(mn.RIGHT * shift_x)

    def _bg_rect_construct(self):
        """
        ...
        """

        # find bg_rect wigth
        if not self._precode_lines:
            text_width = max([line_mob.width for line_mob in self._code_mobs])
        else:
            max_width_precode = max([line_mob.width for line_mob in self._precode_mobs])
            max_width_code = max([line_mob.width for line_mob in self._code_mobs])
            text_width = max(max_width_precode, max_width_code)

        # find bg_rect height
        spec_symbol_mob_height = mn.Text(
            "│",
            font=self._font,
            font_size=self._font_size,
            color=self._text_color_regular,
        ).height
        text_height = self._limit * spec_symbol_mob_height + self._code_buff * (
            self._limit - 1
        )

        # if self._precode_lines:
        #     text_height += self._between_blocks_buff
        # else:
        #     text_height += self._code_buff

        # mob construction
        bg_rect = mn.RoundedRectangle(
            width=text_width + self._bg_rect_buff,
            height=text_height + self._bg_rect_buff * 2,
            fill_color=self._bg_rect_fill_color,
            fill_opacity=1,
            stroke_width=self._bg_rect_stroke_width,
            stroke_color=self._bg_rect_stroke_color,
            corner_radius=self._bg_rect_corner_radius,
        )
        return bg_rect

    def _construct_text_vgroup(
        self,
        precode_indices: tuple[int, ...] = (),
        code_indices: tuple[int, ...] = (),
    ):
        mobs = []

        if precode_indices:
            if not self._precode_lines:
                raise ValueError(
                    "precode_indices passed without precode_lines in instance"
                )

            precode_mobs = [self._precode_mobs[i] for i in precode_indices]
            mobs.extend(precode_mobs)

        code_mobs = [self._code_mobs[i] for i in code_indices]
        mobs.extend(code_mobs)

        text_vgroup = mn.VGroup(*mobs)

        # arranging
        for i, mob in enumerate(mobs[1:]):
            prev_mob = mobs[i]
            if i < len(precode_indices) - 1:
                buff = self._precode_buff
            elif i == len(precode_indices) - 1 and code_indices:
                buff = self._between_blocks_buff
            else:
                buff = self._code_buff
            mob.next_to(
                prev_mob,
                mn.DOWN,
                buff=buff,
                aligned_edge=mn.LEFT,
            )

        return text_vgroup

    def _get_initial_indices(self):
        """
        ...
        """
        precode_indices = []
        code_indices = []

        precode_len = len(self._precode_lines)

        for idx in range(self._limit):
            if idx < precode_len:
                precode_indices.append(idx)
            else:
                code_indices.append(idx - precode_len)
        return tuple(precode_indices), tuple(code_indices)

    def _get_indices_for_highlight(self):
        """
        ...
        """
        ...

    def _dim_lines(self, *indices: int):
        """
        ...
        """
        for idx in indices:
            self._text_vgroup[idx].set_opacity(self._dimm_opacity)

    # def highlight(self, block_line_idx: int):
    #     # block_line_idx = 0..(precode_len + code_len - 1)
    #     if block_line_idx < self._precode_lines_len:
    #         # Это прекод
    #         precode_idx = block_line_idx
    #         code_idx = None
    #     else:
    #         # Это код
    #         precode_idx = None
    #         code_idx = block_line_idx - self._precode_lines_len
    #
    #     # Вычисляем срезы для прокрутки
    #     precode_indices, code_indices = self._get_indices_for_highlight(code_idx, precode_idx)

    # def highlight(self, *code_indices, precode_indices=None):
    #     # Удалить старый прямоугольник
    #     if self._current_highlight_rect:
    #         self.remove(self._current_highlight_rect)
    #         self._current_highlight_rect = None
    #
    #     # Создать новый на основе новых позиций строк
    #     # ...

    # def _highlight_block(
    #     self,
    #     code_mobs_list: List[mn.Text],
    #     rects_list: List[mn.Rectangle | None],
    #     indices: tuple[int, ...],
    # ) -> None:
    #     """Helper method to highlight lines in a code block.
    #
    #     Args:
    #         code_mobs_list: List of text mobjects to highlight.
    #         rects_list: List of background rectangles (parallel to code_mobs_list).
    #         indices: Tuple of line indices to highlight.
    #     """
    #     for k, mob in enumerate(code_mobs_list):
    #         if k in indices:
    #             # change font color
    #             mob.set_color(self._text_color_highlight)
    #             # create bg rectangle
    #             if rects_list[k] is None:
    #                 bg_rect = mn.Rectangle(
    #                     width=mob.width + 0.2,
    #                     height=mob.height + 0.1,
    #                     fill_color=self._bg_highlight_color,
    #                     fill_opacity=1,
    #                     stroke_width=0,
    #                 )
    #                 bg_rect.move_to(mob.get_center())
    #                 self.add(bg_rect)
    #                 bg_rect.z_index = -1  # medium layout
    #                 rects_list[k] = bg_rect
    #         else:
    #             # normal line: regular font color
    #             mob.set_color(self._text_color_regular)
    #             # remove rect
    #             bg_rect = rects_list[k]
    #             if bg_rect:
    #                 self.remove(bg_rect)
    #                 rects_list[k] = None

    # def _clear_block_highlights(
    #     self,
    #     code_mobs_list: List[mn.Text],
    #     rects_list: List[mn.Rectangle | None],
    # ) -> None:
    #     """Clear all highlights from a code block.
    #
    #     Args:
    #         code_mobs_list: List of text mobjects in the block.
    #         rects_list: List of background rectangles (parallel to code_mobs_list).
    #     """
    #
    #     for k, mob in enumerate(code_mobs_list):
    #         # normal line: regular font color
    #         mob.set_color(self._text_color_regular)
    #         # remove rect
    #         bg_rect = rects_list[k]
    #         if bg_rect:
    #             self.remove(bg_rect)
    #             rects_list[k] = None

    # def highlight(
    #     self,
    #     *code_indices: int,
    #     precode_indices: list[int] | None = None,
    # ):
    #     """Highlights one or more lines with background and text color.
    #
    #     Args:
    #         *i: Tuple of code line indices to highlight.
    #         precode: list of precode line indices to highlight, or None.
    #     """
    #
    #     self._highlight_block(self._code_mobs, self._bg_rects_code, code_indices)
    #
    #     if hasattr(self, "_precode_mobs"):
    #         if precode_indices is not None:
    #             self._highlight_block(
    #                 self._precode_mobs, self._bg_rects_precode, tuple(precode_indices)
    #             )
    #         else:
    #             self._clear_block_highlights(self._precode_mobs, self._bg_rects_precode)
