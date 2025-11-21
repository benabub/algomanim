"""
Manim use notes:

  - mobject.arrange() resets previous position
  - fill_color requires fill_opacity=1 to be visible
  - Simply assigning  causes an unexpected shift in position:
    example: var = mobject
"""

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


from .datastructures import (
    #     Node,
    #     TreeNode,
    ListNode,
)
from .svg import SVG_DIR


class AlgoManimBase(mn.VGroup):
    """Base class for all algomanim classes"""

    def __init__(self):
        super().__init__()
        # ---- position ----
        self._vector: np.ndarray = mn.ORIGIN
        self._mob_center: mn.Mobject = mn.Dot(mn.ORIGIN)
        self._align_edge: Literal["up", "down", "left", "right"] | None = None

    def first_appear(self, scene: mn.Scene, time=0.5):
        """Animate the initial appearance in scene.

        Args:
            scene: The scene to play the animation in.
            time: Duration of the fade-in animation.
        """
        scene.play(mn.FadeIn(self), run_time=time)

    def appear(self, scene: mn.Scene):
        """Add VGroup the given scene.

        Args:
            scene: The scene to add the logo group to.
        """
        scene.add(self)

    def _position(
        self,
        mobject_to_move: mn.Mobject,
        align_point: mn.Mobject,
    ) -> None:
        """Position mobject relative to center with optional edge alignment.

        Args:
            mobject: The object to position
            mob_center: Reference center object
        """

        align_edge = self._align_edge.lower() if self._align_edge else None

        if isinstance(self._mob_center, VisualDataStructure):
            mob_center = self._mob_center.get_containers_mob()
        else:
            mob_center = self._mob_center

        mobject_point = align_point.get_center()
        target_point = mob_center.get_center() + self._vector

        if align_edge:
            if align_edge == "left":
                mobject_point = align_point.get_left()
                target_point = mob_center.get_left() + self._vector

            elif align_edge == "right":
                mobject_point = align_point.get_right()
                target_point = mob_center.get_right() + self._vector

            elif align_edge == "up":
                mobject_point = align_point.get_top()
                target_point = mob_center.get_top() + self._vector

            elif align_edge == "down":
                mobject_point = align_point.get_bottom()
                target_point = mob_center.get_bottom() + self._vector

        shift_vector = target_point - mobject_point
        mobject_to_move.shift(shift_vector)


