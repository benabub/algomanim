from typing import (
    List,
    Tuple,
    Callable,
    Any,
    Literal,
)

import numpy as np
import manim as mn
from manim import ManimColor

from algomanim.core.base import AlgoManimBase


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
