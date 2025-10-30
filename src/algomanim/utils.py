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


def create_pointers(self, cell_mob: mn.VGroup):
    """Create pointer triangles above and below each cell in the group.

    Args:
        cell_mob: VGroup of cells to attach pointers to.

    Note:
        Creates self.pointers_list with top and bottom pointer groups.
        Result structure:
        self.pointers_list[0] = [nameless_top_triple_Vgroup_0, ...]
        self.pointers_list[1] = [nameless_bottom_triple_Vgroup_0, ...]
    """

    # create pointers as a list with top and bottom groups
    self.pointers_list = [[], []]  # [0] for top, [1] for bottom

    # create template triangles
    top_triangle = (
        mn.Triangle(color=self.bg_color)
        .stretch_to_fit_width(0.7)
        .scale(0.1)
        .rotate(mn.PI)
    )
    bottom_triangle = (
        mn.Triangle(color=self.bg_color).stretch_to_fit_width(0.7).scale(0.1)
    )

    for cell in cell_mob:
        # create top triangles (3 per cell)
        top_triple_group = mn.VGroup(*[top_triangle.copy() for _ in range(3)])
        # arrange top triangles horizontally above the cell
        top_triple_group.arrange(mn.RIGHT, buff=0.08)
        top_triple_group.next_to(cell, mn.UP, buff=0.15)
        self.pointers_list[0].append(top_triple_group)

        # create bottom triangles (3 per cell)
        bottom_triple_group = mn.VGroup(*[bottom_triangle.copy() for _ in range(3)])
        # arrange bottom triangles horizontally below the cell
        bottom_triple_group.arrange(mn.RIGHT, buff=0.08)
        bottom_triple_group.next_to(cell, mn.DOWN, buff=0.15)
        self.pointers_list[1].append(bottom_triple_group)