class VisualDataStructure(AlgoManimBase):
    """Base class for visual data structures with common attributes and methods."""

    def __init__(self):
        super().__init__()

        self._data = None

        # --- mobjects ---
        self._containers_mob = mn.VGroup()
        self._values_mob = mn.VGroup()
        self._pointers_top = mn.VGroup()
        self._pointers_bottom = mn.VGroup()

        # --- containers colors ---
        self._container_color: ManimColor | str = mn.LIGHT_GRAY
        self._fill_color: ManimColor | str = mn.GRAY
        self._bg_color: ManimColor | str = mn.DARK_GRAY

        # --- colors state management ---
        self._containers_colors: dict[int, ManimColor | str] = {}
        self._top_pointers_colors: dict[int, list[ManimColor | str]] = {}
        self._bottom_pointers_colors: dict[int, list[ManimColor | str]] = {}

        # ---- position ----
        self._vector: np.ndarray = mn.ORIGIN
        self._mob_center: mn.Mobject = mn.Dot(mn.ORIGIN)
        self._align_edge: Literal["up", "down", "left", "right"] | None = None

        # ---- font ----
        self._font = ("",)
        self._font_size = (35,)
        self._font_color: ManimColor | str = mn.WHITE
        self._weight: str = "NORMAL"

        # ---- container colors ----
        self._container_color: ManimColor | str = mn.DARK_GRAY
        self._fill_color: ManimColor | str = mn.GRAY
        self._bg_color: ManimColor | str = mn.DARK_GRAY

        # ---- highlight containers colors ----
        self._color_1: ManimColor | str = mn.RED
        self._color_2: ManimColor | str = mn.BLUE
        self._color_3: ManimColor | str = mn.GREEN
        self._color_123: ManimColor | str = mn.BLACK
        self._color_12: ManimColor | str = mn.PURPLE
        self._color_13: ManimColor | str = mn.YELLOW_E
        self._color_23: ManimColor | str = mn.TEAL

    def get_containers_mob(self):
        return self._containers_mob

    def _text_config(self):
        return {
            "font": self._font,
            "font_size": self._font_size,
            "weight": self._weight,
            "color": self._font_color,
        }

    def clear_pointers_highlights(self, pos: int):
        """Clear the highlights for pointers at the specified position.

        Args:
            pos: Position to clear highlights for (0 for top, 1 for bottom).
        """

        if pos not in (0, 1):
            raise ValueError("pos must be 0 (top) or 1 (bottom)")

        if pos == 0:
            self._top_pointers_colors = {}
        elif pos == 1:
            self._bottom_pointers_colors = {}

        self._apply_pointers_colors(pos)

    def clear_containers_highlights(self):
        """Clear the highlights for all containers."""
        self._containers_colors = {}
        self._apply_containers_colors()

    def _apply_containers_colors(self):
        """Apply stored color highlights to container objects."""

        for i, mob in enumerate(self._containers_mob):
            if i in self._containers_colors:
                if self._data:
                    mob.set_fill(self._containers_colors[i])
                else:
                    mob.set_fill(self._fill_color)
            else:
                mob.set_fill(self._fill_color)

    def _apply_pointers_colors(self, pos: int):
        """Apply stored color highlights to pointer objects at the specified position.

        Args:
            pos: Position to apply colors for (0 for top, 1 for bottom).
        """

        # ------- checks --------
        if pos not in (0, 1):
            raise ValueError("pos must be 0 (top) or 1 (bottom)")

        # ------- asserts --------
        if pos == 0:
            pointers = self._pointers_top
            colors_dict = self._top_pointers_colors

        elif pos == 1:
            pointers = self._pointers_bottom
            colors_dict = self._bottom_pointers_colors

        # ------- set colors --------
        for i, pointers_group in enumerate(pointers):
            if i in colors_dict:
                stored_group = colors_dict[i]
                if self._data:
                    for j in range(3):
                        pointers_group[j].set_color(stored_group[j])
                else:
                    for j in range(3):
                        pointers_group[j].set_color(self._bg_color)
            else:
                for j in range(3):
                    pointers_group[j].set_color(self._bg_color)

    def _update_internal_state(
        self,
        new_value,
        new_group: "VisualDataStructure",
    ):
        """Update internal state with data from a new group.

        Args:
            new_value: New data value to store.
            new_group: New group to copy state from.
        """
        self._data = new_value
        self._containers_mob = new_group._containers_mob
        self._values_mob = new_group._values_mob
        self._pointers_top = new_group._pointers_top
        self._pointers_bottom = new_group._pointers_bottom
        self.submobjects = new_group.submobjects

    def _save_highlights_states(self):
        """Save current highlight states for containers and pointers.

        Returns:
            Dictionary containing current highlight states.
        """
        return {
            "_containers_colors": self._containers_colors,
            "_top_pointers_colors": self._top_pointers_colors,
            "_bottom_pointers_colors": self._bottom_pointers_colors,
        }

    @staticmethod
    def _preserve_highlights_states(
        new_group: "VisualDataStructure",
        status: dict,
    ):
        """Apply saved highlight states to a new group.

        Args:
            new_group: Group to apply the saved states to.
            status: Dictionary containing the saved highlight states.
        """
        new_group._containers_colors = status["_containers_colors"]
        new_group._top_pointers_colors = status["_top_pointers_colors"]
        new_group._bottom_pointers_colors = status["_bottom_pointers_colors"]

        new_group._apply_containers_colors()
        new_group._apply_pointers_colors(0)
        new_group._apply_pointers_colors(1)

    def create_pointers(self, cell_mob: mn.VGroup) -> tuple[mn.VGroup, mn.VGroup]:
        """Create pointer triangles above and below each cell in the group.

        Args:
            cell_mob: VGroup of cells to attach pointers to.

        Returns:
            Tuple of (top_pointers, bottom_pointers) VGroups where each contains
            triple triangle groups for every cell | node.

        Note:
            Each cell gets 3 triangles above and 3 below, arranged horizontally.
            Triangle groups are positioned with fixed buffering from cells.
        """

        # create template triangles
        top_triangle = (
            mn.Triangle(color=self._bg_color)
            .stretch_to_fit_width(0.7)
            .scale(0.1)
            .rotate(mn.PI)
        )
        bottom_triangle = (
            mn.Triangle(color=self._bg_color).stretch_to_fit_width(0.7).scale(0.1)
        )

        pointers_top = mn.VGroup()
        pointers_bottom = mn.VGroup()
        for cell in cell_mob:
            # create top triangles (3 per cell)
            top_triple_group = mn.VGroup(*[top_triangle.copy() for _ in range(3)])

            # arrange top triangles horizontally above the cell
            top_triple_group.arrange(mn.RIGHT, buff=0.08)
            top_triple_group.next_to(cell, mn.UP, buff=0.15)
            pointers_top.add(top_triple_group)

            # create bottom triangles (3 per cell)
            bottom_triple_group = mn.VGroup(*[bottom_triangle.copy() for _ in range(3)])

            # arrange bottom triangles horizontally below the cell
            bottom_triple_group.arrange(mn.RIGHT, buff=0.08)
            bottom_triple_group.next_to(cell, mn.DOWN, buff=0.15)
            pointers_bottom.add(bottom_triple_group)

        return pointers_top, pointers_bottom

    def pointers(
        self,
        idx_list: list[int],
        pos: int = 0,
        color_1: ManimColor | str = mn.RED,
        color_2: ManimColor | str = mn.BLUE,
        color_3: ManimColor | str = mn.GREEN,
    ):
        """Highlight pointers at one side (top | bottom) in array.

        First, this function clears the existing pointer highlight state for the specified position,
        then sets the new highlight state based on the provided indices and colors,
        and finally applies the new state to the visual objects if data exists.

        Args:
            idx_list: List of indices to highlight (1-3 elements).
            pos: 0 for top side, 1 for bottom.
            color_1: idx_list[0] highlighted pointer color.
            color_2: idx_list[1] highlighted pointer color.
            color_3: idx_list[2] highlighted pointer color.

        Raises:
            ValueError: If idx_list has invalid length or pos is invalid.
        """

        # ------- checks --------

        if not 1 <= len(idx_list) <= 3:
            raise ValueError("idx_list must contain between 1 and 3 indices")

        if pos not in (0, 1):
            raise ValueError("pos must be 0 (top) or 1 (bottom)")

        # ------- asserts --------

        if pos == 0:
            self._top_pointers_colors = {}
            colors_dict = self._top_pointers_colors
        elif pos == 1:
            self._bottom_pointers_colors = {}
            colors_dict = self._bottom_pointers_colors

        # ------- fill store --------

        if len(idx_list) == 1:
            i = idx_list[0]
            colors_dict[i] = [self._bg_color, color_1, self._bg_color]

        elif len(idx_list) == 2:
            i = idx_list[0]
            j = idx_list[1]

            for idx, _ in enumerate(self._containers_mob):
                if idx == i == j:
                    colors_dict[idx] = [color_1, self._bg_color, color_2]
                elif idx == i:
                    colors_dict[idx] = [self._bg_color, color_1, self._bg_color]
                elif idx == j:
                    colors_dict[idx] = [self._bg_color, color_2, self._bg_color]

        elif len(idx_list) == 3:
            i = idx_list[0]
            j = idx_list[1]
            k = idx_list[2]

            for idx, _ in enumerate(self._containers_mob):
                if idx == i == j == k:
                    colors_dict[idx] = [color_1, color_2, color_3]
                elif idx == i == j:
                    colors_dict[idx] = [color_1, self._bg_color, color_2]
                elif idx == i == k:
                    colors_dict[idx] = [color_1, self._bg_color, color_3]
                elif idx == k == j:
                    colors_dict[idx] = [color_2, self._bg_color, color_3]
                elif idx == i:
                    colors_dict[idx] = [self._bg_color, color_1, self._bg_color]
                elif idx == j:
                    colors_dict[idx] = [self._bg_color, color_2, self._bg_color]
                elif idx == k:
                    colors_dict[idx] = [self._bg_color, color_3, self._bg_color]

        # ------- apply --------

        if not self._data:
            return

        self._apply_pointers_colors(pos)

    def pointers_on_value(
        self,
        val: int | str,
        pos: int = 1,
        color: ManimColor | str = mn.BLACK,
    ):
        """Highlight middle pointers on all cells whose values
        equal the provided value.

        First, this function clears the existing pointer highlight state for the specified position,
        then sets the new highlight state based on the provided value and color,
        and finally applies the new state to the visual objects if data exists.

        Args:
            val: The value to compare with array elements.
            pos: 0 for top pointers, 1 for bottom pointers.
            color: Color for the highlighted pointer.
        """

        # ------- checks --------
        if pos not in (0, 1):
            raise ValueError("pos must be 0 (top) or 1 (bottom)")

        # ------- asserts --------
        if pos == 0:
            self._top_pointers_colors = {}
            colors_store = self._top_pointers_colors

        elif pos == 1:
            self._bottom_pointers_colors = {}
            colors_store = self._bottom_pointers_colors

        # ------- checks --------
        if not self._data:
            return

        # ------- fill store --------
        for idx in range(len(self._data)):
            if self._data[idx] == val:
                colors_store[idx] = [self._bg_color, color, self._bg_color]

        # ------- apply --------
        self._apply_pointers_colors(pos)

    def highlight_containers(
        self,
        idx_list: list[int],
        color_1: ManimColor | str | None = None,
        color_2: ManimColor | str | None = None,
        color_3: ManimColor | str | None = None,
        color_123: ManimColor | str | None = None,
        color_12: ManimColor | str | None = None,
        color_13: ManimColor | str | None = None,
        color_23: ManimColor | str | None = None,
    ):
        """Highlight cells in the array visualization.

        First, this function clears the existing container highlight state,
        then sets the new highlight state based on the provided indices and colors,
        and finally applies the new state to the visual objects if data exists.

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

        # ------- checks --------
        if not 1 <= len(idx_list) <= 3:
            raise ValueError("idx_list must contain between 1 and 3 indices")

        # ------- asserts --------
        if not color_1:
            color_1 = self._color_1
        if not color_2:
            color_2 = self._color_2
        if not color_3:
            color_3 = self._color_3
        if not color_123:
            color_123 = self._color_123
        if not color_12:
            color_12 = self._color_12
        if not color_13:
            color_13 = self._color_13
        if not color_23:
            color_23 = self._color_23

        self._containers_colors = {}

        # ------- fill self._containers_colors --------

        if len(idx_list) == 1:
            i = idx_list[0]
            self._containers_colors[i] = color_1

        elif len(idx_list) == 2:
            i = idx_list[0]
            j = idx_list[1]

            for idx, _ in enumerate(self._containers_mob):
                if idx == i == j:
                    self._containers_colors[idx] = color_12
                elif idx == i:
                    self._containers_colors[idx] = color_1
                elif idx == j:
                    self._containers_colors[idx] = color_2

        elif len(idx_list) == 3:
            i = idx_list[0]
            j = idx_list[1]
            k = idx_list[2]

            for idx, _ in enumerate(self._containers_mob):
                if idx == i == j == k:
                    self._containers_colors[idx] = color_123
                elif idx == i == j:
                    self._containers_colors[idx] = color_12
                elif idx == i == k:
                    self._containers_colors[idx] = color_13
                elif idx == k == j:
                    self._containers_colors[idx] = color_23
                elif idx == i:
                    self._containers_colors[idx] = color_1
                elif idx == j:
                    self._containers_colors[idx] = color_2
                elif idx == k:
                    self._containers_colors[idx] = color_3

        if not self._data:
            return

        self._apply_containers_colors()

    def highlight_containers_with_value(
        self,
        val: int | str,
        color: ManimColor | str = mn.BLACK,
    ):
        """Highlight all cells whose values equal the provided value.

        First, this function clears the existing container highlight state,
        then sets the new highlight state based on the provided value and color,
        and finally applies the new state to the visual objects if data exists.

        Note:
            Cell coloring methods are mutually exclusive - the last called
            method determines the final appearance.

        Args:
            val: The value to compare with array elements.
            color: Color for the highlighted pointer.
        """

        # ------- asserts --------
        self._containers_colors = {}

        # ------- checks --------
        if not self._data:
            return

        # ------- fill store --------
        for idx in range(len(self._data)):
            if self._data[idx] == val:
                self._containers_colors[idx] = color

        # ------- apply --------
        self._apply_containers_colors()


class RectangleCellsDataStructure(VisualDataStructure):
    """
    ...
    """

    def __init__(self):
        super().__init__()
        self._cell_params_auto = True
        self._cell_height = 0.65625
        self._top_bottom_buff = 0.15
        self._top_buff = 0.09
        self._bottom_buff = 0.16
        self._deep_bottom_buff = 0.05

    def _get_cell_params(
        self,
        font_size: float,
        font: str,
        weight: str,
        test_sign: str = "0",
    ) -> dict:
        """Calculate comprehensive cell layout parameters.

        Args:
            font_size: Font size for text measurement.
            font: Font family name.
            weight: Font weight (NORMAL, BOLD, etc.).
            test_sign: Character used for measurement (default "0").

        Returns:
            Dictionary containing:
            - top_bottom_buff: Internal top/bottom padding
            - cell_height: Total cell height
            - top_buff: Top alignment buffer
            - bottom_buff: Standard bottom alignment buffer
            - deep_bottom_buff: Deep bottom alignment buffer
        """
        zero_mob = mn.Text(test_sign, font=font, font_size=font_size, weight=weight)

        zero_mob_height = zero_mob.height  # 0.35625

        top_bottom_buff = zero_mob_height / 2.375
        cell_height = top_bottom_buff * 2 + zero_mob_height
        top_buff = zero_mob_height / 3.958
        bottom_buff = zero_mob_height / 35.625 + top_bottom_buff
        deep_bottom_buff = zero_mob_height / 7.125

        return {
            "top_bottom_buff": top_bottom_buff,
            "cell_height": cell_height,
            "top_buff": top_buff,
            "bottom_buff": bottom_buff,
            "deep_bottom_buff": deep_bottom_buff,
        }

    def _get_cell_width(
        self,
        text_mob: mn.Mobject,
        inter_buff: float,
        cell_height: float,
    ) -> float:
        """Calculate cell width based on text content and constraints.

        Args:
            text_mob: Text mobject to measure.
            inter_buff: Internal padding within cells.
            cell_height: Pre-calculated cell height.

        Returns:
            Cell width, ensuring it's at least as tall as the cell height
            for consistent visual proportions.
        """
        text_mob_height = text_mob.width
        res = inter_buff * 2.5 + text_mob_height
        if cell_height >= res:
            return cell_height
        else:
            return res

    def _cell_params(
        self,
        cell_params_auto,
        font_size,
        font,
        weight,
        cell_height,
        top_bottom_buff,
        top_buff,
        bottom_buff,
        deep_bottom_buff,
    ):
        if cell_params_auto:
            cell_params = self._get_cell_params(font_size, font, weight)
            self._cell_height = cell_params["cell_height"]
            self._top_bottom_buff = cell_params["top_bottom_buff"]
            self._top_buff = cell_params["top_buff"]
            self._bottom_buff = cell_params["bottom_buff"]
            self._deep_bottom_buff = cell_params["deep_bottom_buff"]
        else:
            self._cell_height = cell_height
            self._top_bottom_buff = top_bottom_buff
            self._top_buff = top_buff
            self._bottom_buff = bottom_buff
            self._deep_bottom_buff = deep_bottom_buff


class NodeDataStructure(VisualDataStructure):
    """
    ...
    """

    def __init__(self):
        super().__init__()
        self._radius: float = 0.4


class Array(RectangleCellsDataStructure):
    """Array visualization as a VGroup of cells with values and pointers.

    Args:
        arr: List of values to visualize.
        vector: Position offset from mob_center.
        font: Font family for text elements.
        font_size: Font size for text, scales the whole mobject.
        font_color: Color for text elements.
        weight: Font weight (NORMAL, BOLD, etc.).
        mob_center: Reference mobject for positioning.
        align_edge: Edge alignment relative to mob_center.
        container_color: Border color for cells.
        bg_color: Background color for cells and default pointer color.
        fill_color: Fill color for cells.
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
        # ---- position ----
        vector: np.ndarray = mn.ORIGIN,
        mob_center: mn.Mobject = mn.Dot(mn.ORIGIN),
        align_edge: Literal["up", "down", "left", "right"] | None = None,
        # ---- font ----
        font="",
        font_size=35,
        font_color: ManimColor | str = mn.WHITE,
        weight: str = "NORMAL",
        # ---- cell colors ----
        container_color: ManimColor | str = mn.LIGHT_GRAY,
        bg_color: ManimColor | str = mn.DARK_GRAY,
        fill_color: ManimColor | str = mn.DARK_GRAY,
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
        # create class instance fields
        self._data = arr.copy()
        self._vector = vector
        self._font = font
        self._font_size = font_size
        self._font_color = font_color
        self._weight = weight
        self._mob_center = mob_center
        self._align_edge = align_edge
        self._container_color = container_color
        self._bg_color = bg_color
        self._fill_color = fill_color
        self._cell_params_auto = cell_params_auto
        self._cell_height = cell_height
        self._top_bottom_buff = top_bottom_buff
        self._top_buff = top_buff
        self._bottom_buff = bottom_buff
        self._deep_bottom_buff = deep_bottom_buff

        self._cell_params(
            self._cell_params_auto,
            self._font_size,
            self._font,
            self._weight,
            self._cell_height,
            self._top_bottom_buff,
            self._top_buff,
            self._bottom_buff,
            self._deep_bottom_buff,
        )

        # empty value
        if not self._data:
            self._containers_mob, self._empty_value_mob = self._create_empty_array()
            self.add(self._containers_mob, self._empty_value_mob)
            return

        self._values_mob = self._create_values_mob()
        self._containers_mob = self._create_containers_mob()

        # arrange cells in a row
        self._containers_mob.arrange(mn.RIGHT, buff=0.1)

        # move VGroup to the specified position
        self._position(self._containers_mob, self._containers_mob)

        # move text mobjects in containers
        self._position_values_in_containers()

        # pointers
        self._pointers_top, self._pointers_bottom = self.create_pointers(
            self._containers_mob
        )

        # adds local objects as instance attributes
        self.add(
            self._containers_mob,
            self._values_mob,
            self._pointers_top,
            self._pointers_bottom,
        )

    def _create_empty_array(self):
        # clear old fields
        self._values_mob = mn.VGroup()
        self._pointers_top = mn.VGroup()
        self._pointers_bottom = mn.VGroup()

        empty_value_mob = mn.Text("[]", **self._text_config())
        containers_mob = mn.Rectangle(
            height=self._cell_height,
            width=self._get_cell_width(
                empty_value_mob, self._top_bottom_buff, self._cell_height
            ),
            color=self._bg_color,
            fill_color=self._fill_color,
            fill_opacity=1.0,
        )
        self._position(containers_mob, containers_mob)
        empty_value_mob.move_to(containers_mob.get_center())
        empty_value_mob.align_to(containers_mob, mn.DOWN)
        empty_value_mob.align_to(containers_mob, mn.LEFT)
        return containers_mob, empty_value_mob

    def _create_values_mob(self):
        return mn.VGroup(
            *[mn.Text(str(val), **self._text_config()) for val in self._data]
        )

    def _create_containers_mob(self):
        # NB: if opacity is not specified, it will be set to None
        # and some methods will break for unknown reasons
        cells_mobs_list = []
        for text_mob in self._values_mob:
            cell_mob = mn.Rectangle(
                height=self._cell_height,
                width=self._get_cell_width(
                    text_mob, self._top_bottom_buff, self._cell_height
                ),
                color=self._container_color,
                fill_color=self._fill_color,
                fill_opacity=1.0,
            )
            cells_mobs_list.append(cell_mob)

        return mn.VGroup(*cells_mobs_list)

    def _position_values_in_containers(
        self,
    ):
        for i in range(len(self._data)):
            if not isinstance(self._data[i], str):  # center alignment
                self._values_mob[i].move_to(self._containers_mob[i])
            else:
                val_set = set(self._data[i])
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
                    self._values_mob[i].move_to(self._containers_mob[i])
                elif val_set.issubset(
                    {
                        '"',
                        "'",
                        "^",
                        "`",
                    }
                ):  # top alignment
                    self._values_mob[i].next_to(
                        self._containers_mob[i].get_top(),
                        direction=mn.DOWN,
                        buff=self._top_buff,
                    )

                elif val_set.issubset(
                    {
                        "y",
                        "p",
                        "g",
                        "j",
                    }
                ):  # deep bottom alignment
                    self._values_mob[i].next_to(
                        self._containers_mob[i].get_bottom(),
                        direction=mn.UP,
                        buff=self._deep_bottom_buff,
                    )

                else:  # bottom alignment
                    self._values_mob[i].next_to(
                        self._containers_mob[i].get_bottom(),
                        direction=mn.UP,
                        buff=self._bottom_buff,
                    )

    def update_value(
        self,
        scene: mn.Scene,
        new_value: List[int],
        animate: bool = False,
        left_aligned=True,
        run_time: float = 0.2,
    ) -> None:
        """Replace the array visualization with a new set of values.

        This method creates a new `Array` instance with `new_value` and either
        animates a smooth transformation from the old to the new state, or performs
        an instantaneous update. Highlight states (container and pointer colors)
        are preserved across the update.

        Args:
            scene: The Manim scene in which the animation or update will be played.
            new_value: The new list of integer values to display in the array.
            animate: If True, animates the transition using a Transform.
                     If False, updates the object instantly.
            left_aligned: If True, aligns the left edge of the new array with the
                         left edge of the current array, maintaining horizontal position.
                         If False, the new array is centered on the original mob_center.
            run_time: Duration (in seconds) of the animation if `animate=True`.
                     Has no effect if `animate=False`.
        """

        # checks
        if not self._data and not new_value:
            return

        # save old group status
        highlight_status = self._save_highlights_states()

        # new group
        new_group = Array(
            new_value,
            font=self._font,
            bg_color=self._bg_color,
            font_size=self._font_size,
        )
        if left_aligned:
            new_group.align_to(self.get_left(), mn.LEFT)
            new_group.set_y(self.get_y())

        # restore colors
        self._preserve_highlights_states(new_group, highlight_status)

        # add
        if animate:
            scene.play(mn.Transform(self, new_group), run_time=run_time)
            self._update_internal_state(new_value, new_group)
        else:
            scene.remove(self)
            self._update_internal_state(new_value, new_group)
            scene.add(self)


