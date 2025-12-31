"""
Manim use notes:

  - mobject.arrange() resets previous position
  - fill_color requires fill_opacity=1 to be visible
  - Simply assigning  causes an unexpected shift in position:
    example: var = mobject
  - hasattr(mobject, "method_name") -> True (always), so it's bad idea to use it
  - Transform animations with SVGMobjects will produce visual artifacts
    for unknown reason (artifacts are located in mn.ORIGIN)
"""

import numpy as np
import manim as mn


class AlgoManimBase(mn.VGroup):
    """Base class for all algomanim classes.

    Warning:
        This is base class only, cannot be instantiated directly.

    Args:
        vector (np.ndarray): Position offset from mob_center.
        mob_center (mn.Mobject): Reference mobject for positioning.
        align_left (mn.Mobject | None): Reference mobject to align left edge with.
        align_right (mn.Mobject | None): Reference mobject to align right edge with.
        align_top (mn.Mobject | None): Reference mobject to align top edge with.
        align_bottom (mn.Mobject | None): Reference mobject to align bottom edge with.
        **kwargs: Additional keyword arguments passed to VGroup.

    Raises:
        ValueError: If both align_left and align_right are provided,
                   or both align_up and align_down are provided.
        NotImplementedError: If instantiated directly.
    """

    def __init__(
        self,
        vector: np.ndarray = mn.ORIGIN,
        mob_center: mn.Mobject = mn.Dot(mn.ORIGIN),
        align_left: mn.Mobject | None = None,
        align_right: mn.Mobject | None = None,
        align_top: mn.Mobject | None = None,
        align_bottom: mn.Mobject | None = None,
        **kwargs,
    ):
        # ------ checks -------
        if align_left and align_right:
            raise ValueError("Cannot use align_left and align_right together")
        if align_top and align_bottom:
            raise ValueError("Cannot use align_up and align_down together")

        if type(self) is AlgoManimBase:
            raise NotImplementedError(
                "AlgoManimBase is base class only, cannot be instantiated directly."
            )

        # ------ inition -------
        super().__init__(**kwargs)
        self._vector = vector
        self._mob_center = mob_center
        self._align_left = align_left
        self._align_right = align_right
        self._align_top = align_top
        self._align_bottom = align_bottom

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
    ) -> None:
        """Position the object relative to reference mobject with optional edge alignment.

        Positioning is performed in this order:
        1. Move to mob_center's positioning point
        2. Apply edge alignments if specified
        3. Apply vector offset

        The positioning point of mob_center is obtained via its `_get_positioning()`
        method if available, otherwise uses its center.
        """

        if hasattr(self._mob_center, "_get_position"):
            mob_center = self._mob_center._get_position()
        else:
            mob_center = self._mob_center

        self.move_to(mob_center)

        if self._align_left:
            align_mob = self._align_left
            if hasattr(align_mob, "_get_position"):
                align_mob = align_mob._get_position()
            shift_x = align_mob.get_left()[0] - self.get_left()[0]
            self.shift(mn.RIGHT * shift_x)

        if self._align_right:
            align_mob = self._align_right
            if hasattr(align_mob, "_get_position"):
                align_mob = align_mob._get_position()
            shift_x = align_mob.get_right()[0] - self.get_right()[0]
            self.shift(mn.RIGHT * shift_x)

        if self._align_top:
            align_mob = self._align_top
            if hasattr(align_mob, "_get_position"):
                align_mob = align_mob._get_position()
            shift_y = align_mob.get_top()[1] - self.get_top()[1]
            self.shift(mn.UP * shift_y)

        if self._align_bottom:
            align_mob = self._align_bottom
            if hasattr(align_mob, "_get_position"):
                align_mob = align_mob._get_position()
            shift_y = align_mob.get_bottom()[1] - self.get_bottom()[1]
            self.shift(mn.UP * shift_y)

        self.shift(self._vector)
