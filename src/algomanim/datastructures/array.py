from typing import (
    List,
    Literal,
)

import numpy as np
import manim as mn
from manim import ManimColor

from algomanim.core.rectangle_cells import RectangleCellsStructure


class Array(RectangleCellsStructure):
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
        pointers: Whether to create and display pointers.

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
        # ---- pointers ----
        pointers: bool = True,
        # ---- kwargs ----
        **kwargs,
    ):
        # call __init__ of the parent classes
        super().__init__(
            vector=vector,
            mob_center=mob_center,
            align_edge=align_edge,
            font=font,
            font_size=font_size,
            font_color=font_color,
            weight=weight,
            container_color=container_color,
            bg_color=bg_color,
            fill_color=fill_color,
            cell_params_auto=cell_params_auto,
            cell_height=cell_height,
            top_bottom_buff=top_bottom_buff,
            top_buff=top_buff,
            bottom_buff=bottom_buff,
            deep_bottom_buff=deep_bottom_buff,
            **kwargs,
        )

        # create class instance fields
        self._data = arr.copy()
        self._pointers = pointers
        self._color_containers_with_value = mn.RED

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

        # adds local objects as instance attributes
        self.add(
            self._containers_mob,
            self._values_mob,
        )

        # pointers
        if self._pointers:
            self._pointers_top, self._pointers_bottom = self.create_pointers(
                self._containers_mob
            )
            self.add(
                self._pointers_top,
                self._pointers_bottom,
            )

    def _create_empty_array(self):
        """Create visualization for empty array.

        Returns:
            tuple: Tuple containing (containers_mob, empty_value_mob).
        """

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
        """Create text mobjects for array values.

        Returns:
            mn.VGroup: Group of value text mobjects.
        """

        return mn.VGroup(
            *[mn.Text(str(val), **self._text_config()) for val in self._data]
        )

    def _create_containers_mob(self):
        """Create rectangle mobjects for array cells.

        Returns:
            mn.VGroup: Group of cell rectangle mobjects.
        """

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
        """Position value text mobjects within their respective cells with proper alignment."""

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
                        "q",
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
            pointers=self._pointers,
        )
        if left_aligned:
            new_group.align_to(self.get_left(), mn.LEFT)
            new_group.set_y(self.get_y())
        else:
            new_group.move_to(self._mob_center.get_center() + self._vector)

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
