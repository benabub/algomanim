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
        *vars (Tuple[str, Callable[[], Any], str | ManimColor]):
            Tuples of (name, value_getter, color).
        mob_center (mn.Mobject): Reference mobject for positioning.
        vector (np.ndarray): Offset vector from reference mobject center.
        # align_edge (Literal["up", "down", "left", "right"] | None): Edge alignment.
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
        vector: np.ndarray = mn.UP * 1.2,
        align_edge: Literal["up", "down", "left", "right"] | None = None,
        # --- font ---
        font="",
        font_size=35,
        weight: str = "NORMAL",
        # --- other ---
        buff=0.5,
        equal_sign: bool = True,
        items_align_edge: np.ndarray = mn.UP,
        **kwargs,
    ):
        super().__init__(
            vector=vector,
            mob_center=mob_center,
            align_edge=align_edge,
            **kwargs,
        )

        self._vars = vars
        self._font = font
        self._font_size = font_size
        self._weight = weight
        self._buff = buff
        self._equal_sign = equal_sign
        self._items_align_edge = items_align_edge
        self._align_edge = align_edge

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

        # move to the specified position
        self._position(self._text_mob, self._text_mob)

        self.add(*self._text_mob)

    def update_text(self, scene: mn.Scene, time=0.1, animate: bool = True):
        """Update text values with current variable values.

        Args:
            scene: The scene to play animations in.
            time: Duration of animation if animate=True.
            animate: Whether to animate the update.
        """

        # create a new object with the same parameters
        new_group = RelativeTextValue(
            *self._vars,
            font_size=self._font_size,
            buff=self._buff,
            font=self._font,
            equal_sign=self._equal_sign,
            items_align_edge=self._items_align_edge,
        )

        self._position_mob_to_self(new_group, self._align_edge)

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
        # align_edge (Literal["up", "down", "left", "right"] | None): Edge alignment.
        font (str): Text font family.
        font_size (float): Text font size.
        font_color (str | ManimColor): Text color.
        weight (str): Text weight (NORMAL, BOLD, etc.).
        **kwargs: Additional keyword arguments passed to parent class.
    """

    def __init__(
        self,
        text: str,
        # --- position ---
        mob_center: mn.Mobject = mn.Dot(mn.ORIGIN),
        vector: np.ndarray = mn.UP * 1.1,
        # align_edge: Literal["up", "down", "left", "right"] | None = None,
        align_left: mn.Mobject | None = None,
        align_right: mn.Mobject | None = None,
        align_up: mn.Mobject | None = None,
        align_down: mn.Mobject | None = None,
        # --- font ---
        font="",
        font_size=35,
        font_color: str | ManimColor = mn.WHITE,
        weight: str = "NORMAL",
        **kwargs,
    ):
        super().__init__(
            vector=vector,
            mob_center=mob_center,
            # align_edge=align_edge,
            align_left=align_left,
            align_right=align_right,
            align_up=align_up,
            align_down=align_down,
            **kwargs,
        )

        self._text = text
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

        # self._position(self._text_mob, self._text_mob)

        self.add(self._text_mob)
        self._position()
