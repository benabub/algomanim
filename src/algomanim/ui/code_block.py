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
        font_size: int = 20,
        font: str = "",
        text_color_regular: ManimColor | str = "WHITE",
        text_color_highlight: ManimColor | str = "YELLOW",
        # --- buffs ---
        code_buff: float = 0.05,
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
    """Code block with limited viewport and scrolling highlighting.

    Displays only `limit` lines at a time, dimming boundary lines when scrolling.
    Designed for long code blocks where full display is impractical.

    Args:
        code_lines: List of code lines to display.
        limit: Maximum number of visible lines (odd number, minimum 5).
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
        dim_high: Opacity for strongly dimmed boundary lines.
        dim_low: Opacity for weakly dimmed boundary lines.

    Raises:
        ValueError: If `limit` < 5, or `len(code_lines)` <= `limit`.
    """

    def __init__(
        self,
        code_lines: list[str],
        limit: int = 13,
        # --- position ---
        vector: np.ndarray = mn.ORIGIN,
        mob_center: mn.Mobject = mn.Dot(mn.ORIGIN),
        align_left: mn.Mobject | None = None,
        align_right: mn.Mobject | None = None,
        align_top: mn.Mobject | None = None,
        align_bottom: mn.Mobject | None = None,
        # --- font ---
        font_size: int = 20,
        font: str = "",
        text_color_regular: ManimColor | str = "WHITE",
        text_color_highlight: ManimColor | str = "YELLOW",
        # --- buffs ---
        code_buff: float = 0.05,
        # --- bg_rect ---
        bg_rect_fill_color: ManimColor | str = "#545454",
        bg_rect_stroke_width: float = 4,
        bg_rect_stroke_color: ManimColor | str = "#151515",
        bg_rect_corner_radius: float = 0.1,
        # bg_rect_buff: float = 0.5,
        bg_rect_buff: float = 0.3,
        # --- highlights ---
        bg_highlight_color: ManimColor | str = mn.BLACK,
        dim_high: float = 0.3,
        dim_low: float = 0.7,
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
        # checks
        if limit < 7:
            raise ValueError("limit must be at least 7")

        if len(self._code_lines) <= limit:
            raise ValueError("code lines <= limit (too short), use CodeBlock instead")

        # self fields
        # --- dim ---
        self._dim_high = dim_high
        self._dim_low = dim_low
        # --- limit ---
        if limit % 2:
            self._limit = limit
        else:
            self._limit = limit - 1
        # --- highlights ---
        self._highlighted_indices = set()

        self._text_mobs = self._create_text_mobs()
        self._rect_mobs = self._create_rect_mobs(self._text_mobs)
        self._line_vgroups = self._create_line_vgroups(
            self._rect_mobs,
            self._text_mobs,
        )

        self._bg_rect = self._create_bg_rect(
            max([mob.width for mob in self._rect_mobs]),
            self._rect_height * self._limit,
        )
        self.add(self._bg_rect)
        self._position()

        self._text_left_edge = self._bg_rect.get_left()[0] + (self._bg_rect_buff / 2)

        self._code_vgroup = self._create_code_vgroup(0)
        self._position_code_vgroup(self._code_vgroup)

        self._dim_lines(self._code_vgroup, (-1,), (-2,))

        self.add(self._code_vgroup)

    def _create_code_vgroup(self, start: int) -> mn.VGroup:
        """Create a VGroup containing visible lines for the given start index.

        Args:
            start: Starting line index (0-based) for the visible window.

        Returns:
            VGroup containing `limit` line groups arranged vertically.

        Raises:
            ValueError: If `start` is out of valid range.
        """
        if start < 0 or start + self._limit > len(self._code_lines):
            raise ValueError("start index out of scope")

        split = self._line_vgroups[start : start + self._limit]
        code_vgroup = mn.VGroup(*split).arrange(
            mn.DOWN,
            aligned_edge=mn.LEFT,
            buff=0,
        )
        return code_vgroup

    def _position_code_vgroup(self, code_vgroup: mn.VGroup) -> None:
        """Position the code VGroup within the background rectangle.

        Aligns left edge with internal text boundary and centers vertically.

        Args:
            code_vgroup: The VGroup to position.
        """
        code_vgroup.move_to(self._bg_rect)
        shift_x = self._text_left_edge - code_vgroup.get_left()[0]
        code_vgroup.shift(mn.RIGHT * shift_x)

    def _dim_lines(
        self,
        code_vgroup: mn.VGroup,
        dim_high_indices: tuple[int, ...],
        dim_low_indices: tuple[int, ...],
    ) -> None:
        """Apply dimming opacity to lines with two intensity levels.

        Args:
            code_vgroup: VGroup containing line groups.
            dim_high_indices: Line indices for strong dimming.
            dim_low_indices: Line indices for weak dimming.
        """

        for idx in dim_high_indices:
            code_vgroup[idx][1].set_opacity(self._dim_high)
        for idx in dim_low_indices:
            code_vgroup[idx][1].set_opacity(self._dim_low)

    def _get_dim_indices_for_highlight(
        self, *indices: int
    ) -> tuple[tuple[int, ...], tuple[int, ...]]:
        """Calculate which lines to dim based on highlight position.

        Args:
            *indices: Highlighted line indices (global).

        Returns:
            Tuple of two tuples: (dim_high_indices, dim_low_indices) where
            each contains line indices within the current viewport.
        """

        first_idx = indices[0]
        total_len = len(self._line_vgroups)
        middle = self._limit // 2 + 1

        if first_idx <= 1:
            dim_low = (-2,)
            dim_high = (-1,)
        elif 1 < first_idx < middle:
            dim_low = (0, -2)
            dim_high = (-1,)
        elif total_len - middle < first_idx < total_len - 2:
            dim_low = (1, -1)
            dim_high = (0,)
        elif first_idx >= total_len - 2:
            dim_high = (0,)
            dim_low = (1,)
        else:
            dim_high = (0, -1)
            dim_low = (1, -2)

        return dim_high, dim_low

    def _get_code_index_for_highlight(self, *indices: int) -> int:
        """Calculate starting index for viewport to center highlights.

        Args:
            *indices: Highlighted line indices (global).

        Returns:
            Start index for the visible window.
        """
        first_idx = indices[0]
        total_len = len(self._line_vgroups)
        middle = self._limit // 2 + 1

        # top lines only
        if first_idx < middle:
            return 0
        # bottom lines only
        elif first_idx >= total_len - middle:
            return total_len - self._limit
        # fix first_idx in middle position
        else:
            return first_idx - middle + 1

    def highlight(
        self,
        scene: mn.Scene,
        *indices: int,
    ) -> None:
        """Highlight lines and scroll viewport to center them.

        Args:
            scene: Manim scene for rendering updates.
            *indices: Consecutive line indices to highlight (global 0-based).

        Raises:
            ValueError: If indices are not consecutive or exceed limit//2.
        """

        # --- checks ---
        if not indices:
            return
        if not list(indices) == list(range(min(indices), max(indices) + 1)):
            raise ValueError("indices must be consecutive integers")
        if len(indices) > self._limit // 2:
            raise ValueError(
                f"Cannot highlight {len(indices)} lines, maximum is {self._limit // 2}"
            )

        # --- calculate new viewport ---
        start_idx = self._get_code_index_for_highlight(*indices)
        new_code_vgroup = self._create_code_vgroup(start_idx)
        dim_indices = self._get_dim_indices_for_highlight(*indices)

        # --- clear old dim ---
        for i in range(len(self._code_vgroup)):
            self._code_vgroup[i][1].set_opacity(1.0)

        # --- apply new dim ---
        self._dim_lines(new_code_vgroup, *dim_indices)

        # --- transfer highlights ---
        for i in range(len(new_code_vgroup)):
            global_idx = start_idx + i
            if global_idx in self._highlighted_indices:
                if global_idx not in indices:
                    if self._text_mobs[global_idx]:
                        new_code_vgroup[i][1].set_color(self._text_color_regular)
                        new_code_vgroup[i][0].set_fill_color(self._bg_rect_fill_color)
            elif global_idx in indices:
                if self._text_mobs[global_idx]:
                    new_code_vgroup[i][1].set_color(self._text_color_highlight)
                    new_code_vgroup[i][0].set_fill_color(self._bg_highlight_color)

        # --- update ---
        self._highlighted_indices = set(indices)
        self._position_code_vgroup(new_code_vgroup)

        scene.remove(self._code_vgroup)
        self._code_vgroup = new_code_vgroup
        scene.add(self._code_vgroup)
