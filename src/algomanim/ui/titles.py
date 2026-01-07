import numpy as np
import manim as mn
from manim import ManimColor

from algomanim.core.base import AlgoManimBase


class TitleText(AlgoManimBase):
    """Title group with optional decorative flourish and text|svg undercaption.

    Args:
        text: The title text to display.
        mob_center: Reference mobject for positioning. Defaults to Dot(ORIGIN).
        vector: Offset vector from mob_center for positioning. Defaults to ORIGIN.
        align_left: Reference mobject to align left edge with.
        align_right: Reference mobject to align right edge with.
        align_top: Reference mobject to align top edge with.
        align_bottom: Reference mobject to align bottom edge with.
        font: Font family for the title text. Defaults to system default.
        font_size: Font size for the title text.
        text_color: Color of the title text. Defaults to WHITE.
        flourish: Whether to render decorative flourish under the text. Defaults to False.
        flourish_color: Color of the flourish line. Defaults to WHITE.
        flourish_stroke_width: Stroke width of the flourish. Defaults to 4.
        flourish_padding: Horizontal padding added to text width for flourish width.
            Defaults to 0.2.
        flourish_buff_manual: Manual override for vertical buffer between text and flourish.
            If 0 (default), buffer is auto-calculated based on text glyphs.
        spiral_offset: Vertical offset of spiral centers relative to flourish line.
            Defaults to 0.3.
        spiral_radius: Radius of the spiral ends. Defaults to 0.15.
        spiral_turns: Number of turns in each spiral. Defaults to 1.0.
        undercaption_text: Text to display below the flourish or text. Defaults to empty.
        undercaption_color: Color of the undercaption text. Defaults to WHITE.
        undercaption_font: Font family for the undercaption. Inherits from font if empty.
        undercaption_font_size: Font size for the undercaption. Defaults to 20.
        undercaption_svg: Path to SVG file to display as undercaption instead of text.
        svg_height: Height of the undercaption SVG. Defaults to 0.20.
        undercaption_buff_manual: Manual override for vertical buffer between
            text/flourish and undercaption. If 0 (default), buffer is auto-calculated.

    Note:
        Automatic buffer calculation depends on text:
        - If text contains descending characters (q, y, j, p, g):
          flourish_buff = 0.05, buff_increment = 0.15
        - Otherwise: flourish_buff = 0.15, buff_increment = 0.10
        - undercaption_buff = flourish_buff + buff_increment

    Raises:
        ValueError: If both align_left and align_right, or align_top and align_bottom
            are provided simultaneously.
    """

    def __init__(
        self,
        text: str,
        # --- position ---
        mob_center: mn.Mobject = mn.Dot(mn.ORIGIN),
        vector: np.ndarray = mn.ORIGIN,
        align_left: mn.Mobject | None = None,
        align_right: mn.Mobject | None = None,
        align_top: mn.Mobject | None = None,
        align_bottom: mn.Mobject | None = None,
        # --- font ---
        font: str = "",
        font_size: float = 40,
        text_color: ManimColor | str = "WHITE",
        # --- flourish ---
        flourish: bool = False,
        flourish_color: ManimColor | str = "WHITE",
        flourish_stroke_width: float = 4,
        flourish_padding: float = 0.2,
        flourish_buff_manual: float = 0.0,
        spiral_offset: float = 0.3,
        spiral_radius: float = 0.15,
        spiral_turns: float = 1.0,
        # --- undercaption ---
        undercaption_text: str = "",
        undercaption_color: ManimColor | str = "WHITE",
        undercaption_font: str = "",
        undercaption_font_size: float = 20,
        # --- undercaption svg ---
        undercaption_svg: str = "",
        svg_height: float = 0.20,
        # --- undercaption buff ---
        undercaption_buff_manual: float = 0.0,
    ):
        super().__init__(
            vector=vector,
            mob_center=mob_center,
            align_left=align_left,
            align_right=align_right,
            align_top=align_top,
            align_bottom=align_bottom,
        )

        self._flourish = flourish

        has_descenders = not set(text).isdisjoint(set("qyjpg"))

        if flourish_buff_manual:
            flourish_buff = flourish_buff_manual
        else:
            if has_descenders:
                flourish_buff = 0.05
            else:
                flourish_buff = 0.15

        if undercaption_buff_manual:
            undercaption_buff = undercaption_buff_manual
        else:
            if has_descenders:
                buff_increment = 0.15
            else:
                buff_increment = 0.10
            undercaption_buff = flourish_buff + buff_increment

        # create the text mobject
        self._text_mobject = mn.Text(
            text,
            font=font,
            font_size=font_size,
            color=text_color,
        )

        self.add(self._text_mobject)

        # optionally create the flourish under the text
        if self._flourish:
            flourish_width = self._text_mobject.width + flourish_padding
            self._flourish = self._create_flourish(
                width=flourish_width,
                color=flourish_color,
                stroke_width=flourish_stroke_width,
                spiral_radius=spiral_radius,
                spiral_turns=spiral_turns,
                spiral_offset=spiral_offset,
            )
            # position the flourish below the text
            self._flourish.next_to(self._text_mobject, mn.DOWN, flourish_buff)
            self.add(self._flourish)

        # optionally create the undercaption under the text
        if undercaption_text:
            # create the text mobject
            undercaption_text_mob = mn.Text(
                undercaption_text,
                font=undercaption_font,
                font_size=undercaption_font_size,
                color=undercaption_color,
            )
            undercaption_text_mob.next_to(
                self._text_mobject, mn.DOWN, undercaption_buff
            )
            self.add(undercaption_text_mob)

        # create the svg mobject
        if undercaption_svg:
            svg_mob = mn.SVGMobject(
                undercaption_svg,
                height=svg_height,
            )
            svg_mob.next_to(self._text_mobject, mn.DOWN, undercaption_buff)
            self.add(svg_mob)

        self._position()

    def _create_flourish(
        self,
        width: float,
        color: ManimColor | str,
        stroke_width: float,
        spiral_radius: float,
        spiral_turns: float,
        spiral_offset: float,
    ) -> mn.VGroup:
        """Create decorative flourish with horizontal line and spiral ends.

        Args:
            width (float): Total width of the flourish.
            color (ManimColor | str): Color of the flourish.
            stroke_width (float): Stroke width of the flourish.
            spiral_radius (float): Radius of the spiral ends.
            spiral_turns (float): Number of turns in each spiral.
            spiral_offset (float): Vertical offset of the spirals.

        Returns:
            mn.VGroup: Group containing the flourish components.
        """

        # left spiral (from outer to inner)
        left_center = np.array([-width / 2, -spiral_offset, 0])
        left_spiral = []
        for t in np.linspace(0, 1, 100):
            angle = 2 * np.pi * spiral_turns * t
            current_radius = spiral_radius * (1 - t)
            rotated_angle = angle + 1.2217
            x = left_center[0] + current_radius * np.cos(rotated_angle)
            y = left_center[1] + current_radius * np.sin(rotated_angle)
            left_spiral.append(np.array([x, y, 0]))

        # right spiral (from outer to inner)
        right_center = np.array([width / 2, -spiral_offset, 0])
        right_spiral = []
        for t in np.linspace(0, 1, 100):
            angle = -2 * np.pi * spiral_turns * t
            current_radius = spiral_radius * (1 - t)
            rotated_angle = angle + 1.9199
            x = right_center[0] + current_radius * np.cos(rotated_angle)
            y = right_center[1] + current_radius * np.sin(rotated_angle)
            right_spiral.append(np.array([x, y, 0]))

        # line between the outer points of the spirals (slightly overlaps into the spirals)
        straight_start = left_spiral[1]
        straight_end = right_spiral[1]
        straight_line = [
            straight_start + t * (straight_end - straight_start)
            for t in np.linspace(0, 1, 50)
        ]

        # create separate VMobjects for each part
        flourish_line = mn.VMobject()
        flourish_line.set_color(color)
        flourish_line.set_stroke(width=stroke_width)
        flourish_line.set_points_smoothly(straight_line)

        flourish_right = mn.VMobject()
        flourish_right.set_color(color)
        flourish_right.set_stroke(width=stroke_width)
        flourish_right.set_points_smoothly(right_spiral)

        flourish_left = mn.VMobject()
        flourish_left.set_color(color)
        flourish_left.set_stroke(width=stroke_width)
        flourish_left.set_points_smoothly(left_spiral)

        # group all parts into a single VGroup
        flourish_path = mn.VGroup(flourish_line, flourish_right, flourish_left)

        return flourish_path


