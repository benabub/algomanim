import pytest  # type: ignore
from algomanim.algomanim import Array, TopText, CodeBlock, TitleTop  # type: ignore
import manim as mn  # type: ignore
from unittest.mock import Mock, patch


class TestArray:
    @pytest.fixture
    def array_obj(self):
        arr = [1, 2, 3]
        mob_center = mn.Dot(mn.ORIGIN)
        vector = mn.ORIGIN
        return Array(arr, vector, mob_center=mob_center)

    def test_init(self, array_obj):
        assert array_obj.arr == [1, 2, 3]
        assert len(array_obj.sq_mob) == 3
        assert len(array_obj.num_mob) == 3
        assert len(array_obj.pointers) == 2
        assert len(array_obj.pointers[0]) == 3
        assert len(array_obj.pointers[1]) == 3
        assert array_obj.bg_color == mn.DARK_GRAY
        assert array_obj.num_mob[0].text == "1"
        assert array_obj.num_mob[1].text == "2"
        assert array_obj.num_mob[2].text == "3"
        assert array_obj.sq_mob[0].get_center()[0] < array_obj.sq_mob[1].get_center()[0]
        assert array_obj.sq_mob[1].get_center()[0] < array_obj.sq_mob[2].get_center()[0]
        assert array_obj.sq_mob[0].fill_color == mn.DARK_GRAY

    def test_pointer_special_highlights_correct_indices(self, array_obj):
        for pointer_group in array_obj.pointers[0]:
            pointer_group[1].set_color = Mock()

        array_obj.pointer_special(2, pos=0, pnt_color=mn.RED)

        array_obj.pointers[0][0][1].set_color.assert_called_with(array_obj.bg_color)
        array_obj.pointers[0][1][1].set_color.assert_called_with(mn.RED)
        array_obj.pointers[0][2][1].set_color.assert_called_with(array_obj.bg_color)

    def test_pointer_special_bottom_position(self, array_obj):
        for pointer_group in array_obj.pointers[1]:
            pointer_group[1].set_color = Mock()

        array_obj.pointer_special(3, pos=1, pnt_color=mn.BLUE)

        array_obj.pointers[1][0][1].set_color.assert_called_with(array_obj.bg_color)
        array_obj.pointers[1][1][1].set_color.assert_called_with(array_obj.bg_color)
        array_obj.pointers[1][2][1].set_color.assert_called_with(mn.BLUE)

    def test_pointer_special_default_parameters(self, array_obj):
        for pointer_group in array_obj.pointers[1]:
            pointer_group[1].set_color = Mock()

        array_obj.pointer_special(1)

        array_obj.pointers[1][0][1].set_color.assert_called_with(mn.WHITE)
        array_obj.pointers[1][1][1].set_color.assert_called_with(array_obj.bg_color)
        array_obj.pointers[1][2][1].set_color.assert_called_with(array_obj.bg_color)

    def test_pointers_1(self, array_obj):
        array_obj.pointers_1(1, pos=0, i_color=mn.GREEN)
        for idx in range(3):
            expected = mn.GREEN if idx == 1 else array_obj.bg_color
            assert array_obj.pointers[0][idx][1].color == expected

    def test_pointers_2(self, array_obj):
        array_obj.pointers_2(0, 2, pos=0, i_color=mn.RED, j_color=mn.BLUE)
        for idx in range(3):
            if idx == 0:
                assert array_obj.pointers[0][idx][1].color == mn.RED
            elif idx == 2:
                assert array_obj.pointers[0][idx][1].color == mn.BLUE
            else:
                assert array_obj.pointers[0][idx][1].color == array_obj.bg_color

        array_obj.pointers_2(1, 1, pos=0, i_color=mn.RED, j_color=mn.BLUE)
        for idx in range(3):
            if idx == 1:
                assert array_obj.pointers[0][idx][0].color == mn.RED
                assert array_obj.pointers[0][idx][1].color == array_obj.bg_color
                assert array_obj.pointers[0][idx][2].color == mn.BLUE
            else:
                for tri_idx in range(3):
                    assert (
                        array_obj.pointers[0][idx][tri_idx].color == array_obj.bg_color
                    )

        array_obj.pointers_2(0, 1, pos=1, i_color=mn.YELLOW, j_color=mn.PURPLE)
        for idx in range(3):
            if idx == 0:
                assert array_obj.pointers[1][idx][1].color == mn.YELLOW
            elif idx == 1:
                assert array_obj.pointers[1][idx][1].color == mn.PURPLE
            else:
                assert array_obj.pointers[1][idx][1].color == array_obj.bg_color

        with pytest.raises(ValueError, match="pos must be 0 .top. or 1 .bottom."):
            array_obj.pointers_2(0, 1, pos=2)

    def test_pointers_3(self, array_obj):
        array_obj.pointers_3(
            0, 1, 2, pos=0, i_color=mn.RED, j_color=mn.GREEN, k_color=mn.BLUE
        )
        for idx in range(3):
            if idx == 0:
                assert array_obj.pointers[0][idx][1].color == mn.RED
            elif idx == 1:
                assert array_obj.pointers[0][idx][1].color == mn.GREEN
            elif idx == 2:
                assert array_obj.pointers[0][idx][1].color == mn.BLUE
            else:
                assert array_obj.pointers[0][idx][1].color == array_obj.bg_color

        array_obj.pointers_3(
            1, 1, 2, pos=0, i_color=mn.RED, j_color=mn.GREEN, k_color=mn.BLUE
        )
        for idx in range(3):
            if idx == 1:
                assert array_obj.pointers[0][idx][0].color == mn.RED
                assert array_obj.pointers[0][idx][1].color == array_obj.bg_color
                assert array_obj.pointers[0][idx][2].color == mn.GREEN
            elif idx == 2:
                assert array_obj.pointers[0][idx][1].color == mn.BLUE
            else:
                for tri_idx in range(3):
                    assert (
                        array_obj.pointers[0][idx][tri_idx].color == array_obj.bg_color
                    )

        array_obj.pointers_3(
            0, 0, 0, pos=0, i_color=mn.RED, j_color=mn.GREEN, k_color=mn.BLUE
        )
        for idx in range(3):
            if idx == 0:
                assert array_obj.pointers[0][idx][0].color == mn.RED
                assert array_obj.pointers[0][idx][1].color == mn.GREEN
                assert array_obj.pointers[0][idx][2].color == mn.BLUE
            else:
                for tri_idx in range(3):
                    assert (
                        array_obj.pointers[0][idx][tri_idx].color == array_obj.bg_color
                    )

        array_obj.pointers_3(
            0, 2, 2, pos=1, i_color=mn.RED, j_color=mn.GREEN, k_color=mn.BLUE
        )
        for idx in range(3):
            if idx == 0:
                assert array_obj.pointers[1][idx][1].color == mn.RED
            elif idx == 2:
                assert array_obj.pointers[1][idx][0].color == mn.GREEN
                assert array_obj.pointers[1][idx][1].color == array_obj.bg_color
                assert array_obj.pointers[1][idx][2].color == mn.BLUE
            else:
                for tri_idx in range(3):
                    assert (
                        array_obj.pointers[1][idx][tri_idx].color == array_obj.bg_color
                    )

        array_obj.pointers_3(
            1, 0, 1, pos=0, i_color=mn.RED, j_color=mn.GREEN, k_color=mn.BLUE
        )
        for idx in range(3):
            if idx == 0:
                assert array_obj.pointers[0][idx][1].color == mn.GREEN
            elif idx == 1:
                assert array_obj.pointers[0][idx][0].color == mn.RED
                assert array_obj.pointers[0][idx][1].color == array_obj.bg_color
                assert array_obj.pointers[0][idx][2].color == mn.BLUE
            else:
                for tri_idx in range(3):
                    assert (
                        array_obj.pointers[0][idx][tri_idx].color == array_obj.bg_color
                    )

    def test_highlight_blocks_1(self, array_obj):
        array_obj.highlight_blocks_1(1, i_color=mn.GREEN)

        for idx, square in enumerate(array_obj.sq_mob):
            expected = mn.GREEN if idx == 1 else array_obj.bg_color
            assert square.fill_color == expected

        array_obj.highlight_blocks_1(0, i_color=mn.RED)
        assert array_obj.sq_mob[0].fill_color == mn.RED
        assert array_obj.sq_mob[1].fill_color == array_obj.bg_color
        assert array_obj.sq_mob[2].fill_color == array_obj.bg_color

    def test_highlight_blocks_2(self, array_obj):
        array_obj.highlight_blocks_2(0, 2, i_color=mn.RED, j_color=mn.BLUE)
        assert array_obj.sq_mob[0].fill_color == mn.RED
        assert array_obj.sq_mob[1].fill_color == array_obj.bg_color
        assert array_obj.sq_mob[2].fill_color == mn.BLUE

        array_obj.highlight_blocks_2(
            1, 1, i_color=mn.RED, j_color=mn.BLUE, ij_color=mn.PURPLE
        )
        assert array_obj.sq_mob[0].fill_color == array_obj.bg_color
        assert array_obj.sq_mob[1].fill_color == mn.PURPLE
        assert array_obj.sq_mob[2].fill_color == array_obj.bg_color

        array_obj.highlight_blocks_2(
            0, 1, i_color=mn.YELLOW, j_color=mn.ORANGE, ij_color=mn.PINK
        )
        assert array_obj.sq_mob[0].fill_color == mn.YELLOW
        assert array_obj.sq_mob[1].fill_color == mn.ORANGE
        assert array_obj.sq_mob[2].fill_color == array_obj.bg_color

    def test_highlight_blocks_3(self, array_obj):
        array_obj.highlight_blocks_3(
            0, 1, 2, i_color=mn.RED, j_color=mn.GREEN, k_color=mn.BLUE
        )
        assert array_obj.sq_mob[0].fill_color == mn.RED
        assert array_obj.sq_mob[1].fill_color == mn.GREEN
        assert array_obj.sq_mob[2].fill_color == mn.BLUE

        array_obj.highlight_blocks_3(
            1,
            1,
            2,
            i_color=mn.RED,
            j_color=mn.GREEN,
            k_color=mn.BLUE,
            ij_color=mn.YELLOW,
        )
        assert array_obj.sq_mob[0].fill_color == array_obj.bg_color
        assert array_obj.sq_mob[1].fill_color == mn.YELLOW
        assert array_obj.sq_mob[2].fill_color == mn.BLUE

        array_obj.highlight_blocks_3(
            0,
            0,
            0,
            i_color=mn.RED,
            j_color=mn.GREEN,
            k_color=mn.BLUE,
            ijk_color=mn.BLACK,
        )
        assert array_obj.sq_mob[0].fill_color == mn.BLACK
        assert array_obj.sq_mob[1].fill_color == array_obj.bg_color
        assert array_obj.sq_mob[2].fill_color == array_obj.bg_color

        array_obj.highlight_blocks_3(
            0, 2, 2, i_color=mn.RED, j_color=mn.GREEN, k_color=mn.BLUE, jk_color=mn.TEAL
        )
        assert array_obj.sq_mob[0].fill_color == mn.RED
        assert array_obj.sq_mob[1].fill_color == array_obj.bg_color
        assert array_obj.sq_mob[2].fill_color == mn.TEAL

        array_obj.highlight_blocks_3(
            1,
            0,
            1,
            i_color=mn.RED,
            j_color=mn.GREEN,
            k_color=mn.BLUE,
            ik_color=mn.PURPLE,
        )
        assert array_obj.sq_mob[0].fill_color == mn.GREEN
        assert array_obj.sq_mob[1].fill_color == mn.PURPLE
        assert array_obj.sq_mob[2].fill_color == array_obj.bg_color


