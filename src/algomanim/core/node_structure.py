import manim as mn
from manim import ManimColor
from .base import AlgoManimBase


class NodeStructure(AlgoManimBase):
    """Base class for node-based data structures.

    Provides common functionality for visualizing node-based structures
    like linked lists, trees, etc.

    Args:
        radius: Radius of circular nodes.
        node_color: Border color for nodes.
        fill_color: Fill color for nodes.
        bg_color: Background color for nodes.
        font: Font family for text elements.
        text_color: Color for text elements.
        weight: Font weight (NORMAL, BOLD, etc.).
        **kwargs: Additional keyword arguments passed to parent class.
    """

    def __init__(
        self,
        radius: float = 0.4,
        # --- nodes colors ---
        node_color: ManimColor | str = mn.BLACK,
        fill_color: ManimColor | str = mn.LIGHT_GRAY,
        bg_color: ManimColor | str = mn.DARK_GRAY,
        # -- font --
        font: str = "",
        text_color: ManimColor | str = mn.BLACK,
        weight: str = "NORMAL",
        # ---- kwargs ----
        **kwargs,
    ):
        super().__init__(**kwargs)

        self._radius = radius
        # --- node colors ---
        self._node_color = node_color
        self._fill_color = fill_color
        self._bg_color = bg_color
        # -- font --
        self._font = font
        self._text_color = text_color
        self._weight = weight
        # ---- base font size ----
        self._base_font_size = None

    def _create_single_node(self) -> mn.Circle:
        """Create a single circular node mobject.

        Returns:
            Circle mobject with configured radius, colors and stroke.
        """

        return mn.Circle(
            radius=self._radius,
            color=self._node_color,
            fill_color=self._fill_color,
            fill_opacity=1,
            stroke_width=self._radius * 7,
        )

    def _text_config(self) -> dict:
        """Get text configuration dictionary for node labels.

        Returns:
            Dictionary with font, weight and color settings.
        """
        return {
            "font": self._font,
            "weight": self._weight,
            "color": self._text_color,
        }

    def _get_base_font_size(self) -> int:
        """Calculate optimal font size for node text based on radius.

        Returns:
            Font size that fits within the node.
        """
        top_bottom_buff = self._radius / 2
        max_size_test = (self._radius - top_bottom_buff) * 2

        base_font_size = 10
        test_mob = mn.Text("0", font_size=base_font_size)
        while test_mob.height < max_size_test:
            base_font_size += 1
            test_mob = mn.Text("0", font_size=base_font_size)

        return base_font_size

    def _assign_base_font_size(self) -> None:
        """Assign base font size if not already set.

        Computes and stores the optimal font size for node text.
        """
        if self._base_font_size is None:
            self._base_font_size = self._get_base_font_size()

    def _get_node_text_params(self) -> dict:
        """Get node text positioning parameters.

        Returns:
            Dictionary with top_bottom_buff, ypgj_shift,
            max_size_center and max_size_shift values.
        """
        top_bottom_buff = self._radius / 2
        ypgj_shift = self._radius / 16
        max_size_center = (self._radius - top_bottom_buff) * 2.5
        max_size_shift = (self._radius - top_bottom_buff) * 2.2

        return {
            "top_bottom_buff": top_bottom_buff,
            "ypgj_shift": ypgj_shift,
            "max_size_center": max_size_center,
            "max_size_shift": max_size_shift,
        }

    def _position_value_in_node(
        self,
        mob: mn.Text,
        value: str,
        node: mn.Circle,
    ) -> None:
        """Position a text mobject inside a node with proper alignment.

        Args:
            mob: Text mobject to position.
            value: String value to position (for alignment logic).
            node: Target node to position text within.
        """
        params = self._get_node_text_params()

        val_set = set(value)
        width = mob.width

        # Single digit -> center
        if len(value) == 1 and value in "0123456789":
            mob.move_to(node)
            return

        # Top alignment (quotes and accents)
        if val_set.issubset({'"', "'", "^", "`"}):
            if width > params["max_size_shift"]:
                mob.scale_to_fit_width(params["max_size_shift"])
            mob.next_to(
                node.get_top(), direction=mn.DOWN, buff=params["top_bottom_buff"]
            )
            return

        # Deep bottom alignment (descenders)
        if val_set.issubset({"y", "p", "g", "j"}):
            if width > params["max_size_center"]:
                mob.scale_to_fit_width(params["max_size_center"])
            mob.move_to(node)
            mob.shift(mn.DOWN * params["ypgj_shift"])
            return

        # Bottom alignment (punctuation)
        if val_set.issubset({".", ",", "_"}):
            if width > params["max_size_shift"]:
                mob.scale_to_fit_width(params["max_size_shift"])
            mob.next_to(
                node.get_bottom(), direction=mn.UP, buff=params["top_bottom_buff"]
            )
            return

        # Default: center with size constraint
        if width > params["max_size_center"]:
            mob.scale_to_fit_width(params["max_size_center"])
        mob.move_to(node)
