from typing import Any

import numpy as np
import manim as mn
from manim import ManimColor

from algomanim.helpers.datastructures import ListNode
from algomanim.core.linear_container import LinearContainerStructure
from algomanim.assets.svg import SVG_DIR


class LinkedList(LinearContainerStructure):
    """Linked list visualization as a VGroup of nodes with values and pointers.

    Args:
        head (ListNode | None): Head node of the linked list.
        radius (float): Radius of the circular nodes.
        direction (np.ndarray): Direction vector for list orientation.
        node_color (ManimColor | str): Border color for nodes.
        fill_color (ManimColor | str): Fill color for nodes.
        bg_color (ManimColor | str): Background color of scene and default pointer color.
        vector (np.ndarray): Position offset from mob_center.
        mob_center (mn.Mobject): Reference mobject for positioning.
        align_left: Reference mobject to align left edge with.
        align_right: Reference mobject to align right edge with.
        align_top: Reference mobject to align top edge with.
        align_bottom: Reference mobject to align bottom edge with.
        anchor: Optional alignment anchor when neither align_left nor align_right
        font (str): Font family for text elements.
        text_color (ManimColor | str): Color for text elements.
        weight (str): Font weight (NORMAL, BOLD, etc.).
        pointers: Whether to create and display pointers.
        **kwargs: Additional keyword arguments passed to parent class.
    """

    def __init__(
        self,
        head: ListNode | None,
        radius: float = 0.4,
        direction: np.ndarray = mn.RIGHT,
        # --- containers colors ---
        node_color: ManimColor | str = mn.BLACK,
        fill_color: ManimColor | str = mn.LIGHT_GRAY,
        bg_color: ManimColor | str = mn.DARK_GRAY,
        # -- position --
        vector: np.ndarray = mn.ORIGIN,
        mob_center: mn.Mobject = mn.Dot(mn.ORIGIN),
        align_left: mn.Mobject | None = None,
        align_right: mn.Mobject | None = None,
        align_top: mn.Mobject | None = None,
        align_bottom: mn.Mobject | None = None,
        anchor: np.ndarray | None = mn.LEFT,
        # -- font --
        font: str = "",
        text_color: ManimColor | str = mn.BLACK,
        weight: str = "NORMAL",
        # ---- pointers ----
        pointers: bool = True,
        # ---- kwargs ----
        **kwargs,
    ):
        kwargs.setdefault("color_123", mn.WHITE)
        kwargs.setdefault("color_containers_with_value", mn.RED)
        self._parent_kwargs = kwargs.copy()

        super().__init__(
            container_color=node_color,
            fill_color=fill_color,
            bg_color=bg_color,
            vector=vector,
            mob_center=mob_center,
            align_left=align_left,
            align_right=align_right,
            align_top=align_top,
            align_bottom=align_bottom,
            font=font,
            text_color=text_color,
            weight=weight,
            **kwargs,
        )

        # create class instance fields
        self._data = self.linked_list_to_list(head)  # save head as py builtin list
        self._radius = radius
        self._direction = direction
        # --- containers colors ---
        self._node_color = node_color
        self._fill_color = fill_color
        self._bg_color = bg_color
        # -- position --
        self._vector = vector
        self._mob_center = mob_center
        self._align_left = align_left
        self._align_right = align_right
        self._align_top = align_top
        self._align_bottom = align_bottom
        # -- font --
        self._font = font
        self._text_color = text_color
        self._weight = weight
        # ---- pointers ----
        self._pointers = pointers
        # ---- anchor ----
        if not (align_left or align_right) and anchor is not None:
            if not (
                np.array_equal(anchor, mn.RIGHT) or np.array_equal(anchor, mn.LEFT)
            ):
                raise ValueError("anchor must be mn.RIGHT or mn.LEFT")
            self._anchor = anchor
        else:
            self._anchor = None

        # empty value
        if not self._data:
            self._create_empty_linked_list()
            return

        # nodes
        self._containers_mob = self._create_containers_mob()

        # arrows
        self._arrows_mob = self._create_and_pos_arrows_mob()

        self._frame_mob = mn.VGroup(
            self._containers_mob,
            self._arrows_mob,
        )

        # rotate frame
        self._rotate_frame()

        self.add(self._containers_mob, self._arrows_mob)
        self._position()

        # pointers
        if self._pointers:
            self._pointers_top, self._pointers_bottom = self.create_pointers(
                self._containers_mob, direction=self._direction
            )
            self.add(self._pointers_top, self._pointers_bottom)

        # values
        self._values_mob = self._create_and_pos_values_mob()
        self.add(self._values_mob)

    def _create_empty_linked_list(self):
        """Initialize empty linked list visualization."""

        self._containers_mob = mn.Circle(
            radius=self._radius,
            color=self._bg_color,
            fill_color=self._bg_color,
            fill_opacity=1,
            stroke_width=self._radius * 7,
        )

        self.add(self._containers_mob)
        self._position()

        top_bottom_buff = self._radius / 2
        max_size_center = (self._radius - top_bottom_buff) * 2.5
        self._empty_value_mob = mn.Text(
            "None",
            font_size=40,
            font=self._font,
            weight=self._weight,
            color=mn.WHITE,
        )
        self._empty_value_mob.scale_to_fit_width(max_size_center)
        self._empty_value_mob.move_to(self._containers_mob)
        self.add(self._empty_value_mob)

    @staticmethod
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

    @staticmethod
    def get_head_value(head: ListNode | None) -> Any | None:
        """Get the value of the head node in a linked list.

        If the linked list is empty (head is None), returns None. Otherwise,
        extracts and returns the value of the first node.

        Args:
            head: Head node of the linked list, or None for empty list.

        Returns:
            Value of the head node, or None if the list is empty.
        """
        return LinkedList.linked_list_to_list(head)[0] if head else None

    @staticmethod
    def get_length(head: ListNode | None) -> int:
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

    @staticmethod
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

    def _create_containers_mob(self):
        """Create circular node mobjects for the linked list.

        Returns:
            mn.VGroup: Group of circular node mobjects.
        """

        node = mn.Circle(
            radius=self._radius,
            color=self._container_color,
            fill_color=self._fill_color,
            fill_opacity=1,
            stroke_width=self._radius * 7,
        )
        containers_mob = mn.VGroup(*[node.copy() for _ in range(len(self._data))])
        containers_mob.arrange(buff=self._radius)

        return containers_mob

    def _create_and_pos_arrows_mob(self):
        """Create and position arrow mobjects between nodes.

        Returns:
            mn.VGroup: Group of arrow mobjects connecting the nodes.
        """

        arrow_path = str(SVG_DIR / "arrows/radius_x10.svg")
        arrow = mn.SVGMobject(
            arrow_path,
            width=self._radius,
        )
        arrows_mob = mn.VGroup()
        for i in range(len(self._data) - 1):
            new_arrow = arrow.copy()
            new_arrow.next_to(self._containers_mob[i], buff=0)
            arrows_mob.add(new_arrow)
        return arrows_mob

    def _create_frame_mob(self):
        """Create frame mobject containing all linked list elements.

        Returns:
            mn.VGroup: Group containing containers, arrows, and pointers.
        """
        if self._pointers:
            return mn.VGroup(
                self._containers_mob,
                self._arrows_mob,
                self._pointers_top,
                self._pointers_bottom,
            )
        else:
            return mn.VGroup(
                self._containers_mob,
                self._arrows_mob,
            )

    def _rotate_frame(self) -> None:
        """Rotate the entire linked list frame to match the specified direction."""

        if not np.allclose(self._direction, mn.RIGHT):
            angle = mn.angle_of_vector(self._direction)
            self._frame_mob.rotate(
                angle,
                about_point=self._containers_mob[0].get_center(),
            )

    def _text_config(self):
        return {
            "font": self._font,
            "weight": self._weight,
            "color": self._text_color,
        }

    def _create_and_pos_values_mob(self):
        """Create and position value text mobjects inside nodes.

        Returns:
            mn.VGroup: Group of value text mobjects positioned within nodes.
        """

        top_bottom_buff = self._radius / 2
        ypgj_shift = self._radius / 16
        max_size_test = (self._radius - top_bottom_buff) * 2
        max_size_center = (self._radius - top_bottom_buff) * 2.5
        max_size_shift = (self._radius - top_bottom_buff) * 2.2

        # find base font_size
        font_size = 10
        test_mob = mn.Text("0", font_size=font_size)
        while test_mob.height < max_size_test:
            font_size += 1
            test_mob = mn.Text("0", font_size=font_size)

        values_mob = mn.VGroup(
            *[
                mn.Text(str(val), font_size=font_size, **self._text_config())
                for val in self._data
            ]
        )

        for i in range(len(self._data)):
            val = str(self._data[i])
            val_set = set(val)
            mob = values_mob[i]
            width = mob.width
            container = self._containers_mob[i]

            if len(val) == 1 and val in "0123456789":  # center alignment
                mob.move_to(container)
                continue

            if val_set.issubset({'"', "'", "^", "`"}):  # top alignment
                if width > max_size_shift:
                    mob.scale_to_fit_width(max_size_shift)
                mob.next_to(
                    container.get_top(),
                    direction=mn.DOWN,
                    buff=top_bottom_buff,
                )
                continue

            if val_set.issubset({"y", "p", "g", "j"}):  # down shift
                if width > max_size_center:
                    mob.scale_to_fit_width(max_size_center)
                mob.move_to(container)
                mob.shift(mn.DOWN * ypgj_shift)
                continue

            if val_set.issubset({".", ",", "_"}):  # bottom alignment
                if width > max_size_shift:
                    mob.scale_to_fit_width(max_size_shift)
                mob.next_to(
                    container.get_bottom(),
                    direction=mn.UP,
                    buff=top_bottom_buff,
                )
                continue

            if width > max_size_center:
                mob.scale_to_fit_width(max_size_center)
            mob.move_to(container)

        return values_mob

    def update_value(
        self,
        scene: mn.Scene,
        new_value: ListNode | None,
        animate: bool = False,
        run_time: float = 0.2,
    ) -> None:
        """Replace the linked list visualization with new nodes.

        Args:
            scene (mn.Scene): The Manim scene to play animations in.
            new_value: New linked list head node.
            animate (bool): If True, animates the transition using Transform.
            run_time (float): Duration of animation if animate=True.
        """

        # checks
        if not self._data and not new_value:
            return

        # new group
        new_group = LinkedList(
            head=new_value,
            radius=self._radius,
            direction=self._direction,
            # --- containers colors ---
            node_color=self._node_color,
            fill_color=self._fill_color,
            bg_color=self._bg_color,
            # -- position --
            vector=self._vector,
            mob_center=self._mob_center,
            align_left=self._align_left,
            align_right=self._align_right,
            align_top=self._align_top,
            align_bottom=self._align_bottom,
            # -- font --
            font=self._font,
            text_color=self._text_color,
            weight=self._weight,
            # ---- pointers ----
            pointers=self._pointers,
            # ---- kwargs ----
            **self._parent_kwargs,
        )

        if self._anchor is not None:
            if self._direction[0] >= 0:
                left_idx = 0
                right_idx = -1
            else:
                left_idx = -1
                right_idx = 0

            if np.array_equal(self._anchor, mn.LEFT):
                self_left_node_center = self._containers_mob[left_idx].get_center()
                new_left_node_center = new_group._containers_mob[left_idx].get_center()
                shift_vector = self_left_node_center - new_left_node_center
                new_group.shift(shift_vector)

            elif np.array_equal(self._anchor, mn.RIGHT):
                self_right_node_center = self._containers_mob[right_idx].get_center()
                new_right_node_center = new_group._containers_mob[
                    right_idx
                ].get_center()
                shift_vector = self_right_node_center - new_right_node_center
                new_group.shift(shift_vector)

        # restore colors
        if new_value:
            highlight_status = self._save_highlights_states()
            self._preserve_highlights_states(new_group, highlight_status)

        # add
        if animate:
            scene.play(mn.Transform(self, new_group), run_time=run_time)
            self._update_internal_state(self.linked_list_to_list(new_value), new_group)
        else:
            scene.remove(self)
            self._update_internal_state(self.linked_list_to_list(new_value), new_group)
            scene.add(self)
