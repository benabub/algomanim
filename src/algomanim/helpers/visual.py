import manim as mn


def grid(
    scene: mn.Scene,
    lines_color: mn.ManimColor | str = mn.WHITE,
):
    """Draw a coordinate grid and origin dot on the scene.

    Creates a grid spanning the standard Manim frame:
    - Horizontal lines from y = -4 to y = 4
    - Vertical lines from x = -7 to x = 7
    - Places a red dot at the origin (0, 0)

    Args:
        scene: The Manim scene to add the grid to.
        lines_color: Color of the grid lines. Defaults to WHITE.
    """
    for x in range(-7, 8):
        line = mn.Line(
            start=mn.RIGHT * x + mn.UP * 4,
            end=mn.RIGHT * x + mn.DOWN * 4,
            color=lines_color,
            stroke_width=1,
        )
        scene.add(line)

    for y in range(-4, 5):
        line = mn.Line(
            start=mn.LEFT * 7 + mn.UP * y,
            end=mn.RIGHT * 7 + mn.UP * y,
            color=lines_color,
            stroke_width=1,
        )
        scene.add(line)

    central_dot = mn.Dot(color=mn.RED)
    scene.add(central_dot)
