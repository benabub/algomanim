import manim as mn


class Array(mn.VGroup):
    def __init__(
        self,
        arr: list,
        position: mn.Mobject,
        bg_color=mn.DARK_GRAY
    ):
        """
        Create a Manim array visualization as a VGroup.

        Args:
            arr (list): The array of values to visualize.
            position (mn.Mobject): The position to place the array
            on the screen.

        Attributes:
            arr (list): The data array.
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
        self.sq_mob = mn.VGroup(*[
            mn.Square().set_fill(
                self.bg_color, 1).set_width(0.7).set_height(0.7)
            for _ in arr
        ])
        # Construction: Arrange squares in a row
        self.sq_mob.arrange(mn.RIGHT, buff=0.1)
        # Construction: Move array to the specified position
        self.sq_mob.move_to(position)

        # Construction: Create text mobjects and center them in squares
        self.num_mob = mn.VGroup(*[
            mn.Text(str(num)).move_to(square)
            for num, square in zip(arr, self.sq_mob)
        ])

        # Create pointers as a list with top and bottom groups
        self.pointers = [[], []]  # [0] for top, [1] for bottom

        for square in self.sq_mob:
            # Create top triangles (3 per square)
            top_tri_group = mn.VGroup(*[
                mn.Triangle(
                    color=self.bg_color,
                )
                .scale([0.5, 1, 1])
                .scale(0.1)
                .rotate(mn.PI)
                for _ in range(3)
            ])
            # Arrange top triangles horizontally above the square
            top_tri_group.arrange(mn.RIGHT, buff=0.08)
            top_tri_group.next_to(square, mn.UP, buff=0.15)
            self.pointers[0].append(top_tri_group)

            # Create bottom triangles (3 per square)
            bottom_tri_group = mn.VGroup(*[
                mn.Triangle(
                    color=self.bg_color,
                )
                .scale([0.5, 1, 1])
                .scale(0.1)
                for _ in range(3)
            ])
            # Arrange bottom triangles horizontally below the square
            bottom_tri_group.arrange(mn.RIGHT, buff=0.08)
            bottom_tri_group.next_to(square, mn.DOWN, buff=0.15)
            self.pointers[1].append(bottom_tri_group)

        # Adds local objects as instance attributes
        self.add(self.sq_mob, self.num_mob)
        self.add(*[ptr for group in self.pointers for ptr in group])

    def first_appear(self, scene, time=0.5):
        scene.play(mn.FadeIn(self), run_time=time)

    def pointers_1(
        self, i: int,
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
            raise ValueError('pos must be 0 (top) or 1 (bottom)')
        for idx, mob in enumerate(self.sq_mob):
            self.pointers[pos][idx][1].set_color(
                i_color if idx == i else self.bg_color)

    # Highlight blocks for 1 index
    def highlight_blocks_1(
        self, i: int,
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

    def pointers_2(
        self, i: int, j: int,
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
            raise ValueError('pos must be 0 (top) or 1 (bottom)')
        for idx, mob in enumerate(self.sq_mob):
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

    # Highlight blocks for 2 indices
    def highlight_blocks_2(
        self, i: int, j: int,
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

    def pointers_3(
        self, i: int, j: int, k: int,
        pos: int = 0,
        i_color=mn.RED,
        j_color=mn.GREEN,
        k_color=mn.BLUE,
    ):
        """
        Highlight two pointers at one side (top | bottom) in the
        array visualization.

        Args:
            i (int), j (int), k (int): Indices of the block whose pointer
                to highlight.
            pos (int): 0 for top pointers, 1 for bottom. Defaults to 0.
            i_color: Color for the highlighted pointer. Defaults to mn.GREEN.
        """
        for idx, mob in enumerate(self.sq_mob):
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

    # Highlight blocks for 3 indices
    def highlight_blocks_3(
        self, i: int, j: int, k: int,
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

    # Animation of changing values in the array
    def update_number_mobject(
            self, scene, i: int,
            add_arr: list, j: int):
        """
        Animate the change of a number in the array visualization.
        The number at index i in num_mob is replaced with a new value
        from add_arr[j], and the new text is positioned at the center
        of the corresponding square.

        Args:
            i (int): Index in the array to update.
            add_arr (list): Source array for the new value.
            j (int): Index in add_arr to get the new value from.
        """
        # self.num_mob - group of text objects in the array
        # .animate.become() - animation of transforming the receiver object
        # into the argument
        # mn.Text(str(arr[i])) - construction of a new text object
        # self.arr_mob - group of graphical square objects
        # .move_to(self.arr_mob[j]) - positioning the new text object
        # in the same location, that self.arr_mob[k] has
        # location in Manim is the center of mass

        # Animate replacing the text at index i with new value from add_arr[j]
        scene.play(
            self.num_mob[i].animate.become(
                mn.Text(
                    str(add_arr[j]),
                ).move_to(self.sq_mob[i])),
            # animation duration
            run_time=0.2
        )


class TopText(mn.VGroup):
    def __init__(
        self,
        mob_center: mn.Mobject,
        *vars: tuple,
        font_size=40,
        buff=0.7,
        vector=mn.UP * 1.2,
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
            mn.Text(f"{name} = {value()}",
                    font_size=self.font_size, color=color)
            for name, value, color in self.vars
        ]
        top_text = mn.VGroup(*parts).arrange(mn.RIGHT, buff=self.buff)
        top_text.move_to(self.mob_center.get_center() + self.vector)
        self.add(*top_text)

    def first_appear(self, scene, time=0.5):
        scene.play(mn.FadeIn(self), run_time=time)

    def update_text(self, scene, time=0.1):
        # Create a new object with the same parameters
        # (vars may be updated)
        new_group = TopText(
            self.mob_center,
            *self.vars,
            font_size=self.font_size,
            buff=self.buff,
            vector=self.vector,
        )
        scene.play(mn.Transform(self, new_group), run_time=time)


class CodeBlock(mn.VGroup):
    def __init__(
        self,
        code_lines: list,
        position: mn.Mobject,
        font_size=25,
        font="MesloLGS NF"
    ):
        """
        Creates a code block visualization on the screen.

        Args:
            code_lines (list): List of code lines to display.
            position (mn.Mobject): Position to place the code block.
            font_size (int, optional): Font size for the code text.
            font (str, optional): Font for the code text.
        """
        super().__init__()
        # Construction
        code_mobs = [
            mn.Text(line, font=font, font_size=font_size)
            for line in code_lines
        ]
        code_vgroup = mn.VGroup(
            *code_mobs).arrange(mn.DOWN, aligned_edge=mn.LEFT)
        code_vgroup.move_to(position)
        self.code_vgroup = code_vgroup
        # Construstion: add to scene
        self.add(self.code_vgroup)

    def first_appear(self, scene, time=0.5):
        scene.play(mn.FadeIn(self), run_time=time)

    def highlight_line(self, scene, i: int):
        """
        Highlights a single line of code in the code block by fading it
        to yellow, instead of white.

        Args:
            scene (mn.Scene): The scene to play the animation in.
            i (int): Index of the line to highlight.
        """
        scene.play(*[
            mn.FadeToColor(
                mob,
                mn.YELLOW if k == i else mn.WHITE,
                run_time=0.2
            )
            for k, mob in enumerate(self.code_vgroup)
        ])
