from abc import ABC, abstractmethod
from typing import Any
import manim as mn

from algomanim.core.base import AlgoManimBase


class UpdatableMixin(AlgoManimBase, ABC):
    """
    ...
    """

    @abstractmethod
    def _create_new_instance(self) -> "AlgoManimBase":
        """Create a new instance with current configuration and fresh data.

        Returns:
            New instance with the same configuration and updated data.
        """
        pass

    @abstractmethod
    def _update_internal_state(self, new_instance: Any) -> None:
        """Update the current instance with data from a new instance.

        Copies data, mobject references, and highlight states from the new instance.
        Highlights are preserved and reapplied to the updated containers.

        Args:
            new_instance: The instance to copy state from.
        """
        pass

    def _set_new_value(self) -> None:
        """Update internal data from callable without scene animation.

        Replaces the current instance with a newly created one if the data has changed.
        Preserves highlights and alignment. Does not add to scene.
        """
        new_instance = self._create_new_instance()
        self._update_internal_state(new_instance)

    def update_value(
        self,
        scene: mn.Scene,
        animate: bool = True,
        anim_time: float = 0.2,
    ) -> None:
        """Replace the linked list visualization with new nodes.

        Args:
            scene: The Manim scene to play animations in.
            animate: If True, plays a fade transition. If False, updates instantly.
            update_time: Duration of the fade transition if animate=True.
        """
        new_instance = self._create_new_instance()

        if animate:
            scene.play(
                mn.FadeOut(self),
                mn.FadeIn(new_instance),
                run_time=anim_time,
            )

        scene.remove(self)
        scene.remove(new_instance)

        self._update_internal_state(new_instance)
        scene.add(self)

        self._clear_scene(scene)
