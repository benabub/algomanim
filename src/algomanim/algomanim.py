from typing import (
    List,
    Tuple,
    Callable,
    Any,
    Optional,
    Literal,
)

import manim as mn
from manim import ManimColor
import numpy as np

from . import utils

from .datastructures import (
    #     Node,
    #     TreeNode,
    ListNode,
)


class Array(mn.VGroup):
    """Array visualization as a VGroup of cells with values and pointers.

    Args:
        arr: List of values to visualize.
        vector: Position offset from mob_center.
        font: Font family for text elements.
        font_size: Font size for text, scales the whole mobject.
        font_color: Color for text elements.
        weight: Font weight (NORMAL, BOLD, etc.).
        bg_color: Background color for cells and default pointer color.
        cell_color: Border color for cells.
        mob_center: Reference mobject for positioning.
        align_edge: Edge alignment relative to mob_center.
        cell_params_auto: Whether to auto-calculate cell parameters.
        cell_height: Manual cell height when auto-calculation disabled.
        top_bottom_buff: Internal top/bottom padding within cells.
        top_buff: Top alignment buffer for specific characters.
        bottom_buff: Bottom alignment buffer for most characters.
        deep_bottom_buff: Deep bottom alignment for descending characters.

    Note:
        Character alignment is automatically handled based on typography:
        - Top: Quotes and accents (", ', ^, `)
        - Deep bottom: Descenders (y, p, g, j)
        - Center: Numbers, symbols, brackets
        - Bottom: Most letters and other characters
    """

    def __init__(
        self,
        arr: List,
        vector: np.ndarray = mn.ORIGIN,
        font="",
        font_size=35,
        font_color: ManimColor | str = mn.WHITE,
        weight: str = "NORMAL",
        bg_color: ManimColor | str = mn.DARK_GRAY,
        cell_color: ManimColor | str = mn.LIGHT_GRAY,
        mob_center: mn.Mobject = mn.Dot(mn.ORIGIN),
        align_edge: Literal["up", "down", "left", "right"] | None = None,
        # ---- cell params ----
        cell_params_auto=True,
        cell_height=0.65625,
        top_bottom_buff=0.15,
        top_buff=0.09,
        bottom_buff=0.16,
        deep_bottom_buff=0.05,
    ):
        # call __init__ of the parent classes
        super().__init__()
        # add class attributes
        self.data = arr.copy()
        self.bg_color = bg_color
        self.font = font
        self.font_size = font_size
        self.font_color = font_color

        if cell_params_auto:
            cell_params = utils.get_cell_params(font_size, font, weight)
            self.cell_height = cell_params["cell_height"]
            self.top_bottom_buff = cell_params["top_bottom_buff"]
            self.top_buff = cell_params["top_buff"]
            self.bottom_buff = cell_params["bottom_buff"]
            self.deep_bottom_buff = cell_params["deep_bottom_buff"]
        else:
            self.cell_height = cell_height
            self.top_bottom_buff = top_bottom_buff
            self.top_buff = top_buff
            self.bottom_buff = bottom_buff
            self.deep_bottom_buff = deep_bottom_buff

        self.TEXT_CONFIG = {
            "font": font,
            "font_size": self.font_size,
        }

        # --------- empty value ------------

        if not arr:
            self.text_mob = mn.Text("[]", **self.TEXT_CONFIG)
            self.containers_mob = mn.Rectangle(
                height=self.cell_height,
                width=utils.get_cell_width(
                    self.text_mob, self.top_bottom_buff, self.cell_height
                ),
                color=bg_color,
                fill_opacity=1.0,
            )
            self.containers_mob.set_fill(bg_color)
            utils.position(self.containers_mob, mob_center, align_edge, vector)
            self.text_mob.move_to(self.containers_mob.get_center())
            self.text_mob.align_to(self.containers_mob, mn.DOWN)
            self.text_mob.align_to(self.containers_mob, mn.LEFT)
            self.add(self.containers_mob, self.text_mob)
            return

        # --------- cells ------------

        text_mobs_list = [mn.Text(str(val), **self.TEXT_CONFIG) for val in arr]

        # NB: if opacity is not specified, it will be set to None
        # and some methods will break for unknown reasons
        cells_mobs_list = []
        for text_mob in text_mobs_list:
            cell_mob = mn.Rectangle(
                height=self.cell_height,
                width=utils.get_cell_width(
                    text_mob, self.top_bottom_buff, self.cell_height
                ),
                color=cell_color,
                fill_opacity=1.0,
            )
            cells_mobs_list.append(cell_mob)

        cells_mobs_list = [item.set_fill(bg_color) for item in cells_mobs_list]
        self.containers_mob = mn.VGroup(*cells_mobs_list)

        # construction: Arrange cells in a row
        self.containers_mob.arrange(mn.RIGHT, buff=0.1)

        # construction: Move VGroup to the specified position
        utils.position(self.containers_mob, mob_center, align_edge, vector)

        # ------ values ---------

        # construction: Create text mobjects and move them in squares
        self.values_mob = mn.VGroup(
            *[mn.Text(str(val), **self.TEXT_CONFIG) for val in arr]
        )

        for i in range(len(arr)):
            if not isinstance(arr[i], str):  # center alignment
                self.values_mob[i].move_to(self.containers_mob[i])
            else:
                val_set = set(arr[i])
                if not {
                    "\\",
                    "/",
                    "|",
                    "(",
                    ")",
                    "[",
                    "]",
                    "{",
                    "}",
                    "&",
                    "$",
                }.isdisjoint(val_set) or val_set.issubset(
                    {
                        ":",
                        "*",
                        "-",
                        "+",
                        "=",
                        "#",
                        "~",
                        "%",
                        "0",
                        "1",
                        "2",
                        "3",
                        "4",
                        "5",
                        "6",
                        "7",
                        "8",
                        "9",
                    }
                ):  # center alignment
                    self.values_mob[i].move_to(self.containers_mob[i])
                elif val_set.issubset(
                    {
                        '"',
                        "'",
                        "^",
                        "`",
                    }
                ):  # top alignment
                    self.values_mob[i].next_to(
                        self.containers_mob[i].get_top(),
                        direction=mn.DOWN,
                        buff=self.top_buff,
                    )

                elif val_set.issubset(
                    {
                        "y",
                        "p",
                        "g",
                        "j",
                    }
                ):  # deep bottom alignment
                    self.values_mob[i].next_to(
                        self.containers_mob[i].get_bottom(),
                        direction=mn.UP,
                        buff=self.deep_bottom_buff,
                    )

                else:  # bottom alignment
                    self.values_mob[i].next_to(
                        self.containers_mob[i].get_bottom(),
                        direction=mn.UP,
                        buff=self.bottom_buff,
                    )

        # ------- pointers ----------

        self.pointers_top, self.pointers_bottom = utils.create_pointers(
            self, self.containers_mob
        )

        # ------- add ----------

        # adds local objects as instance attributes
        self.add(
            self.containers_mob,
            self.values_mob,
            self.pointers_top,
            self.pointers_bottom,
        )

    def first_appear(self, scene: mn.Scene, time=0.5):
        """Animate the initial appearance of the array in scene.

        Args:
            scene: The scene to play the animation in.
            time: Duration of the fade-in animation.
        """

        scene.play(mn.FadeIn(self), run_time=time)

    def _update_internal_state(self, new_group: "Array", new_value: List[int]):
        """Update internal state for new made class instance.

        Args:
            new_group: New Array instance to copy state from.
            new_value: New array values.
        """

        # save old attributes with highlights
        old_cells = getattr(self, "containers_mob", None)
        old_pointers_top = getattr(self, "pointers_top", None)
        old_pointers_bottom = getattr(self, "pointers_bottom", None)

        self.data = new_value.copy()
        self.containers_mob = new_group.containers_mob
        self.submobjects = new_group.submobjects.copy()

        if self.data:
            self.values_mob = new_group.values_mob

            self.pointers_top = new_group.pointers_top
            self.pointers_bottom = new_group.pointers_bottom

            # restore old highlights
            if old_cells:
                for old, new in zip(old_cells, self.containers_mob):
                    new.set_fill(old.get_fill_color())

            if old_pointers_top:
                for old_ptrs, new_ptrs in zip(old_pointers_top, self.pointers_top):
                    for old_tri, new_tri in zip(old_ptrs, new_ptrs):
                        new_tri.set_color(old_tri.get_color())

            if old_pointers_bottom:
                for old_ptrs, new_ptrs in zip(
                    old_pointers_bottom, self.pointers_bottom
                ):
                    for old_tri, new_tri in zip(old_ptrs, new_ptrs):
                        new_tri.set_color(old_tri.get_color())

        else:
            self.pointers_top = mn.VGroup()
            self.pointers_bottom = mn.VGroup()

    def update_value(
        self,
        scene: mn.Scene,
        new_value: List[int],
        animate: bool = False,
        left_aligned=True,
        run_time: float = 0.2,
    ) -> None:
        """Replace mobject with new one, based on new_value.

        Args:
            scene: The scene to play animations in.
            new_value: New array to display.
            animate: Whether to animate the changes (True) or update
                instantly (False).
            left_aligned: Whether to maintain left edge alignment.
            run_time: Duration of animation if animate=True.
        """

        if not self.data and not new_value:
            return

        new_group = Array(
            new_value,
            font=self.font,
            bg_color=self.bg_color,
            font_size=self.font_size,
        )

        if left_aligned:
            new_group.align_to(self.get_left(), mn.LEFT)
            new_group.set_y(self.get_y())

        if animate:
            scene.play(mn.Transform(self, new_group), run_time=run_time)
            self._update_internal_state(new_group, new_value)
        else:
            scene.remove(self)
            self._update_internal_state(new_group, new_value)
            scene.add(self)

    def pointers(
        self,
        idx_list: list[int],
        pos: int = 0,
        color_1: ManimColor | str = mn.RED,
        color_2: ManimColor | str = mn.BLUE,
        color_3: ManimColor | str = mn.GREEN,
    ):
        """Highlight pointers at one side (top | bottom) in array.

        Args:
            idx_list: List of indices to highlight (1-3 elements).
            pos: 0 for top side, 1 for bottom.
            color_1: idx_list[0] highlighted pointer color.
            color_2: idx_list[1] highlighted pointer color.
            color_3: idx_list[2] highlighted pointer color.

        Raises:
            ValueError: If idx_list has invalid length or pos is invalid.
        """

        if not self.data:
            return

        if not 1 <= len(idx_list) <= 3:
            raise ValueError("idx_list must contain between 1 and 3 indices")

        if pos not in (0, 1):
            raise ValueError("pos must be 0 (top) or 1 (bottom)")

        if pos == 0:
            pointers_mob = self.pointers_top
        elif pos == 1:
            pointers_mob = self.pointers_bottom

        if len(idx_list) == 1:
            i = idx_list[0]

            for idx, _ in enumerate(self.containers_mob):
                pointers_mob[idx][1].set_color(color_1 if idx == i else self.bg_color)

        elif len(idx_list) == 2:
            i = idx_list[0]
            j = idx_list[1]

            for idx, _ in enumerate(self.containers_mob):
                if idx == i == j:
                    pointers_mob[idx][0].set_color(color_1)
                    pointers_mob[idx][1].set_color(self.bg_color)
                    pointers_mob[idx][2].set_color(color_2)
                elif idx == i:
                    pointers_mob[idx][0].set_color(self.bg_color)
                    pointers_mob[idx][1].set_color(color_1)
                    pointers_mob[idx][2].set_color(self.bg_color)
                elif idx == j:
                    pointers_mob[idx][0].set_color(self.bg_color)
                    pointers_mob[idx][1].set_color(color_2)
                    pointers_mob[idx][2].set_color(self.bg_color)
                else:
                    pointers_mob[idx][0].set_color(self.bg_color)
                    pointers_mob[idx][1].set_color(self.bg_color)
                    pointers_mob[idx][2].set_color(self.bg_color)

        elif len(idx_list) == 3:
            i = idx_list[0]
            j = idx_list[1]
            k = idx_list[2]

            for idx, _ in enumerate(self.containers_mob):
                if idx == i == j == k:
                    pointers_mob[idx][0].set_color(color_1)
                    pointers_mob[idx][1].set_color(color_2)
                    pointers_mob[idx][2].set_color(color_3)
                elif idx == i == j:
                    pointers_mob[idx][0].set_color(color_1)
                    pointers_mob[idx][1].set_color(self.bg_color)
                    pointers_mob[idx][2].set_color(color_2)
                elif idx == i == k:
                    pointers_mob[idx][0].set_color(color_1)
                    pointers_mob[idx][1].set_color(self.bg_color)
                    pointers_mob[idx][2].set_color(color_3)
                elif idx == k == j:
                    pointers_mob[idx][0].set_color(color_2)
                    pointers_mob[idx][1].set_color(self.bg_color)
                    pointers_mob[idx][2].set_color(color_3)
                elif idx == i:
                    pointers_mob[idx][0].set_color(self.bg_color)
                    pointers_mob[idx][1].set_color(color_1)
                    pointers_mob[idx][2].set_color(self.bg_color)
                elif idx == j:
                    pointers_mob[idx][0].set_color(self.bg_color)
                    pointers_mob[idx][1].set_color(color_2)
                    pointers_mob[idx][2].set_color(self.bg_color)
                elif idx == k:
                    pointers_mob[idx][0].set_color(self.bg_color)
                    pointers_mob[idx][1].set_color(color_3)
                    pointers_mob[idx][2].set_color(self.bg_color)
                else:
                    pointers_mob[idx][0].set_color(self.bg_color)
                    pointers_mob[idx][1].set_color(self.bg_color)
                    pointers_mob[idx][2].set_color(self.bg_color)

    def pointers_on_value(
        self,
        val: int,
        pos: int = 1,
        color: ManimColor | str = mn.BLACK,
    ):
        """Highlight middle pointers on all cells whose values
        equal the provided value.

        Args:
            val: The value to compare with array elements.
            pos: 0 for top pointers, 1 for bottom pointers.
            color: Color for the highlighted pointer.
        """

        if not self.data:
            return

        if pos not in (0, 1):
            raise ValueError("pos must be 0 (top) or 1 (bottom)")

        if pos == 0:
            pointers_mob = self.pointers_top
        elif pos == 1:
            pointers_mob = self.pointers_bottom

        for idx, _ in enumerate(self.containers_mob):
            pointers_mob[idx][1].set_color(
                color if self.data[idx] == val else self.bg_color
            )

    def highlight_cells(
        self,
        idx_list: list[int],
        color_1: ManimColor | str = mn.RED,
        color_2: ManimColor | str = mn.BLUE,
        color_3: ManimColor | str = mn.GREEN,
        color_123: ManimColor | str = mn.BLACK,
        color_12: ManimColor | str = mn.PURPLE,
        color_13: ManimColor | str = mn.YELLOW_E,
        color_23: ManimColor | str = mn.TEAL,
    ):
        """Highlight cells in the array visualization.

        Note:
            Cell coloring methods are mutually exclusive - the last called
            method determines the final appearance.

        Args:
            idx_list: List of indices to highlight.
            color_1: Color for the idx_list[0].
            color_2: Color for the idx_list[1].
            color_3: Color for the idx_list[2].
            color_123: Color if all three indices are the same.
            color_12: Color if idx_list[0] == idx_list[1].
            color_13: Color if idx_list[0] == idx_list[2].
            color_23: Color if idx_list[1] == idx_list[2].

        Raises:
            ValueError: If idx_list has invalid length.
        """

        if not self.data:
            return

        if not 1 <= len(idx_list) <= 3:
            raise ValueError("idx_list must contain between 1 and 3 indices")

        if len(idx_list) == 1:
            i = idx_list[0]

            for idx, mob in enumerate(self.containers_mob):
                mob.set_fill(color_1 if idx == i else self.bg_color)

        elif len(idx_list) == 2:
            i = idx_list[0]
            j = idx_list[1]

            for idx, mob in enumerate(self.containers_mob):
                if idx == i == j:
                    mob.set_fill(color_12)
                elif idx == i:
                    mob.set_fill(color_1)
                elif idx == j:
                    mob.set_fill(color_2)
                else:
                    mob.set_fill(self.bg_color)

        elif len(idx_list) == 3:
            i = idx_list[0]
            j = idx_list[1]
            k = idx_list[2]

            for idx, mob in enumerate(self.containers_mob):
                if idx == i == j == k:
                    mob.set_fill(color_123)
                elif idx == i == j:
                    mob.set_fill(color_12)
                elif idx == i == k:
                    mob.set_fill(color_13)
                elif idx == k == j:
                    mob.set_fill(color_23)
                elif idx == i:
                    mob.set_fill(color_1)
                elif idx == j:
                    mob.set_fill(color_2)
                elif idx == k:
                    mob.set_fill(color_3)
                else:
                    mob.set_fill(self.bg_color)

    def highlight_cells_with_value(
        self,
        val: int | str,
        color: ManimColor | str = mn.BLACK,
    ):
        """Highlight all cells whose values equal the provided value.

        Note:
            Cell coloring methods are mutually exclusive - the last called
            method determines the final appearance.

        Args:
            val: The value to compare with array elements.
            color: Color for the highlighted pointer.
        """

        if not self.data:
            return

        for idx, mob in enumerate(self.containers_mob):
            mob.set_fill(color if self.data[idx] == val else self.bg_color)


