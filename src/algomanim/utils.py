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
