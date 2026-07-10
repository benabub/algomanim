class ListNode:
    """Leetcode definition for singly-linked list node.

    Args:
        val (int, optional): Node value. Defaults to 0.
        next (ListNode, optional): Next node reference. Defaults to None.
    """

    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __contains__(
        self,
        key: "ListNode | None",
    ) -> bool:
        """Check if a node exists in the linked list.

        Traverses the list starting from self and compares each node
        by object identity (is) with the given key.

        Args:
            key: The node to search for.

        Returns:
            True if the node is found in the list, False otherwise.
        """
        if self is None or key is None:
            return False

        current = self
        while current:
            if current is key:
                return True
            current = current.next

        return False

    def index(
        self,
        target: "ListNode | None",
    ) -> int | None:
        """Return the index of the target node in the list starting from self.

        Traverses the list from the current node and compares nodes by object id.

        Args:
            target: The node to search for.

        Returns:
            Zero-based index of the target node if found, None otherwise.
        """

        if target is None or self is None:
            return None

        current = self
        i = 0

        while current:
            if current is target:
                return i
            i += 1
            current = current.next


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
