from typing import List, Tuple, Callable, Any, Union, Optional
import numpy as np
import manim as mn  # type: ignore
from manim import ManimColor


class Array(mn.VGroup):
    def __init__(
        self,
        arr: List[int],
        vector: np.ndarray,
        font="",
        bg_color=mn.DARK_GRAY,
        mob_center: mn.Mobject = mn.Dot(mn.ORIGIN),
    ):
        """
        Create a Manim array visualization as a VGroup.

        Args:
            arr (List[int]): The array of values to visualize.
            position (mn.Mobject): The position to place the array
            on the screen.

        Attributes:
            arr (List[int]): The data array.
            sq_mob (mn.VGroup): Group of square mobjects for array cells.
            num_mob (mn.VGroup): Group of text mobjects for array values.
        """
        # Call __init__ of the parent classes
        super().__init__()
        # Add class attributes
        self.arr = arr
        self.bg_color = bg_color
        self.font = font

        # Construction: Create square mobjects for each array element
        # NB: if opacity is not specified, it will be set to None
        # and some methods will break for unknown reasons
        self.sq_mob = mn.VGroup(
            *[
                mn.Square().set_fill(self.bg_color, 1).set(width=0.7, height=0.7)
                for _ in arr
            ]
        )
        # Construction: Arrange squares in a row
        self.sq_mob.arrange(mn.RIGHT, buff=0.1)

        # Construction: Move array to the specified position
        self.sq_mob.move_to(mob_center.get_center() + vector)

        # Construction: Create text mobjects and center them in squares
        self.num_mob = mn.VGroup(
            *[
                mn.Text(str(num), font=self.font).move_to(square)
                for num, square in zip(arr, self.sq_mob)
            ]
        )

        # Create pointers as a list with top and bottom groups
        self.pointers: List[List[Any]] = [[], []]  # [0] for top, [1] for bottom

        for square in self.sq_mob:
            # Create top triangles (3 per square)
            top_tri_group = mn.VGroup(
                *[
                    mn.Triangle(
                        color=self.bg_color,
                    )
                    .stretch_to_fit_width(square.width)
                    .scale(0.1)
                    .rotate(mn.PI)
                    for _ in range(3)
                ]
            )
            # Arrange top triangles horizontally above the square
            top_tri_group.arrange(mn.RIGHT, buff=0.08)
            top_tri_group.next_to(square, mn.UP, buff=0.15)
            self.pointers[0].append(top_tri_group)

            # Create bottom triangles (3 per square)
            bottom_tri_group = mn.VGroup(
                *[
                    mn.Triangle(
                        color=self.bg_color,
                    )
                    .stretch_to_fit_width(square.width)
                    .scale(0.1)
                    for _ in range(3)
                ]
            )
            # Arrange bottom triangles horizontally below the square
            bottom_tri_group.arrange(mn.RIGHT, buff=0.08)
            bottom_tri_group.next_to(square, mn.DOWN, buff=0.15)
            self.pointers[1].append(bottom_tri_group)

        # Adds local objects as instance attributes
        self.add(self.sq_mob, self.num_mob)
        self.add(*[ptr for group in self.pointers for ptr in group])

    def first_appear(self, scene: mn.Scene, time=0.5):
        scene.play(mn.FadeIn(self), run_time=time)

    def update_numbers(
        self,
        scene: mn.Scene,
        new_values: List[int],
        animate: bool = True,
        run_time: float = 0.2,
    ) -> None:
        """
        Update all text mobjects in the array.
        Can perform the update with or without animation.

        Args:
            scene: The scene to play animations in
            new_values: New array values to display
            animate: Whether to animate the changes (True) or
                     update instantly (False)
            run_time: Duration of animation if animate=True

        Raises:
            ValueError: If new_values length doesn't match array length
        """
        if len(new_values) != len(self.arr):
            raise ValueError(
                f"Length mismatch: array has {len(self.arr)} elements, "
                f"but {len(new_values)} new values provided"
            )

        animations = []

        for i in range(len(new_values)):
            new_val_str = str(new_values[i])

            new_text = mn.Text(new_val_str, font=self.font).move_to(self.sq_mob[i])

            if animate:
                animations.append(self.num_mob[i].animate.become(new_text))
            else:
                self.num_mob[i].become(new_text)

        if animate and animations:
            scene.play(*animations, run_time=run_time)

    def pointer_special(
        self,
        val: int,
        pos: int = 1,
        pnt_color=mn.WHITE,
    ):
        """
        Highlight a pointer at one side (top or bottom) in the
        array visualization based on integer value comparison.

        Args:
            val (int): The value to compare with array elements
            pos (int): 0 for top pointers, 1 for bottom pointers.
            pnt_color: Color for the highlighted pointer.
        """
        for idx, _ in enumerate(self.sq_mob):
            self.pointers[pos][idx][1].set_color(
                pnt_color if self.arr[idx] == val else self.bg_color
            )

    def pointers_1(
        self,
        i: int,
        pos: int = 0,
        i_color=mn.GREEN,
    ):
        """
        Highlight a single pointer at one side (top | bottom) in the
        array visualization.

        Args:
            i (int): Index of the block whose pointer to highlight.
            pos (int): 0 for top pointers, 1 for bottom.
            i_color: Color for the highlighted pointer.
        """
        if pos not in (0, 1):
            raise ValueError("pos must be 0 (top) or 1 (bottom)")
        for idx, _ in enumerate(self.sq_mob):
            self.pointers[pos][idx][1].set_color(i_color if idx == i else self.bg_color)

    def pointers_2(
        self,
        i: int,
        j: int,
        pos: int = 0,
        i_color=mn.RED,
        j_color=mn.BLUE,
    ):
        """
        Highlight two pointers at one side (top | bottom) in the
        array visualization.

        Args:
            i (int), j (int): Indices of the block whose pointer to highlight.
            pos (int): 0 for top pointers, 1 for bottom.
            i_color: Color for the highlighted pointer.
        """
        if pos not in (0, 1):
            raise ValueError("pos must be 0 (top) or 1 (bottom)")
        for idx, _ in enumerate(self.sq_mob):
            if idx == i == j:
                self.pointers[pos][idx][0].set_color(i_color)
                self.pointers[pos][idx][1].set_color(self.bg_color)
                self.pointers[pos][idx][2].set_color(j_color)
            elif idx == i:
                self.pointers[pos][idx][0].set_color(self.bg_color)
                self.pointers[pos][idx][1].set_color(i_color)
                self.pointers[pos][idx][2].set_color(self.bg_color)
            elif idx == j:
                self.pointers[pos][idx][0].set_color(self.bg_color)
                self.pointers[pos][idx][1].set_color(j_color)
                self.pointers[pos][idx][2].set_color(self.bg_color)
            else:
                self.pointers[pos][idx][0].set_color(self.bg_color)
                self.pointers[pos][idx][1].set_color(self.bg_color)
                self.pointers[pos][idx][2].set_color(self.bg_color)

    def pointers_3(
        self,
        i: int,
        j: int,
        k: int,
        pos: int = 0,
        i_color=mn.RED,
        j_color=mn.GREEN,
        k_color=mn.BLUE,
    ):
        """
        Highlight three pointers at one side (top | bottom) in the
        array visualization.

        Args:
            i (int), j (int), k (int): Indices of the block whose pointer
                to highlight.
            pos (int): 0 for top pointers, 1 for bottom.
            i_color: Color for the highlighted pointer.
        """
        for idx, _ in enumerate(self.sq_mob):
            if idx == i == j == k:
                self.pointers[pos][idx][0].set_color(i_color)
                self.pointers[pos][idx][1].set_color(j_color)
                self.pointers[pos][idx][2].set_color(k_color)
            elif idx == i == j:
                self.pointers[pos][idx][0].set_color(i_color)
                self.pointers[pos][idx][1].set_color(self.bg_color)
                self.pointers[pos][idx][2].set_color(j_color)
            elif idx == i == k:
                self.pointers[pos][idx][0].set_color(i_color)
                self.pointers[pos][idx][1].set_color(self.bg_color)
                self.pointers[pos][idx][2].set_color(k_color)
            elif idx == k == j:
                self.pointers[pos][idx][0].set_color(j_color)
                self.pointers[pos][idx][1].set_color(self.bg_color)
                self.pointers[pos][idx][2].set_color(k_color)
            elif idx == i:
                self.pointers[pos][idx][0].set_color(self.bg_color)
                self.pointers[pos][idx][1].set_color(i_color)
                self.pointers[pos][idx][2].set_color(self.bg_color)
            elif idx == j:
                self.pointers[pos][idx][0].set_color(self.bg_color)
                self.pointers[pos][idx][1].set_color(j_color)
                self.pointers[pos][idx][2].set_color(self.bg_color)
            elif idx == k:
                self.pointers[pos][idx][0].set_color(self.bg_color)
                self.pointers[pos][idx][1].set_color(k_color)
                self.pointers[pos][idx][2].set_color(self.bg_color)
            else:
                self.pointers[pos][idx][0].set_color(self.bg_color)
                self.pointers[pos][idx][1].set_color(self.bg_color)
                self.pointers[pos][idx][2].set_color(self.bg_color)

    # Highlight blocks for 1 index
    def highlight_blocks_1(
        self,
        i: int,
        i_color=mn.GREEN,
    ):
        """
        Highlight a single block in the array visualization.

        Args:
            i (int): Index of the block to highlight.
            i_color: Color for the highlighted block.
        """
        for idx, mob in enumerate(self.sq_mob):
            mob.set_fill(i_color if idx == i else self.bg_color)

    # Highlight blocks for 2 indices
    def highlight_blocks_2(
        self,
        i: int,
        j: int,
        i_color=mn.RED,
        j_color=mn.BLUE,
        ij_color=mn.PURPLE,
    ):
        """
        Highlight two blocks in the array visualization.
        If indices coincide, use a special color.

        Args:
            i (int): First index to highlight.
            j (int): Second index to highlight.
            i_color: Color for the first index.
            j_color: Color for the second index.
            ij_color: Color if both indices are the same.
        """
        for idx, mob in enumerate(self.sq_mob):
            if idx == i == j:
                mob.set_fill(ij_color)
            elif idx == i:
                mob.set_fill(i_color)
            elif idx == j:
                mob.set_fill(j_color)
            else:
                mob.set_fill(self.bg_color)

    # Highlight blocks for 3 indices
    def highlight_blocks_3(
        self,
        i: int,
        j: int,
        k: int,
        i_color=mn.RED,
        j_color=mn.GREEN,
        k_color=mn.BLUE,
        ijk_color=mn.BLACK,
        ij_color=mn.YELLOW_E,
        ik_color=mn.PURPLE,
        jk_color=mn.TEAL,
    ):
        """
        Highlight three blocks in the array visualization.
        Use special colors for index coincidences.

        Args:
            i (int): First index to highlight.
            j (int): Second index to highlight.
            k (int): Third index to highlight.
            i_color: Color for the first index.
            j_color: Color for the second index.
            k_color: Color for the third index.
            ijk_color: Color if all three indices are the same.
            ij_color: Color if i and j are the same.
            ik_color: Color if i and k are the same.
            jk_color: Color if j and k are the same.
        """
        for idx, mob in enumerate(self.sq_mob):
            if idx == i == j == k:
                mob.set_fill(ijk_color)
            elif idx == i == j:
                mob.set_fill(ij_color)
            elif idx == i == k:
                mob.set_fill(ik_color)
            elif idx == k == j:
                mob.set_fill(jk_color)
            elif idx == i:
                mob.set_fill(i_color)
            elif idx == j:
                mob.set_fill(j_color)
            elif idx == k:
                mob.set_fill(k_color)
            else:
                mob.set_fill(self.bg_color)


