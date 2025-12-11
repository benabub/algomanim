from typing import Literal

import numpy as np
import manim as mn
from manim import ManimColor

from algomanim.core.rectangle_cells import RectangleCellsStructure


class String(RectangleCellsStructure):
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
        pointers: Whether to create and display pointers.

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
        self._data = string
        self._pointers = pointers

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

        # adds local objects as instance attributes
        self.add(
            self._all_cell_mob,
            self._values_mob,
            self._quotes_mob,
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

        self._coordinate_y = self.get_y()

    def _containers_cell_config(self):
        """Get configuration for character cell containers.

        Returns:
            dict: Dictionary with container configuration parameters.
        """

        return {
            "color": self._container_color,
            "fill_color": self._fill_color,
            "side_length": self._cell_height,
            "fill_opacity": 1,
        }

    def _quotes_cell_config(self):
        """Get configuration for quote cell containers.

        Returns:
            dict: Dictionary with quote cell configuration parameters.
        """

        return {
            "color": self._bg_color,
            "fill_color": self._bg_color,
            "side_length": self._cell_height,
            "fill_opacity": 1,
        }

    def _create_empty_string(self):
        """Create visualization for empty string.

        Returns:
            tuple: Tuple containing (containers_mob, empty_value_mob).
        """

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
        """Create square mobjects for character cells.

        Returns:
            mn.VGroup: Group of character cell square mobjects.
        """

        # create square mobjects for each letter
        return mn.VGroup(
            *[mn.Square(**self._containers_cell_config()) for _ in self._data]
        )

    def _create_and_pos_quote_cell_mobs(self):
        """Create and position quote cell mobjects.

        Returns:
            tuple: Tuple containing (left_quote_cell, right_quote_cell).
        """

        left_quote_cell = mn.Square(**self._quotes_cell_config())
        right_quote_cell = mn.Square(**self._quotes_cell_config())
        left_quote_cell.next_to(self._containers_mob, mn.LEFT, buff=0.0)
        right_quote_cell.next_to(self._containers_mob, mn.RIGHT, buff=0.0)
        return left_quote_cell, right_quote_cell

    def _create_and_pos_quotes_mob(self):
        """Create and position quote text mobjects.

        Returns:
            mn.VGroup: Group of quote text mobjects.
        """

        return mn.VGroup(
            mn.Text('"', **self._text_config())
            .move_to(self._left_quote_cell_mob, aligned_edge=mn.UP + mn.RIGHT)
            .shift(mn.DOWN * self._top_buff),
            mn.Text('"', **self._text_config())
            .move_to(self._right_quote_cell_mob, aligned_edge=mn.UP + mn.LEFT)
            .shift(mn.DOWN * self._top_buff),
        )

    def _create_values_mob(self):
        """Create text mobjects for string characters.

        Returns:
            mn.VGroup: Group of character text mobjects.
        """

        return mn.VGroup(
            *[mn.Text(str(letter), **self._text_config()) for letter in self._data]
        )

    def _position_values_in_containers(
        self,
    ):
        """Position character text mobjects within their respective cells with proper alignment."""

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
            pointers=self._pointers,
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
