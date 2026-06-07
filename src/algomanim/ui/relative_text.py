from typing import Any, Callable, List, Literal, Tuple

import numpy as np
import manim as mn
from manim import ManimColor

from algomanim.core.relative_text_base import RelativeTextBase, RelativeTextUpdatable
from algomanim.core.paths.hl_rect import HLRect


class RelativeTextValue(RelativeTextUpdatable):
    """Text group showing scope variables positioned relative to mobject.

    Args:
        input: Tuple of (var name, value_getter, color).
        mob_center (mn.Mobject): Reference mobject for positioning.
        vector (np.ndarray): Offset vector from reference mobject center.
        align_left: Reference mobject to align left edge with.
        align_right: Reference mobject to align right edge with.
        align_top: Reference mobject to align top edge with.
        align_bottom: Reference mobject to align bottom edge with.
        align_screen (np.ndarray | None): Direction vector for screen edge alignment
        screen_buff (float): Buffer distance from screen edge when using align_screen.
        anchor: Alignment anchor when no edge alignment specified.
            Must be "start", "end", or None. Defaults to "start".
        font (str): Text font family.
        font_size (float): Text font size.
        weight (str): Font weight (NORMAL, BOLD, etc.).
        spaces(bool): Whether to add spaces around the equals sign.
        equal_sign (bool): Whether to use equals sign between name and value.
        highlight (bool): If True, creates a highlight rectangle around the text.
    """

    def __init__(
        self,
        input: Tuple[str, Callable[[], Any], str | ManimColor],
        # --- position ---
        mob_center: mn.Mobject = mn.Dot(mn.ORIGIN),
        vector: np.ndarray = mn.ORIGIN,
        align_left: mn.Mobject | None = None,
        align_right: mn.Mobject | None = None,
        align_top: mn.Mobject | None = None,
        align_bottom: mn.Mobject | None = None,
        align_screen: np.ndarray | None = None,
        screen_buff: float = 0.2,
        anchor: Literal["start", "end"] | None = "start",
        # --- font ---
        font="",
        font_size: float = 25,
        weight: str = "NORMAL",
        # --- other ---
        spaces: bool = True,
        equal_sign: bool = True,
        highlight: bool = True,
    ):
        super().__init__(
            mob_center=mob_center,
            vector=vector,
            align_left=align_left,
            align_right=align_right,
            align_top=align_top,
            align_bottom=align_bottom,
            align_screen=align_screen,
            screen_buff=screen_buff,
            anchor=anchor,
            font=font,
            font_size=font_size,
            weight=weight,
        )

        self._input = input
        self._name = input[0]
        self._callable = input[1]
        self._color = input[2]
        # --- other ---
        self._spaces = spaces
        self._equal_sign = equal_sign
        self._highlight = highlight

        self._text_mob = self._build_text_mob()

        self.add(self._text_mob)
        self._position()

        if self._highlight:
            self._hl_rect = HLRect(
                self._text_mob,
                self._get_hl_color(self._color),
            )
            self.add_to_back(self._hl_rect)
        else:
            self._hl_rect = None

    def _build_text_mob(self):
        """Build a text mobject with formatted value.

        Formats the value from callable, adds quotes for strings,
        and applies spacing and equal sign rules.

        Returns:
            Text mobject ready for positioning.
        """
        if not isinstance(self._callable(), str):
            val = self._callable()
        else:
            val = f'"{self._callable()}"'

        if self._equal_sign:
            if self._spaces:
                text = f"{self._name} = {val}"
            else:
                text = f"{self._name}={val}"
        else:
            text = f"{self._name} {val}"

        return self._create_text_mob(text, self._color)

    def _create_new_instance(self) -> "RelativeTextValue":
        """Create a new RelativeTextValue instance with current variable values.

        Returns:
            New RelativeTextValue instance with the same configuration and fresh data.
        """
        # create new instance
        new_instance = RelativeTextValue(
            self._input,
            # --- position ---
            mob_center=self._mob_center,
            vector=self._vector,
            align_left=self._align_left,
            align_right=self._align_right,
            align_top=self._align_top,
            align_bottom=self._align_bottom,
            align_screen=self._align_screen,
            screen_buff=self._screen_buff,
            anchor=self._anchor,
            # --- font ---
            font=self._font,
            font_size=self._font_size,
            weight=self._weight,
            # --- other ---
            spaces=self._spaces,
            equal_sign=self._equal_sign,
            highlight=self._highlight,
        )

        # copy anchor alignment
        self._align_with_anchor(new_instance)

        return new_instance