class RelativeText(mn.VGroup):
    def __init__(
        self,
        mob_center: mn.Mobject,
        *vars: Tuple[str, Callable[[], Any], Union[str, ManimColor]],
        font="",
        font_size=40,
        buff=0.7,
        vector: np.ndarray = mn.UP * 1.4,
    ):
        super().__init__()
        self.mob_center = mob_center
        self.vars = vars
        self.font = font
        self.font_size = font_size
        self.buff = buff
        self.vector = vector

        self.submobjects: List = []
        parts = [
            mn.Text(
                f"{name} = {value()}",
                font=self.font,
                font_size=self.font_size,
                color=color,
            )
            for name, value, color in self.vars
        ]
        top_text = mn.VGroup(*parts).arrange(mn.RIGHT, buff=self.buff)
        top_text.move_to(self.mob_center.get_center() + self.vector)
        self.add(*top_text)

    def first_appear(self, scene: mn.Scene, time=0.5):
        scene.play(mn.FadeIn(self), run_time=time)

    def update_text(self, scene: mn.Scene, time=0.1, animate: bool = True):
        # Create a new object with the same parameters
        # (vars may be updated)
        new_group = RelativeText(
            self.mob_center,
            *self.vars,
            font_size=self.font_size,
            buff=self.buff,
            vector=self.vector,
        )
        if animate:
            scene.play(mn.Transform(self, new_group), run_time=time)
        else:
            scene.remove(self)
            self.become(new_group)
            scene.add(self)


