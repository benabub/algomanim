# import manim as mn

from .datastructures import (
    ListNode,
)


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
