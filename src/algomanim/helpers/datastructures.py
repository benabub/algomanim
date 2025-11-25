class ListNode:
    """Leetcode definition for singly-linked list node.

    Args:
        val (int, optional): Node value. Defaults to 0.
        next (ListNode, optional): Next node reference. Defaults to None.
    """

    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class TreeNode:
    """Leetcode definition for a binary tree node.

    Args:
        val (int, optional): Node value. Defaults to 0.
        left (TreeNode, optional): Left child node. Defaults to None.
        right (TreeNode, optional): Right child node. Defaults to None.
    """

    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Node:
    """Leetcode definition for a doubly linked list node with child.

    Args:
        val: Node value.
        prev: Previous node reference.
        next: Next node reference.
        child: Child node reference.
    """

    def __init__(self, val, prev, next, child):
        self.val = val
        self.prev = prev
        self.next = next
        self.child = child