class CodeBlock(mn.VGroup):
    def __init__(
        self,
        code_lines: List[str],
        vector: np.ndarray,
        font_size=25,
        font="",
        font_color_regular="white",
        font_color_highlight="yellow",
        bg_highlight_color="blue",
        mob_center: mn.Mobject = mn.Dot(mn.ORIGIN),
    ):
        """
        Creates a code block visualization on the screen.

        Args:
            code_lines (List[str]): List of code lines to display.
            position (mn.Mobject): Position to place the code block.
            font_size (int, optional): Font size for the code text.
            font (str, optional): Font for the code text.
        """
        super().__init__()
        # Construction
        self.font_color_regular = font_color_regular
        self.font_color_highlight = font_color_highlight
        self.bg_highlight_color = bg_highlight_color

        self.code_mobs = [
            mn.Text(line, font=font, font_size=font_size, color=self.font_color_regular)
            for line in code_lines
        ]
        self.bg_rects: List[Optional[mn.Rectangle]] = [None] * len(
            code_lines
        )  # List to save links on all possible rectangles and to manage=delete them

        code_vgroup = mn.VGroup(*self.code_mobs).arrange(mn.DOWN, aligned_edge=mn.LEFT)
        code_vgroup.move_to(mob_center.get_center() + vector)
        self.code_vgroup = code_vgroup
        # Animation
        self.add(self.code_vgroup)

    def first_appear(self, scene: mn.Scene, time=0.5):
        scene.play(mn.FadeIn(self), run_time=time)

    def highlight_line(self, i: int):
        """
        Highlights a single line of code by changing both text color and background.

        Args:
            i (int): Index of the line to highlight.
        """
        for k, mob in enumerate(self.code_mobs):
            if k == i:
                # Change font color
                mob.set_color(self.font_color_highlight)
                # Create bg rectangle
                if self.bg_rects[k] is None:
                    bg_rect = mn.Rectangle(
                        width=mob.width + 0.2,
                        height=mob.height + 0.1,
                        fill_color=self.bg_highlight_color,
                        fill_opacity=0.3,
                        stroke_width=0,
                    )
                    bg_rect.move_to(mob.get_center())
                    self.add(bg_rect)
                    bg_rect.z_index = -1  # Send background to back
                    self.bg_rects[k] = bg_rect
            else:
                # Normal line:
                # regular font color
                mob.set_color(self.font_color_regular)
                # remove rect
                bg_rect = self.bg_rects[k]
                if bg_rect:
                    self.remove(bg_rect)
                    self.bg_rects[k] = None


