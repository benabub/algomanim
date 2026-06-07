import manim as mn


class HLRect(mn.VGroup):
    """Highlight rectangle with blurred edges effect.

    Creates a layered rounded rectangle stack where lower layers are larger
    and more opaque, creating a glow effect around the central mobject.

    Args:
        central_mob: The mobject to highlight (used for dimensions only).
        hl_color: Color for the activated highlight state.
        bg_color: Base color for the deactivated state.
        corner_radius: Corner radius for all layers.
        layers: Number of stacked rectangles.
        max_opacity: Maximum opacity of the bottom layer.
        max_size_increase: Maximum size increase factor for the bottom layer.
    """

    def __init__(
        self,
        central_mob: mn.Mobject,
        hl_color: mn.ManimColor | str,
        bg_color: mn.ManimColor | str = mn.DARK_GRAY,
        corner_radius: float = 0.1,
        layers: int = 10,
        inner_buff: float = 0.0,
        dim_zone: float = 0.2,
        min_opacity: float = 0.1,
    ):
        super().__init__()
        self._central_mob = central_mob
        self._bg_color = bg_color
        self._hl_color = hl_color
        self._corner_radius = corner_radius
        self._layers = layers
        self._inner_buff = inner_buff
        self._dim_zone = dim_zone
        self._min_opacity = min_opacity

        if isinstance(central_mob, mn.Text) and central_mob.text == '""':
            self._empty_str = True
        else:
            self._empty_str = False

        self.add(self._build_hl_rect())

    def _build_hl_rect(self):
        """Build the layered rectangle stack.

        For empty string text (`""`), adjusts height and shifts rectangles
        to properly align with the quoted text.

        Returns:
            VGroup containing all rectangle layers.
        """
        delta = self._dim_zone * 2
        width = self._central_mob.width + self._inner_buff * 2
        height = self._central_mob.height + self._inner_buff * 2
        if self._empty_str:
            height *= 3

        size_step = delta / self._layers
        opacity_step = (1 - self._min_opacity) / (self._layers - 1)

        layers = []

        for i in range(self._layers):
            opacity = 1 - (i * opacity_step)

            rect = mn.RoundedRectangle(
                width=width + (i * size_step),
                height=height + (i * size_step),
                corner_radius=self._corner_radius,
                fill_color=self._hl_color,
                fill_opacity=opacity,
                stroke_width=0,
            )
            rect.move_to(self._central_mob)
            if self._empty_str:
                rect.shift(mn.DOWN * height * 0.5)
            layers.append(rect)

        hl_rect = mn.VGroup(*layers)
        return hl_rect

    def activate(self) -> None:
        """Activate highlight by setting all layers to hl_color."""
        for rect in self:
            rect.set_fill(self._hl_color)

    def deactivate(self) -> None:
        """Deactivate highlight by resetting all layers to bg_color."""
        for rect in self:
            rect.set_fill(self._bg_color)