class String(mn.VGroup):
    """String visualization as a VGroup of character cells with quotes.

    Args:
        string: Text string to visualize.
        vector: Position offset from mob_center.
        font: Font family for text elements.
        font_size: Font size for text, scales the whole mobject.
        weight: Font weight (NORMAL, BOLD, etc.).
        font_color: Color for text elements.
        bg_color: Background color for quote cells and default pointer color.
        fill_color: Fill color for character cells.
        cell_color: Border color for cells.
        mob_center: Reference mobject for positioning.
        align_edge: Edge alignment relative to mob_center.
        cell_params_auto: Whether to auto-calculate cell parameters.
        cell_height: Manual cell height when auto-calculation disabled.
        top_bottom_buff: Internal top/bottom padding within cells.
        top_buff: Top alignment buffer for quotes and accents.
        bottom_buff: Bottom alignment buffer for most characters.
        deep_bottom_buff: Deep bottom alignment for descending characters.

    Note:
        Character alignment is automatically handled based on typography:
        - Top: Quotes and accents (", ', ^, `)
        - Center: Numbers, symbols, brackets, and operators
        - Deep bottom: Descenders (y, p, g, j)
        - Bottom: Most letters and other characters
        Empty string display as quoted empty cell.
    """

    def __init__(
        self,
        string: str,
        vector: np.ndarray = mn.ORIGIN,
        font="",
        font_size=35,
        weight: str = "NORMAL",
        font_color: ManimColor | str = mn.WHITE,
        bg_color: ManimColor | str = mn.DARK_GRAY,
        fill_color: ManimColor | str = mn.GRAY,
        cell_color: ManimColor | str = mn.DARK_GRAY,
        mob_center: mn.Mobject = mn.Dot(mn.ORIGIN),
        align_edge: Literal["up", "down", "left", "right"] | None = None,
        # ---- cell params ----
        cell_params_auto=True,
        cell_height=0.65625,
        top_bottom_buff=0.15,
        top_buff=0.09,
        bottom_buff=0.16,
        deep_bottom_buff=0.05,
    ):
        # call __init__ of the parent classes
        super().__init__()
        # add class attributes
        self.data = string
        self.vector = vector
        self.font = font
        self.weight = weight
        self.font_color = font_color
        self.bg_color = bg_color
        self.fill_color = fill_color
        self.mob_center = mob_center
        self.align_edge = align_edge

        self.TEXT_CONFIG = {
            "font_size": font_size,
            "font": font,
            "color": font_color,
            "weight": weight,
        }

        # --------- cells params ------------

        if cell_params_auto:
            cell_params = utils.get_cell_params(font_size, font, weight)
            self.cell_height = cell_params["cell_height"]
            self.top_bottom_buff = cell_params["top_bottom_buff"]
            self.top_buff = cell_params["top_buff"]
            self.bottom_buff = cell_params["bottom_buff"]
            self.deep_bottom_buff = cell_params["deep_bottom_buff"]
        else:
            self.cell_height = cell_height
            self.top_bottom_buff = top_bottom_buff
            self.top_buff = top_buff
            self.bottom_buff = bottom_buff
            self.deep_bottom_buff = deep_bottom_buff

        # NB: if opacity is not specified, it will be set to None
        # and some methods will break for unknown reasons
        self.SQUARE_CONFIG = {
            "side_length": self.cell_height,
            "fill_opacity": 1,
        }
        # --------- empty value ------------

        if not string:
            self.text_mob = mn.Text('""', **self.TEXT_CONFIG)
            self.containers_mob = mn.Square(
                **self.SQUARE_CONFIG,
                color=cell_color,
                fill_color=fill_color,
            )
            utils.position(self.containers_mob, mob_center, align_edge, vector)
            self.text_mob.next_to(
                self.containers_mob.get_top(),
                direction=mn.DOWN,
                buff=top_buff,
            )
            self.add(self.containers_mob, self.text_mob)
            return

        # --------- cells ------------

        # construction: Create square mobjects for each letter
        self.containers_mob = mn.VGroup(
            *[
                mn.Square(
                    **self.SQUARE_CONFIG,
                    color=cell_color,
                    fill_color=fill_color,
                )
                for _ in string
            ]
        )
        # construction: Arrange squares in a row
        self.containers_mob.arrange(mn.RIGHT, buff=0.0)
        self.letters_cell_left_edge = self.containers_mob.get_left()

        # construction: Move VGroup to the specified position
        utils.position(self.containers_mob, mob_center, align_edge, vector)

        quote_cell_mob = [
            mn.Square(**self.SQUARE_CONFIG, color=bg_color, fill_color=bg_color)
            for _ in range(2)
        ]

        quote_cell_mob[0].next_to(self.containers_mob, mn.LEFT, buff=0.0)
        quote_cell_mob[1].next_to(self.containers_mob, mn.RIGHT, buff=0.0)

        self.all_cell_mob = mn.VGroup(
            [quote_cell_mob[0], self.containers_mob, quote_cell_mob[1]],
        )

        self.quote_cell_left_edge = self.all_cell_mob.get_left()

        # construction: text mobs quotes group
        self.quotes_mob = mn.VGroup(
            mn.Text('"', **self.TEXT_CONFIG)
            .move_to(quote_cell_mob[0], aligned_edge=mn.UP + mn.RIGHT)
            .shift(mn.DOWN * top_buff),
            mn.Text('"', **self.TEXT_CONFIG)
            .move_to(quote_cell_mob[1], aligned_edge=mn.UP + mn.LEFT)
            .shift(mn.DOWN * top_buff),
        )

        # ------ values ---------

        # construction: Create text mobjects and move them in squares
        self.values_mob = mn.VGroup(
            *[mn.Text(str(letter), **self.TEXT_CONFIG) for letter in string]
        )

        for i in range(len(string)):
            if string[i] in "\"'^`":  # top alignment
                self.values_mob[i].next_to(
                    self.containers_mob[i].get_top(),
                    direction=mn.DOWN,
                    buff=self.top_buff,
                )
            elif string[i] in "<>-=+~:#%*[]{}()\\/|@&$0123456789":  # center alignment
                self.values_mob[i].move_to(self.containers_mob[i])
            elif string[i] in "ypgj":  # deep bottom alignment
                self.values_mob[i].next_to(
                    self.containers_mob[i].get_bottom(),
                    direction=mn.UP,
                    buff=self.deep_bottom_buff,
                )
            else:  # bottom alignment
                self.values_mob[i].next_to(
                    self.containers_mob[i].get_bottom(),
                    direction=mn.UP,
                    buff=self.bottom_buff,
                )

        # ------- pointers ----------

        self.pointers_top, self.pointers_bottom = utils.create_pointers(
            self, self.containers_mob
        )

        # ------- add ----------

        # adds local objects as instance attributes
        self.add(
            self.all_cell_mob,
            self.values_mob,
            self.quotes_mob,
            self.pointers_top,
            self.pointers_bottom,
        )

        self.coordinate_y = self.get_y()

    def first_appear(self, scene: mn.Scene, time=0.5):
        """Animate the initial appearance of the string in scene.

        Args:
            scene: The scene to play the animation in.
            time: Duration of the fade-in animation.
        """

        scene.play(mn.FadeIn(self), run_time=time)

    def _update_internal_state(self, new_group: "String", new_value: str):
        """Update internal state for new made class instance.

        Args:
            new_group: New String instance to copy state from.
            new_value: New string value.
        """

        # save old attributes with highlights
        old_cells = getattr(self, "containers_mob", None)
        old_pointers_top = getattr(self, "pointers_top", None)
        old_pointers_bottom = getattr(self, "pointers_bottom", None)

        self.data = new_value
        self.containers_mob = new_group.containers_mob
        self.submobjects = new_group.submobjects.copy()

        self.quote_cell_left_edge = new_group.quote_cell_left_edge
        self.letters_cell_left_edge = new_group.letters_cell_left_edge

        if self.data:
            self.values_mob = new_group.values_mob

            self.pointers_top = new_group.pointers_top
            self.pointers_bottom = new_group.pointers_bottom

            # restore old highlights
            if old_cells:
                for old, new in zip(old_cells, self.containers_mob):
                    new.set_fill(old.get_fill_color())

            if old_pointers_top:
                for old_ptrs, new_ptrs in zip(old_pointers_top, self.pointers_top):
                    for old_tri, new_tri in zip(old_ptrs, new_ptrs):
                        new_tri.set_color(old_tri.get_color())

            if old_pointers_bottom:
                for old_ptrs, new_ptrs in zip(
                    old_pointers_bottom, self.pointers_bottom
                ):
                    for old_tri, new_tri in zip(old_ptrs, new_ptrs):
                        new_tri.set_color(old_tri.get_color())

        else:
            self.pointers_top = mn.VGroup()
            self.pointers_bottom = mn.VGroup()

    def update_value(
        self,
        scene: mn.Scene,
        new_value: str,
        animate: bool = False,
        left_aligned=True,
        run_time: float = 0.2,
    ) -> None:
        """Replace mobject with new one based on new_value.

        Args:
            scene: The scene to play animations in.
            new_value: New string value to display.
            animate: Whether to animate the changes.
            left_aligned: Whether to maintain left edge alignment.
            run_time: Duration of animation if animate=True.
        """

        if not self.data and not new_value:
            return

        new_group = String(
            new_value,
            font=self.font,
            weight=self.weight,
            font_color=self.font_color,
            bg_color=self.bg_color,
            fill_color=self.fill_color,
        )
        new_group.coordinate_y = self.coordinate_y

        if left_aligned:
            new_group.quote_cell_left_edge = self.quote_cell_left_edge
            new_group.letters_cell_left_edge = self.letters_cell_left_edge

            if new_value:
                left_edge = self.quote_cell_left_edge
            else:
                left_edge = self.letters_cell_left_edge

            new_group.align_to(left_edge, mn.LEFT)
            new_group.set_y(self.coordinate_y)

        else:
            new_group.move_to(self.mob_center)
            new_group.shift(self.vector)

        if animate:
            scene.play(mn.Transform(self, new_group), run_time=run_time)
            self._update_internal_state(new_group, new_value)

        else:
            scene.remove(self)
            self._update_internal_state(new_group, new_value)
            scene.add(self)

    def pointers(
        self,
        idx_list: list[int],
        pos: int = 0,
        color_1: ManimColor | str = mn.RED,
        color_2: ManimColor | str = mn.BLUE,
        color_3: ManimColor | str = mn.GREEN,
    ):
        """Highlight pointers at one side (top | bottom) in string.

        Args:
            idx_list: List of indices to highlight (1-3 elements).
            pos: 0 for top pointers, 1 for bottom pointers.
            color_1: Color for idx_list[0] pointer.
            color_2: Color for idx_list[1] pointer.
            color_3: Color for idx_list[2] pointer.

        Raises:
            ValueError: If idx_list has invalid length or pos is invalid.
        """
        if not self.data:
            return

        if not 1 <= len(idx_list) <= 3:
            raise ValueError("idx_list must contain between 1 and 3 indices")

        if pos not in (0, 1):
            raise ValueError("pos must be 0 (top) or 1 (bottom)")

        if pos == 0:
            pointers_mob = self.pointers_top
        elif pos == 1:
            pointers_mob = self.pointers_bottom

        if len(idx_list) == 1:
            i = idx_list[0]

            for idx, _ in enumerate(self.containers_mob):
                pointers_mob[idx][1].set_color(color_1 if idx == i else self.bg_color)

        elif len(idx_list) == 2:
            i = idx_list[0]
            j = idx_list[1]

            for idx, _ in enumerate(self.containers_mob):
                if idx == i == j:
                    pointers_mob[idx][0].set_color(color_1)
                    pointers_mob[idx][1].set_color(self.bg_color)
                    pointers_mob[idx][2].set_color(color_2)
                elif idx == i:
                    pointers_mob[idx][0].set_color(self.bg_color)
                    pointers_mob[idx][1].set_color(color_1)
                    pointers_mob[idx][2].set_color(self.bg_color)
                elif idx == j:
                    pointers_mob[idx][0].set_color(self.bg_color)
                    pointers_mob[idx][1].set_color(color_2)
                    pointers_mob[idx][2].set_color(self.bg_color)
                else:
                    pointers_mob[idx][0].set_color(self.bg_color)
                    pointers_mob[idx][1].set_color(self.bg_color)
                    pointers_mob[idx][2].set_color(self.bg_color)

        elif len(idx_list) == 3:
            i = idx_list[0]
            j = idx_list[1]
            k = idx_list[2]

            for idx, _ in enumerate(self.containers_mob):
                if idx == i == j == k:
                    pointers_mob[idx][0].set_color(color_1)
                    pointers_mob[idx][1].set_color(color_2)
                    pointers_mob[idx][2].set_color(color_3)
                elif idx == i == j:
                    pointers_mob[idx][0].set_color(color_1)
                    pointers_mob[idx][1].set_color(self.bg_color)
                    pointers_mob[idx][2].set_color(color_2)
                elif idx == i == k:
                    pointers_mob[idx][0].set_color(color_1)
                    pointers_mob[idx][1].set_color(self.bg_color)
                    pointers_mob[idx][2].set_color(color_3)
                elif idx == k == j:
                    pointers_mob[idx][0].set_color(color_2)
                    pointers_mob[idx][1].set_color(self.bg_color)
                    pointers_mob[idx][2].set_color(color_3)
                elif idx == i:
                    pointers_mob[idx][0].set_color(self.bg_color)
                    pointers_mob[idx][1].set_color(color_1)
                    pointers_mob[idx][2].set_color(self.bg_color)
                elif idx == j:
                    pointers_mob[idx][0].set_color(self.bg_color)
                    pointers_mob[idx][1].set_color(color_2)
                    pointers_mob[idx][2].set_color(self.bg_color)
                elif idx == k:
                    pointers_mob[idx][0].set_color(self.bg_color)
                    pointers_mob[idx][1].set_color(color_3)
                    pointers_mob[idx][2].set_color(self.bg_color)
                else:
                    pointers_mob[idx][0].set_color(self.bg_color)
                    pointers_mob[idx][1].set_color(self.bg_color)
                    pointers_mob[idx][2].set_color(self.bg_color)

    def pointers_on_value(
        self,
        val: str,
        pos: int = 1,
        color: ManimColor | str = mn.BLACK,
    ):
        """Highlight middle pointers on cells with matching value.

        Args:
            val: The value to compare with string elements.
            pos: 0 for top pointers, 1 for bottom pointers.
            color: Color for highlighted pointers.
        """

        if not self.data:
            return

        if pos not in (0, 1):
            raise ValueError("pos must be 0 (top) or 1 (bottom)")

        if pos == 0:
            pointers_mob = self.pointers_top
        elif pos == 1:
            pointers_mob = self.pointers_bottom

        for idx, _ in enumerate(self.containers_mob):
            pointers_mob[idx][1].set_color(
                color if self.data[idx] == val else self.bg_color
            )

    def highlight_cells(
        self,
        idx_list: list[int],
        color_1: ManimColor | str = mn.RED,
        color_2: ManimColor | str = mn.BLUE,
        color_3: ManimColor | str = mn.GREEN,
        color_123: ManimColor | str = mn.BLACK,
        color_12: ManimColor | str = mn.PURPLE,
        color_13: ManimColor | str = mn.YELLOW_E,
        color_23: ManimColor | str = mn.TEAL,
    ):
        """Highlight blocks in the string visualization.

        Args:
            idx_list: List of indices to highlight.
            color_1: Color for the idx_list[0].
            color_2: Color for the idx_list[1].
            color_3: Color for the idx_list[2].
            color_123: Color if all three indices are the same.
            color_12: Color if idx_list[0] == idx_list[1].
            color_13: Color if idx_list[0] == idx_list[2].
            color_23: Color if idx_list[1] == idx_list[2].

        Raises:
            ValueError: If idx_list has invalid length.
        """

        if not self.data:
            return

        if not 1 <= len(idx_list) <= 3:
            raise ValueError("idx_list must contain between 1 and 3 indices")

        if len(idx_list) == 1:
            i = idx_list[0]

            for idx, mob in enumerate(self.containers_mob):
                mob.set_fill(color_1 if idx == i else self.fill_color)

        elif len(idx_list) == 2:
            i = idx_list[0]
            j = idx_list[1]

            for idx, mob in enumerate(self.containers_mob):
                if idx == i == j:
                    mob.set_fill(color_12)
                elif idx == i:
                    mob.set_fill(color_1)
                elif idx == j:
                    mob.set_fill(color_2)
                else:
                    mob.set_fill(self.fill_color)

        elif len(idx_list) == 3:
            i = idx_list[0]
            j = idx_list[1]
            k = idx_list[2]

            for idx, mob in enumerate(self.containers_mob):
                if idx == i == j == k:
                    mob.set_fill(color_123)
                elif idx == i == j:
                    mob.set_fill(color_12)
                elif idx == i == k:
                    mob.set_fill(color_13)
                elif idx == k == j:
                    mob.set_fill(color_23)
                elif idx == i:
                    mob.set_fill(color_1)
                elif idx == j:
                    mob.set_fill(color_2)
                elif idx == k:
                    mob.set_fill(color_3)
                else:
                    mob.set_fill(self.fill_color)

    def highlight_cells_with_value(
        self,
        val: str,
        color: ManimColor | str = mn.BLACK,
    ):
        """Highlight all cells whose values equal the provided value.

        Args:
            val: The value to compare with string elements.
            color: Color for highlighted cells.
        """

        if not self.data:
            return

        for idx, mob in enumerate(self.containers_mob):
            mob.set_fill(color if self.data[idx] == val else self.fill_color)


