from ..datastructures import (
    ListNode,
)


def create_linked_list(values: list) -> ListNode:
    """Create linked list from list of values"""
    head = ListNode(values[0])
    current = head
    for val in values[1:]:
        current.next = ListNode(val)
        current = current.next
    return head


def to_list(head: ListNode) -> list:
    """Convert linked list to Python list"""
    result = []
    current = head
    while current:
        result.append(current.val)
        current = current.next
    return result


def get_length(head: ListNode) -> int:
    """Get length of linked list"""
    count = 0
    current = head
    while current:
        count += 1
        current = current.next
    return count
