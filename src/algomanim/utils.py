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
    font: str,
    inter_buff: float,
    test_sign: str = "0",
) -> float:
    zero_mob = mn.Text(test_sign, font=font, font_size=font_size)
    zero_mob_height = zero_mob.height
    return inter_buff * 2 + zero_mob_height


def get_cell_width(
    text_mob: mn.Mobject,
    inter_buff: float,
    cell_height: float,
) -> float:
    text_mob_height = text_mob.width
    res = inter_buff * 2.5 + text_mob_height
    if cell_height >= res:
        return cell_height
    else:
        return res


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