class LinkedList(mn.VGroup):
    """
    ...
    """

    def __init__(
        self,
        head: ListNode,
    ): ...


class RelativeTextValue(mn.VGroup):
    """Text group showing scope variables positioned relative to mobject.

    Args:
        *vars: Tuples of (name, value_getter, color) for each text.
        mob_center: Reference mobject for positioning.
        font: Text font family.
        font_size: Text font size.
        buff: Spacing between text elements.
        equal_sign: Whether to use equals sign between name and value.
        vector: Offset vector from reference mobject center.
        align_edge: Edge to align with reference mobject. If None,
            centers at mobject center.

    Raises:
        ValueError: If align_edge is not valid direction.
    """

    def __init__(
        self,
        *vars: Tuple[str, Callable[[], Any], str | ManimColor],
        mob_center: mn.Mobject = mn.Dot(mn.ORIGIN),
        font="",
        font_size=35,
        buff=0.5,
        equal_sign: bool = True,
        vector: np.ndarray = mn.UP * 1.2,
        align_edge: Literal["up", "down", "left", "right"] | None = None,
    ):
        super().__init__()
        self.vars = vars
        self.mob_center = mob_center
        self.font = font
        self.font_size = font_size
        self.buff = buff
        self.vector = vector
        self.align_edge = align_edge
        self.equal_sign = equal_sign

        self.submobjects: List = []
        parts = [
            mn.Text(
                f"{name} = {value()}" if equal_sign else f"{name} {value()}",
                font=self.font,
                font_size=self.font_size,
                color=color,
            )
            for name, value, color in self.vars
        ]
        text_mob = mn.VGroup(*parts).arrange(
            mn.RIGHT, buff=self.buff, aligned_edge=mn.UP
        )

        # construction: Move VGroup to the specified position
        utils.position(text_mob, mob_center, align_edge, vector)

        self.add(*text_mob)

    def first_appear(self, scene: mn.Scene, time=0.5):
        """Animate the initial appearance of the text group in scene.

        Args:
            scene: The scene to play the animation in.
            time: Duration of the fade-in animation.
        """

        scene.play(mn.FadeIn(self), run_time=time)

    def update_text(self, scene: mn.Scene, time=0.1, animate: bool = False):
        """Update text values with current variable values.

        Args:
            scene: The scene to play animations in.
            time: Duration of animation if animate=True.
            animate: Whether to animate the update.
        """

        # save position
        old_left_edge = self.get_left()
        old_y = self.get_y()

        # create a new object with the same parameters
        new_group = RelativeTextValue(
            *self.vars,
            font_size=self.font_size,
            buff=self.buff,
            font=self.font,
            equal_sign=self.equal_sign,
        )

        # move to position
        new_group.align_to(old_left_edge, mn.LEFT)
        new_group.set_y(old_y)

        if animate:
            scene.play(mn.Transform(self, new_group), run_time=time)
        else:
            scene.remove(self)
            self.become(new_group)
            scene.add(self)


