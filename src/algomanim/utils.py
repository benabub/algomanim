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
import manim as mn

from .datastructures import (
    ListNode,
)


def get_cell_params(
    font_size: float,
    font: str,
    weight: str,
    test_sign: str = "0",
) -> dict:
    """Calculate comprehensive cell layout parameters.

    Args:
        font_size: Font size for text measurement.
        font: Font family name.
        weight: Font weight (NORMAL, BOLD, etc.).
        test_sign: Character used for measurement (default "0").

    Returns:
        Dictionary containing:
        - top_bottom_buff: Internal top/bottom padding
        - cell_height: Total cell height
        - top_buff: Top alignment buffer
        - bottom_buff: Standard bottom alignment buffer
        - deep_bottom_buff: Deep bottom alignment buffer
    """
    zero_mob = mn.Text(test_sign, font=font, font_size=font_size, weight=weight)

    zero_mob_height = zero_mob.height  # 0.35625

    top_bottom_buff = zero_mob_height / 2.375
    cell_height = top_bottom_buff * 2 + zero_mob_height
    top_buff = zero_mob_height / 3.958
    bottom_buff = zero_mob_height / 35.625 + top_bottom_buff
    deep_bottom_buff = zero_mob_height / 7.125

    return {
        "top_bottom_buff": top_bottom_buff,
        "cell_height": cell_height,
        "top_buff": top_buff,
        "bottom_buff": bottom_buff,
        "deep_bottom_buff": deep_bottom_buff,
    }


def get_cell_width(
    text_mob: mn.Mobject,
    inter_buff: float,
    cell_height: float,
) -> float:
    """Calculate cell width based on text content and constraints.

    Args:
        text_mob: Text mobject to measure.
        inter_buff: Internal padding within cells.
        cell_height: Pre-calculated cell height.

    Returns:
        Cell width, ensuring it's at least as tall as the cell height
        for consistent visual proportions.
    """
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


def create_pointers(self, cell_mob: mn.VGroup) -> tuple[mn.VGroup, mn.VGroup]:
    """Create pointer triangles above and below each cell in the group.

    Args:
        cell_mob: VGroup of cells to attach pointers to.

    Returns:
        Tuple of (top_pointers, bottom_pointers) VGroups where each contains
        triple triangle groups for every cell | node.

    Note:
        Each cell gets 3 triangles above and 3 below, arranged horizontally.
        Triangle groups are positioned with fixed buffering from cells.
    """

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

    pointers_top = mn.VGroup()
    pointers_bottom = mn.VGroup()
    for cell in cell_mob:
        # create top triangles (3 per cell)
        top_triple_group = mn.VGroup(*[top_triangle.copy() for _ in range(3)])
        # arrange top triangles horizontally above the cell
        top_triple_group.arrange(mn.RIGHT, buff=0.08)
        top_triple_group.next_to(cell, mn.UP, buff=0.15)
        pointers_top.add(top_triple_group)

        # create bottom triangles (3 per cell)
        bottom_triple_group = mn.VGroup(*[bottom_triangle.copy() for _ in range(3)])
        # arrange bottom triangles horizontally below the cell
        bottom_triple_group.arrange(mn.RIGHT, buff=0.08)
        bottom_triple_group.next_to(cell, mn.DOWN, buff=0.15)
        pointers_bottom.add(bottom_triple_group)

    return pointers_top, pointers_bottom


def update_visual_state(
    self,
    new_group,
    data: list | str | ListNode,
    old_cells: mn.VGroup | None,
    old_pointers_top: mn.VGroup | None,
    old_pointers_bottom: mn.VGroup | None,
):
    """Update visual components while preserving highlight states.

    Args:
        self: Target object to update.
        new_group: Source object with new visual state.
        data: Data to determine if structure is empty.
        old_cells: Previous containers mobject for color preservation.
        old_pointers_top: Previous top pointers for color preservation.
        old_pointers_bottom: Previous bottom pointers for color preservation.
    """
    if data:
        self.values_mob = new_group.values_mob

        self.pointers_top = new_group.pointers_top
        self.pointers_bottom = new_group.pointers_bottom

        # restore old highlights
        if old_cells:
            for old, new in zip(old_cells, self.containers_mob):
                new.set_fill(old.get_fill_color())

        if old_pointers_top:
            for old_ptrs, new_ptrs in zip(old_pointers_top, self.pointers_top):
                for old_tri, new_tri in zip(old_ptrs, new_ptrs):
                    new_tri.set_color(old_tri.get_color())

        if old_pointers_bottom:
            for old_ptrs, new_ptrs in zip(old_pointers_bottom, self.pointers_bottom):
                for old_tri, new_tri in zip(old_ptrs, new_ptrs):
                    new_tri.set_color(old_tri.get_color())

    else:
        self.pointers_top = mn.VGroup()
        self.pointers_bottom = mn.VGroup()


def create_linked_list(value: list) -> ListNode | None:
    """Create a singly-linked list from a list.

    Args:
        value: List to convert into linked list nodes.

    Returns:
        Head node of the created linked list, or None if values is empty.
    """

    if not value:
        return None
    head = ListNode(value[0])
    current = head
    for val in value[1:]:
        current.next = ListNode(val)
        current = current.next
    return head


def linked_list_to_list(head: ListNode | None) -> list:
    """Convert a linked list to a Python list.

    Args:
        head: Head node of the linked list.

    Returns:
        List containing all values from the linked list in order.
        Empty list if head is None.
    """
    result = []
    current = head
    while current:
        result.append(current.val)
        current = current.next
    return result


def get_linked_list_length(head: ListNode | None) -> int:
    """Calculate the length of a linked list.

    Args:
        head: Head node of the linked list.

    Returns:
        Number of nodes in the linked list. 0 if head is None.
    """
    count = 0
    current = head
    while current:
        count += 1
        current = current.next
    return count
