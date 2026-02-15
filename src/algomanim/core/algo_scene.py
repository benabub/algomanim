import manim as mn
from contextlib import contextmanager
from typing import Generator, Any


class AlgoScene(mn.Scene):
    """Base scene class for AlgoManim projects.

    Provides integrated utility methods for synchronized audio and animation
    management within a Manim scene.

    Attributes:
        None (inherits from mn.Scene)
    """

    @contextmanager
    def sound_block(
        self, sound: str, offset: float = 0.0, after: float = 0.5
    ) -> Generator[None, Any, None]:
        """Context manager to play a sound and wait after an animation block.

        This helper synchronizes sound playback with an animation sequence.
        The sound starts with a specified offset, and the scene execution
        pauses after the block's animations are completed.

        Args:
            sound (str): Path to the audio file.
            offset (float): Time offset in seconds before the sound starts.
                Defaults to 0.0.
            wait_after (float): Duration in seconds to wait after the
                context block finishes. Defaults to 0.5.

        Yields:
            None: Control is yielded to the animations inside the 'with' block.

        Example:
            with self.sound_block(Sounds.click, offset=0.2, wait_after=1.0):
                self.play(FadeIn(mobject))
        """

        if offset < 0:
            self.add_sound(sound)
            self.wait(abs(offset))
            yield
        else:
            self.add_sound(sound, time_offset=offset)
            yield

        self.wait(after)