class String(RectangleCellsDataStructure):
    """String visualization as a VGroup of character cells with quotes.

    Args:
        string: Text string to visualize.
        vector: Position offset from mob_center.
        font: Font family for text elements.
        font_size: Font size for text, scales the whole mobject.
        weight: Font weight (NORMAL, BOLD, etc.).
        font_color: Color for text elements.
        mob_center: Reference mobject for positioning.
        align_edge: Edge alignment relative to mob_center.
        container_color: Border color for cells.
        fill_color: Fill color for character cells.
        bg_color: Background color for quote cells and default pointer color.
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
        # ---- position ----
        vector: np.ndarray = mn.ORIGIN,
        mob_center: mn.Mobject = mn.Dot(mn.ORIGIN),
        align_edge: Literal["up", "down", "left", "right"] | None = None,
        # ---- font ----
        font="",
        font_size=35,
        font_color: ManimColor | str = mn.WHITE,
        weight: str = "NORMAL",
        # ---- cell colors ----
        container_color: ManimColor | str = mn.DARK_GRAY,
        fill_color: ManimColor | str = mn.GRAY,
        bg_color: ManimColor | str = mn.DARK_GRAY,
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
        # create class instance fields
        self._data = string
        self._vector = vector
        self._mob_center = mob_center
        self._align_edge = align_edge
        self._font = font
        self._font_size = font_size
        self._font_color = font_color
        self._weight = weight
        self._container_color = container_color
        self._fill_color = fill_color
        self._bg_color = bg_color
        self._cell_params_auto = cell_params_auto
        self._cell_height = cell_height
        self._top_bottom_buff = top_bottom_buff
        self._top_buff = top_buff
        self._bottom_buff = bottom_buff
        self._deep_bottom_buff = deep_bottom_buff

        # cells params
        self._cell_params(
            self._cell_params_auto,
            self._font_size,
            self._font,
            self._weight,
            self._cell_height,
            self._top_bottom_buff,
            self._top_buff,
            self._bottom_buff,
            self._deep_bottom_buff,
        )

        # empty value
        if not string:
            self._containers_mob, self._empty_value_mob = self._create_empty_string()
            self.add(self._containers_mob, self._empty_value_mob)
            return

        # letters cells
        self._containers_mob = self._create_containers_mob()

        # arrange cells in a row
        self._containers_mob.arrange(mn.RIGHT, buff=0.0)
        self._letters_cells_left_edge = self._containers_mob.get_left()

        # move letters cells to the specified position
        self._position(self._containers_mob, self._containers_mob)

        self._left_quote_cell_mob, self._right_quote_cell_mob = (
            self._create_and_pos_quote_cell_mobs()
        )

        self._all_cell_mob = mn.VGroup(
            [
                self._left_quote_cell_mob,
                self._containers_mob,
                self._right_quote_cell_mob,
            ],
        )

        self._quote_cell_left_edge = self._all_cell_mob.get_left()

        # text mobs quotes group
        self._quotes_mob = self._create_and_pos_quotes_mob()

        # create text mobjects
        self._values_mob = self._create_values_mob()

        # move text mobjects in containers
        self._position_values_in_containers()

        # pointers
        self._pointers_top, self._pointers_bottom = self.create_pointers(
            self._containers_mob
        )

        # adds local objects as instance attributes
        self.add(
            self._all_cell_mob,
            self._values_mob,
            self._quotes_mob,
            self._pointers_top,
            self._pointers_bottom,
        )

        self._coordinate_y = self.get_y()

    def _containers_cell_config(self):
        # NB: if opacity is not specified, it will be set to None
        # and some methods will break for unknown reasons
        return {
            "color": self._container_color,
            "fill_color": self._fill_color,
            "side_length": self._cell_height,
            "fill_opacity": 1,
        }

    def _quotes_cell_config(self):
        # NB: if opacity is not specified, it will be set to None
        # and some methods will break for unknown reasons
        return {
            "color": self._bg_color,
            "fill_color": self._bg_color,
            "side_length": self._cell_height,
            "fill_opacity": 1,
        }

    def _create_empty_string(self):
        # clear old fields
        self._values_mob = mn.VGroup()
        self._pointers_top = mn.VGroup()
        self._pointers_bottom = mn.VGroup()

        empty_value_mob = mn.Text('""', **self._text_config())
        containers_mob = mn.Square(**self._containers_cell_config())
        self._position(containers_mob, containers_mob)
        empty_value_mob.next_to(
            containers_mob.get_top(),
            direction=mn.DOWN,
            buff=self._top_buff,
        )
        return containers_mob, empty_value_mob

    def _create_containers_mob(self):
        # create square mobjects for each letter
        return mn.VGroup(
            *[mn.Square(**self._containers_cell_config()) for _ in self._data]
        )

    def _create_and_pos_quote_cell_mobs(self):
        left_quote_cell = mn.Square(**self._quotes_cell_config())
        right_quote_cell = mn.Square(**self._quotes_cell_config())
        left_quote_cell.next_to(self._containers_mob, mn.LEFT, buff=0.0)
        right_quote_cell.next_to(self._containers_mob, mn.RIGHT, buff=0.0)
        return left_quote_cell, right_quote_cell

    def _create_and_pos_quotes_mob(self):
        return mn.VGroup(
            mn.Text('"', **self._text_config())
            .move_to(self._left_quote_cell_mob, aligned_edge=mn.UP + mn.RIGHT)
            .shift(mn.DOWN * self._top_buff),
            mn.Text('"', **self._text_config())
            .move_to(self._right_quote_cell_mob, aligned_edge=mn.UP + mn.LEFT)
            .shift(mn.DOWN * self._top_buff),
        )

    def _create_values_mob(self):
        return mn.VGroup(
            *[mn.Text(str(letter), **self._text_config()) for letter in self._data]
        )

    def _position_values_in_containers(
        self,
    ):
        for i in range(len(self._data)):
            if self._data[i] in "\"'^`":  # top alignment
                self._values_mob[i].next_to(
                    self._containers_mob[i].get_top(),
                    direction=mn.DOWN,
                    buff=self._top_buff,
                )
            elif (
                self._data[i] in "<>-=+~:#%*[]{}()\\/|@&$0123456789"
            ):  # center alignment
                self._values_mob[i].move_to(self._containers_mob[i])
            elif self._data[i] in "ypgj":  # deep bottom alignment
                self._values_mob[i].next_to(
                    self._containers_mob[i].get_bottom(),
                    direction=mn.UP,
                    buff=self._deep_bottom_buff,
                )
            else:  # bottom alignment
                self._values_mob[i].next_to(
                    self._containers_mob[i].get_bottom(),
                    direction=mn.UP,
                    buff=self._bottom_buff,
                )

    def update_value(
        self,
        scene: mn.Scene,
        new_value: str,
        animate: bool = False,
        left_aligned=True,
        run_time: float = 0.2,
    ) -> None:
        """Replace the string visualization with a new string value.

        This method creates a new `String` instance with `new_value` and either
        animates a smooth transformation from the old to the new state, or performs
        an instantaneous update. Highlight states (container and pointer colors)
        are preserved across the update. The left edge alignment of quotes and
        character cells is maintained if `left_aligned=True`.

        Args:
            scene: The Manim scene in which the animation or update will be played.
            new_value: The new string value to display.
            animate: If True, animates the transition using a Transform.
                     If False, updates the object instantly.
            left_aligned: If True, aligns the left edge of the new string's quote cells
                         and character cells with the corresponding left edges of the
                         current string, maintaining horizontal position. If False,
                         the new string is centered on the original mob_center.
            run_time: Duration (in seconds) of the animation if `animate=True`.
                     Has no effect if `animate=False`.
        """

        # checks
        if not self._data and not new_value:
            return

        # save old group status
        highlight_status = self._save_highlights_states()

        # ------ new group ---------
        new_group = String(
            new_value,
            font=self._font,
            weight=self._weight,
            font_color=self._font_color,
            container_color=self._container_color,
            fill_color=self._fill_color,
            bg_color=self._bg_color,
        )
        new_group._coordinate_y = self._coordinate_y

        if left_aligned:
            new_group._quote_cell_left_edge = self._quote_cell_left_edge
            new_group._letters_cells_left_edge = self._letters_cells_left_edge

            if new_value:
                left_edge = self._quote_cell_left_edge
            else:
                left_edge = self._letters_cells_left_edge

            new_group.align_to(left_edge, mn.LEFT)
            new_group.set_y(self._coordinate_y)

        else:
            new_group.move_to(self._mob_center)
            new_group.shift(self._vector)

        self._quote_cell_left_edge = new_group._quote_cell_left_edge
        self._letters_cells_left_edge = new_group._letters_cells_left_edge
        # --------------------------

        # restore colors
        self._preserve_highlights_states(new_group, highlight_status)

        # add
        if animate:
            scene.play(mn.Transform(self, new_group), run_time=run_time)
            self._update_internal_state(new_value, new_group)
        else:
            scene.remove(self)
            self._update_internal_state(new_value, new_group)
            scene.add(self)


class LinkedList(NodeDataStructure):
    """
    ...
    """

    def __init__(
        self,
        head: ListNode | None,
        radius: float = 0.4,
        direction: np.ndarray = mn.RIGHT,
        # --- containers colors ---
        node_color: ManimColor | str = mn.BLACK,
        fill_color: ManimColor | str = mn.LIGHT_GRAY,
        bg_color: ManimColor | str = mn.DARK_GRAY,
        # -- position --
        vector: np.ndarray = mn.ORIGIN,
        mob_center: mn.Mobject = mn.Dot(mn.ORIGIN),
        align_edge: Literal["up", "down", "left", "right"] | None = None,
        # -- font --
        font="",
        font_color: ManimColor | str = mn.BLACK,
        weight: str = "NORMAL",
    ):
        super().__init__()
        self._data = self.linked_list_to_list(head)  # save head as list
        self._radius = radius
        self._direction = direction
        self._container_color = node_color
        self._fill_color = fill_color
        self._bg_color = bg_color
        self._vector = vector
        self._mob_center = mob_center
        self._align_edge = align_edge
        self._font = font
        self._font_color = font_color
        self._weight = weight
        self._color_123 = mn.WHITE

        # empty value
        if not self._data:
            self._empty_linked_list()
            return

        # nodes
        self._containers_mob = self._create_containers_mob()

        # arrows
        self._arrows_mob = self._create_and_pos_arrows_mob()

        # pointers
        self._pointers_top, self._pointers_bottom = self.create_pointers(
            self._containers_mob
        )

        # group all mobs
        self._frame_mob = self._create_frame_mob()

        # rotate frame
        self._rotate_frame()

        self._position(self._frame_mob, self._containers_mob[0])

        # values
        self._values_mob = self._create_and_pos_values_mob()

        # ---- add ------
        self.add(self._frame_mob, self._values_mob)

    def _empty_linked_list(self):
        """ """
        # clear old fields
        self._containers_mob = mn.VGroup()
        self._arrows_mob = mn.VGroup()
        self._pointers_top = mn.VGroup()
        self._pointers_bottom = mn.VGroup()
        self._frame_mob = mn.VGroup()
        self._values_mob = mn.VGroup()

    @staticmethod
    def create_linked_list(value: list) -> ListNode | None:
        """Create a singly-linked list from a list.

        Args:
            value: List to convert into linked list nodes.

        Returns:
            Head node of the created linked list, or None if values is empty.
        """

        if not value:
            return None
        head = ListNode(value[0])
        current = head
        for val in value[1:]:
            current.next = ListNode(val)
            current = current.next
        return head

    @staticmethod
    def get_linked_list_length(head: ListNode | None) -> int:
        """Calculate the length of a linked list.

        Args:
            head: Head node of the linked list.

        Returns:
            Number of nodes in the linked list. 0 if head is None.
        """
        count = 0
        current = head
        while current:
            count += 1
            current = current.next
        return count

    @staticmethod
    def linked_list_to_list(head: ListNode | None) -> list:
        """Convert a linked list to a Python list.

        Args:
            head: Head node of the linked list.

        Returns:
            List containing all values from the linked list in order.
            Empty list if head is None.
        """
        result = []
        current = head
        while current:
            result.append(current.val)
            current = current.next
        return result

    def _create_containers_mob(self):
        """
        ...
        """
        node = mn.Circle(
            radius=self._radius,
            color=self._container_color,
            fill_color=self._fill_color,
            fill_opacity=1,
            stroke_width=self._radius * 7,
        )
        containers_mob = mn.VGroup(*[node.copy() for _ in range(len(self._data))])
        containers_mob.arrange(buff=self._radius)

        return containers_mob

    def _create_and_pos_arrows_mob(self):
        """
        ...
        """

        arrow_path = str(SVG_DIR / "arrows/radius_x10.svg")
        arrow = mn.SVGMobject(
            arrow_path,
            width=self._radius,
        )
        arrows_mob = mn.VGroup()
        for i in range(len(self._data) - 1):
            new_arrow = arrow.copy()
            new_arrow.next_to(self._containers_mob[i], buff=0)
            arrows_mob.add(new_arrow)
        return arrows_mob

    def _create_frame_mob(self):
        return mn.VGroup(
            self._containers_mob,
            self._arrows_mob,
            self._pointers_top,
            self._pointers_bottom,
        )

    def _rotate_frame(self) -> None:
        """
        ...
        """

        if not np.allclose(self._direction, mn.RIGHT):
            angle = mn.angle_of_vector(self._direction)
            self._frame_mob.rotate(
                angle,
                about_point=self._containers_mob[0].get_center(),
            )

    def _text_config(self):
        return {
            "font": self._font,
            "weight": self._weight,
            "color": self._font_color,
        }

    def _create_and_pos_values_mob(self):
        """
        ...
        """

        top_bottom_buff = self._radius / 2
        ypgj_shift = self._radius / 16
        max_size_test = (self._radius - top_bottom_buff) * 2
        max_size_center = (self._radius - top_bottom_buff) * 2.5
        max_size_shift = (self._radius - top_bottom_buff) * 2.2

        # find base font_size
        font_size = 10
        test_mob = mn.Text("0", font_size=font_size)
        while test_mob.height < max_size_test:
            font_size += 1
            test_mob = mn.Text("0", font_size=font_size)

        values_mob = mn.VGroup(
            *[
                mn.Text(str(val), font_size=font_size, **self._text_config())
                for val in self._data
            ]
        )

        for i in range(len(self._data)):
            val = str(self._data[i])
            val_set = set(val)
            mob = values_mob[i]
            width = mob.width
            container = self._containers_mob[i]

            if len(val) == 1 and val in "0123456789":  # center alignment
                mob.move_to(container)
                continue

            if val_set.issubset({'"', "'", "^", "`"}):  # top alignment
                if width > max_size_shift:
                    mob.scale_to_fit_width(max_size_shift)
                mob.next_to(
                    container.get_top(),
                    direction=mn.DOWN,
                    buff=top_bottom_buff,
                )
                continue

            if val_set.issubset({"y", "p", "g", "j"}):  # down shift
                if width > max_size_center:
                    mob.scale_to_fit_width(max_size_center)
                mob.move_to(container)
                mob.shift(mn.DOWN * ypgj_shift)
                continue

            if val_set.issubset({".", ",", "_"}):  # bottom alignment
                if width > max_size_shift:
                    mob.scale_to_fit_width(max_size_shift)
                mob.next_to(
                    container.get_bottom(),
                    direction=mn.UP,
                    buff=top_bottom_buff,
                )
                continue

            if width > max_size_center:
                mob.scale_to_fit_width(max_size_center)
            mob.move_to(container)

        return values_mob

    def update_value(
        self,
        scene: mn.Scene,
        new_value,
        animate: bool = False,
        run_time: float = 0.2,
    ) -> None:
        """
        ...
        """

        # checks
        if not self._data and not new_value:
            return

        # save old group status
        highlight_status = self._save_highlights_states()

        # new group
        new_group = LinkedList(
            new_value,
            font=self._font,
            direction=self._direction,
            mob_center=self._mob_center,
            align_edge=self._align_edge,
            vector=self._vector,
        )

        # restore colors
        self._preserve_highlights_states(new_group, highlight_status)

        # add
        if animate:
            scene.play(mn.Transform(self, new_group), run_time=run_time)
            self._update_internal_state(new_value, new_group)
        else:
            scene.remove(self)
            self._update_internal_state(new_value, new_group)
            scene.add(self)


class RelativeTextValue(AlgoManimBase):
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
        # --- position ---
        mob_center: mn.Mobject = mn.Dot(mn.ORIGIN),
        vector: np.ndarray = mn.UP * 1.2,
        align_edge: Literal["up", "down", "left", "right"] | None = None,
        # --- font ---
        font="",
        font_size=35,
        weight: str = "NORMAL",
        # --- other ---
        buff=0.5,
        equal_sign: bool = True,
    ):
        super().__init__()
        self._vars = vars
        self._mob_center = mob_center
        self._vector = vector
        self._align_edge = align_edge
        self._font = font
        self._font_size = font_size
        self._weight = weight
        self._buff = buff
        self._equal_sign = equal_sign

        self.submobjects: List = []
        parts = [
            mn.Text(
                f"{name} = {value()}" if equal_sign else f"{name} {value()}",
                font=self._font,
                font_size=self._font_size,
                weight=self._weight,
                color=color,
            )
            for name, value, color in self._vars
        ]
        self._text_mob = mn.VGroup(*parts).arrange(
            mn.RIGHT, buff=self._buff, aligned_edge=mn.UP
        )

        # move to the specified position
        self._position(self._text_mob, self._text_mob)

        self.add(*self._text_mob)

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
            *self._vars,
            font_size=self._font_size,
            buff=self._buff,
            font=self._font,
            equal_sign=self._equal_sign,
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


class RelativeText(AlgoManimBase):
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
        # --- position ---
        mob_center: mn.Mobject = mn.Dot(mn.ORIGIN),
        vector: np.ndarray = mn.ORIGIN,
        align_edge: Literal["up", "down", "left", "right"] | None = None,
        # --- font ---
        font="",
        font_size=35,
        font_color: str | ManimColor = mn.WHITE,
        weight: str = "NORMAL",
    ):
        super().__init__()

        self._text = text
        self._mob_center = mob_center
        self._vector = vector
        self._align_edge = align_edge
        self._font = font
        self._font_size = font_size
        self._font_color = font_color
        self._weight = weight

        self._text_mob = mn.Text(
            self._text,
            font=self._font,
            color=self._font_color,
            font_size=self._font_size,
            weight=self._weight,
        )

        # construction: Move VGroup to the specified position
        self._position(self._text_mob, self._text_mob)

        self.add(self._text_mob)


class CodeBlock(AlgoManimBase):
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
        pre_code_lines: List[str] = [],
        # --- position ---
        vector: np.ndarray = mn.ORIGIN,
        mob_center: mn.Mobject = mn.Dot(mn.ORIGIN),
        align_edge: Literal["up", "down", "left", "right"] | None = None,
        # --- font ---
        font_size=20,
        font="",
        font_color_regular: ManimColor | str = "WHITE",
        font_color_highlight: ManimColor | str = "YELLOW",
        # --- buffs ---
        inter_block_buff=0.5,
        pre_code_buff=0.15,
        code_buff=0.05,
        # --- other ---
        bg_highlight_color: ManimColor | str = "BLUE",
    ):
        super().__init__()
        self._code_lines = code_lines
        self._pre_code_lines = pre_code_lines
        self._vector = vector
        self._mob_center = mob_center
        self._align_edge = align_edge
        self._font_size = font_size
        self._font = font
        self._font_color_regular = font_color_regular
        self._font_color_highlight = font_color_highlight
        self._inter_block_buff = inter_block_buff
        self._pre_code_buff = pre_code_buff
        self._code_buff = code_buff
        self._bg_highlight_color = bg_highlight_color

        self._code_mobs = [
            mn.Text(
                line,
                font=self._font,
                font_size=self._font_size,
                color=self._font_color_regular,
            )
            for line in self._code_lines
        ]
        self._bg_rects: List[Optional[mn.Rectangle]] = [None] * len(
            self._code_lines
        )  # list to save links on all possible rectangles and to manage=delete them

        code_vgroup = mn.VGroup(*self._code_mobs).arrange(
            mn.DOWN,
            aligned_edge=mn.LEFT,
            buff=self._code_buff,
        )

        if self._pre_code_lines:
            self._pre_code_mobs = [
                mn.Text(
                    line,
                    font=self._font,
                    font_size=self._font_size,
                    color=self._font_color_regular,
                )
                for line in self._pre_code_lines
            ]
            self._pre_code_vgroup = mn.VGroup(*self._pre_code_mobs).arrange(
                mn.DOWN,
                aligned_edge=mn.LEFT,
                buff=self._pre_code_buff,
            )
            self._code_block_vgroup = mn.VGroup(
                self._pre_code_vgroup, code_vgroup
            ).arrange(
                mn.DOWN,
                aligned_edge=mn.LEFT,
                buff=inter_block_buff,
            )
        else:
            self._code_block_vgroup = code_vgroup

        # construction: Move VGroup to the specified position
        self._position(self._code_block_vgroup, self._code_block_vgroup)

        self.add(self._code_block_vgroup)

    def highlight_line(self, i: int):
        """Highlights a single line of code with background and text color.

        Args:
            i: Index of the line to highlight.
        """

        for k, mob in enumerate(self._code_mobs):
            if k == i:
                # change font color
                mob.set_color(self._font_color_highlight)
                # create bg rectangle
                if self._bg_rects[k] is None:
                    bg_rect = mn.Rectangle(
                        width=mob.width + 0.2,
                        height=mob.height + 0.1,
                        fill_color=self._bg_highlight_color,
                        fill_opacity=0.3,
                        stroke_width=0,
                    )
                    bg_rect.move_to(mob.get_center())
                    self.add(bg_rect)
                    bg_rect.z_index = -1  # send background to back
                    self._bg_rects[k] = bg_rect
            else:
                # normal line: regular font color
                mob.set_color(self._font_color_regular)
                # remove rect
                bg_rect = self._bg_rects[k]
                if bg_rect:
                    self.remove(bg_rect)
                    self._bg_rects[k] = None


class TitleText(AlgoManimBase):
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
        text: str,
        # --- position ---
        mob_center: mn.Mobject = mn.Dot(mn.ORIGIN),
        vector: np.ndarray = mn.UP * 2.7,
        align_edge: Literal["up", "down", "left", "right"] | None = None,
        # --- font ---
        font: str = "",
        font_size: float = 50,
        text_color: ManimColor | str = "WHITE",
        # --- flourish ---
        flourish: bool = False,
        flourish_color: ManimColor | str = "WHITE",
        flourish_stroke_width: float = 4,
        flourish_padding: float = 0.2,
        flourish_buff: float = 0.15,
        spiral_offset: float = 0.3,
        spiral_radius: float = 0.15,
        spiral_turns: float = 1.0,
        # --- undercaption ---
        undercaption: str = "",
        undercaption_color: ManimColor | str = "WHITE",
        undercaption_font: str = "",
        undercaption_font_size: float = 20,
        undercaption_buff: float = 0.23,
    ):
        super().__init__()
        self._mob_center = mob_center
        self._vector = vector
        self._align_edge = align_edge
        self._flourish = flourish
        self._undercaption = undercaption

        # create the text mobject
        self._text_mobject = mn.Text(
            text,
            font=font,
            font_size=font_size,
            color=text_color,
        )

        self._position(self._text_mobject, self._text_mobject)

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
        if self._undercaption:
            # create the text mobject
            self._undercaption_mob = mn.Text(
                self._undercaption,
                font=undercaption_font,
                font_size=undercaption_font_size,
                color=undercaption_color,
            )
            self._undercaption_mob.next_to(
                self._text_mobject, mn.DOWN, undercaption_buff
            )
            self.add(self._undercaption_mob)

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


class TitleLogo(AlgoManimBase):
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
        # --- svg ---
        svg_height: float = 2.0,
        mob_center: mn.Mobject = mn.Dot(mn.ORIGIN),
        align_edge: Literal["up", "down", "left", "right"] | None = None,
        vector: np.ndarray = mn.ORIGIN,
        # --- text ---
        text: str | None = None,
        font_color: ManimColor | str = "WHITE",
        font: str = "",
        font_size: float = 31,
        text_vector: np.ndarray = mn.ORIGIN,
    ):
        super().__init__()
        self._mob_center = mob_center
        self._vector = vector
        self._align_edge = align_edge

        # create the svg mobject
        self._svg = mn.SVGMobject(
            svg,
            height=svg_height,
        )

        # position the entire group relative to the reference mobject and offset vector
        self._position(self._svg, self._svg)

        self.add(self._svg)

        # create the text mobject
        if text:
            self.text_mobject = mn.Text(
                text,
                font=font,
                font_size=font_size,
                color=font_color,
            )
            self.text_mobject.move_to(self._svg.get_center() + text_vector)
            self.add(self.text_mobject)
