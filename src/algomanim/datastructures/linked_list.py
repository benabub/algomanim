from typing import Any, Callable, Literal, cast

import numpy as np
import manim as mn
from manim import ManimColor

from algomanim.helpers.datastructures import ListNode
from algomanim.core.linear_container import LinearContainerStructure
from algomanim.core.node_structure import NodeStructure
from algomanim.assets.svg import SVG_DIR


class LinkedList(LinearContainerStructure, NodeStructure):
    """Linked list visualization as a VGroup of nodes with values and pointers.

    Args:
        value: Callable that returns a head node of the linked list to visualize.
        radius: Radius of the circular nodes.
        direction: Direction vector for list orientation.
        node_color: Border color for nodes.
        fill_color: Fill color for nodes.
        bg_color: Background color of scene and default pointer color.
        vector: Position offset from mob_center.
        mob_center: Reference mobject for positioning.
        align_left: Reference mobject to align left edge with.
        align_right: Reference mobject to align right edge with.
        align_top: Reference mobject to align top edge with.
        align_bottom: Reference mobject to align bottom edge with.
        align_screen: Direction vector for screen edge alignment.
        screen_buff: Buffer distance from screen edge when using align_screen.
        anchor: Alignment anchor when no edge alignment specified.
        font: Font family for text elements.
        text_color: Color for text elements.
        weight: Font weight (NORMAL, BOLD, etc.).
        pointers: Which pointers to create ("top", "bottom", "both" or None).
        **kwargs: Additional keyword arguments passed to parent class.
    """

    def __init__(
        self,
        value: Callable[[], ListNode | None] | None,
        radius: float = 0.4,
        # ---- direction ----
        direction: np.ndarray = mn.RIGHT,
        # ---- pointers ----
        pointers: Literal["top", "bottom", "both"] | None = "top",
        pointers_mode: Literal[3, 5] = 3,
        # -- position --
        vector: np.ndarray = mn.ORIGIN,
        mob_center: mn.Mobject = mn.Dot(mn.ORIGIN),
        align_left: mn.Mobject | None = None,
        align_right: mn.Mobject | None = None,
        align_top: mn.Mobject | None = None,
        align_bottom: mn.Mobject | None = None,
        align_screen: np.ndarray | None = None,
        screen_buff: float = 0.2,
        anchor: Literal["start", "end"] | None = "start",
        # -- font --
        font: str = "",
        text_color: ManimColor | str = mn.BLACK,
        weight: str = "NORMAL",
        # --- node colors ---
        node_color: ManimColor | str = mn.BLACK,
        fill_color: ManimColor | str = mn.LIGHT_GRAY,
        bg_color: ManimColor | str = mn.DARK_GRAY,
        # ---- kwargs ----
        **kwargs,
    ):
        kwargs.setdefault("color_mix_6", mn.WHITE)
        kwargs.setdefault("color_containers_with_value", mn.RED)
        self._parent_kwargs = kwargs.copy()

        super().__init__(
            # ---- pointers ----
            pointers=pointers,
            pointers_mode=pointers_mode,
            # ---- containers ----
            container_color=node_color,
            fill_color=fill_color,
            bg_color=bg_color,
            # ---- position ----
            vector=vector,
            mob_center=mob_center,
            align_left=align_left,
            align_right=align_right,
            align_top=align_top,
            align_bottom=align_bottom,
            align_screen=align_screen,
            screen_buff=screen_buff,
            # ---- font ----
            font=font,
            text_color=text_color,
            weight=weight,
            # ---- kwargs ----
            **kwargs,
        )

        # create class instance fields
        self._callable = value

        if value is not None:
            self._data = self.linked_list_to_list(value())
        else:
            self._data = []

        self._radius = radius
        # ---- direction ----
        self._direction = direction
        # --- node colors ---
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
        self._pointers_mode: Literal[3, 5] = pointers_mode
        # ---- anchor ----
        if not (align_left or align_right) and anchor is not None:
            if anchor not in ["start", "end"]:
                raise ValueError("anchor must be 'start', 'end' or None")
            self._anchor = anchor
        else:
            self._anchor: Literal["start", "end"] | None = None
        # ---- spacing ----
        self.node_width = self._radius * 2
        self.node_arrow_width = self._radius * 3

        # =-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=

        # empty value
        if not self._data:
            self._create_empty_linked_list()
            return

        # nodes
        self._containers_mob = self._create_nodes_mob()

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

        self.set_pointers(
            self._containers_mob,
            self._direction,
        )

        # values
        self._values_mob = self._create_and_pos_values_mob()
        self.add(self._values_mob)

    def _create_empty_linked_list(self) -> None:
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

    def _create_nodes_mob(self) -> mn.VGroup:
        """Create circular node mobjects for the linked list.

        Returns:
            mn.VGroup: Group of circular node mobjects.
        """

        node = self._create_single_node()
        nodes_mob = mn.VGroup(*[node.copy() for _ in range(len(self._data))])
        nodes_mob.arrange(buff=self._radius)

        return nodes_mob

    def _create_and_pos_arrows_mob(self) -> mn.VGroup:
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

    def _create_frame_mob(self) -> mn.VGroup:
        """Create frame mobject containing all linked list elements.

        Returns:
            mn.VGroup: Group containing containers, arrows, and pointers.
        """
        if self._pointers == "top" and self._pointers_top is not None:
            return mn.VGroup(
                self._containers_mob,
                self._arrows_mob,
                self._pointers_top,
            )
        elif self._pointers == "bottom" and self._pointers_bottom is not None:
            return mn.VGroup(
                self._containers_mob,
                self._arrows_mob,
                self._pointers_bottom,
            )
        elif (
            self._pointers == "both"
            and self._pointers_top is not None
            and self._pointers_bottom is not None
        ):
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

    def _text_config(self) -> dict:
        return NodeStructure._text_config(self)

    def _create_and_pos_values_mob(self):
        """Create and position value text mobjects inside nodes.

        Returns:
            mn.VGroup: Group of value text mobjects positioned within nodes.
        """
        self._assign_base_font_size()
        font_size = cast(float, self._base_font_size)

        values_mob = mn.VGroup(
            *[
                mn.Text(str(val), font_size=font_size, **self._text_config())
                for val in self._data
            ]
        )

        for i in range(len(self._data)):
            val = str(self._data[i])
            mob = cast(mn.Text, values_mob[i])
            node = cast(mn.Circle, self._containers_mob[i])

            self._position_value_in_node(mob, str(val), node)

        return values_mob

    def _create_new_instance(self) -> "LinkedList":
        """Create a new LinkedList instance with current parameters and updated data.

        Returns:
            New LinkedList instance with the same configuration and fresh data from callable.
        """
        # create new instance
        new_instance = LinkedList(
            value=self._callable,
            radius=self._radius,
            # ---- direction ----
            direction=self._direction,
            # ---- pointers ----
            pointers=self._pointers,
            pointers_mode=self._pointers_mode,
            # -- position --
            vector=self._vector,
            mob_center=self._mob_center,
            align_left=self._align_left,
            align_right=self._align_right,
            align_top=self._align_top,
            align_bottom=self._align_bottom,
            align_screen=self._align_screen,
            screen_buff=self._screen_buff,
            # -- font --
            font=self._font,
            text_color=self._text_color,
            weight=self._weight,
            # --- nodes colors ---
            node_color=self._node_color,
            fill_color=self._fill_color,
            bg_color=self._bg_color,
            # ---- kwargs ----
            **self._parent_kwargs,
        )

        new_instance._base_font_size = self._base_font_size

        if self._anchor is not None:
            left_idx = 0
            right_idx = -1

            if self._anchor == "start":
                self_left_node_center = self._containers_mob[left_idx].get_center()
                new_left_node_center = new_instance._containers_mob[
                    left_idx
                ].get_center()
                shift_vector = self_left_node_center - new_left_node_center
                new_instance.shift(shift_vector)

            if self._anchor == "end":
                self_right_node_center = self._containers_mob[right_idx].get_center()
                new_right_node_center = new_instance._containers_mob[
                    right_idx
                ].get_center()
                shift_vector = self_right_node_center - new_right_node_center
                new_instance.shift(shift_vector)

        # preserve highlights
        highlight_status = self._save_highlights_states()
        if new_instance._data:
            self._preserve_highlights_states(new_instance, highlight_status)

        return new_instance

    def _update_internal_state(
        self,
        new_instance: "LinkedList",
    ) -> None:
        """Update the current instance with data from a new instance.

        Copies data, mobject references, and highlight states from the new instance.
        Highlights are preserved and reapplied to the updated containers.

        Args:
            new_instance: The instance to copy state from.
        """
        # save highlight rules before overwriting state
        old_containers_colors = (
            self._containers_colors.copy()
            if hasattr(self, "_containers_colors")
            else {}
        )
        old_top_colors = (
            self._top_pointers_colors.copy()
            if hasattr(self, "_top_pointers_colors")
            else {}
        )
        old_bottom_colors = (
            self._bottom_pointers_colors.copy()
            if hasattr(self, "_bottom_pointers_colors")
            else {}
        )

        # sync raw data and closures
        self._data = new_instance._data.copy()
        self._callable = new_instance._callable

        # transfer references to sub-mobject groups
        if hasattr(new_instance, "_containers_mob"):
            self._containers_mob = new_instance._containers_mob
        if hasattr(new_instance, "_arrows_mob"):
            self._arrows_mob = new_instance._arrows_mob
        if hasattr(new_instance, "_values_mob"):
            self._values_mob = new_instance._values_mob
        if hasattr(new_instance, "_pointers_top"):
            self._pointers_top = new_instance._pointers_top
        if hasattr(new_instance, "_pointers_bottom"):
            self._pointers_bottom = new_instance._pointers_bottom

        # restore and apply highlights
        self._containers_colors = old_containers_colors
        self._top_pointers_colors = old_top_colors
        self._bottom_pointers_colors = old_bottom_colors

        if self._data:
            self._apply_containers_colors()
            if hasattr(self, "_pointers") and self._pointers:
                self._apply_pointers_colors(0)
                self._apply_pointers_colors(1)

        # sync pure geometry hierarchy
        self.submobjects = new_instance.submobjects.copy()

    def _set_new_value(self) -> None:
        """Update internal data from callable without scene animation.

        Replaces the current instance with a newly created one if the data has changed.
        Preserves highlights and alignment. Does not add to scene.
        """
        new_instance = self._create_new_instance()
        self._update_internal_state(new_instance)

    def update_value(
        self,
        scene: mn.Scene,
        animate: bool = True,
        update_time: float = 0.2,
    ) -> None:
        """Replace the linked list visualization with new nodes.

        Args:
            scene: The Manim scene to play animations in.
            animate: If True, plays a fade transition. If False, updates instantly.
            update_time: Duration of the fade transition if animate=True.
        """
        new_instance = self._create_new_instance()

        if animate:
            scene.play(
                mn.FadeOut(self),
                mn.FadeIn(new_instance),
                run_time=update_time,
            )

        scene.remove(self)
        scene.remove(new_instance)

        self._update_internal_state(new_instance)

        scene.add(self)
        self._clear_scene(scene)

    def append(
        self,
        scene: mn.Scene,
        tail: "LinkedList",
        animate: bool = False,
        update_time: float = 0.2,
    ) -> None:
        """Append another linked list to the end of this one in the scene.

        Args:
            scene: The Manim scene to play animations in.
            tail: Linked list to append.
            animate: Whether to animate the transition.
            update_time: Animation duration if animate=True.
        """
        if not tail._data:
            return

        self._data = self._data + tail._data

        # Capture current data snapshot to avoid closure bug
        current_data = self._data.copy()
        self._callable = lambda: LinkedList.create_linked_list(current_data)

        new_instance = self._create_new_instance()
        scene.remove(tail)

        if animate:
            scene.play(
                mn.FadeOut(self),
                mn.FadeIn(new_instance),
                run_time=update_time,
            )

        scene.remove(self)
        scene.remove(new_instance)

        self._update_internal_state(new_instance)

        scene.add(self)
        self._clear_scene(scene)

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
    def get_node_index(head: ListNode | None, target: ListNode | None) -> int | None:
        """
        Find the index of target node in linked list starting from head.

        Args:
            head: Head node of the linked list.
            target: Node to find (must be same object reference).

        Returns:
            Zero-based index of target node, or None if not found.
        """

        current = head
        i = 0

        while current:
            if current is target:
                return i
            i += 1
            current = current.next

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
