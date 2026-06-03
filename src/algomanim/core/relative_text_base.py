from typing import Literal
from abc import abstractmethod

import manim as mn
from manim import ManimColor

from algomanim.core.base import AlgoManimBase


class RelativeTextBase(AlgoManimBase):
    """Base class for relative text elements.

    Args:
        font: Font family for text.
        font_size: Font size in points.
        weight: Font weight (NORMAL, BOLD, etc.).
        **kwargs: Additional keyword arguments passed to parent class.
    """

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


class RelativeTextUpdatable(RelativeTextBase):
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
        # ---- kwargs ----
        **kwargs,
    ):
        super().__init__(**kwargs)
        # ---- anchor ----
        if anchor is not None:
            if anchor not in ["start", "end"]:
                raise ValueError("anchor must be 'start', 'end' or None")
            self._anchor = anchor
        else:
            self._anchor: Literal["start", "end"] | None = None

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

    @abstractmethod
    def _create_new_instance(self) -> "RelativeTextUpdatable":
        """Create a new instance with current configuration and fresh data.

        Returns:
            New instance with the same configuration and updated data.
        """
        pass

    def _set_new_value(self) -> None:
        """Update internal data from callables without scene animation.

        Replaces the current instance with a newly created one.
        Does not add to scene. Useful for silent updates before appearance.
        """

        new_instance = self._create_new_instance()

        # replace self
        self.become(new_instance)

    def update_value(
        self,
        scene: mn.Scene,
        time=0.1,
        animate: bool = True,
    ) -> None:
        """Update text values with current variable values.

        Args:
            scene: The scene to play animations in.
            time: Duration of animation if animate=True.
            animate: Whether to animate the update.
        """

        new_instance = self._create_new_instance()

        if animate:
            scene.play(mn.Transform(self, new_instance), run_time=time)
        else:
            scene.remove(self)
            self.become(new_instance)
            scene.add(self)
