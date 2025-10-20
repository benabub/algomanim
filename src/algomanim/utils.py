from typing import (
    # cast,
    # List,
    # Tuple,
    # Callable,
    # Any,
    # Union,
    # Optional,
    Literal,
)
import numpy as np
import manim as mn  # type: ignore
# from manim import ManimColor


def get_cell_height(
    font_size: float,
    inter_buff: float,
    test_sign: str = "0",
) -> float:
    zero_mob = mn.Text(test_sign, font_size=font_size)
    zero_mob_height = zero_mob.height
    return inter_buff * 2 + zero_mob_height


def get_cell_width(
    text_mob: mn.Mobject,
    inter_buff: float,
    square_height: float,
) -> float:
    text_mob_height = text_mob.width
    res = inter_buff * 2.5 + text_mob_height
    if square_height >= res:
        return square_height
    else:
        return res


def square_scale(size: Literal["s", "m", "l", "ls"]) -> dict[str, float]:
    """Returns scaling parameters for a square mobject.

    Args:
        size: Size identifier - 's' (small), 'm' (medium), 'l' (large),
        'ls' (large squares, small font).

    Returns:
        Dictionary containing 'side_length' and 'font_size'.

    Raises:
        ValueError: if invalid size is provided.
    """

    SIZES = {
        "s": {"side_length": 0.5, "font_size": 35},
        "m": {"side_length": 0.6, "font_size": 40},
        "l": {"side_length": 0.7, "font_size": 50},
        "ls": {"side_length": 0.7, "font_size": 35},
    }
    if size not in SIZES:
        available_sizes = ", ".join(f"'{s}'" for s in SIZES.keys())
        raise ValueError(f"size must be one of: {available_sizes}")
    return SIZES[size]


def position(
    mobject: mn.Mobject,
    mob_center: mn.Mobject,
    align_edge: Literal["up", "down", "left", "right"] | None,
    vector: np.ndarray,
) -> None:
    """Position mobject relative to center with optional edge alignment.

    Args:
        mobject: The object to position
        mob_center: Reference center object
        align_edge: Which edge to align to (None for center)
        vector: Additional offset vector
    """
    if align_edge:
        if align_edge in ["UP", "up"]:
            mobject.move_to(mob_center.get_center())
            mobject.align_to(mob_center, mn.UP)
            mobject.shift(vector)
        elif align_edge in ["DOWN", "down"]:
            mobject.move_to(mob_center.get_center())
            mobject.align_to(mob_center, mn.DOWN)
            mobject.shift(vector)
        elif align_edge in ["RIGHT", "right"]:
            mobject.move_to(mob_center.get_center())
            mobject.align_to(mob_center, mn.RIGHT)
            mobject.shift(vector)
        elif align_edge in ["LEFT", "left"]:
            mobject.move_to(mob_center.get_center())
            mobject.align_to(mob_center, mn.LEFT)
            mobject.shift(vector)
    else:
        mobject.move_to(mob_center.get_center() + vector)