class TestTopText:
    @pytest.fixture
    def toptext_obj(self):
        mob_center = mn.Dot(mn.ORIGIN)
        var1 = ("a", lambda: 5, mn.RED)
        var2 = ("b", lambda: 10, mn.BLUE)
        return TopText(mob_center, var1, var2)

    def test_init_basic(self, toptext_obj):
        assert toptext_obj.mob_center is not None
        assert len(toptext_obj.vars) == 2
        assert toptext_obj.font_size == 40
        assert toptext_obj.buff == 0.7
        assert mn.np.array_equal(toptext_obj.vector, mn.UP * 1.4)
        assert len(toptext_obj.submobjects) == 2

    def test_init_single_var(self):
        mob_center = mn.Dot(mn.ORIGIN)
        var = ("x", lambda: 42, mn.GREEN)
        toptext = TopText(mob_center, var)

        assert len(toptext.vars) == 1
        assert len(toptext.submobjects) == 1

    def test_init_three_vars(self):
        mob_center = mn.Dot(mn.ORIGIN)
        var1 = ("a", lambda: 1, mn.RED)
        var2 = ("b", lambda: 2, mn.BLUE)
        var3 = ("c", lambda: 3, mn.GREEN)
        toptext = TopText(mob_center, var1, var2, var3)

        assert len(toptext.vars) == 3
        assert len(toptext.submobjects) == 3

    def test_init_custom_parameters(self):
        mob_center = mn.Dot(mn.RIGHT * 2)
        var = ("test", lambda: "hello", mn.YELLOW)

        toptext = TopText(mob_center, var, font_size=30, buff=1.0, vector=mn.DOWN * 2)

        assert toptext.font_size == 30
        assert toptext.buff == 1.0
        assert mn.np.array_equal(toptext.vector, mn.DOWN * 2)

    def test_refresh_creates_texts(self, toptext_obj):
        texts = list(toptext_obj.submobjects)
        assert len(texts) == 2

        text0 = str(texts[0].text)
        text1 = str(texts[1].text)
        assert text0 in ["a = 5", "a=5"]
        assert text1 in ["b = 10", "b=10"]
        assert hasattr(texts[0], "color")
        assert hasattr(texts[1], "color")

    def test_refresh_position(self, toptext_obj):
        texts = list(toptext_obj.submobjects)
        text_group = mn.VGroup(*texts)

        expected_position = toptext_obj.mob_center.get_center() + toptext_obj.vector
        assert mn.np.allclose(text_group.get_center(), expected_position)

    def test_refresh_with_updated_values(self):
        counter = [0]

        def get_value():
            counter[0] += 1
            return counter[0]

        mob_center = mn.Dot(mn.ORIGIN)
        var = ("counter", get_value, mn.WHITE)
        toptext = TopText(mob_center, var)

        text_content = str(toptext.submobjects[0].text)
        assert text_content in ["counter = 1", "counter=1"]

        counter[0] = 1
        new_toptext = TopText(mob_center, var)
        text_content = str(new_toptext.submobjects[0].text)
        assert text_content in ["counter = 2", "counter=2"]

    def test_text_arrangement(self, toptext_obj):
        texts = list(toptext_obj.submobjects)

        assert texts[0].get_center()[0] < texts[1].get_center()[0]
        distance = texts[1].get_center()[0] - texts[0].get_center()[0]
        assert distance > 0

    def test_first_appear_method_exists(self, toptext_obj):
        assert hasattr(toptext_obj, "first_appear")
        assert callable(toptext_obj.first_appear)

    def test_update_text_method_exists(self, toptext_obj):
        assert hasattr(toptext_obj, "update_text")
        assert callable(toptext_obj.update_text)

    def test_empty_vars_handling(self):
        mob_center = mn.Dot(mn.ORIGIN)

        toptext = TopText(mob_center)
        assert len(toptext.vars) == 0
        assert len(toptext.submobjects) == 0

    def test_different_value_types(self):
        mob_center = mn.Dot(mn.ORIGIN)

        vars = [
            ("int", lambda: 42, mn.RED),
            ("float", lambda: 3.14, mn.BLUE),
            ("string", lambda: "hello", mn.GREEN),
            ("bool", lambda: True, mn.YELLOW),
        ]

        toptext = TopText(mob_center, *vars)

        texts = list(toptext.submobjects)
        assert str(texts[0].text) in ["int = 42", "int=42"]
        assert str(texts[1].text) in ["float = 3.14", "float=3.14"]
        assert str(texts[2].text) in ["string = hello", "string=hello"]
        assert str(texts[3].text) in ["bool = True", "bool=True"]


