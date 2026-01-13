import numpy as np
import manim as mn
from manim import ManimColor

from ..core.code_block_base import CodeBlockBase


class CodeBlock(CodeBlockBase):
    """Code block visualization with syntax highlighting capabilities.

    Args:
        code_lines: List of code lines to display.
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
        code_buff: Vertical buffer between code lines.
        bg_rect_fill_color: Background fill color for the code block container.
        bg_rect_stroke_width: Stroke width for the code block container.
        bg_rect_stroke_color: Stroke color for the code block container.
        bg_rect_corner_radius: Corner radius for the rounded rectangle container.
        bg_rect_buff: Padding around the code text within the background container.
        bg_highlight_color: Background color for highlighted lines.
    """

    def __init__(
        self,
        code_lines: list[str],
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
        code_buff=0.05,
        # --- bg_rect ---
        bg_rect_fill_color: ManimColor | str = "#545454",
        bg_rect_stroke_width: float = 4,
        bg_rect_stroke_color: ManimColor | str = "#151515",
        bg_rect_corner_radius: float = 0.1,
        bg_rect_buff: float = 0.2,
        # --- highlights ---
        bg_highlight_color: ManimColor | str = mn.BLACK,
    ):
        super().__init__(
            code_lines=code_lines,
            # --- position ---
            vector=vector,
            mob_center=mob_center,
            align_left=align_left,
            align_right=align_right,
            align_top=align_top,
            align_bottom=align_bottom,
            # --- font ---
            font_size=font_size,
            font=font,
            text_color_regular=text_color_regular,
            text_color_highlight=text_color_highlight,
            # --- buffs ---
            code_buff=code_buff,
            # --- bg_rect ---
            bg_rect_fill_color=bg_rect_fill_color,
            bg_rect_stroke_width=bg_rect_stroke_width,
            bg_rect_stroke_color=bg_rect_stroke_color,
            bg_rect_corner_radius=bg_rect_corner_radius,
            bg_rect_buff=bg_rect_buff,
            # --- highlights ---
            bg_highlight_color=bg_highlight_color,
        )

        # --- highlights ---
        self._highlighted_indices: set[int] = set()

        self._text_mobs = self._create_text_mobs()
        self._rect_mobs = self._create_rect_mobs(self._text_mobs)
        self._line_vgroups = self._create_line_vgroups(
            self._rect_mobs,
            self._text_mobs,
        )

        self._code_vgroup = mn.VGroup(*self._line_vgroups).arrange(
            mn.DOWN,
            aligned_edge=mn.LEFT,
            buff=0,
        )

        self._bg_rect = self._create_bg_rect(
            self._code_vgroup.width, self._code_vgroup.height
        )

        self.add(self._bg_rect)
        self._position()

        self._code_vgroup.move_to(self._bg_rect)
        self.add(self._code_vgroup)

    def highlight(self, *indices: int):
        """Highlight specified lines by changing text and rectangle colors.

        Maintains internal set of highlighted indices to minimize state changes.
        Empty lines are ignored.

        Args:
            *indices: line indices to highlight.

        Note:
            Previous highlights are cleared from lines not in the new indices.
        """
        new_highlighted = set(indices)

        # Clear old highlights
        for idx in self._highlighted_indices - new_highlighted:
            if self._text_mobs[idx]:
                self._text_mobs[idx].set_color(self._text_color_regular)
                self._rect_mobs[idx].set_fill_color(self._bg_rect_fill_color)

        # Apply new highlights
        for idx in new_highlighted - self._highlighted_indices:
            if self._text_mobs[idx]:
                self._text_mobs[idx].set_color(self._text_color_highlight)
                self._rect_mobs[idx].set_fill_color(self._bg_highlight_color)

        self._highlighted_indices = new_highlighted


