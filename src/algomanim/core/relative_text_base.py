from typing import Literal
from dataclasses import dataclass

import manim as mn
from manim import ManimColor

from algomanim.core.base import AlgoManimBase
from algomanim.core.updatable import UpdatableMixin
from algomanim.core.paths.hl_rect import HLRect


@dataclass(frozen=True)
class HLColors:
    colors = {
        mn.BLACK: mn.YELLOW,
    }


class RelativeTextBase(AlgoManimBase):
    """Base class for relative text elements.

    Args:
        font: Font family for text.
        font_size: Font size in points.
        weight: Font weight (NORMAL, BOLD, etc.).
        **kwargs: Additional keyword arguments passed to parent class.
    """

    HL_MAP = HLColors().colors

    def __init__(
        self,
        # --- font ---
        font="",
        font_size: float = 25,
        weight: str = "NORMAL",
        # ---- kwargs ----
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._font = font
        self._font_size = font_size
        self._weight = weight
        self._hl_rect: HLRect | None = None

    def _get_text_config(self) -> dict:
        """Return common text configuration dictionary.

        Returns:
            Dictionary with font, font_size, and weight.
        """
        return {
            "font": self._font,
            "font_size": self._font_size,
            "weight": self._weight,
        }

    def _create_text_mob(
        self,
        text: str,
        color: ManimColor | str,
    ) -> mn.Text:
        """Create a text mobject with common configuration.

        Args:
            text: The text string to display.
            color: Color of the text.

        Returns:
            Text mobject with configured font and size.
        """
        return mn.Text(text, color=color, **self._get_text_config())

    def _get_position(self):
        """Return text mobject for positioning purposes."""

        return self._text_mob

    def _get_hl_color(
        self,
        text_color: ManimColor | list[ManimColor] | str | None = None,
    ) -> ManimColor | str:
        """Get highlight color based on text color.

        Args:
            text_color: The text color to map to a glow color.
                If None or not found in HL_MAP, returns BLACK.

        Returns:
            Highlight color for the given text color.
        """
        if text_color:
            # If text_color is a list (gradient), take the first color
            if isinstance(text_color, list):
                text_color = text_color[0]
            if isinstance(text_color, str):
                text_color = ManimColor(text_color)
            if text_color in self.HL_MAP:
                return self.HL_MAP[text_color]
        return mn.BLACK

    def first_appear(
        self,
        scene: mn.Scene,
        update: bool = True,
        anim_time: float = 0.2,
        hl: bool = True,
        hl_time: float = 1.0,
    ):
        """Animate the initial appearance with optional highlight.

        For non-updatable objects (without `_set_new_value`), activates highlight
        before fading in. For updatable objects, highlight is already active
        (set in constructor). After fade-in, waits and deactivates highlight.

        Args:
            scene: The scene to play the animation in.
            update: If True, calls `_set_new_value()` before appearing.
            appear_time: Duration of the fade-in animation.
            hl: If True, enables highlight behavior.
            hl_time: Time to wait before deactivating the highlight.
        """

        if update:
            if hasattr(self, "_set_new_value"):
                self._set_new_value()

        if not hl and self._hl_rect is not None:
            self._hl_rect.deactivate()

        scene.play(mn.FadeIn(self), run_time=anim_time)

        if not hl and self._hl_rect is not None:
            return

        if hl and self._hl_rect is not None:
            scene.wait(hl_time)
            self._hl_rect.deactivate()


class RelativeTextUpdatable(RelativeTextBase, UpdatableMixin):
    """Base class for updatable relative text elements.

    Args:
        anchor: Alignment anchor when no edge alignment specified.
            Must be "start", "end", or None. Defaults to "start".
        **kwargs: Additional keyword arguments passed to parent class.
    """

    def __init__(
        self,
        # --- position ---
        anchor: Literal["start", "end"] | None = "start",
        align_left: mn.Mobject | None = None,
        align_right: mn.Mobject | None = None,
        # ---- kwargs ----
        **kwargs,
    ):
        super().__init__(**kwargs)
        # ---- align left|right ----
        self._align_left = align_left
        self._align_right = align_right
        # ---- anchor ----
        if anchor is not None:
            if anchor not in ["start", "end"]:
                raise ValueError("anchor must be 'start', 'end' or None")
            self._anchor = anchor
        else:
            self._anchor: Literal["start", "end"] | None = None

        self._sync_anchor()

    def _sync_anchor(self) -> None:
        """Synchronize anchor with align_left/align_right.

        If align_left is set, anchor becomes "start".
        If align_right is set, anchor becomes "end".
        """
        if self._align_left is not None:
            self._anchor = "start"
        elif self._align_right is not None:
            self._anchor = "end"

    def _align_with_anchor(
        self,
        new_instance: "RelativeTextUpdatable",
    ) -> None:
        """Align new instance based on anchor.

        Args:
            new_instance: The new instance to align relative to this one.
        """
        if self._anchor == "start":
            new_instance.align_to(self.get_left(), mn.LEFT)
        elif self._anchor == "end":
            new_instance.align_to(self.get_right(), mn.RIGHT)

    def update_value(
        self,
        scene: mn.Scene,
        animate: bool = True,
        anim_time=0.2,
        hl: bool = True,
        hl_time: float = 1.0,
    ) -> None:
        """Update text values with current variable values.

        Args:
            scene: The scene to play animations in.
            time: Duration of animation if animate=True.
            animate: Whether to animate the update.
        """
        if self not in scene.mobjects:
            RelativeTextBase.first_appear(
                self,
                scene,
                anim_time=anim_time,
                hl=hl,
                hl_time=hl_time,
            )
            return

        UpdatableMixin.update_value(self, scene, animate=animate, anim_time=anim_time)

        if hl and self._hl_rect is not None:
            scene.wait(hl_time)
            self._hl_rect.deactivate()


class SingleRelativeTextMixin(AlgoManimBase):
    """
    Mixin for RelativeText classes with single mn.Text mobject.
    """

    def change_color(
        self,
        scene: mn.Scene,
        color: str | ManimColor,
        hl: bool = True,
        hl_time: float = 1.3,
    ) -> None:
        """Change text color with optional highlight effect.

        Args:
            scene: The Manim scene to play animations in.
            color: New color for the text.
            hl: If True, activates highlight before color change and
                deactivates after hl_time.
            hl_time: Duration to keep highlight active.

        Raises:
            ValueError: If object lacks required `_hl_rect` or `_text_mob` attributes.
        """
        if not hasattr(self, "_hl_rect") or not isinstance(self._hl_rect, HLRect):
            raise ValueError("Object must have _hl_rect attribute of HLRect type")

        if hl:
            if self._hl_rect is None:
                hl = False

        if hasattr(self, "_text_mob") and isinstance(self._text_mob, mn.Text):
            self._text_mob.set_color(color)

        if hl:
            self._hl_rect.activate()
            scene.wait(hl_time)
            self._hl_rect.deactivate()
