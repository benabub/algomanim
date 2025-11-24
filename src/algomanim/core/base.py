"""
Manim use notes:

  - mobject.arrange() resets previous position
  - fill_color requires fill_opacity=1 to be visible
  - Simply assigning  causes an unexpected shift in position:
    example: var = mobject
  - hasattr(mobject, "method_name") -> True (always), so it's bad idea to use it
"""

from abc import ABC
from typing import Literal

import numpy as np
import manim as mn


class AlgoManimBase(mn.VGroup, ABC):
    """Base class for all algomanim classes"""

    def __init__(
        self,
    ):
        super().__init__()
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
        from algomanim.core.linear_container import LinearContainerStructure

        align_edge = self._align_edge.lower() if self._align_edge else None

        if isinstance(self._mob_center, LinearContainerStructure):
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
