from typing import Any, Literal, Mapping
from collections.abc import Collection
from dataclasses import dataclass
import numpy as np
import manim as mn
from manim import ManimColor
import math

from .base import AlgoManimBase


@dataclass(frozen=True)
class Colors:
    color_1: ManimColor | str = mn.RED  # #FC6255
    color_2: ManimColor | str = mn.BLUE  # #58C4DD
    color_3: ManimColor | str = mn.GREEN  # #83C167
    color_4: ManimColor | str = mn.PINK  # #D147BD
    color_5: ManimColor | str = mn.LOGO_BLUE  # #525893
    color_6: ManimColor | str = mn.GREEN_E  # #699C52

    color_mix_3: ManimColor | str = mn.GOLD_E
    color_mix_4: ManimColor | str = mn.ORANGE
    color_mix_5: ManimColor | str = mn.DARK_BROWN
    color_mix_6: ManimColor | str = mn.BLACK


class LinearContainerStructure(AlgoManimBase):
    """Base class for visual data structures with common attributes and methods.

    Warning:
        This is base class only, cannot be instantiated directly.

    Args:
        pointers: Which pointers to create. "top", "bottom", "both", or None.
        pointers_mode: Number of pointer triangles per cell. 3 or 5.
        font: Font family for text elements.
        font_size: Font size for text elements.
        text_color: Color for text elements.
        weight: Font weight (NORMAL, BOLD, etc.).
        container_color: Border color for containers.
        fill_color: Fill color for containers.
        bg_color: Background color for pointers.
        color_containers_with_value: Color for containers with specific value.
        color_1: Highlight color for first index.
        color_2: Highlight color for second index.
        color_3: Highlight color for third index.
        color_4: Highlight color for fourth index.
        color_5: Highlight color for fifth index.
        color_6: Highlight color for sixth index.
        color_mix_3: Blend color for 3 colors.
        color_mix_4: Blend color for 4 colors.
        color_mix_5: Blend color for 5 colors.
        color_mix_6: Blend color for 6 colors.
        **kwargs: Additional keyword arguments passed to VGroup.
    """

    COLORS = Colors()

    def __init__(
        self,
        # ---- pointers ----
        pointers: Literal["top", "bottom", "both"] | None = "top",
        pointers_mode: Literal[3, 5] = 3,
        # ---- font ----
        font="",
        font_size: float = 35,
        text_color: ManimColor | str = mn.WHITE,
        weight: str = "NORMAL",
        # ---- container colors ----
        container_color: ManimColor | str = mn.DARK_GRAY,
        fill_color: ManimColor | str = mn.GRAY,
        bg_color: ManimColor | str = mn.DARK_GRAY,
        # ---- highlight containers colors ----
        color_containers_with_value: ManimColor | str = mn.BLACK,
        color_1: ManimColor | str = COLORS.color_1,
        color_2: ManimColor | str = COLORS.color_2,
        color_3: ManimColor | str = COLORS.color_3,
        color_4: ManimColor | str = COLORS.color_4,
        color_5: ManimColor | str = COLORS.color_5,
        color_6: ManimColor | str = COLORS.color_6,
        color_mix_3: ManimColor | str = COLORS.color_mix_3,
        color_mix_4: ManimColor | str = COLORS.color_mix_4,
        color_mix_5: ManimColor | str = COLORS.color_mix_5,
        color_mix_6: ManimColor | str = COLORS.color_mix_6,
        # ---- kwargs ----
        **kwargs,
    ):
        if type(self) is LinearContainerStructure:
            raise NotImplementedError(
                "LinearContainerStructure is base class only, cannot be instantiated directly."
            )
        super().__init__(**kwargs)

        self._data = None

        # ---- pointers ----
        if pointers not in ["top", "bottom", "both", None]:
            raise ValueError("pointers must be 'top' | 'bottom' | 'both' | None")
        self._pointers: Literal["top", "bottom", "both"] | None = pointers
        if pointers_mode not in [3, 5]:
            raise ValueError("pointers_mode must be 3 or 5")
        self._pointers_mode = pointers_mode

        # --- mobjects ---
        self._containers_mob = mn.VGroup()
        self._values_mob = mn.VGroup()
        self._pointers_top = mn.VGroup()
        self._pointers_bottom = mn.VGroup()

        # --- colors state management ---
        self._containers_colors: dict[int, ManimColor | str] = {}
        self._top_pointers_colors: dict[int, list[ManimColor | str]] = {}
        self._bottom_pointers_colors: dict[int, list[ManimColor | str]] = {}

        # ---- font ----
        self._font = font
        self._font_size = font_size
        self._text_color = text_color
        self._weight = weight

        # ---- container colors ----
        self._container_color = container_color
        self._fill_color = fill_color
        self._bg_color = bg_color

        # ---- highlight containers colors ----
        self._color_containers_with_value = color_containers_with_value
        self._color_1 = color_1
        self._color_2 = color_2
        self._color_3 = color_3
        self._color_4 = color_4
        self._color_5 = color_5
        self._color_6 = color_6
        self._color_mix_3 = color_mix_3
        self._color_mix_4 = color_mix_4
        self._color_mix_5 = color_mix_5
        self._color_mix_6 = color_mix_6

    def _get_position(self):
        """Return containers mobject for positioning purposes."""

        return self._containers_mob

    def _update_internal_state(
        self,
        new_value,
        new_group: "LinearContainerStructure",
    ):
        """Update internal state with data from a new group.

        Args:
            new_value: New data value to store.
            new_group (LinearContainerStructure): New group to copy state from.
        """
        self._data = new_value
        self._containers_mob = new_group._containers_mob
        self._values_mob = new_group._values_mob
        self.submobjects = new_group.submobjects

        if hasattr(self, "_pointers") and not self._pointers:
            return
        self._pointers_top = new_group._pointers_top
        self._pointers_bottom = new_group._pointers_bottom

    def _text_config(self):
        """Get text configuration dictionary.

        Returns:
            dict: Dictionary with font configuration parameters.
        """
        return {
            "font": self._font,
            "font_size": self._font_size,
            "weight": self._weight,
            "color": self._text_color,
        }

    def clear_pointers_highlights(self, pos: int = 0):
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
            pos (int): Position to apply colors for (0 for top, 1 for bottom).

        Raises:
            ValueError: If pos is not 0 or 1.
        """

        # ------- validation --------
        if pos not in (0, 1):
            raise ValueError("pos must be 0 (top) or 1 (bottom)")

        # ------- asserts --------
        if pos == 0:
            if not self._pointers_top:
                return
            pointers = self._pointers_top
            colors_dict = self._top_pointers_colors

        elif pos == 1:
            if not self._pointers_bottom:
                return
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

    def _save_highlights_states(self):
        """Save current highlight states for containers and pointers.

        Returns:
            dict: Dictionary containing current highlight states.
        """
        return {
            "_containers_colors": self._containers_colors,
            "_top_pointers_colors": self._top_pointers_colors,
            "_bottom_pointers_colors": self._bottom_pointers_colors,
        }

    @staticmethod
    def _preserve_highlights_states(
        new_group: "LinearContainerStructure",
        status: dict,
    ):
        """Apply saved highlight states to a new group.

        Args:
            new_group (LinearContainerStructure): Group to apply the saved states to.
            status (dict): Dictionary containing the saved highlight states.
        """
        new_group._containers_colors = status["_containers_colors"]
        new_group._top_pointers_colors = status["_top_pointers_colors"]
        new_group._bottom_pointers_colors = status["_bottom_pointers_colors"]

        new_group._apply_containers_colors()
        new_group._apply_pointers_colors(0)
        new_group._apply_pointers_colors(1)

    def _create_horizontal_top_pointers(self, cell_mob: mn.VGroup):
        """Create top pointer triangles for each cell.

        Returns:
            VGroup of pointer triangles positioned above cells.
        """

        pointers_top = mn.VGroup()

        if self._pointers_mode == 3:
            top_triangle = (
                mn.Triangle(color=self._bg_color)
                .stretch_to_fit_width(0.7)
                .scale(0.1)
                .rotate(mn.PI)
            )
            for cell in cell_mob:
                # create top triangles (3 per cell)
                top_triple_group = mn.VGroup(*[top_triangle.copy() for _ in range(3)])
                # arrange top triangles horizontally above the cell
                top_triple_group.arrange(mn.RIGHT, buff=0.08)
                top_triple_group.next_to(cell, mn.UP, buff=0.15)
                pointers_top.add(top_triple_group)

        elif self._pointers_mode == 5:
            top_triangle = (
                mn.Triangle(color=self._bg_color)
                .stretch_to_fit_width(0.5)
                .scale(0.1)
                .rotate(mn.PI)
            )
            for cell in cell_mob:
                # create top triangles (5 per cell)
                top_triple_group = mn.VGroup(*[top_triangle.copy() for _ in range(5)])
                # arrange top triangles horizontally above the cell
                top_triple_group.arrange(mn.RIGHT, buff=0.05)
                top_triple_group.next_to(cell, mn.UP, buff=0.15)
                pointers_top.add(top_triple_group)

        return pointers_top

    def _create_horizontal_bottom_pointers(self, cell_mob: mn.VGroup):
        """Create bottom pointer triangles for each cell.

        Returns:
            VGroup of pointer triangles positioned below cells.
        """

        pointers_bottom = mn.VGroup()

        if self._pointers_mode == 3:
            bottom_triangle = (
                mn.Triangle(color=self._bg_color).stretch_to_fit_width(0.7).scale(0.1)
            )

            for cell in cell_mob:
                # create bottom triangles (3 per cell)
                bottom_triple_group = mn.VGroup(
                    *[bottom_triangle.copy() for _ in range(3)]
                )
                bottom_triple_group.arrange(mn.RIGHT, buff=0.08)
                bottom_triple_group.next_to(cell, mn.DOWN, buff=0.15)
                pointers_bottom.add(bottom_triple_group)
        elif self._pointers_mode == 5:
            bottom_triangle = (
                mn.Triangle(color=self._bg_color).stretch_to_fit_width(0.5).scale(0.1)
            )
            for cell in cell_mob:
                # create bottom triangles (5 per cell)
                bottom_triple_group = mn.VGroup(
                    *[bottom_triangle.copy() for _ in range(5)]
                )
                bottom_triple_group.arrange(mn.RIGHT, buff=0.05)
                bottom_triple_group.next_to(cell, mn.DOWN, buff=0.15)
                pointers_bottom.add(bottom_triple_group)

        return pointers_bottom

    def set_pointers(
        self,
        cell_mob: mn.VGroup,
        pointers: Literal["top", "bottom", "both"] | None,
        direction: np.ndarray,
    ) -> None:
        """Create and attach pointer triangles to cells based on direction and side.

        Args:
            cell_mob: VGroup of cells to attach pointers to.
            direction: Direction vector for pointer orientation.
            pointers: Which pointers to create.
                - "top": Only above/before cells.
                - "bottom": Only below/after cells.
                - "both": Both sides.
                - None: No pointers.
        """
        # -------------- checks --------------
        if not pointers:
            self._pointers_top = None
            self._pointers_bottom = None
            return

        # -------------- create pointers --------------
        if np.allclose(direction, mn.RIGHT):  # horizontal pointers
            pointers_top, pointers_bottom = self._create_horizontal_pointers(cell_mob)

        else:  # rotate pointers
            angle = mn.angle_of_vector(direction)

            # swich top/bottom pointers
            if direction[0] < 0:
                extra_rotation = mn.PI
            else:
                extra_rotation = 0

            pointers_top, pointers_bottom = self._create_horizontal_pointers(cell_mob)

            # pointers rotation
            for i, cell in enumerate(cell_mob):
                center = cell.get_center()
                total_angle = angle + extra_rotation
                pointers_top[i].rotate(total_angle, about_point=center)
                pointers_bottom[i].rotate(total_angle, about_point=center)

        # -------------- set pointers --------------
        if pointers == "both":
            self._pointers_top, self._pointers_bottom = pointers_top, pointers_bottom
            self.add(
                self._pointers_top,
                self._pointers_bottom,
            )
        elif pointers == "top":
            self._pointers_top, self._pointers_bottom = pointers_top, None
            self.add(
                self._pointers_top,
            )
        elif pointers == "bottom":
            self._pointers_top, self._pointers_bottom = None, pointers_bottom
            self.add(
                self._pointers_bottom,
            )

    def _create_horizontal_pointers(self, cell_mob: mn.VGroup):
        """Create pointer triangles for horizontal direction (direction = RIGHT).

        Args:
            cell_mob: VGroup of cells to attach pointers to.

        Returns:
            Tuple of (top_pointers, bottom_pointers) VGroups where each contains
            triple triangle groups for every cell | node.

        Note:
            Each cell gets 3 triangles above and 3 below, arranged horizontally.
            Triangle groups are positioned with fixed buffering from cells.
        """

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
            bottom_triple_group.arrange(mn.RIGHT, buff=0.08)
            bottom_triple_group.next_to(cell, mn.DOWN, buff=0.15)
            pointers_bottom.add(bottom_triple_group)

        return pointers_top, pointers_bottom

    @staticmethod
    def _color_to_rgb(color: str | ManimColor) -> tuple[int, int, int]:
        """Convert a color to RGB tuple.

        Args:
            color: Color as hex string or ManimColor object.

        Returns:
            Tuple of (red, green, blue) integers in range 0-255.
        """
        if isinstance(color, ManimColor):
            hex = color.to_hex()
        else:
            hex = color

        strip_hex = hex.lstrip("#")

        return (
            int(strip_hex[0:2], 16),
            int(strip_hex[2:4], 16),
            int(strip_hex[4:6], 16),
        )

    @staticmethod
    def _blend_colors_algo(*colors: str | ManimColor) -> str:
        """Blend multiple colors using RGB channel averaging with ceiling.

        Args:
            *colors: Variable number of colors as hex strings or ManimColor objects.

        Returns:
            Blended color as uppercase hex string.
        """
        rgb_list = [LinearContainerStructure._color_to_rgb(c) for c in colors]
        n = len(rgb_list)

        r = int(math.ceil(sum(v[0] for v in rgb_list) / n))
        g = int(math.ceil(sum(v[1] for v in rgb_list) / n))
        b = int(math.ceil(sum(v[2] for v in rgb_list) / n))

        return f"#{r:02x}{g:02x}{b:02x}".upper()

    def _blend_colors(self, *colors: str | ManimColor) -> str | ManimColor:
        """Blend colors with predefined rules for 3-6 colors.

        For 1 color: returns the color itself.
        For 2 colors: uses algorithmic blending.
        For 3-6 colors: returns predefined palette color (mix_3 to mix_6).

        Args:
            *colors: Variable number of colors to blend.

        Returns:
            Blended color as hex string or ManimColor.

        Raises:
            ValueError: If number of colors is not between 1 and 6.
        """
        if len(colors) == 1:
            return colors[0]

        if len(colors) == 2:
            return self._blend_colors_algo(*colors)

        if 3 <= len(colors) <= 6:
            mix_map = {
                3: self._color_mix_3,
                4: self._color_mix_4,
                5: self._color_mix_5,
                6: self._color_mix_6,
            }
            return mix_map[len(colors)]

        raise ValueError("colors must contain between 2 and 6 elements")

    def highlight_containers(
        self,
        *indices: int,
        color_1: ManimColor | str | None = None,
        color_2: ManimColor | str | None = None,
        color_3: ManimColor | str | None = None,
        color_4: ManimColor | str | None = None,
        color_5: ManimColor | str | None = None,
        color_6: ManimColor | str | None = None,
    ):
        """Highlight containers at specified indices with color blending for duplicates.

        If the same index appears multiple times, the corresponding colors are blended.
        Supports up to 6 indices.

        Args:
            *indices: Container indices to highlight (1-6 elements).
            color_1: Color for first index position. If None, uses default color_1.
            color_2: Color for second index position.
            color_3: Color for third index position.
            color_4: Color for fourth index position.
            color_5: Color for fifth index position.
            color_6: Color for sixth index position.

        Raises:
            ValueError: If number of indices is not between 1 and 6.
        """

        # ------- validation --------
        if not 1 <= len(indices) <= 6:
            raise ValueError("indices must contain between 1 and 6 elements")

        # ------- asserts --------
        if color_1 is None:
            color_1 = self._color_1
        if color_2 is None:
            color_2 = self._color_2
        if color_3 is None:
            color_3 = self._color_3
        if color_4 is None:
            color_4 = self._color_4
        if color_5 is None:
            color_5 = self._color_5
        if color_6 is None:
            color_6 = self._color_6

        # --- clear previous highlights ---
        self._containers_colors = {}

        # --- map colors to their positions ---
        colors = [color_1, color_2, color_3, color_4, color_5, color_6]

        # --- group color indices by target container index ---
        # Example: indices = [1, 1, 2] -> groups = {1: [0, 1], 2: [2]}
        groups = {}
        for idx, color_pos in zip(indices, range(len(indices))):
            if idx not in groups:
                groups[idx] = []
            groups[idx].append(colors[color_pos])

        # --- for each container, assign color or blend multiple colors ---
        for idx, color_list in groups.items():
            if len(color_list) == 1:
                self._containers_colors[idx] = color_list[0]
            else:
                self._containers_colors[idx] = self._blend_colors(*color_list)

        # --- skip if no data ---
        if not self._data:
            return

        # --- apply colors ---
        self._apply_containers_colors()

    def highlight_pointers_1to3(
        self,
        *indices: int,
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
            *indices: Positional arguments for indices to highlight (1-3 elements).
            pos: 0 for top side, 1 for bottom.
            color_1: idx_list[0] highlighted pointer color.
            color_2: idx_list[1] highlighted pointer color.
            color_3: idx_list[2] highlighted pointer color.

        Raises:
            ValueError: if indices has invalid length.
        """

        # ------- validation --------

        if hasattr(self, "_pointers") and not self._pointers:
            return

        if not 1 <= len(indices) <= 3:
            raise ValueError("indices must contain between 1 and 3 elements")

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

        if len(indices) == 1:
            i = indices[0]
            colors_dict[i] = [self._bg_color, color_1, self._bg_color]

        elif len(indices) == 2:
            i = indices[0]
            j = indices[1]

            for idx, _ in enumerate(self._containers_mob):
                if idx == i == j:
                    colors_dict[idx] = [color_1, self._bg_color, color_2]
                elif idx == i:
                    colors_dict[idx] = [self._bg_color, color_1, self._bg_color]
                elif idx == j:
                    colors_dict[idx] = [self._bg_color, color_2, self._bg_color]

        elif len(indices) == 3:
            i = indices[0]
            j = indices[1]
            k = indices[2]

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

    def highlight_containers_monocolor(
        self,
        idx_list: list[int],
        color: ManimColor | str = mn.RED,
    ):
        """Highlight multiple cells with a single color.

        Unlike highlight_containers_1to3(), this method can highlight any number
        of indices using the same color for all specified cells.

        Args:
            idx_list: List of indices to highlight (any number of elements).
            color: Color to apply to all highlighted cells. Default is RED.
        """
        # validation
        if not self._data:
            return

        # clear colors dict
        self._containers_colors = {}

        # fill store
        for idx in idx_list:
            self._containers_colors[idx] = color

        # apply
        self._apply_containers_colors()

    def highlight_pointers_monocolor(
        self,
        indices: Collection[int],
        pos: int = 1,
        color: ManimColor | str | None = mn.ORANGE,
    ):
        """Highlight pointers at specified indices with a single color.

        Clears existing pointer highlights for the given position, then applies
        new highlights to all indices in the collection.

        Args:
            indices: Collection of indices to highlight.
            pos: 0 for top pointers, 1 for bottom pointers. Defaults to 1.
            color: Color for the highlighted pointers. Defaults to ORANGE.
                If None, uses color_containers_with_value.

        Raises:
            ValueError: If pos is not 0 or 1.
        """
        # ------- validation --------

        if hasattr(self, "_pointers") and not self._pointers:
            return

        if pos not in (0, 1):
            raise ValueError("pos must be 0 (top) or 1 (bottom)")

        if pos == 0 and self._pointers not in ("both", "top"):
            raise ValueError("Top pointers were not initialized for highlight.")

        if pos == 1 and self._pointers not in ("both", "bottom"):
            raise ValueError("Bottom pointers were not initialized for highlight.")

        # ------- asserts --------
        if not color:
            color = self._color_containers_with_value

        if pos == 0:
            self._top_pointers_colors = {}
            colors_store = self._top_pointers_colors

        elif pos == 1:
            self._bottom_pointers_colors = {}
            colors_store = self._bottom_pointers_colors

        # ------- validation --------
        if not self._data:
            return

        # ------- fill store --------
        for idx in indices:
            colors_store[idx] = [self._bg_color, color, self._bg_color]

        # ------- apply --------
        self._apply_pointers_colors(pos)

    def highlight_containers_with_value(
        self,
        val: int | str,
        color: ManimColor | str | None = None,
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

        if not color:
            color = self._color_containers_with_value

        self._containers_colors = {}

        # ------- validation --------
        if not self._data:
            return

        # ------- fill store --------
        for idx in range(len(self._data)):
            if self._data[idx] == val:
                self._containers_colors[idx] = color

        # ------- apply --------
        self._apply_containers_colors()

    def highlight_pointers_above_value(
        self,
        value: int | str,
        pos: int = 1,
        color: ManimColor | str | None = None,
    ):
        """Highlight middle pointers on all cells whose values
        equal the provided value.

        First, this function clears the existing pointer highlight state for the specified position,
        then sets the new highlight state based on the provided value and color,
        and finally applies the new state to the visual objects if data exists.

        Args:
            value: The value to compare with array elements.
            pos: 0 for top pointers, 1 for bottom pointers.
            color: Color for the highlighted pointer.
        """

        # ------- validation --------

        if hasattr(self, "_pointers") and not self._pointers:
            return

        if pos not in (0, 1):
            raise ValueError("pos must be 0 (top) or 1 (bottom)")

        # ------- asserts --------
        if not color:
            color = self._color_containers_with_value

        if pos == 0:
            self._top_pointers_colors = {}
            colors_store = self._top_pointers_colors

        elif pos == 1:
            self._bottom_pointers_colors = {}
            colors_store = self._bottom_pointers_colors

        # ------- validation --------
        if not self._data:
            return

        # ------- fill store --------
        for idx in range(len(self._data)):
            if self._data[idx] == value:
                colors_store[idx] = [self._bg_color, color, self._bg_color]

        # ------- apply --------
        self._apply_pointers_colors(pos)

    def highlight_containers_with_values(
        self,
        mapping: Mapping[Any, ManimColor | str],
    ) -> None:
        """Highlight cells whose values match keys in the mapping.

        Args:
            mapping: Dictionary mapping values to highlight colors.

        Raises:
            ValueError: If mapping is empty or data is not initialized.
        """
        # ------- validation --------
        if not self._data:
            return
        if not mapping:
            raise ValueError("Mapping cannot be empty")

        # ------- clean --------
        self._containers_colors = {}

        # ------- fill store --------

        for idx in range(len(self._data)):
            if self._data[idx] in mapping:
                self._containers_colors[idx] = mapping[self._data[idx]]

        # ------- apply --------
        self._apply_containers_colors()

    def text_color_with_values(
        self,
        mapping: Mapping[Any, ManimColor | str],
    ) -> None:
        """Set text color based on cell values.

        Args:
            mapping: Dictionary mapping values to text colors.
                Cells with values not in mapping keep default text color.

        Raises:
            ValueError: If mapping is empty or data is not initialized.
        """
        # ------- validation --------
        if not self._data:
            return
        if not mapping:
            raise ValueError("Mapping cannot be empty")

        # ------- fill store --------

        for idx in range(len(self._data)):
            if self._data[idx] in mapping:
                self._values_mob[idx].set_color(mapping[self._data[idx]])
            else:
                self._values_mob[idx].set_color(self._text_color)

        # ------- apply --------
        self._apply_containers_colors()

    def highlight_pointers_above_values(
        self,
        values: Collection[int | str],
        pos: int = 1,
        color: ManimColor | str | None = None,
    ):
        """Highlight middle pointers on all cells whose values are in the given set.

        First, this function clears the existing pointer highlight state for the specified position,
        then sets the new highlight state based on the provided values and color,
        and finally applies the new state to the visual objects if data exists.

        Args:
            values: Set of values to match against array elements.
            pos: 0 for top pointers, 1 for bottom pointers. Defaults to 1.
            color: Color for the highlighted pointer. If None, uses color_containers_with_value.
        """

        # ------- validation --------

        if hasattr(self, "_pointers") and not self._pointers:
            return

        if pos not in (0, 1):
            raise ValueError("pos must be 0 (top) or 1 (bottom)")

        # ------- asserts --------
        if not color:
            color = self._color_containers_with_value

        if pos == 0:
            self._top_pointers_colors = {}
            colors_store = self._top_pointers_colors

        elif pos == 1:
            self._bottom_pointers_colors = {}
            colors_store = self._bottom_pointers_colors

        # ------- validation --------
        if not self._data:
            return

        # ------- fill store --------
        for idx in range(len(self._data)):
            if self._data[idx] in values:
                colors_store[idx] = [self._bg_color, color, self._bg_color]

        # ------- apply --------
        self._apply_pointers_colors(pos)
