import pytest  # type: ignore
from algomanim.algomanim import Array, TopText, CodeBlock  # type: ignore
import manim as mn  # type: ignore


class TestArray:
    @pytest.fixture
    def array_obj(self):
        arr = [1, 2, 3]
        position = mn.Dot(mn.ORIGIN)
        return Array(arr, position)

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
        # squares positioning
        assert array_obj.sq_mob[0].get_center()[0] < array_obj.sq_mob[1].get_center()[0]
        assert array_obj.sq_mob[1].get_center()[0] < array_obj.sq_mob[2].get_center()[0]
        # squares attrs:
        assert array_obj.sq_mob[0].fill_color == mn.DARK_GRAY

    def test_pointers_1(self, array_obj):
        array_obj.pointers_1(1, pos=0, i_color=mn.GREEN)
        for idx in range(3):
            expected = mn.GREEN if idx == 1 else array_obj.bg_color
            assert array_obj.pointers[0][idx][1].color == expected

    def test_pointers_2(self, array_obj):
        # Test case 1: Different indices (normal case)
        array_obj.pointers_2(0, 2, pos=0, i_color=mn.RED, j_color=mn.BLUE)
        for idx in range(3):
            if idx == 0:  # First pointer - RED
                assert array_obj.pointers[0][idx][1].color == mn.RED
            elif idx == 2:  # Third pointer - BLUE
                assert array_obj.pointers[0][idx][1].color == mn.BLUE
            else:  # Others - background color
                assert array_obj.pointers[0][idx][1].color == array_obj.bg_color

        # Test case 2: Same indices (special handling)
        array_obj.pointers_2(1, 1, pos=0, i_color=mn.RED, j_color=mn.BLUE)
        for idx in range(3):
            if idx == 1:  # Same index uses first and third triangles
                assert array_obj.pointers[0][idx][0].color == mn.RED
                assert array_obj.pointers[0][idx][1].color == array_obj.bg_color
                assert array_obj.pointers[0][idx][2].color == mn.BLUE
            else:  # Others - background color
                for tri_idx in range(3):
                    assert (
                        array_obj.pointers[0][idx][tri_idx].color == array_obj.bg_color
                    )

        # Test case 3: Bottom pointers (pos=1)
        array_obj.pointers_2(0, 1, pos=1, i_color=mn.YELLOW, j_color=mn.PURPLE)
        for idx in range(3):
            if idx == 0:
                assert array_obj.pointers[1][idx][1].color == mn.YELLOW
            elif idx == 1:
                assert array_obj.pointers[1][idx][1].color == mn.PURPLE
            else:
                assert array_obj.pointers[1][idx][1].color == array_obj.bg_color

        # Test case 4: Invalid pos should raise error
        with pytest.raises(ValueError, match="pos must be 0 .top. or 1 .bottom."):
            array_obj.pointers_2(0, 1, pos=2)

    def test_pointers_3(self, array_obj):
        # Test case 1: All different indices
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

        # Test case 2: Two same indices (i == j)
        array_obj.pointers_3(
            1, 1, 2, pos=0, i_color=mn.RED, j_color=mn.GREEN, k_color=mn.BLUE
        )
        for idx in range(3):
            if idx == 1:  # i and j are same - use first and third triangles
                assert array_obj.pointers[0][idx][0].color == mn.RED
                assert array_obj.pointers[0][idx][1].color == array_obj.bg_color
                assert array_obj.pointers[0][idx][2].color == mn.GREEN
            elif idx == 2:  # k - normal
                assert array_obj.pointers[0][idx][1].color == mn.BLUE
            else:
                for tri_idx in range(3):
                    assert (
                        array_obj.pointers[0][idx][tri_idx].color == array_obj.bg_color
                    )

        # Test case 3: All three same indices
        array_obj.pointers_3(
            0, 0, 0, pos=0, i_color=mn.RED, j_color=mn.GREEN, k_color=mn.BLUE
        )
        for idx in range(3):
            if idx == 0:  # All three use all triangles
                assert array_obj.pointers[0][idx][0].color == mn.RED
                assert array_obj.pointers[0][idx][1].color == mn.GREEN
                assert array_obj.pointers[0][idx][2].color == mn.BLUE
            else:
                for tri_idx in range(3):
                    assert (
                        array_obj.pointers[0][idx][tri_idx].color == array_obj.bg_color
                    )

        # Test case 4: j and k same, i different
        array_obj.pointers_3(
            0,
            2,
            2,
            pos=1,  # Test bottom pointers too
            i_color=mn.RED,
            j_color=mn.GREEN,
            k_color=mn.BLUE,
        )
        for idx in range(3):
            if idx == 0:  # i - normal
                assert array_obj.pointers[1][idx][1].color == mn.RED
            elif idx == 2:  # j and k same - use first and third triangles
                assert array_obj.pointers[1][idx][0].color == mn.GREEN
                assert array_obj.pointers[1][idx][1].color == array_obj.bg_color
                assert array_obj.pointers[1][idx][2].color == mn.BLUE
            else:
                for tri_idx in range(3):
                    assert (
                        array_obj.pointers[1][idx][tri_idx].color == array_obj.bg_color
                    )

        # Test case 5: i and k same, j different
        array_obj.pointers_3(
            1, 0, 1, pos=0, i_color=mn.RED, j_color=mn.GREEN, k_color=mn.BLUE
        )
        for idx in range(3):
            if idx == 0:  # j - normal
                assert array_obj.pointers[0][idx][1].color == mn.GREEN
            elif idx == 1:  # i and k same - use first and third triangles
                assert array_obj.pointers[0][idx][0].color == mn.RED
                assert array_obj.pointers[0][idx][1].color == array_obj.bg_color
                assert array_obj.pointers[0][idx][2].color == mn.BLUE
            else:
                for tri_idx in range(3):
                    assert (
                        array_obj.pointers[0][idx][tri_idx].color == array_obj.bg_color
                    )

    def test_highlight_blocks_1(self, array_obj):
        # Test normal case
        array_obj.highlight_blocks_1(1, i_color=mn.GREEN)

        for idx, square in enumerate(array_obj.sq_mob):
            expected = mn.GREEN if idx == 1 else array_obj.bg_color
            assert square.fill_color == expected

        # Test different color
        array_obj.highlight_blocks_1(0, i_color=mn.RED)
        assert array_obj.sq_mob[0].fill_color == mn.RED
        assert array_obj.sq_mob[1].fill_color == array_obj.bg_color  # Reset
        assert array_obj.sq_mob[2].fill_color == array_obj.bg_color

    def test_highlight_blocks_2(self, array_obj):
        # Test case 1: Different indices
        array_obj.highlight_blocks_2(0, 2, i_color=mn.RED, j_color=mn.BLUE)
        assert array_obj.sq_mob[0].fill_color == mn.RED  # i
        assert array_obj.sq_mob[1].fill_color == array_obj.bg_color  # neither
        assert array_obj.sq_mob[2].fill_color == mn.BLUE  # j

        # Test case 2: Same indices (special color)
        array_obj.highlight_blocks_2(
            1, 1, i_color=mn.RED, j_color=mn.BLUE, ij_color=mn.PURPLE
        )
        assert array_obj.sq_mob[0].fill_color == array_obj.bg_color
        assert array_obj.sq_mob[1].fill_color == mn.PURPLE  # i == j
        assert array_obj.sq_mob[2].fill_color == array_obj.bg_color

        # Test case 3: Custom colors
        array_obj.highlight_blocks_2(
            0, 1, i_color=mn.YELLOW, j_color=mn.ORANGE, ij_color=mn.PINK
        )
        assert array_obj.sq_mob[0].fill_color == mn.YELLOW
        assert array_obj.sq_mob[1].fill_color == mn.ORANGE
        assert array_obj.sq_mob[2].fill_color == array_obj.bg_color

    def test_highlight_blocks_3(self, array_obj):
        # Test case 1: All different
        array_obj.highlight_blocks_3(
            0, 1, 2, i_color=mn.RED, j_color=mn.GREEN, k_color=mn.BLUE
        )
        assert array_obj.sq_mob[0].fill_color == mn.RED
        assert array_obj.sq_mob[1].fill_color == mn.GREEN
        assert array_obj.sq_mob[2].fill_color == mn.BLUE

        # Test case 2: Two same (i == j)
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
        assert array_obj.sq_mob[1].fill_color == mn.YELLOW  # i == j
        assert array_obj.sq_mob[2].fill_color == mn.BLUE  # k

        # Test case 3: All three same
        array_obj.highlight_blocks_3(
            0,
            0,
            0,
            i_color=mn.RED,
            j_color=mn.GREEN,
            k_color=mn.BLUE,
            ijk_color=mn.BLACK,
        )
        assert array_obj.sq_mob[0].fill_color == mn.BLACK  # all same
        assert array_obj.sq_mob[1].fill_color == array_obj.bg_color
        assert array_obj.sq_mob[2].fill_color == array_obj.bg_color

        # Test case 4: j and k same
        array_obj.highlight_blocks_3(
            0, 2, 2, i_color=mn.RED, j_color=mn.GREEN, k_color=mn.BLUE, jk_color=mn.TEAL
        )
        assert array_obj.sq_mob[0].fill_color == mn.RED  # i
        assert array_obj.sq_mob[1].fill_color == array_obj.bg_color
        assert array_obj.sq_mob[2].fill_color == mn.TEAL  # j == k

        # Test case 5: i and k same
        array_obj.highlight_blocks_3(
            1,
            0,
            1,
            i_color=mn.RED,
            j_color=mn.GREEN,
            k_color=mn.BLUE,
            ik_color=mn.PURPLE,
        )
        assert array_obj.sq_mob[0].fill_color == mn.GREEN  # j
        assert array_obj.sq_mob[1].fill_color == mn.PURPLE  # i == k
        assert array_obj.sq_mob[2].fill_color == array_obj.bg_color


class TestTopText:
    @pytest.fixture
    def toptext_obj(self):
        mob_center = mn.Dot(mn.ORIGIN)
        var1 = ("a", lambda: 5, "red")
        var2 = ("b", lambda: 10, "blue")
        return TopText(mob_center, var1, var2)

    def test_init(self, toptext_obj):
        assert hasattr(toptext_obj, "vars")
        assert len(toptext_obj.vars) == 2

    def test_refresh_creates_text(self, toptext_obj):
        toptext_obj._refresh()
        assert len(toptext_obj.submobjects) > 0


class TestCodeBlock:
    @pytest.fixture
    def codeblock_obj(self):
        code_lines = ["a = 1", "b = 2"]
        position = mn.Dot(mn.ORIGIN)
        return CodeBlock(code_lines, position)

    def test_init(self, codeblock_obj):
        assert hasattr(codeblock_obj, "code_vgroup")
        assert len(codeblock_obj.code_vgroup) == 2