class RelativeText(mn.VGroup):
    """Text group positioned relative to another mobject.

    Args:
        text: The text string to visualize.
        mob_center: Reference mobject for positioning.
        vector: Offset vector from reference mobject center.
        font: Text font family.
        font_size: Text font size.
        font_color: Text color.
        weight: Text weight (NORMAL, BOLD, etc.).
        align_edge: Edge to align with reference mobject. If None,
            centers at mobject center.

    Raises:
        ValueError: If align_edge is not valid direction.
    """

    def __init__(
        self,
        text: str,
        mob_center: mn.Mobject = mn.Dot(mn.ORIGIN),
        vector: np.ndarray = mn.ORIGIN,
        font="",
        font_size=35,
        font_color: str | ManimColor = mn.WHITE,
        weight: str = "NORMAL",
        align_edge: Literal["up", "down", "left", "right"] | None = None,
    ):
        super().__init__()

        text_mob = mn.Text(
            text,
            font=font,
            color=font_color,
            font_size=font_size,
            weight=weight,
        )

        # construction: Move VGroup to the specified position
        utils.position(text_mob, mob_center, align_edge, vector)

        self.add(text_mob)

    def first_appear(self, scene: mn.Scene, time=0.5):
        """Animate the initial appearance of the text in scene.

        Args:
            scene: The scene to play the animation in.
            time: Duration of the fade-in animation.
        """

        scene.play(mn.FadeIn(self), run_time=time)


