import manim as mn

from algomanim import (
    Array,
    # String,
    RelativeTextValue,
    RelativeText,
    CodeBlock,
    TitleText,
)


class ExampleBubblesort(mn.Scene):
    def construct(self):
        self.camera.background_color = mn.DARK_GRAY  # type: ignore
        pause = 1

        # ======== INPUTS ============

        arr = [5, 4, 3, 2, 1]
        i, j, k = 0, 0, 0
        bubble = 6
        n = len(arr)

        # ======== TITLE ============

        title = TitleText(
            "Bubble Sort",
            flourish=True,
            undercaption="Benabub Viz",
        )
        title.appear(self)

        # ======== ARRAYS ============

        # Construction
        array = Array(
            arr,
            mn.LEFT * 4.2 + mn.DOWN * 0.3,
            # font=Vars.font,
        )
        # Animation
        array.first_appear(self)

        # ========== CODE BLOCK ============

        code_lines = [
            "for i in range(len(arr)):",  # 0
            "│   for j in range(len(arr) - i - 1):",  # 1
            "│   │   k = j + 1",  # 2
            "│   if arr[j] > arr[k]:",  # 3
            "│   │   arr[j], arr[k] = arr[k], arr[j]",  # 4
        ]
        # Construction code_block
        code_block = CodeBlock(
            code_lines,
            mn.DOWN * 0.2 + mn.RIGHT * 2.8,
            font_size=25,
            # font=Vars.font_cb,
        )
        # Animation code_block
        code_block.first_appear(self)
        code_block.highlight_line(0)

        # ========== TOP TEXT ============

        # Construction
        bottom_text = RelativeTextValue(
            ("bubble", lambda: bubble, mn.WHITE),
            mob_center=array,
            vector=mn.DOWN * 1.2,
            # font=Vars.font,
        )
        # Construction
        top_text = RelativeTextValue(
            ("i", lambda: i, mn.RED),
            ("j", lambda: j, mn.BLUE),
            ("k", lambda: k, mn.GREEN),
            mob_center=array,
            # font=Vars.font,
        )
        # Animation
        top_text.first_appear(self)

        # ========== HIGHLIGHT ============

        array.pointers([i, j, k])
        array.highlight_cells([i, j, k])

        # ======== PRE-CYCLE =============

        self.wait(pause)

        # ===== ALGORITHM CYCLE ==========

        for i in range(len(arr)):
            code_block.highlight_line(0)
            bubble -= 1
            array.pointers([i, j, k])
            array.highlight_cells([i, j, k])
            top_text.update_text(self)
            self.wait(pause)

            for j in range(n - i - 1):
                code_block.highlight_line(1)
                array.pointers([i, j, k])
                array.highlight_cells([i, j, k])
                array.pointers_on_value(bubble)
                top_text.update_text(self)
                bottom_text.update_text(self, animate=False)
                self.wait(pause)

                k = j + 1
                code_block.highlight_line(2)
                array.pointers([i, j, k])
                array.highlight_cells([i, j, k])
                top_text.update_text(self)
                self.wait(pause)

                code_block.highlight_line(3)
                self.wait(pause)
                if arr[j] > arr[k]:
                    arr[j], arr[k] = arr[k], arr[j]
                    code_block.highlight_line(4)
                    array.update_value(self, arr, animate=False)
                    array.pointers_on_value(bubble)
                    array.pointers([i, j, k])
                    array.highlight_cells([i, j, k])
                    top_text.update_text(self)
                    self.wait(pause)

        # ========== FINISH ==============

        self.wait(pause)
        self.renderer.file_writer.output_file = f"media/{self.__class__.__name__}.mp4"


