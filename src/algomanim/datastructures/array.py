from typing import (
    List,
)

import numpy as np
import manim as mn
from manim import ManimColor

from algomanim.core.rectangle_cells import RectangleCellsStructure


class Array(RectangleCellsStructure):
    """Array visualization as a VGroup of cells with values and pointers.

    Args:
        arr: List of values to visualize.
        pointers: Whether to create and display pointers.
        vector: Position offset from mob_center.
        font: Font family for text elements.
        font_size: Font size for text, scales the whole mobject.
        text_color: Color for text elements.
        weight: Font weight (NORMAL, BOLD, etc.).
        mob_center: Reference mobject for positioning.
        align_left: Reference mobject to align left edge with.
        align_right: Reference mobject to align right edge with.
        align_top: Reference mobject to align top edge with.
        align_bottom: Reference mobject to align bottom edge with.
        anchor: Optional alignment anchor when neither align_left nor align_right
            is specified. Must be mn.LEFT or mn.RIGHT. Defaults to mn.LEFT.
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
        # ---- pointers ----
        pointers: bool = True,
        # ---- position ----
        vector: np.ndarray = mn.ORIGIN,
        mob_center: mn.Mobject = mn.Dot(mn.ORIGIN),
        align_left: mn.Mobject | None = None,
        align_right: mn.Mobject | None = None,
        align_top: mn.Mobject | None = None,
        align_bottom: mn.Mobject | None = None,
        anchor: np.ndarray | None = mn.LEFT,
        # ---- font ----
        font="",
        font_size=35,
        text_color: ManimColor | str = mn.WHITE,
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
        # ---- kwargs ----
        **kwargs,
    ):
        kwargs.setdefault("color_containers_with_value", mn.RED)
        self._parent_kwargs = kwargs.copy()

        super().__init__(
            # ---- position ----
            vector=vector,
            mob_center=mob_center,
            align_left=align_left,
            align_right=align_right,
            align_top=align_top,
            align_bottom=align_bottom,
            # ---- font ----
            font=font,
            font_size=font_size,
            text_color=text_color,
            weight=weight,
            # ---- cell colors ----
            container_color=container_color,
            bg_color=bg_color,
            fill_color=fill_color,
            # ---- kwargs ----
            **kwargs,
        )

        # create class instance fields
        self._data = arr.copy()
        self._pointers = pointers
        # -- position --
        self._vector = vector
        self._mob_center = mob_center
        self._align_left = align_left
        self._align_right = align_right
        self._align_top = align_top
        self._align_bottom = align_bottom
        # -- font --
        self._font = font
        self._font_size = font_size
        self._text_color = text_color
        self._weight = weight
        # ---- cell colors ----
        self._container_color = container_color
        self._bg_color = bg_color
        self._fill_color = fill_color
        # ---- cell params ----
        if cell_params_auto:
            params = self._get_cell_params(font_size, font, weight)
            self._cell_height = params["cell_height"]
            self._top_bottom_buff = params["top_bottom_buff"]
            self._top_buff = params["top_buff"]
            self._bottom_buff = params["bottom_buff"]
            self._deep_bottom_buff = params["deep_bottom_buff"]
        else:
            self._cell_height = cell_height
            self._top_bottom_buff = top_bottom_buff
            self._top_buff = top_buff
            self._bottom_buff = bottom_buff
            self._deep_bottom_buff = deep_bottom_buff
        # ---- anchor ----
        if not (align_left or align_right) and anchor is not None:
            if not (
                np.array_equal(anchor, mn.RIGHT) or np.array_equal(anchor, mn.LEFT)
            ):
                raise ValueError("anchor must be mn.RIGHT or mn.LEFT")
            self._anchor = anchor
        else:
            self._anchor = None

        # empty value
        if not self._data:
            self._create_empty_array()
            return

        self._values_mob = self._create_values_mob()
        self._containers_mob = self._create_containers_mob()

        # arrange cells in a row
        self._containers_mob.arrange(mn.RIGHT, buff=0.1)

        self.add(self._containers_mob)
        self._position()

        # move text mobjects in containers
        self._position_values_in_containers()

        self.add(
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

        Creates a single rectangle container with "[]" text for empty arrays.
        Initializes or clears pointer groups if pointers are enabled.

        Returns:
            None: Modifies internal mobjects in place instead of returning them.
        """

        # clear old fields
        self._values_mob = mn.VGroup()
        if self._pointers:
            self._pointers_top = mn.VGroup()
            self._pointers_bottom = mn.VGroup()

        self._empty_value_mob = mn.Text("[]", **self._text_config())

        self._containers_mob = mn.Rectangle(
            height=self._cell_height,
            width=self._get_cell_width(
                self._empty_value_mob, self._top_bottom_buff, self._cell_height
            ),
            color=self._bg_color,
            fill_color=self._fill_color,
            fill_opacity=1.0,
        )
        self.add(self._containers_mob)
        self._position()

        self._empty_value_mob.move_to(self._containers_mob.get_center())
        self._empty_value_mob.align_to(self._containers_mob, mn.DOWN)
        self.add(self._empty_value_mob)

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
        animate: bool = True,
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
            run_time: Duration (in seconds) of the animation if `animate=True`.
                     Has no effect if `animate=False`.
        """

        # checks
        if not self._data and not new_value:
            return

        # new group
        new_group = Array(
            new_value,
            # ---- pointers ----
            pointers=self._pointers,
            # -- position --
            vector=self._vector,
            mob_center=self._mob_center,
            align_left=self._align_left,
            align_right=self._align_right,
            align_top=self._align_top,
            align_bottom=self._align_bottom,
            # -- font --
            font=self._font,
            font_size=self._font_size,
            text_color=self._text_color,
            weight=self._weight,
            # --- cell colors ---
            container_color=self._container_color,
            bg_color=self._bg_color,
            fill_color=self._fill_color,
            # ---- cell params ----
            cell_params_auto=False,
            cell_height=self._cell_height,
            top_bottom_buff=self._top_bottom_buff,
            top_buff=self._top_buff,
            bottom_buff=self._bottom_buff,
            deep_bottom_buff=self._deep_bottom_buff,
            # ---- kwargs ----
            **self._parent_kwargs,
        )

        if self._anchor is not None:
            if np.array_equal(self._anchor, mn.LEFT):
                new_group.align_to(self.get_left(), mn.LEFT)
            else:
                new_group.align_to(self.get_right(), mn.RIGHT)

        # save old group status
        highlight_status = self._save_highlights_states()
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
