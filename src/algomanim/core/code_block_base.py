import manim as mn
import re
from manim import ManimColor

from algomanim.core.paths.semi_rounded_rectangle import SemiRoundedRectangle
from algomanim.helpers.parsing import code_to_lines

from .base import AlgoManimBase


class CodeBlockBase(AlgoManimBase):
    """Base class for Code Blocks.

    Warning:
        This is base class only, cannot be instantiated directly.

    Args:
        code: Multiline string of code (first line must be empty).
        head: Multiline string of head block text (first line must be empty).
        limit: Maximum number of visible lines (for CodeBlockLense only).
        font_size: Common font size for all the text.
        font: Common Font family for all the text. Defaults to system default.
        code_buff: Common vertical buffer between codelines vgroups.
        rect_stroke_width: Stroke width for the code block container.
        rect_stroke_color: Stroke color for the code block container.
        rect_corner_radius: Corner radius for the rounded rectangle container.
        rect_buff: Padding around the code text within the background container.
        code_rect_fill_color: Background fill color for the code block container.
        code_highlight_color: Background color for highlighted lines.
        code_text_color_regular: Color for regular (non-highlighted) text.
        code_text_color_highlight: Color for highlighted text.
        head_fill_color: Background fill color for the head block.
        head_text_color: Text color for the head block.
    """

    def __init__(
        self,
        # --- texts ---
        code: str,
        head: str = "",
        # --- limit ---
        limit: int | None = None,
        # --- common font ---
        font_size: int = 20,
        font: str = "",
        # --- common buffs ---
        code_buff: float = 0.05,
        # --- common rect ---
        rect_stroke_width: float = 4,
        rect_stroke_color: ManimColor | str = "#151515",
        rect_corner_radius: float = 0.1,
        rect_buff: float = 0.2,
        # --- code block ---
        code_rect_fill_color: ManimColor | str = "#545454",
        code_rect_highlight_color: ManimColor | str = mn.BLACK,
        code_text_color_regular: ManimColor | str = "WHITE",
        code_text_color_highlight: ManimColor | str = "YELLOW",
        # --- head block ---
        head_fill_color: ManimColor | str = mn.GRAY_BROWN,
        head_text_color: ManimColor | str = mn.PURPLE,
        # --- kwargs ---
        **kwargs,
    ):
        super().__init__(**kwargs)

        # --- texts ---
        self._code_lines = self._format_code_lines(code)
        self._head_code_lines = self._format_code_lines(head)
        # --- common font ---
        self._font_size = font_size
        self._font = font
        # --- common buffs ---
        self._code_buff = code_buff
        # --- common rect ---
        self._rect_stroke_width = rect_stroke_width
        self._rect_stroke_color = rect_stroke_color
        self._rect_corner_radius = rect_corner_radius
        self._rect_buff = rect_buff
        # --- code block ---
        self._code_rect_fill_color = code_rect_fill_color
        self._code_rect_highlight_color = code_rect_highlight_color
        self._code_text_color_regular = code_text_color_regular
        self._code_text_color_highlight = code_text_color_highlight
        # --- head block ---
        self._head_fill_color = head_fill_color
        self._head_text_color = head_text_color
        # --- line rect params ---
        self._line_rect_height = self._get_rect_height()
        # --- block's dicts ---
        self._code_params = {
            "fill_color": self._code_rect_fill_color,
            "text_color": self._code_text_color_regular,
            "weight": mn.NORMAL,
        }
        self._head_params = {
            "fill_color": self._head_fill_color,
            "text_color": self._head_text_color,
            "weight": mn.BOLD,
        }
        # --- head ---
        self._has_head = bool(head)
        # --- limit ---
        if limit is not None:
            if limit % 2:
                self._limit = limit
            else:
                self._limit = limit - 1
        else:
            self._limit = limit

        # ----- code block attrs ---------

        self._code_text_mobs = self._create_text_mobs(
            self._code_lines,
            self._code_params,
        )
        self._code_rect_mobs = self._create_rect_mobs(
            self._code_text_mobs,
            self._code_params,
        )
        self._code_line_vgroups = self._create_line_vgroups(
            self._code_rect_mobs,
            self._code_text_mobs,
        )

        # ----- head block attrs ---------

        self._head_text_mobs = self._create_text_mobs(
            self._head_code_lines,
            self._head_params,
        )
        self._head_rect_mobs = self._create_rect_mobs(
            self._head_text_mobs,
            self._head_params,
        )
        self._head_line_vgroups = self._create_line_vgroups(
            self._head_rect_mobs,
            self._head_text_mobs,
        )

        # ----- max line vgroup width ---------
        self._max_line_width = self._find_max_line_width()

        # ----- _code_vgroup height (difine in childs) ------
        self._code_vgroup_height = self._find_code_vgroup_height()

        # ----- rects ---------

        self._code_rect = self._create_bg_rect(
            self._max_line_width,
            self._code_vgroup_height,
            self._has_head,  # defines the shape of a self._bg_rect
        )
        self.add(self._code_rect)

        if self._has_head:
            self._head = self._create_head()
            self._head.next_to(self._code_rect, mn.UP, buff=0)
            self.add(self._head)

        self._position()

    def _find_max_line_width(self) -> float:
        """Find the maximum width among all line VGroups.

        Returns:
            Maximum line width in units.
        """
        lines_width_list = []

        for group in (self._code_line_vgroups, self._head_line_vgroups):
            width_list = [mob.width for mob in group]
            lines_width_list += width_list

        return max(lines_width_list)

    def _find_code_vgroup_height(self) -> float:
        """Calculate the height of the code VGroup.

        Returns:
            Height of code VGroup, respecting limit if set.
        """
        if self._limit is None:
            return self._line_rect_height * len(self._code_lines)
        else:
            return self._line_rect_height * self._limit

    def _align_code_vgroup(
        self,
        code_vgroup: mn.VGroup,
        rect: mn.Mobject,
    ) -> None:
        """Align code VGroup to the left edge of a rectangle and center vertically.

        Args:
            code_vgroup: The code VGroup to align.
            rect: The reference rectangle.
        """
        code_vgroup.move_to(rect)
        code_vgroup.align_to(rect, mn.LEFT)
        half_buff = self._rect_buff / 2
        code_vgroup.shift(mn.RIGHT * half_buff)

    def _get_rect_height(self):
        """Calculate the standard height for line rectangles.

        Returns:
            Height based on font size and line spacing buffer.
        """
        spec_mob = mn.Text(
            "│",
            font=self._font,
            font_size=self._font_size,
        )
        return spec_mob.height + self._code_buff

    def _create_text_mobs(
        self,
        code_lines: list[str],
        params: dict,
    ):
        """Create text mobjects for each code line.

        Returns:
            List of text mobjects.
        """
        text_mobs = [
            mn.Text(
                line,
                font=self._font,
                font_size=self._font_size,
                weight=params["weight"],
                color=params["text_color"],
            )
            for line in code_lines
        ]
        return text_mobs

    def _create_rect_mobs(
        self,
        text_mobs: list[mn.Text],
        params: dict,
    ):
        """Create background rectangles for each line.

        Returns:
            List of Rectangle mobjects sized according to line content.
            Non-empty lines have width matching text width,
               empty lines use standard height.
        """
        rect_mobs = []
        for line in text_mobs:
            if line:  # not empty
                rect = mn.Rectangle(
                    width=line.width + 0.2,
                    height=self._line_rect_height,
                    fill_color=params["fill_color"],
                    # fill_color=mn.BLUE,
                    fill_opacity=1,
                    stroke_width=0,
                )
            else:  # empty line
                rect = mn.Rectangle(
                    width=self._line_rect_height,
                    height=self._line_rect_height,
                    fill_color=params["fill_color"],
                    fill_opacity=1,
                    stroke_width=0,
                )
            rect_mobs.append(rect)
        return rect_mobs

    def _create_line_vgroups(
        self,
        rect_mobs: list[mn.Rectangle],
        text_mobs: list[mn.Text],
    ):
        """Create VGroups pairing rectangles with text mobjects.

        Returns:
            List of VGroups where each contains (rectangle, text) centered together.
        """
        line_vgroups = []
        for i in range(len(rect_mobs)):
            group = mn.VGroup(
                rect_mobs[i],
                text_mobs[i],
            )
            text_mobs[i].move_to(rect_mobs[i])
            line_vgroups.append(group)
        return line_vgroups

    def _create_head_rect(
        self,
        text_block_width: float,
        text_block_height: float,
    ) -> mn.VMobject:
        """Create the head rectangle with rounded top corners.

        Args:
            text_block_width: Width of the head text content.
            text_block_height: Height of the head text content.

        Returns:
            SemiRoundedRectangle configured as head block.
        """

        return SemiRoundedRectangle(
            width=text_block_width + self._rect_buff,
            height=text_block_height + self._rect_buff * 0.25,
            stroke_color=self._rect_stroke_color,
            stroke_width=self._rect_stroke_width,
            fill_color=self._head_fill_color,
        )

    def _create_head(self) -> mn.VGroup:
        """Create the head block with rectangle and text lines.

        Returns:
            VGroup containing head rectangle and text VGroup.
        """
        head_code_vgroup = mn.VGroup(*self._head_line_vgroups).arrange(
            mn.DOWN,
            aligned_edge=mn.LEFT,
            buff=0,
        )
        head_rect = self._create_head_rect(
            self._max_line_width,
            head_code_vgroup.height,
        )

        self._align_code_vgroup(head_code_vgroup, head_rect)

        head_group = mn.VGroup(head_rect, head_code_vgroup)
        return head_group

    def _create_bg_rect(
        self,
        text_block_width: float,
        text_block_height: float,
        has_head: bool,
    ):
        """Create the background rounded rectangle for the code block.

        Args:
            text_block_width: total width of the text content.
            text_block_height: total height of the text content.

        Returns:
            RoundedRectangle mobject with padding and styling configured
            from instance parameters.
        """

        if has_head:
            bg_rect = SemiRoundedRectangle(
                direction=mn.DOWN,
                width=text_block_width + self._rect_buff,
                height=text_block_height + self._rect_buff,
                fill_color=self._code_rect_fill_color,
                # fill_opacity=1,
                stroke_width=self._rect_stroke_width,
                stroke_color=self._rect_stroke_color,
                corner_radius=self._rect_corner_radius,
            )
        else:
            bg_rect = mn.RoundedRectangle(
                width=text_block_width + self._rect_buff,
                height=text_block_height + self._rect_buff,
                fill_color=self._code_rect_fill_color,
                fill_opacity=1,
                stroke_width=self._rect_stroke_width,
                stroke_color=self._rect_stroke_color,
                corner_radius=self._rect_corner_radius,
            )
        return bg_rect

    def _format_code_lines(self, code: str) -> list[str]:
        """Format code string into indented lines with tree markers.

        Strips trailing inline commands (patterns ending with '=.' followed by
        command characters) used by create_animation_template_sound() for
        generating animation scaffolding with sound blocks.

        Args:
            code: Multiline code string.

        Returns:
            list[str]: Lines formatted with '│   ' prefixes
              for indentation levels and stripped of inline commands.
        """
        lines = code_to_lines(code)
        res = []
        for line in lines:
            indent = len(line) - len(line.lstrip())
            prefix = "│   " * (indent // 4)
            line = prefix + line.lstrip()

            if re.search(r"=[^\s]+$", line):
                line = line.rsplit(" ", 1)[0]

            res.append(line)

        return res
