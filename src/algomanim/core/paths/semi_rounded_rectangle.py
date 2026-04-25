import manim as mn
import numpy as np

from manim import ManimColor


class SemiRoundedRectangle(mn.VMobject):
    """Rectangle with rounded corners on one side only.

    Creates a rectangle where only the corners on the specified direction
    are rounded.

    Args:
        width: width of the rectangle.
        height: height of the rectangle.
        direction: Which side gets rounded corners.
            Must be UP, DOWN, LEFT, or RIGHT.
        corner_radius: Radius of the rounded corners.
        fill_color: Fill color of the rectangle.
        stroke_color: Stroke color of the rectangle.
        stroke_width: Stroke width of the rectangle.
        **kwargs: Additional arguments passed to VMobject.
    """

    def __init__(
        self,
        width: float,
        height: float,
        direction: np.ndarray = mn.UP,
        corner_radius: float = 0.1,
        fill_color: ManimColor | str = mn.GRAY,
        stroke_color: ManimColor | str = mn.BLACK,
        stroke_width: float = 4,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._width = width
        self._height = height
        self._corner_radius = corner_radius
        self._fill_color = fill_color
        self._stroke_color = stroke_color
        self._stroke_width = stroke_width
        if not (
            np.array_equal(direction, mn.LEFT)
            or np.array_equal(direction, mn.RIGHT)
            or np.array_equal(direction, mn.UP)
            or np.array_equal(direction, mn.DOWN)
        ):
            raise ValueError(
                "direction must be one of: mn.LEFT, mn.RIGHT, mn.UP, mn.DOWN"
            )
        else:
            self._direction = direction

        path = self._build_path()
        self.add(path)

    def _build_path(self) -> mn.VMobject:
        """Build the rectangle path based on the specified direction.

        Returns:
            VMobject: Path object with rounded corners on the specified side.
        """

        if np.array_equal(self._direction, mn.UP):
            path = self._build_path_up()
        elif np.array_equal(self._direction, mn.DOWN):
            path = self._build_path_down()
        elif np.array_equal(self._direction, mn.LEFT):
            path = self._build_path_left()
        elif np.array_equal(self._direction, mn.RIGHT):
            path = self._build_path_right()
        else:
            raise ValueError("Invalid direction")

        path.set_fill(
            self._fill_color,
            opacity=1,
        )
        path.set_stroke(
            color=self._stroke_color,
            width=self._stroke_width,
        )

        path.move_to(mn.ORIGIN)

        return path

    def _build_path_up(self) -> mn.VMobject:
        """Build path for rectangle with rounded top corners.

        NB: Manim issue: ArcBetweenPoints: the 'angle' parameter has no effect;
            the path must be drawn exactly counterclockwise.

        Returns:
            VMobject: Path object with rounded top corners.
        """

        w = self._width
        h = self._height
        r = self._corner_radius
        angle = np.pi / 2

        path = mn.VMobject()

        path.set_points_as_corners(
            [
                np.array([0, 0, 0]),  # bottom left
                np.array([w, 0, 0]),  # bottom right
                np.array([w, h - r, 0]),  # top right
            ]
        )

        # top right rounded corner
        path.append_points(
            mn.ArcBetweenPoints(
                np.array([w, h - r, 0]),
                np.array([w - r, h, 0]),
                angle=angle,
                radius=r,
            ).points
        )

        path.add_line_to(np.array([0 + r, h, 0]))  # top side

        # top left rounded corner
        path.append_points(
            mn.ArcBetweenPoints(
                np.array([0 + r, h, 0]),
                np.array([0, h - r, 0]),
                angle=angle,
                radius=r,
            ).points
        )

        # auto form left side
        path.close_path()

        return path

    def _build_path_down(self) -> mn.VMobject:
        """Build path for rectangle with rounded bottom corners.

        NB: Manim issue: ArcBetweenPoints: the 'angle' parameter has no effect;
            the path must be drawn exactly counterclockwise.

        Returns:
            VMobject: Path object with rounded bottom corners.
        """

        w = self._width
        h = self._height
        r = self._corner_radius

        angle = np.pi / 2

        path = mn.VMobject()

        path.set_points_as_corners(
            [
                np.array([0, 0, 0]),  # top right
                np.array([-w, 0, 0]),  # top left
                np.array([-w, -h + r, 0]),  # bottom left
            ]
        )

        # bottom left rounded corner
        path.append_points(
            mn.ArcBetweenPoints(
                np.array([-w, -h + r, 0]),
                np.array([-w + r, -h, 0]),
                angle=angle,
                radius=r,
            ).points
        )

        path.add_line_to(np.array([0 - r, -h, 0]))  # bottom side

        # bottom right rounded corner
        path.append_points(
            mn.ArcBetweenPoints(
                np.array([0 - r, -h, 0]),
                np.array([0, -h + r, 0]),
                angle=angle,
                radius=r,
            ).points
        )

        # auto form right side
        path.close_path()

        return path

    def _build_path_left(self) -> mn.VMobject:
        """Build path for rectangle with rounded left corners.

        NB: Manim issue: ArcBetweenPoints: the 'angle' parameter has no effect;
            the path must be drawn exactly counterclockwise.

        Returns:
            VMobject: Path object with rounded left corners.
        """

        w = self._width
        h = self._height
        r = self._corner_radius
        angle = np.pi / 2

        path = mn.VMobject()

        path.set_points_as_corners(
            [
                np.array([0, 0, 0]),  # bottom right
                np.array([0, h, 0]),  # top right
                np.array([-w + r, h, 0]),  # top left
            ]
        )

        # top left rounded corner
        path.append_points(
            mn.ArcBetweenPoints(
                np.array([-w + r, h, 0]),
                np.array([-w, h - r, 0]),
                angle=angle,
                radius=r,
            ).points
        )

        path.add_line_to(np.array([-w, 0 + r, 0]))  # left side

        # top left rounded corner
        path.append_points(
            mn.ArcBetweenPoints(
                np.array([-w, 0 + r, 0]),
                np.array([-w + r, 0, 0]),
                angle=angle,
                radius=r,
            ).points
        )

        # auto form left side
        path.close_path()

        return path

    def _build_path_right(self) -> mn.VMobject:
        """Build path for rectangle with rounded right corners.

        NB: Manim issue: ArcBetweenPoints: the 'angle' parameter has no effect;
            the path must be drawn exactly counterclockwise.

        Returns:
            VMobject: Path object with rounded right corners.
        """

        w = self._width
        h = self._height
        r = self._corner_radius
        angle = np.pi / 2

        path = mn.VMobject()

        path.set_points_as_corners(
            [
                np.array([0, h, 0]),  # top left
                np.array([0, 0, 0]),  # bottom left
                np.array([w - r, 0, 0]),  # bottom right
            ]
        )

        # bottom right rounded corner
        path.append_points(
            mn.ArcBetweenPoints(
                np.array([w - r, 0, 0]),
                np.array([w, r, 0]),
                angle=angle,
                radius=r,
            ).points
        )

        path.add_line_to(np.array([w, h - r, 0]))  # right side

        # top right rounded corner
        path.append_points(
            mn.ArcBetweenPoints(
                np.array([w, h - r, 0]),
                np.array([w - r, h, 0]),
                angle=angle,
                radius=r,
            ).points
        )

        # auto form top side
        path.close_path()

        return path