class CodeBlock(mn.VGroup):
    """Code block visualization with syntax highlighting capabilities.

    Args:
        code_lines: List of code lines to display.
        vector: Position vector to place the code block.
        pre_code_lines: Lines to display before the main code.
        font_size: Font size for the code text.
        font: Font for the code text.
        font_color_regular: Color for regular text.
        font_color_highlight: Color for highlighted text.
        bg_highlight_color: Background color for highlighted lines.
        inter_block_buff: Buffer between pre-code and code blocks.
        pre_code_buff: Buffer between pre-code lines.
        code_buff: Buffer between code lines.
        mob_center: Center object for positioning.
        align_edge: Edge to align with reference mobject. If None,
            centers at mobject center.
    """

    def __init__(
        self,
        code_lines: List[str],
        vector: np.ndarray,
        pre_code_lines: List[str] = [],
        font_size=20,
        font="",
        font_color_regular: ManimColor | str = "WHITE",
        font_color_highlight: ManimColor | str = "YELLOW",
        bg_highlight_color: ManimColor | str = "BLUE",
        inter_block_buff=0.5,
        pre_code_buff=0.15,
        code_buff=0.05,
        mob_center: mn.Mobject = mn.Dot(mn.ORIGIN),
        align_edge: Literal["up", "down", "left", "right"] | None = None,
    ):
        super().__init__()
        self.font_color_regular = font_color_regular
        self.font_color_highlight = font_color_highlight
        self.bg_highlight_color = bg_highlight_color

        self.code_mobs = [
            mn.Text(line, font=font, font_size=font_size, color=self.font_color_regular)
            for line in code_lines
        ]
        self.bg_rects: List[Optional[mn.Rectangle]] = [None] * len(
            code_lines
        )  # list to save links on all possible rectangles and to manage=delete them

        code_vgroup = mn.VGroup(*self.code_mobs).arrange(
            mn.DOWN,
            aligned_edge=mn.LEFT,
            buff=code_buff,
        )

        if pre_code_lines:
            self.pre_code_mobs = [
                mn.Text(
                    line, font=font, font_size=font_size, color=self.font_color_regular
                )
                for line in pre_code_lines
            ]
            pre_code_vgroup = mn.VGroup(*self.pre_code_mobs).arrange(
                mn.DOWN,
                aligned_edge=mn.LEFT,
                buff=pre_code_buff,
            )
            block_vgroup = mn.VGroup(pre_code_vgroup, code_vgroup).arrange(
                mn.DOWN,
                aligned_edge=mn.LEFT,
                buff=inter_block_buff,
            )
        else:
            block_vgroup = code_vgroup

        # construction: Move VGroup to the specified position
        utils.position(block_vgroup, mob_center, align_edge, vector)

        self.add(block_vgroup)

    def first_appear(self, scene: mn.Scene, time=0.5):
        """Animate the initial appearance of the code block in scene.

        Args:
            scene: The scene to play the animation in.
            time: Duration of the fade-in animation.
        """

        scene.play(mn.FadeIn(self), run_time=time)

    def highlight_line(self, i: int):
        """Highlights a single line of code with background and text color.

        Args:
            i: Index of the line to highlight.
        """

        for k, mob in enumerate(self.code_mobs):
            if k == i:
                # change font color
                mob.set_color(self.font_color_highlight)
                # create bg rectangle
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
                    bg_rect.z_index = -1  # send background to back
                    self.bg_rects[k] = bg_rect
            else:
                # normal line: regular font color
                mob.set_color(self.font_color_regular)
                # remove rect
                bg_rect = self.bg_rects[k]
                if bg_rect:
                    self.remove(bg_rect)
                    self.bg_rects[k] = None