class TestCodeBlock:
    @pytest.fixture
    def codeblock_obj(self):
        code_lines = ["a = 1", "b = 2"]
        mob_center = mn.Dot(mn.ORIGIN)
        vector = mn.ORIGIN
        return CodeBlock(code_lines, vector, mob_center=mob_center)

    @pytest.fixture
    def mock_scene(self):
        scene = Mock()
        scene.play = Mock()
        return scene

    def test_init(self, codeblock_obj):
        assert hasattr(codeblock_obj, "code_vgroup")
        assert len(codeblock_obj.code_vgroup) == 2
        assert isinstance(codeblock_obj.code_vgroup, mn.VGroup)

        for i, line in enumerate(["a = 1", "b = 2"]):
            assert line in str(codeblock_obj.code_vgroup[i])

    def test_init_with_custom_font_settings(self):
        code_lines = ["def test():", "    return True"]
        mob_center = mn.Dot(mn.LEFT)
        vector = mn.ORIGIN
        font_size = 30
        font = "Arial"

        codeblock = CodeBlock(
            code_lines, vector, mob_center=mob_center, font_size=font_size, font=font
        )

        assert len(codeblock.code_vgroup) == 2
        for text_mob in codeblock.code_vgroup:
            assert hasattr(text_mob, "font_size")
            assert hasattr(text_mob, "font")

    def test_init_empty_code_lines(self):
        mob_center = mn.Dot(mn.ORIGIN)
        vector = mn.ORIGIN
        codeblock = CodeBlock([], vector, mob_center=mob_center)

        assert len(codeblock.code_vgroup) == 0
        assert isinstance(codeblock.code_vgroup, mn.VGroup)

    def test_first_appear(self, codeblock_obj, mock_scene):
        run_time = 0.3

        codeblock_obj.first_appear(mock_scene, time=run_time)

        mock_scene.play.assert_called_once()
        args, _ = mock_scene.play.call_args
        assert len(args) == 1
        assert isinstance(args[0], mn.FadeIn)

    def test_highlight_line(self, codeblock_obj):
        line_to_highlight = 0

        codeblock_obj.highlight_line(line_to_highlight)

        assert codeblock_obj.code_mobs[0].color == mn.YELLOW
        assert codeblock_obj.code_mobs[1].color == mn.WHITE

    def test_highlight_line_out_of_bounds(self, codeblock_obj):
        try:
            codeblock_obj.highlight_line(10)
            codeblock_obj.highlight_line(-1)
        except Exception as e:
            pytest.fail(f"highlight_line raised unexpected exception: {e}")

    def test_highlight_line_single_line(self):
        code_lines = ["single_line = True"]
        mob_center = mn.Dot(mn.ORIGIN)
        vector = mn.ORIGIN
        codeblock = CodeBlock(code_lines, vector, mob_center=mob_center)

        codeblock.highlight_line(0)
        assert codeblock.code_mobs[0].color == mn.YELLOW

    def test_code_vgroup_arrangement(self):
        code_lines = ["line1", "line2", "line3"]
        mob_center = mn.Dot(mn.ORIGIN)
        vector = mn.ORIGIN
        codeblock = CodeBlock(code_lines, vector, mob_center=mob_center)

        assert len(codeblock.code_vgroup) == 3
        assert isinstance(codeblock.code_vgroup, mn.VGroup)

    def test_positioning(self):
        mob_center = mn.Dot(mn.RIGHT * 2)
        vector = mn.ORIGIN
        code_lines = ["x = 10", "y = 20"]

        codeblock = CodeBlock(code_lines, vector, mob_center=mob_center)

        assert codeblock.code_vgroup.get_center()[0] == pytest.approx(
            mob_center.get_center()[0], abs=0.1
        )

    @patch("manim.Text")
    def test_text_creation(self, mock_text):
        code_lines = ["test_line"]
        mob_center = mn.Dot(mn.ORIGIN)
        vector = mn.ORIGIN

        CodeBlock(
            code_lines, vector, mob_center=mob_center, font_size=25, font="MesloLGS NF"
        )

        mock_text.assert_called_with(
            "test_line", font="MesloLGS NF", font_size=25, color="white"
        )


class TestTitleTop:
    @pytest.fixture
    def title_obj(self):
        return TitleTop("Test Title")

    def test_initialization_defaults(self, title_obj):
        assert "Test" in title_obj.text
        assert "Title" in title_obj.text
        assert title_obj.font_size == 50
        assert abs(title_obj.get_center()[1] - 2.7) < 0.1

    def test_appear_method(self, title_obj):
        class MockScene:
            def __init__(self):
                self.add_called = False

            def add(self, _):
                self.add_called = True

        mock_scene = MockScene()
        title_obj.appear(mock_scene)
        assert mock_scene.add_called is True