class TitleText(mn.VGroup):
    """
    A title group for Manim scenes, consisting of a text label, an optional decorative flourish underneath, and
    an optional undercaption.

    Args:
        text (str): The title text to display.
        vector (np.ndarray, optional): Offset vector from the center for positioning the group.
        text_color (str, optional): Color of the title text.
        font (str, optional): Font family for the title text.
        font_size (float, optional): Font size for the title text.
        mob_center (mn.Mobject, optional): Reference mobject for positioning.
        flourish (bool, optional): Whether to render the flourish under the text.
        flourish_color (str, optional): Color of the flourish line.
        flourish_stroke_width (float, optional): Stroke width of the flourish.
        flourish_padding (float, optional): Padding between text and flourish.
        flourish_buff (float, optional): Buffer between text and flourish.
        spiral_offset (float, optional): Vertical offset of the spirals relative to the flourish line.
        spiral_radius (float, optional): Radius of the spiral ends of the flourish.
        spiral_turns (float, optional): Number of turns in each spiral.
        undercaption (str, optional): Text under the flourish.
        undercaption_color (str, optional): Color of the undercaption text.
        undercaption_font (str, optional): Font family for the undercaption.
        undercaption_font_size (float, optional): Font size for the undercaption.
        undercaption_buff (float, optional): Buffer between text and undercaption.
        **kwargs: Additional keyword arguments for the text mobject.
    """

    def __init__(
        self,
        # --------- text --------------
        text: str,
        vector: np.ndarray = mn.UP * 2.7,
        text_color: str = "white",
        font: str = "",
        font_size: float = 50,
        mob_center: mn.Mobject = mn.Dot(mn.ORIGIN),
        # ------- flourish ------------
        flourish: bool = False,
        flourish_color: str = "white",
        flourish_stroke_width: float = 4,
        flourish_padding: float = 0.2,
        flourish_buff: float = 0.15,
        spiral_offset: float = 0.3,
        spiral_radius: float = 0.15,
        spiral_turns: float = 1.0,
        # ------- undercaption ------------
        undercaption: str = "",
        undercaption_color: str = "white",
        undercaption_font: str = "",
        undercaption_font_size: float = 20,
        undercaption_buff: float = 0.23,
        # ----------- kwargs ------------
        **kwargs,
    ):
        super().__init__()

        # Create the text mobject
        self.text_mobject = mn.Text(
            text,
            font=font,
            font_size=font_size,
            color=text_color,
            **kwargs,
        )
        self.add(self.text_mobject)

        # Optionally create the flourish under the text
        if flourish:
            flourish_width = (
                # self.text_mobject.width * flourish_width_ratio + flourish_padding
                self.text_mobject.width + flourish_padding
            )
            self.flourish = self._create_flourish(
                width=flourish_width,
                color=flourish_color,
                stroke_width=flourish_stroke_width,
                spiral_radius=spiral_radius,
                spiral_turns=spiral_turns,
                spiral_offset=spiral_offset,
            )
            # Position the flourish below the text
            self.flourish.next_to(self.text_mobject, mn.DOWN, flourish_buff)
            self.add(self.flourish)

        # Optionally create the undercaption under the text
        if undercaption:
            # Create the text mobject
            self.undercaption = mn.Text(
                undercaption,
                font=undercaption_font,
                font_size=undercaption_font_size,
                color=undercaption_color,
                **kwargs,
            )
            self.undercaption.next_to(self.text_mobject, mn.DOWN, undercaption_buff)
            self.add(self.undercaption)

        # Position the entire group relative to the reference mobject and offset vector
        self.move_to(mob_center.get_center() + vector)

    def _create_flourish(
        self,
        width: float,
        color: str,
        stroke_width: float,
        spiral_radius: float,
        spiral_turns: float,
        spiral_offset: float,
    ) -> mn.VGroup:
        """
        Create a decorative flourish consisting of a horizontal line with symmetric spiral ends.

        Args:
            width (float): Total width of the flourish.
            color (str): Color of the flourish.
            stroke_width (float): Stroke width of the flourish.
            spiral_radius (float): Radius of the spiral ends.
            spiral_turns (float): Number of turns in each spiral.
            spiral_offset (float): Vertical offset of the spirals.

        Returns:
            mn.VGroup: The group containing the flourish components.
        """
        # Left spiral (from outer to inner)
        left_center = np.array([-width / 2, -spiral_offset, 0])
        left_spiral = []
        for t in np.linspace(0, 1, 100):
            angle = 2 * np.pi * spiral_turns * t
            current_radius = spiral_radius * (1 - t)
            rotated_angle = angle + 1.2217
            x = left_center[0] + current_radius * np.cos(rotated_angle)
            y = left_center[1] + current_radius * np.sin(rotated_angle)
            left_spiral.append(np.array([x, y, 0]))

        # Right spiral (from outer to inner)
        right_center = np.array([width / 2, -spiral_offset, 0])
        right_spiral = []
        for t in np.linspace(0, 1, 100):
            angle = -2 * np.pi * spiral_turns * t
            current_radius = spiral_radius * (1 - t)
            rotated_angle = angle + 1.9199
            x = right_center[0] + current_radius * np.cos(rotated_angle)
            y = right_center[1] + current_radius * np.sin(rotated_angle)
            right_spiral.append(np.array([x, y, 0]))

        # Line between the outer points of the spirals (slightly overlaps into the spirals)
        straight_start = left_spiral[1]
        straight_end = right_spiral[1]
        straight_line = [
            straight_start + t * (straight_end - straight_start)
            for t in np.linspace(0, 1, 50)
        ]

        # Create separate VMobjects for each part
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

        # Group all parts into a single VGroup
        flourish_path = mn.VGroup(flourish_line, flourish_right, flourish_left)

        return flourish_path

    def appear(self, scene: mn.Scene):
        """
        Add the entire title group to the given Manim scene.

        Args:
            scene (mn.Scene): The Manim scene to add the logo group to.
        """
        scene.add(self)


