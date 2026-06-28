from typing import Any, Callable, Literal, TYPE_CHECKING
import numpy as np
import manim as mn
from manim import ManimColor

from algomanim.core.rectangle_cells import RectangleCellsStructure
from algomanim.core.updatable import UpdatableMixin

if TYPE_CHECKING:
    from algomanim.datastructures.array import Array


class String(RectangleCellsStructure, UpdatableMixin):
    """String visualization as a VGroup of character cells with quotes.

    Args:
        value: Callable that returns a string to visualize.
        pointers: Whether to create and display pointers.
        frame_from: Optional Array or String instance to copy container frames from.
        vector: Position offset from mob_center.
        font: Font family for text elements.
        font_size: Font size for text, scales the whole mobject.
        weight: Font weight (NORMAL, BOLD, etc.).
        text_color: Color for text elements.
        mob_center: Reference mobject for positioning.
        align_left: Reference mobject to align left edge with.
        align_right: Reference mobject to align right edge with.
        align_top: Reference mobject to align top edge with.
        align_bottom: Reference mobject to align bottom edge with.
        align_screen (np.ndarray | None): Direction vector for screen edge alignment
        screen_buff (float): Buffer distance from screen edge when using align_screen.
        anchor: Optional alignment anchor when neither align_left nor align_right
            is specified. Must be `start`, `end` or None.
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
        value: Callable[[], str],
        # ---- pointers ----
        pointers: Literal["top", "bottom", "both"] | None = "top",
        pointers_mode: Literal[3, 5] = 3,
        # ---- frame ----
        frame_from: "Array | String |  None " = None,
        # ---- position ----
        vector: np.ndarray = mn.ORIGIN,
        mob_center: mn.Mobject = mn.Dot(mn.ORIGIN),
        align_left: mn.Mobject | None = None,
        align_right: mn.Mobject | None = None,
        align_top: mn.Mobject | None = None,
        align_bottom: mn.Mobject | None = None,
        align_screen: np.ndarray | None = None,
        screen_buff: float = 0.4,
        anchor: Literal["start", "end"] | None = "start",
        # ---- font ----
        font="",
        font_size: float = 35,
        text_color: ManimColor | str = mn.WHITE,
        weight: str = "BOLD",
        # ---- cell colors ----
        container_color: ManimColor | str = mn.DARK_GRAY,
        fill_color: ManimColor | str = mn.GRAY,
        bg_color: ManimColor | str = mn.DARK_GRAY,
        # ---- value colors mode ----
        value_colors_map: dict[Any, list[ManimColor | str]] = {},
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
            # ---- pointers ----
            pointers=pointers,
            pointers_mode=pointers_mode,
            # ---- frame ----
            frame_from=frame_from,
            # ---- position ----
            vector=vector,
            mob_center=mob_center,
            align_left=align_left,
            align_right=align_right,
            align_top=align_top,
            align_bottom=align_bottom,
            align_screen=align_screen,
            screen_buff=screen_buff,
            # ---- font ----
            font=font,
            font_size=font_size,
            text_color=text_color,
            weight=weight,
            # ---- cell colors ----
            container_color=container_color,
            bg_color=bg_color,
            fill_color=fill_color,
            # ---- value colors mode ----
            value_colors_map=value_colors_map,
            # ---- kwargs ----
            **kwargs,
        )

        # create class instance fields
        self._callable = value
        self._data = value()
        # ---- pointers ----
        self._pointers = pointers
        self._pointers_mode: Literal[3, 5] = pointers_mode
        # ---- frame ----
        self._frame_from = frame_from
        # -- position --
        self._vector = vector
        self._mob_center = mob_center
        self._align_left = align_left
        self._align_right = align_right
        self._align_top = align_top
        self._align_bottom = align_bottom
        self._align_screen = align_screen
        self._screen_buff = screen_buff
        # -- font --
        self._font = font
        if frame_from:
            self._font_size = frame_from._font_size
        else:
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
            if anchor not in ["start", "end"]:
                raise ValueError("anchor must be 'start', 'end' or None")
            self._anchor = anchor
        else:
            self._anchor: Literal["start", "end"] | None = None

        # =-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=

        # empty value
        if not self._data:
            self._create_empty_string()
            return

        self._set_containers_mob()

        self._letters_cells_left_edge = self._containers_mob.get_left()

        self._left_quote_cell_mob, self._right_quote_cell_mob = (
            self._create_and_pos_quote_cell_mobs()
        )

        # text mobs quotes group
        self._quotes_mob = self._create_and_pos_quotes_mob()

        # create text mobjects
        self._values_mob = self._create_values_mob()

        # move text mobjects in containers
        self._position_values_in_containers()

        # adds local objects as instance attributes
        self.add(
            self._left_quote_cell_mob,
            self._right_quote_cell_mob,
            self._values_mob,
            self._quotes_mob,
        )

        self.set_pointers(
            self._containers_mob,
            mn.RIGHT,
        )

        if self._value_colors_map:
            self._apply_value_colors()

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
            "height": self._cell_height,
            "width": self._cell_height / 2,
            "fill_opacity": 1,
        }

    def _create_empty_string(self):
        """Create visualization for empty string.

        Creates a single square container with "" text for empty strings.
        Initializes or clears pointer groups if pointers are enabled.

        Returns:
            None: Modifies internal mobjects in place instead of returning them.
        """

        # clear old fields
        self._values_mob = mn.VGroup()
        if self._pointers:
            self._pointers_top = mn.VGroup()
            self._pointers_bottom = mn.VGroup()

        self._empty_value_mob = mn.Text('""', **self._text_config())
        self._containers_mob = mn.VGroup(
            mn.Square(**self._containers_cell_config()),
        )
        self.add(self._containers_mob)
        self._position()

        self._empty_value_mob.next_to(
            self._containers_mob.get_top(),
            direction=mn.DOWN,
            buff=self._top_buff,
        )
        self.add(self._empty_value_mob)

    def _create_containers_mob(self):
        """Create square mobjects for character cells.

        Returns:
            mn.VGroup: Group of character cell square mobjects.
        """

        # create square mobjects for each letter
        mob_group = mn.VGroup(
            *[mn.Square(**self._containers_cell_config()) for _ in self._data]
        )
        # arrange cells in a row
        mob_group.arrange(mn.RIGHT, buff=0.0)

        return mob_group

    def _create_and_pos_quote_cell_mobs(self):
        """Create and position quote cell mobjects.

        Returns:
            tuple: Tuple containing (left_quote_cell, right_quote_cell).
        """
        left_quote_cell = mn.Rectangle(**self._quotes_cell_config())
        right_quote_cell = mn.Rectangle(**self._quotes_cell_config())
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

    def _create_new_instance(self) -> "String":
        """Create a new String instance with current parameters and updated data.

        Returns:
            New String instance with the same configuration and fresh data from callable.
        """
        new_instance = String(
            value=self._callable,
            # ---- pointers ----
            pointers=self._pointers,
            pointers_mode=self._pointers_mode,
            # ---- frame ----
            frame_from=self._frame_from,
            # -- position --
            vector=self._vector,
            mob_center=self._mob_center,
            align_left=self._align_left,
            align_right=self._align_right,
            align_top=self._align_top,
            align_bottom=self._align_bottom,
            align_screen=self._align_screen,
            screen_buff=self._screen_buff,
            anchor=self._anchor,
            # -- font --
            font=self._font,
            font_size=self._font_size,
            text_color=self._text_color,
            weight=self._weight,
            # --- cell colors ---
            container_color=self._container_color,
            bg_color=self._bg_color,
            fill_color=self._fill_color,
            # ---- value colors mode ----
            value_colors_map=self._value_colors_map,
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

        # copy anchor alignment
        if self._anchor is not None:
            if self._anchor == "start":
                if self._data and self._callable():
                    new_instance.align_to(self.get_left(), mn.LEFT)
                elif self._data and not self._callable():
                    new_instance.align_to(self._containers_mob.get_left(), mn.LEFT)
                elif not self._data and self._callable():
                    target = self._containers_mob.get_left() + mn.LEFT * (
                        self._cell_height / 2
                    )
                    new_instance.align_to(target, mn.LEFT)
            elif self._anchor == "end":
                if self._data and self._callable():
                    new_instance.align_to(self.get_right(), mn.RIGHT)
                elif self._data and not self._callable():
                    new_instance.align_to(self._containers_mob.get_right(), mn.RIGHT)
                elif not self._data and self._callable():
                    target = self._containers_mob.get_right() + mn.RIGHT * (
                        self._cell_height / 2
                    )
                    new_instance.align_to(target, mn.RIGHT)

        # preserve highlights
        highlight_status = self._save_highlights_states()
        if new_instance._data:
            self._preserve_highlights_states(new_instance, highlight_status)

        return new_instance

    def _update_internal_state(self, new_instance: "String") -> None:
        """Update the current instance with data from a new instance.

        Copies data, mobject references, and highlight states from the new instance.
        Highlights are preserved and reapplied to the updated containers.

        Args:
            new_instance: The instance to copy state from.
        """
        # save highlight rules before overwriting state
        (
            old_containers_colors,
            old_top_pointers_colors,
            old_bottom_pointers_colors,
            old_value_colors_map,
        ) = self._get_highlight_dicts()

        # sync raw data and closures
        self._data = new_instance._data
        self._callable = new_instance._callable

        # transfer references to sub-mobject groups
        if hasattr(new_instance, "_containers_mob"):
            self._containers_mob = new_instance._containers_mob
        if hasattr(new_instance, "_values_mob"):
            self._values_mob = new_instance._values_mob
        if hasattr(new_instance, "_letters_cells_left_edge"):
            self._letters_cells_left_edge = new_instance._letters_cells_left_edge
        if hasattr(new_instance, "_empty_value_mob"):
            self._empty_value_mob = new_instance._empty_value_mob
        if hasattr(new_instance, "_left_quote_cell_mob"):
            self._left_quote_cell_mob = new_instance._left_quote_cell_mob
        if hasattr(new_instance, "_right_quote_cell_mob"):
            self._right_quote_cell_mob = new_instance._right_quote_cell_mob
        if hasattr(new_instance, "_quotes_mob"):
            self._quotes_mob = new_instance._quotes_mob
        if hasattr(new_instance, "_pointers_top"):
            self._pointers_top = new_instance._pointers_top
        if hasattr(new_instance, "_pointers_bottom"):
            self._pointers_bottom = new_instance._pointers_bottom

        self._restore_highlight_colors(
            old_containers_colors,
            old_top_pointers_colors,
            old_bottom_pointers_colors,
            old_value_colors_map,
        )

        # sync pure geometry hierarchy
        self.submobjects = new_instance.submobjects.copy()