class TitleLogo(AlgoManimBase):
    """Group for displaying SVG logo with optional text.

    Args:
        svg: Path to the SVG file.
        svg_height: Height of the SVG.
        mob_center: Reference mobject for positioning.
        align_left: Reference mobject to align left edge with.
        align_right: Reference mobject to align right edge with.
        align_top: Reference mobject to align top edge with.
        align_bottom: Reference mobject to align bottom edge with.
            centers at mobject center.
        vector: Offset vector for the SVG.
        text: Optional text to display with the logo.
        text_color: Color of the text.
        font: Font family for the text.
        font_size: Font size for the text.
        text_vector: Offset vector for the text.
        **kwargs: Additional keyword arguments for SVG and text mobjects.
    """

    def __init__(
        self,
        svg: str,
        # --- svg ---
        svg_height: float = 2.0,
        mob_center: mn.Mobject = mn.Dot(mn.ORIGIN),
        align_left: mn.Mobject | None = None,
        align_right: mn.Mobject | None = None,
        align_top: mn.Mobject | None = None,
        align_bottom: mn.Mobject | None = None,
        vector: np.ndarray = mn.ORIGIN,
        # --- text ---
        text: str | None = None,
        text_color: ManimColor | str = "WHITE",
        font: str = "",
        font_size: float = 31,
        text_vector: np.ndarray = mn.ORIGIN,
    ):
        super().__init__(
            vector=vector,
            mob_center=mob_center,
            align_left=align_left,
            align_right=align_right,
            align_top=align_top,
            align_bottom=align_bottom,
        )

        # create the svg mobject
        self._svg = mn.SVGMobject(
            svg,
            height=svg_height,
        )

        self.add(self._svg)

        self._position()

        # create the text mobject
        if text:
            self.text_mobject = mn.Text(
                text,
                font=font,
                font_size=font_size,
                color=text_color,
            )
            self.text_mobject.move_to(self._svg.get_center() + text_vector)
            self.add(self.text_mobject)