class TitleText(mn.VGroup):
    """Title group with optional decorative flourish and undercaption.

    Args:
        text: The title text to display.
        vector: Offset vector from center for positioning.
        text_color: Color of the title text.
        font: Font family for the title text.
        font_size: Font size for the title text.
        mob_center: Reference mobject for positioning.
        align_edge: Edge to align with reference mobject. If None,
            centers at mobject center.
        flourish: Whether to render flourish under the text.
        flourish_color: Color of the flourish line.
        flourish_stroke_width: Stroke width of the flourish.
        flourish_padding: Padding between text and flourish.
        flourish_buff: Buffer between text and flourish.
        spiral_offset: Vertical offset of spirals relative to flourish.
        spiral_radius: Radius of the spiral ends of the flourish.
        spiral_turns: Number of turns in each spiral.
        undercaption: Text under the flourish.
        undercaption_color: Color of the undercaption text.
        undercaption_font: Font family for the undercaption.
        undercaption_font_size: Font size for the undercaption.
        undercaption_buff: Buffer between text and undercaption.
        **kwargs: Additional keyword arguments for text mobject.
    """

    def __init__(
        self,
        # --------- text --------------
        text: str,
        vector: np.ndarray = mn.UP * 2.7,
        text_color: ManimColor | str = "WHITE",
        font: str = "",
        font_size: float = 50,
        mob_center: mn.Mobject = mn.Dot(mn.ORIGIN),
        align_edge: Literal["up", "down", "left", "right"] | None = None,
        # ------- flourish ------------
        flourish: bool = False,
        flourish_color: ManimColor | str = "WHITE",
        flourish_stroke_width: float = 4,
        flourish_padding: float = 0.2,
        flourish_buff: float = 0.15,
        spiral_offset: float = 0.3,
        spiral_radius: float = 0.15,
        spiral_turns: float = 1.0,
        # ------- undercaption ------------
        undercaption: str = "",
        undercaption_color: ManimColor | str = "WHITE",
        undercaption_font: str = "",
        undercaption_font_size: float = 20,
        undercaption_buff: float = 0.23,
        # ----------- kwargs ------------
        **kwargs,
    ):
        super().__init__()

        # create the text mobject
        text_mobject = mn.Text(
            text,
            font=font,
            font_size=font_size,
            color=text_color,
            **kwargs,
        )

        utils.position(text_mobject, mob_center, align_edge, vector)

        self.add(text_mobject)

        # optionally create the flourish under the text
        if flourish:
            flourish_width = (
                # self.text_mobject.width * flourish_width_ratio + flourish_padding
                text_mobject.width + flourish_padding
            )
            self.flourish = self._create_flourish(
                width=flourish_width,
                color=flourish_color,
                stroke_width=flourish_stroke_width,
                spiral_radius=spiral_radius,
                spiral_turns=spiral_turns,
                spiral_offset=spiral_offset,
            )
            # position the flourish below the text
            self.flourish.next_to(text_mobject, mn.DOWN, flourish_buff)
            self.add(self.flourish)

        # optionally create the undercaption under the text
        if undercaption:
            # create the text mobject
            self.undercaption = mn.Text(
                undercaption,
                font=undercaption_font,
                font_size=undercaption_font_size,
                color=undercaption_color,
                **kwargs,
            )
            self.undercaption.next_to(text_mobject, mn.DOWN, undercaption_buff)
            self.add(self.undercaption)

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
            width: Total width of the flourish.
            color: Color of the flourish.
            stroke_width: Stroke width of the flourish.
            spiral_radius: Radius of the spiral ends.
            spiral_turns: Number of turns in each spiral.
            spiral_offset: Vertical offset of the spirals.

        Returns:
            Group containing the flourish components.
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

    def appear(self, scene: mn.Scene):
        """Add the entire title group to the given scene.

        Args:
            scene: The scene to add the title group to.
        """

        scene.add(self)