class TitleLogo(mn.VGroup):
    """
    A group for displaying an SVG logo with optional text, positioned relative to a reference mobject.

    Args:
        svg (str): Path to the SVG file.
        svg_height (float, optional): Height of the SVG.
        mob_center (mn.Mobject, optional): Reference mobject for positioning.
        svg_vector (np.ndarray, optional): Offset vector for the SVG.
        text (str, optional): Optional text to display with the logo.
        text_color (str, optional): Color of the text.
        font (str, optional): Font family for the text.
        font_size (float, optional): Font size for the text.
        text_vector (np.ndarray, optional): Offset vector for the text.
        **kwargs: Additional keyword arguments for the SVG and text mobjects.
    """

    def __init__(
        self,
        svg: str,
        # ----------- svg -------------
        svg_height: float = 2.0,
        mob_center: mn.Mobject = mn.Dot(mn.ORIGIN),
        svg_vector: np.ndarray = mn.ORIGIN,
        # --------- text --------------
        text: str | None = None,
        text_color: str = "white",
        font: str = "",
        font_size: float = 31,
        text_vector: np.ndarray = mn.ORIGIN,
        # --------- kwargs -------------
        **kwargs,
    ):
        super().__init__()

        # Create the svg mobject
        self.svg = mn.SVGMobject(
            svg,
            height=svg_height,
            **kwargs,
        )
        self.add(self.svg)

        # Create the text mobject
        if text:
            self.text_mobject = mn.Text(
                text,
                font=font,
                font_size=font_size,
                color=text_color,
                **kwargs,
            )
            self.text_mobject.move_to(self.svg.get_center() + text_vector)
            self.add(self.text_mobject)

        # Position the entire group relative to the reference mobject and offset vector
        self.move_to(mob_center.get_center() + svg_vector)

    def appear(self, scene: mn.Scene):
        """
        Add the entire logo group to the given Manim scene.

        Args:
            scene (mn.Scene): The Manim scene to add the logo group to.
        """
        scene.add(self)