class RelativeTextValueGroup(RelativeTextUpdatable):
    """Text group showing scope variables positioned relative to mobject.

    Args:
        *inputs (Tuple[str, Callable[[], Any], str | ManimColor]):
            Tuples of (name, value_getter, color).
        mob_center (mn.Mobject): Reference mobject for positioning.
        vector (np.ndarray): Offset vector from reference mobject center.
        align_left: Reference mobject to align left edge with.
        align_right: Reference mobject to align right edge with.
        align_top: Reference mobject to align top edge with.
        align_bottom: Reference mobject to align bottom edge with.
        align_screen (np.ndarray | None): Direction vector for screen edge alignment
        screen_buff (float): Buffer distance from screen edge when using align_screen.
        anchor: Alignment anchor when no edge alignment specified.
            Must be "start", "end", or None. Defaults to "start".
        font (str): Text font family.
        font_size (float): Text font size.
        weight (str): Font weight (NORMAL, BOLD, etc.).
        spaces(bool): Whether to add spaces around the equals sign.
        buff (float): Spacing between text elements.
        equal_sign (bool): Whether to use equals sign between name and value.
        items_align_edge (np.ndarray): Alignment edge for text items within the group.
        highlight (bool): If True, creates a highlight rectangle around the text.
    """

    def __init__(
        self,
        *inputs: Tuple[str, Callable[[], Any], str | ManimColor],
        # --- position ---
        mob_center: mn.Mobject = mn.Dot(mn.ORIGIN),
        vector: np.ndarray = mn.ORIGIN,
        align_left: mn.Mobject | None = None,
        align_right: mn.Mobject | None = None,
        align_top: mn.Mobject | None = None,
        align_bottom: mn.Mobject | None = None,
        align_screen: np.ndarray | None = None,
        screen_buff: float = 0.2,
        anchor: Literal["start", "end"] | None = "start",
        # --- font ---
        font="",
        font_size: float = 25,
        weight: str = "NORMAL",
        # --- other ---
        spaces: bool = True,
        buff=0.5,
        equal_sign: bool = True,
        items_align_edge: np.ndarray = mn.UP,
        highlight: bool = True,
    ):
        super().__init__(
            mob_center=mob_center,
            vector=vector,
            align_left=align_left,
            align_right=align_right,
            align_top=align_top,
            align_bottom=align_bottom,
            align_screen=align_screen,
            screen_buff=screen_buff,
            anchor=anchor,
            font=font,
            font_size=font_size,
            weight=weight,
        )

        self._inputs = inputs
        self._data = [tpl[1]() for tpl in inputs]
        # --- other ---
        self._spaces = spaces
        self._buff = buff
        self._equal_sign = equal_sign
        self._items_align_edge = items_align_edge
        self.submobjects: List = []
        self._highlight = highlight

        self._text_mob = self._build_text_mob()
        self.add(*self._text_mob)
        self._position()

        if self._highlight:
            self._hl_rect = HLRect(
                self._text_mob,
                mn.BLACK,
            )
            self.add_to_back(self._hl_rect)
        else:
            self._hl_rect = None

    def _build_text_mob(self):
        """Build a VGroup of text mobjects for all variables.

        Returns:
            VGroup containing text mobjects for each variable.
        """
        parts = []
        for name, value, color in self._inputs:
            if not isinstance(value(), str):
                val = value()
            else:
                val = f'"{value()}"'

            if self._equal_sign:
                if self._spaces:
                    text = f"{name} = {val}"
                else:
                    text = f"{name}={val}"
            else:
                text = f"{name} {val}"

            parts.append(self._create_text_mob(text, color))

        return mn.VGroup(*parts).arrange(
            mn.RIGHT, buff=self._buff, aligned_edge=self._items_align_edge
        )

    def _create_new_instance(self) -> "RelativeTextValueGroup":
        """Create a new RelativeTextValue instance with current variable values.

        Returns:
            New RelativeTextValue instance with the same configuration and fresh data.
        """
        # create new instance
        new_instance = RelativeTextValueGroup(
            *self._inputs,
            # --- position ---
            mob_center=self._mob_center,
            vector=self._vector,
            align_left=self._align_left,
            align_right=self._align_right,
            align_top=self._align_top,
            align_bottom=self._align_bottom,
            align_screen=self._align_screen,
            screen_buff=self._screen_buff,
            anchor=self._anchor,
            # --- font ---
            font=self._font,
            font_size=self._font_size,
            weight=self._weight,
            # --- other ---
            spaces=self._spaces,
            buff=self._buff,
            equal_sign=self._equal_sign,
            items_align_edge=self._items_align_edge,
            highlight=self._highlight,
        )

        # copy anchor alignment
        self._align_with_anchor(new_instance)

        return new_instance