class TitleLogo(mn.VGroup):
    """Group for displaying SVG logo with optional text.

    Args:
        svg: Path to the SVG file.
        svg_height: Height of the SVG.
        mob_center: Reference mobject for positioning.
        align_edge: Edge to align with reference mobject. If None,
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
        # ----------- svg -------------
        svg_height: float = 2.0,
        mob_center: mn.Mobject = mn.Dot(mn.ORIGIN),
        align_edge: Literal["up", "down", "left", "right"] | None = None,
        vector: np.ndarray = mn.ORIGIN,
        # --------- text --------------
        text: str | None = None,
        text_color: ManimColor | str = "WHITE",
        font: str = "",
        font_size: float = 31,
        text_vector: np.ndarray = mn.ORIGIN,
        # --------- kwargs -------------
        **kwargs,
    ):
        super().__init__()

        # create the svg mobject
        self.svg = mn.SVGMobject(
            svg,
            height=svg_height,
            **kwargs,
        )

        # position the entire group relative to the reference mobject and offset vector
        utils.position(self.svg, mob_center, align_edge, vector)

        self.add(self.svg)

        # create the text mobject
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

    def appear(self, scene: mn.Scene):
        """Add the entire logo group to the given scene.

        Args:
            scene: The scene to add the logo group to.
        """
        scene.add(self)
