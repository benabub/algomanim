import manim as mn
from manim import ManimColor
import pyperclip

from .base import AlgoManimBase


class CodeBlockBase(AlgoManimBase):
    """Base class for Code Blocks.

    Warning:
        This is base class only, cannot be instantiated directly.

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
        # --- kwargs ---
        **kwargs,
    ):
        super().__init__(**kwargs)

        self._code_lines = code_lines
        # --- font ---
        self._font_size = font_size
        self._font = font
        self._text_color_regular = text_color_regular
        self._text_color_highlight = text_color_highlight
        # --- buffs ---
        self._code_buff = code_buff
        # --- bg_rect ---
        self._bg_rect_fill_color = bg_rect_fill_color
        self._bg_rect_stroke_width = bg_rect_stroke_width
        self._bg_rect_stroke_color = bg_rect_stroke_color
        self._bg_rect_corner_radius = bg_rect_corner_radius
        self._bg_rect_buff = bg_rect_buff
        # --- highlights ---
        self._bg_highlight_color = bg_highlight_color
        # --- rect params ---
        self._rect_height = self._get_rect_height()

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

    def _create_text_mobs(self):
        """Create text mobjects for each code line.

        Returns:
            List of text mobjects.
        """
        text_mobs = [
            mn.Text(
                line,
                font=self._font,
                font_size=self._font_size,
                color=self._text_color_regular,
            )
            for line in self._code_lines
        ]
        return text_mobs

    def _create_rect_mobs(
        self,
        text_mobs: list[mn.Text],
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
                    height=self._rect_height,
                    fill_color=self._bg_rect_fill_color,
                    fill_opacity=1,
                    stroke_width=0,
                )
            else:  # empty line
                rect = mn.Rectangle(
                    width=self._rect_height,
                    height=self._rect_height,
                    fill_color=self._bg_rect_fill_color,
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

    def _create_bg_rect(
        self,
        text_block_width: float,
        text_block_height: float,
    ):
        """Create the background rounded rectangle for the code block.

        Args:
            text_block_width: total width of the text content.
            text_block_height: total height of the text content.

        Returns:
            RoundedRectangle mobject with padding and styling configured
            from instance parameters.
        """
        bg_rect = mn.RoundedRectangle(
            width=text_block_width + self._bg_rect_buff,
            height=text_block_height + self._bg_rect_buff,
            fill_color=self._bg_rect_fill_color,
            fill_opacity=1,
            stroke_width=self._bg_rect_stroke_width,
            stroke_color=self._bg_rect_stroke_color,
            corner_radius=self._bg_rect_corner_radius,
        )
        return bg_rect

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
        for j, line in enumerate(code_lines):
            line_lstrip = line.lstrip()
            indent = line[: len(line) - len(line_lstrip)]

            if not line_lstrip:
                i += 1
                continue
            elif line_lstrip.startswith("if ") or (
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