class RelativeTextActive(RelativeTextUpdatable):
    """Dynamic text element that updates its value from a callable.

    Args:
        input: Callable that returns the current value to display.
        mob_center: Reference mobject for positioning.
        vector: Offset vector from reference mobject center.
        align_left: Reference mobject to align left edge with.
        align_right: Reference mobject to align right edge with.
        align_top: Reference mobject to align top edge with.
        align_bottom: Reference mobject to align bottom edge with.
        align_screen: Direction vector for screen edge alignment.
        screen_buff: Buffer distance from screen edge when using align_screen.
        anchor: Alignment anchor when no edge alignment specified.
            Must be "start", "end", or None. Defaults to "start".
        font: Text font family.
        font_size: Text font size.
        text_color: Text color.
        weight: Font weight (NORMAL, BOLD, etc.).
        highlight (bool): If True, creates a highlight rectangle around the text.
    """

    def __init__(
        self,
        input: Callable[[], Any],
        # --- position ---
        mob_center: mn.Mobject = mn.Dot(mn.ORIGIN),
        vector: np.ndarray = mn.ORIGIN,
        align_left: mn.Mobject | None = None,
        align_right: mn.Mobject | None = None,
        align_top: mn.Mobject | None = None,
        align_bottom: mn.Mobject | None = None,
        align_screen: np.ndarray | None = None,
        screen_buff: float = 0.2,
        anchor: Literal["start", "end"] | None = "start",
        # --- font ---
        font="",
        font_size: float = 25,
        text_color: ManimColor | str = mn.WHITE,
        weight: str = "NORMAL",
        # --- other ---
        highlight: bool = True,
    ):
        super().__init__(
            mob_center=mob_center,
            vector=vector,
            align_left=align_left,
            align_right=align_right,
            align_top=align_top,
            align_bottom=align_bottom,
            align_screen=align_screen,
            screen_buff=screen_buff,
            anchor=anchor,
            font=font,
            font_size=font_size,
            weight=weight,
        )

        self._callable = input
        if not isinstance(input(), str):
            self._text = str(input())
        else:
            self._text = f'"{str(input())}"'
        # --- font ---
        self._text_color = text_color
        self.submobjects: List = []
        self._highlight = highlight

        self._text_mob = self._create_text_mob(
            self._text,
            color=self._text_color,
        )
        self.add(*self._text_mob)
        self._position()

        if self._highlight:
            self._hl_rect = HLRect(
                self._text_mob,
                self._get_hl_color(self._text_color),
            )
            self.add_to_back(self._hl_rect)
        else:
            self._hl_rect = None

    def _create_new_instance(self) -> "RelativeTextActive":
        """Create a new RelativeTextActive instance with current variable values.

        Returns:
            New RelativeTextActive instance with the same configuration and fresh data.
        """
        # create new instance
        new_instance = RelativeTextActive(
            self._callable,
            # --- position ---
            mob_center=self._mob_center,
            vector=self._vector,
            align_left=self._align_left,
            align_right=self._align_right,
            align_top=self._align_top,
            align_bottom=self._align_bottom,
            align_screen=self._align_screen,
            screen_buff=self._screen_buff,
            anchor=self._anchor,
            # --- font ---
            font=self._font,
            font_size=self._font_size,
            weight=self._weight,
            highlight=self._highlight,
        )

        # copy anchor alignment
        self._align_with_anchor(new_instance)

        return new_instance


class RelativeText(RelativeTextBase):
    """Static text element positioned relative to another mobject.

    Args:
        text: The text string to visualize.
        mob_center: Reference mobject for positioning.
        vector: Offset vector from reference mobject center.
        align_left: Reference mobject to align left edge with.
        align_right: Reference mobject to align right edge with.
        align_top: Reference mobject to align top edge with.
        align_bottom: Reference mobject to align bottom edge with.
        align_screen: Direction vector for screen edge alignment.
        screen_buff: Buffer distance from screen edge when using align_screen.
        font: Text font family.
        font_size: Text font size.
        text_color: Text color.
        weight: Font weight (NORMAL, BOLD, etc.).
        highlight (bool): If True, creates a highlight rectangle around the text.
    """

    def __init__(
        self,
        text: str,
        # --- position ---
        mob_center: mn.Mobject = mn.Dot(mn.ORIGIN),
        vector: np.ndarray = mn.ORIGIN,
        align_left: mn.Mobject | None = None,
        align_right: mn.Mobject | None = None,
        align_top: mn.Mobject | None = None,
        align_bottom: mn.Mobject | None = None,
        align_screen: np.ndarray | None = None,
        screen_buff: float = 0.2,
        # --- font ---
        font="",
        font_size: float = 25,
        text_color: str | ManimColor = mn.WHITE,
        weight: str = "NORMAL",
        # --- other ---
        highlight: bool = True,
    ):
        super().__init__(
            mob_center=mob_center,
            vector=vector,
            align_left=align_left,
            align_right=align_right,
            align_top=align_top,
            align_bottom=align_bottom,
            align_screen=align_screen,
            screen_buff=screen_buff,
            font=font,
            font_size=font_size,
            weight=weight,
        )

        self._text = text
        self._text_color = text_color

        self._text_mob = self._create_text_mob(
            self._text,
            color=self._text_color,
        )

        self.add(self._text_mob)
        self._position()

        if highlight:
            self._hl_rect = HLRect(
                self._text_mob,
                self._get_hl_color(self._text_color),
            )
            self.add_to_back(self._hl_rect)
        else:
            self._hl_rect = None
