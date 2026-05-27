import pytest
import manim as mn
from algomanim.core.linear_container import LinearContainerStructure
from algomanim.core.linear_container import Colors

blend = LinearContainerStructure._blend_colors_algo


color_1 = Colors.color_1  # mn.RED  #FC6255
color_2 = Colors.color_2  # mn.BLUE  #58C4DD
color_3 = Colors.color_3  # mn.GREEN  #83C167
color_4 = Colors.color_4  # mn.PINK  #D147BD
color_5 = Colors.color_5  # mn.LOGO_BLUE  #525893
color_6 = Colors.color_6  # mn.GREEN_E  #699C52

color_12 = "#AA9399"
color_13 = "#C0925E"
color_14 = "#E75589"
color_15 = "#A75D74"
color_16 = "#B37F54"
color_23 = "#6EC3A2"
color_24 = "#9586CD"
color_25 = "#558EB8"
color_26 = "#61B098"
color_34 = "#AA8492"
color_35 = "#6B8D7D"
color_36 = "#76AF5D"
color_45 = "#9250A8"
color_46 = "#9D7288"
color_56 = "#5E7A73"


def test_12():
    assert blend(color_1, color_2) == color_12


def test_12_manim():
    assert blend(mn.RED, mn.BLUE) == color_12


def test_13():
    assert blend(color_1, color_3) == color_13


def test_14():
    assert blend(color_1, color_4) == color_14


def test_15():
    assert blend(color_1, color_5) == color_15


def test_16():
    assert blend(color_1, color_6) == color_16


def test_23():
    assert blend(color_2, color_3) == color_23


def test_24():
    assert blend(color_2, color_4) == color_24


def test_25():
    assert blend(color_2, color_5) == color_25


def test_26():
    assert blend(color_2, color_6) == color_26


def test_34():
    assert blend(color_3, color_4) == color_34


def test_35():
    assert blend(color_3, color_5) == color_35


def test_36():
    assert blend(color_3, color_6) == color_36


def test_45():
    assert blend(color_4, color_5) == color_45


def test_46():
    assert blend(color_4, color_6) == color_46


def test_56():
    assert blend(color_5, color_6) == color_56


def test_mix_red_green():
    assert blend("#FF0000", "#00FF00") == "#808000"


def test_mix_red_blue():
    assert blend("#FF0000", "#0000FF") == "#800080"


def test_mix_green_blue():
    assert blend("#00FF00", "#0000FF") == "#008080"


def test_mix_red_white():
    assert blend("#FF0000", "#FFFFFF") == "#FF8080"


def test_mix_blue_white():
    assert blend("#0000FF", "#FFFFFF") == "#8080FF"


def test_mix_red_black():
    assert blend("#FF0000", "#000000") == "#800000"


def test_mix_yellow_blue():
    assert blend("#FFFF00", "#0000FF") == "#808080"


def test_mix_red_green_blue():
    assert blend("#FF0000", "#00FF00", "#0000FF") == "#555555"


def test_mix_red_yellow_blue():
    assert blend("#FF0000", "#FFFF00", "#0000FF") == "#AA5555"


def test_mix_white_black_red():
    assert blend("#FFFFFF", "#000000", "#FF0000") == "#AA5555"


def test_mix_4_colors():
    assert blend("#FF0000", "#00FF00", "#0000FF", "#FFFFFF") == "#808080"


def test_mix_6_colors():
    colors = ["#FF0000", "#FFA500", "#FFFF00", "#00FF00", "#0000FF", "#800080"]
    assert blend(*colors) == "#957140"


if __name__ == "__main__":
    pytest.main()
