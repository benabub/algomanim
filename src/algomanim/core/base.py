"""
Manim use notes:

  - mobject.arrange() resets previous position
  - fill_color requires fill_opacity=1 to be visible
  - Simply assigning  causes an unexpected shift in position:
    example: var = mobject
  - hasattr(mobject, "method_name") -> True (always), so it's bad idea to use it
"""

from typing import Literal

import numpy as np
import manim as mn


class AlgoManimBase(mn.VGroup):
    """Base class for all algomanim classes.

    Warning:
        This is base class only, cannot be instantiated directly.

    Args:
        vector (np.ndarray): Position offset from mob_center.
        mob_center (mn.Mobject): Reference mobject for positioning.
        align_edge (Literal["up", "down", "left", "right"] | None): Edge alignment.
        **kwargs: Additional keyword arguments passed to VGroup.
    """

    def __init__(
        self,
        vector: np.ndarray = mn.ORIGIN,
        mob_center: mn.Mobject = mn.Dot(mn.ORIGIN),
        align_edge: Literal["up", "down", "left", "right"] | None = None,
        **kwargs,
    ):
        if type(self) is AlgoManimBase:
            raise NotImplementedError(
                "AlgoManimBase is base class only, cannot be instantiated directly."
            )
        super().__init__(**kwargs)
        self._vector = vector
        self._mob_center = mob_center
        self._align_edge: Literal["up", "down", "left", "right"] | None = align_edge

    def first_appear(self, scene: mn.Scene, time=0.5):
        """Animate the initial appearance in scene.

        Args:
            scene: The scene to play the animation in.
            time: Duration of the fade-in animation.
        """
        scene.play(mn.FadeIn(self), run_time=time)

    def group_appear(self, scene: mn.Scene, *mobjects: mn.Mobject, time: float = 0.5):
        """Animate the appearance of this object together with additional mobjects.

        All mobjects fade in simultaneously with the same duration.

        Args:
            scene: The Manim scene to play the animation in.
            *mobjects: Additional mobjects to fade in together with this object.
            time: Duration of the fade-in animation for all objects.
        """

        animations = [mn.FadeIn(self)] + [mn.FadeIn(mob) for mob in mobjects]
        scene.play(*animations, run_time=time)

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
            mobject_to_move (mn.Mobject): The object to position.
            align_point (mn.Mobject): Reference point object for alignment.
        """

        align_edge = self._align_edge.lower() if self._align_edge else None

        if hasattr(self._mob_center, "_get_positioning"):
            mob_center = self._mob_center._get_positioning()
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

    def _position_mob_to_self(
        self: mn.Mobject,
        new_group: mn.Mobject,
        align_edge: Literal["up", "down", "left", "right"] | None = None,
    ):
        if align_edge == "left":
            new_group.align_to(self.get_left(), mn.LEFT)
            new_group.set_y(self.get_y())
        elif align_edge == "right":
            new_group.align_to(self.get_right(), mn.RIGHT)
            new_group.set_y(self.get_y())
        elif align_edge == "up":
            new_group.align_to(self.get_top(), mn.UP)
            new_group.set_x(self.get_x())
        elif align_edge == "down":
            new_group.align_to(self.get_bottom(), mn.DOWN)
            new_group.set_x(self.get_x())
        else:
            new_group.move_to(self.get_center())
