from typing import Literal

import numpy as np
import manim as mn
from manim import ManimColor

from algomanim.helpers.datastructures import ListNode
from algomanim.core.linear_container import LinearContainerStructure
from algomanim.assets.svg import SVG_DIR


class LinkedList(LinearContainerStructure):
    """
    ...
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
        align_edge: Literal["up", "down", "left", "right"] | None = None,
        # -- font --
        font="",
        font_color: ManimColor | str = mn.BLACK,
        weight: str = "NORMAL",
    ):
        super().__init__()
        self._data = self.linked_list_to_list(head)  # save head as list
        self._radius = radius
        self._direction = direction
        self._container_color = node_color
        self._fill_color = fill_color
        self._bg_color = bg_color
        self._vector = vector
        self._mob_center = mob_center
        self._align_edge = align_edge
        self._font = font
        self._font_color = font_color
        self._weight = weight
        self._color_123 = mn.WHITE
        self._color_containers_with_value = mn.WHITE

        # empty value
        if not self._data:
            self._empty_linked_list()
            return

        # nodes
        self._containers_mob = self._create_containers_mob()

        # arrows
        self._arrows_mob = self._create_and_pos_arrows_mob()

        # pointers
        self._pointers_top, self._pointers_bottom = self.create_pointers(
            self._containers_mob
        )

        # group all mobs
        self._frame_mob = self._create_frame_mob()

        # rotate frame
        self._rotate_frame()

        self._position(self._frame_mob, self._containers_mob[0])

        # values
        self._values_mob = self._create_and_pos_values_mob()

        # ---- add ------
        self.add(self._frame_mob, self._values_mob)

    def _empty_linked_list(self):
        """ """
        # clear old fields
        self._containers_mob = mn.VGroup()
        self._arrows_mob = mn.VGroup()
        self._pointers_top = mn.VGroup()
        self._pointers_bottom = mn.VGroup()
        self._frame_mob = mn.VGroup()
        self._values_mob = mn.VGroup()

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
        """
        ...
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
        """
        ...
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
        return mn.VGroup(
            self._containers_mob,
            self._arrows_mob,
            self._pointers_top,
            self._pointers_bottom,
        )

    def _rotate_frame(self) -> None:
        """
        ...
        """

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
            "color": self._font_color,
        }

    def _create_and_pos_values_mob(self):
        """
        ...
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

    def __update_internal_state(
        self,
        new_value,
        new_group: "LinkedList",
    ):
        """Update internal state with data from a new group.

        Args:
            new_value: New data value to store.
            new_group: New group to copy state from.
        """
        self._data = new_value
        self._containers_mob = new_group._containers_mob
        self._values_mob = new_group._values_mob
        self._pointers_top = new_group._pointers_top
        self._pointers_bottom = new_group._pointers_bottom
        self.submobjects = new_group.submobjects

    def update_value(
        self,
        scene: mn.Scene,
        new_value,
        animate: bool = False,
        run_time: float = 0.2,
    ) -> None:
        """
        ...
        """

        # checks
        if not self._data and not new_value:
            return

        # save old group status
        highlight_status = self._save_highlights_states()

        # new group
        new_group = LinkedList(
            new_value,
            font=self._font,
            direction=self._direction,
            mob_center=self._mob_center,
            align_edge=self._align_edge,
            vector=self._vector,
        )

        # restore colors
        self._preserve_highlights_states(new_group, highlight_status)

        # add
        if animate:
            scene.play(mn.Transform(self, new_group), run_time=run_time)
            self.__update_internal_state(self.linked_list_to_list(new_value), new_group)
        else:
            scene.remove(self)
            self.__update_internal_state(self.linked_list_to_list(new_value), new_group)
            scene.add(self)
