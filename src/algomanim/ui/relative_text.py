from typing import (
    List,
    Tuple,
    Callable,
    Any,
)

import numpy as np
import manim as mn
from manim import ManimColor

from algomanim.core.base import AlgoManimBase


class RelativeTextValue(AlgoManimBase):
    """Text group showing scope variables positioned relative to mobject.

    Args:
        *vars (Tuple[str, Callable[[], Any], str | ManimColor]):
            Tuples of (name, value_getter, color).
        mob_center (mn.Mobject): Reference mobject for positioning.
        vector (np.ndarray): Offset vector from reference mobject center.
        align_left: Reference mobject to align left edge with.
        align_right: Reference mobject to align right edge with.
        align_top: Reference mobject to align top edge with.
        align_bottom: Reference mobject to align bottom edge with.
        anchor: Optional alignment anchor when neither align_left nor align_right
            is specified. Must be mn.LEFT or mn.RIGHT. Defaults to mn.LEFT.
        font (str): Text font family.
        font_size (float): Text font size.
        weight (str): Font weight (NORMAL, BOLD, etc.).
        buff (float): Spacing between text elements.
        equal_sign (bool): Whether to use equals sign between name and value.
        items_align_edge (np.ndarray): Alignment edge for text items within the group.
        **kwargs: Additional keyword arguments passed to parent class.
    """

    def __init__(
        self,
        *vars: Tuple[str, Callable[[], Any], str | ManimColor],
        # --- position ---
        mob_center: mn.Mobject = mn.Dot(mn.ORIGIN),
        vector: np.ndarray = mn.ORIGIN,
        align_left: mn.Mobject | None = None,
        align_right: mn.Mobject | None = None,
        align_top: mn.Mobject | None = None,
        align_bottom: mn.Mobject | None = None,
        anchor: np.ndarray | None = mn.LEFT,
        # --- font ---
        font="",
        font_size=35,
        weight: str = "NORMAL",
        # --- other ---
        buff=0.5,
        equal_sign: bool = True,
        items_align_edge: np.ndarray = mn.UP,
    ):
        super().__init__(
            vector=vector,
            mob_center=mob_center,
            align_left=align_left,
            align_right=align_right,
            align_top=align_top,
            align_bottom=align_bottom,
        )

        self._vars = vars
        # --- font ---
        self._font = font
        self._font_size = font_size
        self._weight = weight
        # --- other ---
        self._buff = buff
        self._equal_sign = equal_sign
        self._items_align_edge = items_align_edge
        # ---- anchor ----
        if not (align_left or align_right) and anchor is not None:
            if not (
                np.array_equal(anchor, mn.RIGHT) or np.array_equal(anchor, mn.LEFT)
            ):
                raise ValueError("anchor must be mn.RIGHT or mn.LEFT")
            self._anchor = anchor
        else:
            self._anchor = None

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
            mn.RIGHT, buff=self._buff, aligned_edge=self._items_align_edge
        )

        self.add(*self._text_mob)

        self._position()

    def update_value(self, scene: mn.Scene, time=0.1, animate: bool = True):
        """Update text values with current variable values.

        Args:
            scene: The scene to play animations in.
            time: Duration of animation if animate=True.
            animate: Whether to animate the update.
        """

        # create a new object with the same parameters
        new_group = RelativeTextValue(
            *self._vars,
            # --- position ---
            mob_center=self._mob_center,
            vector=self._vector,
            align_left=self._align_left,
            align_right=self._align_right,
            align_top=self._align_top,
            align_bottom=self._align_bottom,
            # --- font ---
            font=self._font,
            font_size=self._font_size,
            weight=self._weight,
            # --- other ---
            buff=self._buff,
            equal_sign=self._equal_sign,
            items_align_edge=self._items_align_edge,
        )

        if self._anchor is not None:
            if np.array_equal(self._anchor, mn.LEFT):
                new_group.align_to(self.get_left(), mn.LEFT)
            else:
                new_group.align_to(self.get_right(), mn.RIGHT)

        if animate:
            scene.play(mn.Transform(self, new_group), run_time=time)
        else:
            scene.remove(self)
            self.become(new_group)
            scene.add(self)


class RelativeText(AlgoManimBase):
    """Text group positioned relative to another mobject.

    Args:
        text (str): The text string to visualize.
        mob_center (mn.Mobject): Reference mobject for positioning.
        vector (np.ndarray): Offset vector from reference mobject center.
        align_left: Reference mobject to align left edge with.
        align_right: Reference mobject to align right edge with.
        align_top: Reference mobject to align top edge with.
        align_bottom: Reference mobject to align bottom edge with.
        font (str): Text font family.
        font_size (float): Text font size.
        text_color (str | ManimColor): Text color.
        weight (str): Text weight (NORMAL, BOLD, etc.).
        **kwargs: Additional keyword arguments passed to parent class.
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
        # --- font ---
        font="",
        font_size=35,
        text_color: str | ManimColor = mn.WHITE,
        weight: str = "NORMAL",
    ):
        super().__init__(
            vector=vector,
            mob_center=mob_center,
            align_left=align_left,
            align_right=align_right,
            align_top=align_top,
            align_bottom=align_bottom,
        )

        self._text = text
        self._font = font
        self._font_size = font_size
        self._text_color = text_color
        self._weight = weight

        self._text_mob = mn.Text(
            self._text,
            font=self._font,
            color=self._text_color,
            font_size=self._font_size,
            weight=self._weight,
        )

        self.add(self._text_mob)
        self._position()
