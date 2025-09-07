from typing import List, Tuple, Callable, Any, Union, Optional
import manim as mn  # type: ignore
from manim import ManimColor


class Array(mn.VGroup):
    def __init__(self, arr: List[int], position: mn.Mobject, bg_color=mn.DARK_GRAY):
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
        self.sq_mob.move_to(position)

        # Construction: Create text mobjects and center them in squares
        self.num_mob = mn.VGroup(
            *[
                mn.Text(str(num)).move_to(square)
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

            new_text = mn.Text(new_val_str).move_to(self.sq_mob[i])

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
            pos (int): 0 for top pointers, 1 for bottom pointers. Defaults to 1.
            pnt_color: Color for the highlighted pointer. Defaults to mn.WHITE.
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
            pos (int): 0 for top pointers, 1 for bottom. Defaults to 0.
            i_color: Color for the highlighted pointer. Defaults to mn.GREEN.
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
            pos (int): 0 for top pointers, 1 for bottom. Defaults to 0.
            i_color: Color for the highlighted pointer. Defaults to mn.GREEN.
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
            pos (int): 0 for top pointers, 1 for bottom. Defaults to 0.
            i_color: Color for the highlighted pointer. Defaults to mn.GREEN.
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


class TopText(mn.VGroup):
    def __init__(
        self,
        mob_center: mn.Mobject,
        *vars: Tuple[str, Callable[[], Any], Union[str, ManimColor]],
        font_size=40,
        buff=0.7,
        vector=mn.UP * 1.4,
    ):
        super().__init__()
        self.mob_center = mob_center
        self.vars = vars
        self.font_size = font_size
        self.buff = buff
        self.vector = vector
        self._refresh()

    def _refresh(self):
        self.submobjects = []
        parts = [
            mn.Text(f"{name} = {value()}", font_size=self.font_size, color=color)
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
        new_group = TopText(
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
        position: mn.Mobject,
        font_size=25,
        font="MesloLGS NF",
        font_color_regular="white",
        font_color_highlight="yellow",
        bg_highlight_color="blue",
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
        code_vgroup.move_to(position)
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


class TitleTop(mn.Text):
    def __init__(
        self,
        text: str,
        position: mn.Mobject = mn.Dot(mn.UP * 2.7),
        text_color="#FFA116",
        font="FiraCode-Retina",
        font_size=50,
        **kwargs,
    ):
        """
        Specialized class for creating titles at the top of the scene.

        Inherits all functionality from manim.Text with predefined parameters
        for convenient title creation.

        Attributes:
            text: Text string to display.
            position: Position of the title on the scene. Defaults to top-left corner.
            text_color: Color of the text. Defaults to WHITE.
            font: Font name. Defaults to 'MesloLGS NF'.
            font_size: Font size. Defaults to 40.
            **kwargs: Additional arguments passed to manim.Text.
        """
        super().__init__(
            text, font=font, font_size=font_size, color=text_color, **kwargs
        )
        self.move_to(position)

    def appear(self, scene: mn.Scene):
        scene.add(self)