class CodeBlockLense(CodeBlockBase):
    ...

    # """Code block visualization with syntax highlighting capabilities.
    #
    # Args:
    #     code_lines: List of code lines to display.
    #     precode_lines: Lines to display before the main code.
    #     limit: ...
    #     vector: Position offset from mob_center for positioning.
    #     mob_center: Reference mobject for positioning.
    #     align_left: Reference mobject to align left edge with.
    #     align_right: Reference mobject to align right edge with.
    #     align_top: Reference mobject to align top edge with.
    #     align_bottom: Reference mobject to align bottom edge with.
    #     font_size: Font size for the code text.
    #     font: Font family for the code text. Defaults to system default.
    #     text_color_regular: Color for regular (non-highlighted) text.
    #     text_color_highlight: Color for highlighted text.
    #     between_blocks_buff: Vertical buffer between pre-code and code blocks.
    #     precode_buff: Vertical buffer between pre-code lines.
    #     code_buff: Vertical buffer between code lines.
    #     bg_rect_fill_color: Background fill color for the code block container.
    #     bg_rect_stroke_width: Stroke width for the code block container.
    #     bg_rect_stroke_color: Stroke color for the code block container.
    #     bg_rect_corner_radius: Corner radius for the rounded rectangle container.
    #     bg_rect_buff: Padding around the code text within the background container.
    #     bg_highlight_color: Background color for highlighted lines.
    #     dimm_opacity: ...
    #
    # Note:
    #     The code block uses a layered z-index system:
    #     -2: Main background rectangle (deepest)
    #     -1: Line highlight rectangles
    #     -0: Text lines (topmost)
    # """
    #
    # def __init__(
    #     self,
    #     code_lines: List[str],
    #     precode_lines: List[str] = [],
    #     limit: int = 7,
    #     # --- position ---
    #     vector: np.ndarray = mn.ORIGIN,
    #     mob_center: mn.Mobject = mn.Dot(mn.ORIGIN),
    #     align_left: mn.Mobject | None = None,
    #     align_right: mn.Mobject | None = None,
    #     align_top: mn.Mobject | None = None,
    #     align_bottom: mn.Mobject | None = None,
    #     # --- font ---
    #     font_size=20,
    #     font="",
    #     text_color_regular: ManimColor | str = "WHITE",
    #     text_color_highlight: ManimColor | str = "YELLOW",
    #     # --- buffs ---
    #     between_blocks_buff=0.5,
    #     precode_buff=0.15,
    #     code_buff=0.05,
    #     # --- bg_rect ---
    #     bg_rect_fill_color: ManimColor | str = "#545454",
    #     bg_rect_stroke_width: float = 4,
    #     bg_rect_stroke_color: ManimColor | str = "#151515",
    #     bg_rect_corner_radius: float = 0.1,
    #     # bg_rect_buff: float = 0.5,
    #     bg_rect_buff: float = 0.3,
    #     # --- highlights ---
    #     bg_highlight_color: ManimColor | str = mn.BLACK,
    #     dim_opacity: float = 0.5,
    # ):
    #     super().__init__(
    #         vector=vector,
    #         mob_center=mob_center,
    #         align_left=align_left,
    #         align_right=align_right,
    #         align_top=align_top,
    #         align_bottom=align_bottom,
    #     )
    #     # checks
    #     if limit < 5:
    #         raise ValueError("limit must be at least 5")
    #
    #     # self fields
    #     self._code_lines = code_lines
    #     self._precode_lines = precode_lines
    #     self._all_code_lines = self._precode_lines + self._code_lines
    #     # --- font ---
    #     self._font_size = font_size
    #     self._font = font
    #     self._text_color_regular = text_color_regular
    #     self._text_color_highlight = text_color_highlight
    #     # --- buffs ---
    #     self._between_blocks_buff = between_blocks_buff
    #     self._precode_buff = precode_buff
    #     self._code_buff = code_buff
    #     # --- colors ---
    #     self._bg_highlight_color = bg_highlight_color
    #     # --- bg_rect ---
    #     self._bg_rect_fill_color = bg_rect_fill_color
    #     self._bg_rect_stroke_width = bg_rect_stroke_width
    #     self._bg_rect_stroke_color = bg_rect_stroke_color
    #     self._bg_rect_corner_radius = bg_rect_corner_radius
    #     self._bg_rect_buff = bg_rect_buff
    #     # --- highlight ---
    #     self._highlight_rect = None  # the only highlight rect possible
    #     self._dimm_opacity = dim_opacity
    #     # --- limit ---
    #     if limit % 2:
    #         self._limit = limit
    #     else:
    #         self._limit = limit - 1
    #     # --- lengths ---
    #     self._code_lines_len = len(self._code_lines)
    #     self._precode_lines_len = len(self._precode_lines)  # default=0
    #
    #     if self._precode_lines:
    #         self._precode_mobs = [
    #             mn.Text(
    #                 line,
    #                 font=self._font,
    #                 font_size=self._font_size,
    #                 color=self._text_color_regular,
    #             )
    #             for line in self._precode_lines
    #         ]
    #
    #     self._code_mobs = [
    #         mn.Text(
    #             line,
    #             font=self._font,
    #             font_size=self._font_size,
    #             color=self._text_color_regular,
    #         )
    #         for line in self._code_lines
    #     ]
    #
    #     self._bg_rect = self._bg_rect_construct()
    #     self._bg_rect.z_index = -2
    #     self.add(self._bg_rect)
    #     self._position()
    #
    #     self._text_left_edge = self._bg_rect.get_left()[0] + (self._bg_rect_buff / 2)
    #
    #     precode_indices, code_indices = self._get_initial_indices()
    #     self._text_vgroup = self._construct_text_vgroup(precode_indices, code_indices)
    #
    #     self._position_text_vgroup(self._text_vgroup)
    #
    #     self._dim_lines(self._text_vgroup, -1)
    #
    #     self.add(self._text_vgroup)
    #
    # def _position_text_vgroup(self, text_vgroup: mn.VGroup):
    #     """
    #     ...
    #     """
    #     text_vgroup.move_to(self._bg_rect)
    #     shift_x = self._text_left_edge - self._text_vgroup.get_left()[0]
    #     text_vgroup.shift(mn.RIGHT * shift_x)
    #
    # def _dim_lines(self, text_vgroup: mn.VGroup, *indices: int):
    #     """
    #     ...
    #     """
    #     for idx in indices:
    #         text_vgroup[idx].set_opacity(self._dimm_opacity)
    #
    # def _bg_rect_construct(self):
    #     """
    #     ...
    #     """
    #
    #     # find bg_rect wigth
    #     if not self._precode_lines:
    #         text_width = max([line_mob.width for line_mob in self._code_mobs])
    #     else:
    #         max_width_precode = max([line_mob.width for line_mob in self._precode_mobs])
    #         max_width_code = max([line_mob.width for line_mob in self._code_mobs])
    #         text_width = max(max_width_precode, max_width_code)
    #
    #     # find bg_rect height
    #     spec_symbol_mob_height = mn.Text(
    #         "│",
    #         font=self._font,
    #         font_size=self._font_size,
    #         color=self._text_color_regular,
    #     ).height
    #     text_height = self._limit * spec_symbol_mob_height + self._code_buff * (
    #         self._limit - 1
    #     )
    #
    #     # if self._precode_lines:
    #     #     text_height += self._between_blocks_buff
    #     # else:
    #     #     text_height += self._code_buff
    #
    #     # mob construction
    #     bg_rect = mn.RoundedRectangle(
    #         width=text_width + self._bg_rect_buff,
    #         height=text_height + self._bg_rect_buff * 2,
    #         fill_color=self._bg_rect_fill_color,
    #         fill_opacity=1,
    #         stroke_width=self._bg_rect_stroke_width,
    #         stroke_color=self._bg_rect_stroke_color,
    #         corner_radius=self._bg_rect_corner_radius,
    #     )
    #     return bg_rect
    #
    # def _construct_text_vgroup(
    #     self,
    #     precode_indices: tuple[int, ...] = (),
    #     code_indices: tuple[int, ...] = (),
    # ):
    #     """
    #     ...
    #     """
    #     mobs = []
    #
    #     if precode_indices:
    #         if not self._precode_lines:
    #             raise ValueError(
    #                 "precode_indices passed without precode_lines in instance"
    #             )
    #
    #         precode_mobs = [self._precode_mobs[i] for i in precode_indices]
    #         mobs.extend(precode_mobs)
    #
    #     code_mobs = [self._code_mobs[i] for i in code_indices]
    #     mobs.extend(code_mobs)
    #
    #     text_vgroup = mn.VGroup(*mobs)
    #
    #     # arranging
    #     for i, mob in enumerate(mobs[1:]):
    #         prev_mob = mobs[i]
    #         if i < len(precode_indices) - 1:
    #             buff = self._precode_buff
    #         elif i == len(precode_indices) - 1 and code_indices:
    #             buff = self._between_blocks_buff
    #         else:
    #             buff = self._code_buff
    #         mob.next_to(
    #             prev_mob,
    #             mn.DOWN,
    #             buff=buff,
    #             aligned_edge=mn.LEFT,
    #         )
    #
    #     return text_vgroup
    #
    # def _get_initial_indices(self):
    #     """
    #     ...
    #     """
    #     precode_indices = []
    #     code_indices = []
    #
    #     precode_len = len(self._precode_lines)
    #
    #     for idx in range(self._limit):
    #         if idx < precode_len:
    #             precode_indices.append(idx)
    #         else:
    #             code_indices.append(idx - precode_len)
    #     return tuple(precode_indices), tuple(code_indices)
    #
    # def _get_indices_for_highlight(self, *indices):
    #     first_idx = indices[0]
    #     total_len = len(self._all_code_lines)
    #     precode_len = len(self._precode_lines)
    #     middle = self._limit // 2 + 1
    #
    #     if first_idx <= middle:
    #         # top lines only
    #         return self._get_initial_indices()
    #
    #     elif first_idx >= total_len - middle:
    #         # bottom lines only
    #         start = max(0, total_len - self._limit)
    #         precode_indices = []
    #         code_indices = []
    #         for idx in range(start, total_len):
    #             if idx < precode_len:
    #                 precode_indices.append(idx)
    #             else:
    #                 code_indices.append(idx - precode_len)
    #         return tuple(precode_indices), tuple(code_indices)
    #
    #     else:
    #         # fix first_idx in middle position
    #         start = first_idx - (middle - 1)
    #         end = start + self._limit
    #         if end > total_len:
    #             end = total_len
    #             start = end - self._limit
    #
    #         precode_indices = []
    #         code_indices = []
    #         for idx in range(start, end):
    #             if idx < precode_len:
    #                 precode_indices.append(idx)
    #             else:
    #                 code_indices.append(idx - precode_len)
    #         return tuple(precode_indices), tuple(code_indices)
    #
    # # 0
    # # 1
    # # 2
    # # ----
    # # 3
    # # 4
    # # 5
    # # 6 --
    # # 7
    # # 8
    # # 9
    #
    # def _get_dim_indices_for_highlight(self, *indices):
    #     """
    #     ...
    #     """
    #     first_idx = indices[0]
    #
    #     if first_idx <= 1:
    #         dim_indices = (-1,)
    #
    #     elif first_idx >= len(self._all_code_lines) - 2:
    #         dim_indices = (0,)
    #
    #     else:
    #         dim_indices = 0, -1
    #
    #     return dim_indices
    #
    # def highlight(
    #     self,
    #     scene: mn.Scene,
    #     *indices,
    #     # run_time: float = 0.2,
    # ):
    #     """
    #     ...
    #     """
    #
    #     # --- checks ---
    #     if not list(indices) == list(range(min(indices), max(indices) + 1)):
    #         raise ValueError("indices must be consecutive integers")
    #     if len(indices) > self._limit // 2:
    #         raise ValueError(
    #             f"Cannot highlight {len(indices)} lines, maximum is {self._limit // 2}"
    #         )
    #
    #     # --- new_text_vgroup ---
    #
    #     precode_indices, code_indices = self._get_indices_for_highlight(*indices)
    #     new_text_vgroup = self._construct_text_vgroup(precode_indices, code_indices)
    #
    #     dim_indices = self._get_dim_indices_for_highlight(*indices)
    #     self._dim_lines(new_text_vgroup, *dim_indices)
    #
    #     scene.remove(self._text_vgroup)
    #     self._text_vgroup = new_text_vgroup
    #
    #     self._position_text_vgroup(self._text_vgroup)
    #     scene.add(self._text_vgroup)
    #
    #     # scene.play(mn.Transform(self._text_vgroup, new_text_vgroup), run_time=run_time)
    #     # self._text_vgroup = new_text_vgroup
