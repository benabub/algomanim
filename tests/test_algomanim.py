import pytest  # type: ignore
from algomanim.algomanim import Array, TopText, CodeBlock  # type: ignore
import manim as mn  # type: ignore


# ---------- Array Tests ----------
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

    def test_pointers_1(self, array_obj):
        array_obj.pointers_1(1, pos=0, i_color=mn.GREEN)
        for idx in range(3):
            expected = mn.GREEN if idx == 1 else array_obj.bg_color
            assert array_obj.pointers[0][idx][1].color == expected

    def test_highlight_blocks_2(self, array_obj):
        array_obj.highlight_blocks_2(0, 2, i_color=mn.RED, j_color=mn.BLUE)
        assert array_obj.sq_mob[0].fill_color == mn.RED
        assert array_obj.sq_mob[2].fill_color == mn.BLUE
        assert array_obj.sq_mob[1].fill_color == array_obj.bg_color


# ---------- TopText Tests ----------
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


# ---------- CodeBlock Tests ----------
class TestCodeBlock:
    @pytest.fixture
    def codeblock_obj(self):
        code_lines = ["a = 1", "b = 2"]
        position = mn.Dot(mn.ORIGIN)
        return CodeBlock(code_lines, position)

    def test_init(self, codeblock_obj):
        assert hasattr(codeblock_obj, "code_vgroup")
        assert len(codeblock_obj.code_vgroup) == 2