class ExampleArray(mn.Scene):
    def construct(self):
        self.camera.background_color = mn.GREY  # type: ignore
        pause = 1

        # ======== INPUTS ============

        arr = [1, 20, "abc", "ABC", 9999, 0]

        # ============================

        array = Array(arr)
        array.first_appear(self)

        pause = 0.5

        array_20 = Array(
            arr,
            mob_center=array,
            vector=mn.UP * 2.8,
            font_size=20,
        )
        array_20.first_appear(self, time=0.1)

        array_30 = Array(
            arr,
            mob_center=array,
            vector=mn.UP * 1.4,
            font_size=30,
        )
        array_30.first_appear(self, time=0.1)

        array_40 = Array(
            arr,
            mob_center=array,
            vector=mn.DOWN * 1.5,
            font_size=40,
        )
        array_40.first_appear(self, time=0.1)

        array_50 = Array(
            arr,
            mob_center=array,
            vector=mn.DOWN * 3.0,
            font_size=50,
        )
        array_50.first_appear(self, time=0.1)

        self.wait(1)

        # ============================

        self.remove(
            array_20,
            array_30,
            array_40,
            array_50,
        )

        array_20 = Array(
            arr,
            mob_center=array,
            vector=mn.UP * 2.8,
            font_size=20,
            align_edge="left",
        )
        array_20.first_appear(self, time=0.1)

        array_30 = Array(
            arr,
            mob_center=array,
            vector=mn.UP * 1.4,
            font_size=30,
            align_edge="left",
        )
        array_30.first_appear(self, time=0.1)

        array_40 = Array(
            arr,
            mob_center=array,
            vector=mn.DOWN * 1.5,
            font_size=40,
            align_edge="left",
        )
        array_40.first_appear(self, time=0.1)

        array_50 = Array(
            arr,
            mob_center=array,
            vector=mn.DOWN * 3.0,
            font_size=50,
            align_edge="left",
        )
        array_50.first_appear(self, time=0.1)

        self.wait(1)

        # ============================

        self.remove(
            array_20,
            array_30,
            array_40,
            array_50,
        )

        array_20 = Array(
            arr,
            mob_center=array,
            vector=mn.UP * 2.8,
            font_size=20,
            align_edge="right",
        )
        array_20.first_appear(self, time=0.1)

        array_30 = Array(
            arr,
            mob_center=array,
            vector=mn.UP * 1.4,
            font_size=30,
            align_edge="right",
        )
        array_30.first_appear(self, time=0.1)

        array_40 = Array(
            arr,
            mob_center=array,
            vector=mn.DOWN * 1.5,
            font_size=40,
            align_edge="right",
        )
        array_40.first_appear(self, time=0.1)

        array_50 = Array(
            arr,
            mob_center=array,
            vector=mn.DOWN * 3.0,
            font_size=50,
            align_edge="right",
        )
        array_50.first_appear(self, time=0.1)

        self.wait(1)

        self.remove(
            array_20,
            array_30,
            array_40,
            array_50,
        )

        # ============================

        pause = 0.5
        top_text = RelativeText(
            "update_value()",
            vector=mn.UP * 2,
        )
        top_text.first_appear(self)

        array.update_value(self, [1, 12, 123, 1234, 12345, 123456], left_aligned=False)
        self.wait(1)
        array.update_value(self, [123456, 12345, 1234, 123, 12, 1])
        self.wait(pause)
        array.update_value(self, [1, 11, 1, 11, 1])
        self.wait(pause)
        array.update_value(self, [11, 1, 11, 1])
        self.wait(pause)
        array.update_value(self, [1, 11, 1])
        self.wait(pause)
        array.update_value(self, [11, 1])
        self.wait(pause)
        array.update_value(self, [1])
        self.wait(pause)
        array.update_value(self, [])
        self.wait(1)
        self.remove(top_text)

        # ============================

        top_text = RelativeText(
            "pointers()   highlight_cells()",
            vector=mn.UP * 2,
        )
        top_text.first_appear(self)

        array.update_value(self, [10, 2, 3000, 2, 100, 1, 40], left_aligned=False)
        self.wait(1)
        array.pointers([0, 3, 6])
        array.highlight_cells([0, 3, 6])
        self.wait(pause)
        array.pointers([1, 3, 5])
        array.highlight_cells([1, 3, 5])
        self.wait(pause)
        array.pointers([2, 3, 4])
        array.highlight_cells([2, 3, 4])
        self.wait(pause)
        array.pointers([3, 3, 3])
        array.highlight_cells([3, 3, 3])
        self.wait(pause)
        array.pointers([2, 3, 4])
        array.highlight_cells([2, 3, 4])
        self.wait(pause)
        array.pointers([2, 2, 4])
        array.highlight_cells([2, 2, 4])
        self.wait(pause)
        array.pointers([2, 3, 4])
        array.highlight_cells([2, 3, 4])
        self.wait(pause)
        array.pointers([2, 4, 4])
        array.highlight_cells([2, 4, 4])
        self.wait(pause)
        array.pointers([2, 4, 3])
        array.highlight_cells([2, 4, 3])
        self.wait(pause)
        array.pointers([2, 4, 2])
        array.highlight_cells([2, 4, 2])
        self.wait(1)
        self.remove(top_text)

        # ============================

        top_text = RelativeText(
            "highlight_cells_with_value()   pointers_on_value()",
            vector=mn.UP * 2,
        )
        top_text.first_appear(self)

        array.update_value(self, [10, 2, 3000, 2, 100, 1, 40], left_aligned=False)
        self.wait(1)
        array.highlight_cells_with_value(0)
        array.pointers_on_value(0)
        self.wait(pause)
        array.update_value(self, [22, 0, 22, 0, 22, 0])
        array.highlight_cells_with_value(0)
        array.pointers_on_value(0, pos=0)
        self.wait(pause)
        array.update_value(self, [0, 22, 0, 22, 0, 22])
        array.highlight_cells_with_value(0, color=mn.LIGHT_BROWN)
        array.pointers_on_value(0, color=mn.LIGHT_BROWN)
        self.wait(pause)
        array.update_value(self, [22, 0, 22, 0, 22, 0])
        array.highlight_cells_with_value(0, color=mn.LIGHT_BROWN)
        array.pointers_on_value(0, color=mn.LIGHT_BROWN, pos=0)
        self.wait(pause)
        array.update_value(self, [0, 22, 0, 22, 0, 22])
        array.highlight_cells_with_value(0, color=mn.PURPLE)
        array.pointers_on_value(0, color=mn.PURPLE)
        self.wait(pause)
        array.update_value(self, [22, 0, 22, 0, 22])
        array.highlight_cells_with_value(0, color=mn.PURPLE)
        array.pointers_on_value(0, color=mn.PURPLE, pos=0)
        self.wait(pause)
        array.update_value(self, [0, 22, 0, 22, 0, 22])
        array.highlight_cells_with_value(0, color=mn.PINK)
        array.pointers_on_value(0, color=mn.PINK)
        self.wait(pause)
        array.update_value(self, [22, 0, 22, 0, 22])
        array.highlight_cells_with_value(0, color=mn.PINK)
        array.pointers_on_value(0, color=mn.PINK, pos=0)
        self.wait(1)
        self.remove(top_text)

        # ============================

        top_text = RelativeText(
            "mix",
            vector=mn.UP * 2,
        )
        top_text.first_appear(self)

        array.update_value(self, [0, 1, 22, 333, 4444, 55555], left_aligned=False)
        self.wait(1)
        array.highlight_cells([0, 2, 4])
        array.pointers([0, 2, 4])
        # array.highlight_cells_with_value(0, color=mn.PINK)
        array.pointers_on_value(0, color=mn.PINK)
        self.wait(pause)

        array.update_value(self, [1, 0, 55555, 333])
        array.highlight_cells([0, 2, 4])
        array.pointers([0, 2, 4])
        array.highlight_cells_with_value(0, color=mn.PINK)
        array.pointers_on_value(0, color=mn.PINK)
        self.wait(pause)

        array.update_value(self, [0, 333, 0])
        array.highlight_cells([0, 2, 4])
        array.pointers([0, 2, 4])
        # array.highlight_cells_with_value(0, color=mn.PINK)
        array.pointers_on_value(0, color=mn.PINK)
        self.wait(pause)

        array.update_value(self, [0, 0])
        array.highlight_cells([0, 2, 4])
        array.pointers([0, 2, 4])
        array.highlight_cells_with_value(0, color=mn.PINK)
        array.pointers_on_value(0, color=mn.PINK)
        self.wait(pause)

        array.update_value(self, [0])
        array.highlight_cells([0, 2, 4])
        array.pointers([0, 2, 4])
        # array.highlight_cells_with_value(0, color=mn.PINK)
        array.pointers_on_value(0, color=mn.PINK)
        self.wait(pause)

        array.update_value(self, [])
        array.highlight_cells([0, 2, 4])
        array.pointers([0, 2, 4])
        array.highlight_cells_with_value(0, color=mn.PINK)
        array.pointers_on_value(0, color=mn.PINK)
        self.wait(1)

        array.update_value(self, [333])
        array.highlight_cells([0, 2, 4])
        array.pointers([0, 2, 4])
        # array.highlight_cells_with_value(0, color=mn.PINK)
        array.pointers_on_value(0, color=mn.PINK)
        self.wait(1)

        array.update_value(self, [1, 0, 22, 0, 333, 0])
        array.highlight_cells([0, 1, 2])
        array.pointers([0, 1, 2])
        array.highlight_cells_with_value(0, color=mn.PINK)
        array.pointers_on_value(0, color=mn.PINK)
        self.wait(pause)

        array.update_value(self, [0, 22, 0, 333, 0])
        array.highlight_cells([1, 1, 2])
        array.pointers([1, 1, 2])
        # array.highlight_cells_with_value(0, color=mn.PINK)
        array.pointers_on_value(0, color=mn.PINK)
        self.wait(pause)

        array.update_value(self, [1, 0, 22, 0, 333, 0, 22])
        array.highlight_cells([0, 2, 2])
        array.pointers([0, 2, 2])
        array.highlight_cells_with_value(0, color=mn.PINK)
        array.pointers_on_value(0, color=mn.PINK)
        self.wait(pause)

        array.update_value(self, [0, 22, 0, 333, 0, 55555])
        array.highlight_cells([3, 5, 3])
        array.pointers([3, 5, 3])
        # array.highlight_cells_with_value(0, color=mn.PINK)
        array.pointers_on_value(0, color=mn.PINK)
        self.wait(pause)

        array.update_value(self, [1, 0])
        array.highlight_cells([0, 0, 0])
        array.pointers([0, 0, 0])
        # array.highlight_cells_with_value(0, color=mn.PINK)
        array.pointers_on_value(0, color=mn.PINK)
        self.wait(pause)

        array.update_value(self, [0, 0, 0, 0, 0, 0])
        array.highlight_cells([9, 9, 9])
        array.pointers([9, 9, 9])
        array.highlight_cells_with_value(0, color=mn.PINK)
        array.pointers_on_value(0, color=mn.PINK)
        self.wait(1)
        # self.remove(top_text)

        # ========== FINISH ==============

        self.wait(pause)
        self.renderer.file_writer.output_file = f"./{self.__class__.__name__}.mp4"
