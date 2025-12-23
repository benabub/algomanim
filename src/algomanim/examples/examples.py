"""
Example scenes demonstrating algomanim functionality and serving as visual tests.

This module contains Example classes that:
  - Showcase algomanim features in action
  - Serve as visual tests to verify classes work correctly
  - Help identify rendering issues on different systems

Note: Uses default Manim fonts. For better visual results, consider installing
and specifying custom fonts in the scene configurations.
"""

import numpy as np
import manim as mn

from algomanim import (
    Array,
    String,
    RelativeTextValue,
    RelativeText,
    CodeBlock,
    TitleText,
    LinkedList,
)


class ExampleBubblesort(mn.Scene):
    def construct(self):
        self.camera.background_color = mn.DARK_GRAY  # type: ignore
        pause = 1
        # pause = 0.3

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
            mn.LEFT * 4.1 + mn.DOWN * 0.35,
            font_size=40,
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
            vector=mn.DOWN * 0.2 + mn.RIGHT * 2.8,
            font_size=25,
            # font=Vars.font_cb,
        )
        # Animation code_block
        code_block.first_appear(self)
        code_block.highlight(0)

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
        array.highlight_containers_1to3([i, j, k])

        # ======== PRE-CYCLE =============

        self.wait(pause)

        # ===== ALGORITHM CYCLE ==========

        for i in range(len(arr)):
            code_block.highlight(0)
            bubble -= 1
            array.pointers([i, j, k])
            array.highlight_containers_1to3([i, j, k])
            top_text.update_text(self)
            self.wait(pause)

            for j in range(n - i - 1):
                code_block.highlight(1)
                array.pointers([i, j, k])
                array.highlight_containers_1to3([i, j, k])
                array.pointers_on_value(bubble, color=mn.WHITE)
                top_text.update_text(self)
                bottom_text.update_text(self, animate=False)
                self.wait(pause)

                k = j + 1
                code_block.highlight(2)
                array.pointers([i, j, k])
                array.highlight_containers_1to3([i, j, k])
                top_text.update_text(self)
                self.wait(pause)

                code_block.highlight(3)
                self.wait(pause)
                if arr[j] > arr[k]:
                    arr[j], arr[k] = arr[k], arr[j]
                    code_block.highlight(4)
                    array.update_value(self, arr, animate=False)
                    array.pointers_on_value(bubble, color=mn.WHITE)
                    array.pointers([i, j, k])
                    array.highlight_containers_1to3([i, j, k])
                    top_text.update_text(self)
                    self.wait(pause)

        # ========== FINISH ==============

        self.wait(pause)
        self.renderer.file_writer.output_file = f"media/{self.__class__.__name__}.mp4"


class ExampleArray(mn.Scene):
    def construct(self):
        self.camera.background_color = mn.GREY  # type: ignore
        # ============================

        pause = 0.5

        arr = [0, "\"'`^", "ace", "ygpj", "ABC", ":*#", "."]

        array = Array(
            arr,
            # pointers=False,
        )
        array.first_appear(self)

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
            align_left=array,
            vector=mn.UP * 2.8,
            font_size=20,
        )
        array_20.first_appear(self, time=0.1)

        array_30 = Array(
            arr,
            mob_center=array,
            align_left=array,
            vector=mn.UP * 1.4,
            font_size=30,
        )
        array_30.first_appear(self, time=0.1)

        array_40 = Array(
            arr,
            mob_center=array,
            align_left=array,
            vector=mn.DOWN * 1.5,
            font_size=40,
        )
        array_40.first_appear(self, time=0.1)

        array_50 = Array(
            arr,
            mob_center=array,
            align_left=array,
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
            align_right=array,
            vector=mn.UP * 2.8,
            font_size=20,
        )
        array_20.first_appear(self, time=0.1)

        array_30 = Array(
            arr,
            mob_center=array,
            align_right=array,
            vector=mn.UP * 1.4,
            font_size=30,
        )
        array_30.first_appear(self, time=0.1)

        array_40 = Array(
            arr,
            mob_center=array,
            align_right=array,
            vector=mn.DOWN * 1.5,
            font_size=40,
        )
        array_40.first_appear(self, time=0.1)

        array_50 = Array(
            arr,
            mob_center=array,
            align_right=array,
            vector=mn.DOWN * 3.0,
            font_size=50,
        )
        array_50.first_appear(self, time=0.1)

        self.wait(1)

        self.remove(
            array,
            array_20,
            array_30,
            array_40,
            array_50,
        )
        # ============================

        pause = 1
        arr = list("arr")

        center = Array(list("mob_center"), font_size=40)
        center.first_appear(self)

        top_text = RelativeText(
            "mob_center=mob_center\nvector=mn.UP * 1",
            vector=mn.DOWN * 2 + mn.RIGHT * 0,
        )
        array = Array(arr, mob_center=center, vector=mn.UP * 2)
        array.group_appear(self, top_text)
        self.wait(pause)

        self.remove(array, top_text)

        top_text = RelativeText(
            "mob_center=mob_center\nalign_left=mob_center\nvector=mn.UP * 1",
            vector=mn.DOWN * 2 + mn.RIGHT * 0,
        )
        array = Array(arr, mob_center=center, align_left=center, vector=mn.UP * 2)
        array.group_appear(self, top_text)
        self.wait(pause)

        self.remove(array, top_text)

        top_text = RelativeText(
            "mob_center=mob_center\nalign_right=mob_center\nvector=mn.UP * 1",
            vector=mn.DOWN * 2 + mn.RIGHT * 0,
        )
        array = Array(arr, mob_center=center, align_right=center, vector=mn.UP * 2)
        array.group_appear(self, top_text)
        self.wait(pause)

        self.clear()

        one = Array(list("one"), font_size=60, vector=mn.UP * 2.7 + mn.LEFT * 4)
        two = Array(list("two"), font_size=60, vector=mn.DOWN * 2.4 + mn.RIGHT * 3)
        one.group_appear(self, two)
        self.wait(pause)

        # -----------------------

        top_text = RelativeText(
            "align_left=one\nalign_bottom=two",
            vector=mn.UP * 1 + mn.RIGHT * 2,
        )
        array = Array(arr, align_left=one, align_bottom=two)
        array.group_appear(self, top_text)
        self.wait(pause)
        self.remove(array, top_text)

        top_text = RelativeText(
            "align_left=one\nalign_top=two",
            vector=mn.UP * 1 + mn.RIGHT * 2,
        )
        array = Array(arr, align_left=one, align_top=two)
        array.group_appear(self, top_text)
        self.wait(pause)
        self.remove(array, top_text)

        top_text = RelativeText(
            "align_right=one\nalign_top=two",
            vector=mn.UP * 1 + mn.RIGHT * 2,
        )
        array = Array(arr, align_right=one, align_top=two)
        array.group_appear(self, top_text)
        self.wait(pause)
        self.remove(array, top_text)

        top_text = RelativeText(
            "align_right=one\nalign_bottom=two",
            vector=mn.UP * 1 + mn.RIGHT * 2,
        )
        array = Array(arr, align_right=one, align_bottom=two)
        array.group_appear(self, top_text)
        self.wait(pause)
        self.remove(array, top_text)

        top_text = RelativeText(
            "align_left=one\nalign_bottom=two\nvector=mn.UP * 1 + mn.RIGHT * 1",
            vector=mn.UP * 0.7 + mn.RIGHT * 2,
        )
        array = Array(
            arr,
            align_left=one,
            align_bottom=two,
            vector=mn.UP * 1 + mn.RIGHT * 1,
        )
        array.group_appear(self, top_text)
        self.wait(pause)
        self.clear()

        # ============================

        pause = 0.5

        array = Array([1, 12, 123, 1234, 12345, 123456])
        array.first_appear(self)

        top_text = RelativeText(
            "update_value()",
            vector=mn.UP * 2,
        )
        top_text.first_appear(self)

        array.pointers([0, 1, 2])
        array.highlight_containers_1to3([0, 1, 2])
        self.wait(1)
        array.update_value(self, [1, 12, 123, 1234, 12345, 123456])
        self.wait(pause)
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
        self.wait(pause)
        array.update_value(self, [])
        self.wait(pause)
        array.update_value(self, [1])
        self.wait(1)
        array.update_value(self, [1, 2, 3, 4, 5, 6], animate=True)
        array.pointers([0, 1, 2])
        array.highlight_containers_1to3([0, 1, 2])
        self.wait(pause)
        array.update_value(self, [6, 1, 2, 3, 4, 5], animate=True)
        self.wait(pause)
        array.update_value(self, [5, 6, 1, 2, 3, 4], animate=True)
        self.wait(pause)
        array.update_value(self, [1, 2, 3, 4, 5], animate=True)
        self.wait(pause)
        array.update_value(self, [11, 2, 33, 4], animate=True)
        self.wait(pause)
        array.update_value(self, [1, 22, 3, 44], animate=True)
        self.wait(pause)
        array.update_value(self, [11, 2, 33], animate=True)
        self.wait(pause)
        array.update_value(self, [], animate=True)
        self.wait(pause)
        array.update_value(self, [1], animate=True)
        self.wait(1)
        self.remove(top_text)

        # ============================

        top_text = RelativeText(
            "pointers()   highlight_containers_1to3()",
            vector=mn.UP * 2,
        )
        top_text.first_appear(self)

        array.update_value(self, [10, 2, 3000, 2, 100, 1, 40], left_aligned=False)
        self.wait(1)
        array.pointers([0, 3, 6])
        array.highlight_containers_1to3([0, 3, 6])
        self.wait(pause)
        array.pointers([1, 3, 5])
        array.highlight_containers_1to3([1, 3, 5])
        self.wait(pause)
        array.pointers([2, 3, 4])
        array.highlight_containers_1to3([2, 3, 4])
        self.wait(pause)
        array.pointers([3, 3, 3])
        array.highlight_containers_1to3([3, 3, 3])
        self.wait(pause)
        array.pointers([2, 3, 4])
        array.highlight_containers_1to3([2, 3, 4])
        self.wait(pause)
        array.pointers([2, 2, 4])
        array.highlight_containers_1to3([2, 2, 4])
        self.wait(pause)
        array.pointers([2, 3, 4])
        array.highlight_containers_1to3([2, 3, 4])
        self.wait(pause)
        array.pointers([2, 4, 4])
        array.highlight_containers_1to3([2, 4, 4])
        self.wait(pause)
        array.pointers([2, 4, 3])
        array.highlight_containers_1to3([2, 4, 3])
        self.wait(pause)
        array.pointers([2, 4, 2])
        array.highlight_containers_1to3([2, 4, 2])
        self.wait(1)
        self.remove(top_text)
        array.clear_pointers_highlights(0)
        array.clear_containers_highlights()

        # ============================

        top_text = RelativeText(
            "highlight_containers_monocolor()",
            vector=mn.UP * 2,
        )
        top_text.first_appear(self)

        array.update_value(self, [1, 2, 3, 4, 5, 6, 7, 8, 9], left_aligned=False)
        self.wait(pause)
        array.highlight_containers_monocolor([0, 2, 4, 6, 8])
        self.wait(pause)
        array.highlight_containers_monocolor([0, 1, 2, 3, 4])
        self.wait(pause)
        array.highlight_containers_monocolor([5, 6, 7, 8])
        self.wait(pause)
        self.remove(top_text)
        array.clear_containers_highlights()

        # ============================

        array.update_value(self, [10, 2, 3000, 2, 100, 1, 40], left_aligned=False)
        self.wait(1)

        top_text = RelativeText(
            "highlight_containers_with_value()   pointers_on_value()",
            vector=mn.UP * 2,
        )
        top_text.first_appear(self)

        array.highlight_containers_with_value(0)
        array.pointers_on_value(0)
        self.wait(pause)
        array.update_value(self, [22, 0, 22, 0, 22, 0])
        array.highlight_containers_with_value(0)
        array.pointers_on_value(0)
        self.wait(pause)
        array.update_value(self, [0, 22, 0, 22, 0, 22])
        array.highlight_containers_with_value(0, color=mn.LIGHT_BROWN)
        array.pointers_on_value(0, color=mn.LIGHT_BROWN)
        self.wait(pause)
        array.update_value(self, [22, 0, 22, 0, 22, 0])
        array.highlight_containers_with_value(0, color=mn.LIGHT_BROWN)
        array.pointers_on_value(0, color=mn.LIGHT_BROWN)
        self.wait(pause)
        array.update_value(self, [0, 22, 0, 22, 0, 22])
        array.highlight_containers_with_value(0, color=mn.PURPLE)
        array.pointers_on_value(0, color=mn.PURPLE)
        self.wait(pause)
        array.update_value(self, [22, 0, 22, 0, 22])
        array.highlight_containers_with_value(0, color=mn.PURPLE)
        array.pointers_on_value(0, color=mn.PURPLE)
        self.wait(pause)
        array.update_value(self, [0, 22, 0, 22, 0, 22])
        array.highlight_containers_with_value(0, color=mn.PINK)
        array.pointers_on_value(0, color=mn.PINK)
        self.wait(pause)
        array.update_value(self, [22, 0, 22, 0, 22])
        array.highlight_containers_with_value(0, color=mn.PINK)
        array.pointers_on_value(0, color=mn.PINK)
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
        array.highlight_containers_1to3([0, 2, 4])
        array.pointers([0, 2, 4])
        array.pointers_on_value(0, color=mn.PINK)
        self.wait(pause)

        array.update_value(self, [1, 0, 55555, 333])
        array.clear_pointers_highlights(0)
        array.highlight_containers_with_value(0, color=mn.PINK)
        array.pointers_on_value(0, color=mn.PINK)
        self.wait(pause)

        array.update_value(self, [0, 333, 0])
        array.highlight_containers_1to3([0, 2, 4])
        array.pointers([0, 2, 4])
        array.pointers_on_value(0, color=mn.PINK)
        self.wait(pause)

        array.update_value(self, [0, 0])
        array.clear_pointers_highlights(0)
        array.highlight_containers_with_value(0, color=mn.PINK)
        array.pointers_on_value(0, color=mn.PINK)
        self.wait(pause)

        array.update_value(self, [0])
        array.highlight_containers_1to3([0, 2, 4])
        array.pointers([0, 2, 4])
        array.pointers_on_value(0, color=mn.PINK)
        self.wait(pause)

        array.update_value(self, [], animate=True)
        array.highlight_containers_1to3([0, 2, 4])
        array.pointers([0, 2, 4])
        array.pointers_on_value(0, color=mn.PINK)
        self.wait(pause)

        array.update_value(self, [0, 0, 0, 0], animate=True)
        self.wait(pause)

        array.update_value(self, [1, 0, 22, 0, 333, 0], animate=True)
        array.clear_pointers_highlights(0)
        array.highlight_containers_with_value(0, color=mn.PINK)
        array.pointers_on_value(0, color=mn.PINK)
        self.wait(pause)

        array.update_value(self, [0, 22, 0, 333, 0], animate=True)
        array.clear_pointers_highlights(1)
        array.highlight_containers_1to3([1, 1, 2])
        array.pointers([1, 1, 2])
        self.wait(pause)

        array.update_value(self, [1, 0, 22, 0, 333, 0, 22], animate=True)
        array.clear_pointers_highlights(0)
        array.highlight_containers_with_value(0, color=mn.PINK)
        array.pointers_on_value(0, color=mn.PINK)
        self.wait(pause)

        array.update_value(self, [0, 22, 0, 333, 0, 55555], animate=True)
        array.clear_pointers_highlights(1)
        array.highlight_containers_1to3([3, 5, 3])
        array.pointers([3, 5, 3])
        self.wait(pause)

        array.update_value(self, [1, 0], animate=True)
        array.highlight_containers_1to3([0, 0, 0])
        array.pointers([0, 0, 0])
        self.wait(pause)

        array.update_value(self, [0, 0, 0, 0, 0, 0], animate=True)
        array.clear_pointers_highlights(0)
        array.highlight_containers_with_value(0, color=mn.PINK)
        array.pointers_on_value(0, color=mn.PINK)
        self.wait(1)

        # ========== FINISH ==============

        self.wait(pause)
        self.renderer.file_writer.output_file = f"./{self.__class__.__name__}.mp4"


class ExampleString(mn.Scene):
    def construct(self):
        self.camera.background_color = mn.GREY  # type: ignore
        pause = 0.5

        # ======== INPUTS ============

        s = "0agA-/*&.^`~"

        # ============================

        string = String(
            s,
            # pointers=False,
        )
        string.first_appear(self)

        string_20 = String(
            s,
            mob_center=string,
            vector=mn.UP * 2.8,
            font_size=25,
        )
        string_20.first_appear(self, time=0.1)

        string_25 = String(
            s,
            mob_center=string,
            vector=mn.UP * 1.4,
            font_size=30,
        )
        string_25.first_appear(self, time=0.1)

        string_35 = String(
            s,
            mob_center=string,
            vector=mn.DOWN * 1.5,
            font_size=37,
        )
        string_35.first_appear(self, time=0.1)

        string_40 = String(
            s,
            mob_center=string,
            vector=mn.DOWN * 3.0,
            font_size=40,
        )
        string_40.first_appear(self, time=0.1)

        self.wait(1)

        # ============================

        self.remove(
            string_20,
            string_25,
            string_35,
            string_40,
        )

        string_20 = String(
            s,
            mob_center=string,
            vector=mn.UP * 2.8,
            font_size=25,
            align_edge="left",
        )
        string_20.first_appear(self, time=0.1)

        string_25 = String(
            s,
            mob_center=string,
            vector=mn.UP * 1.4,
            font_size=30,
            align_edge="left",
        )
        string_25.first_appear(self, time=0.1)

        string_35 = String(
            s,
            mob_center=string,
            vector=mn.DOWN * 1.5,
            font_size=37,
            align_edge="left",
        )
        string_35.first_appear(self, time=0.1)

        string_40 = String(
            s,
            mob_center=string,
            vector=mn.DOWN * 3.0,
            font_size=40,
            align_edge="left",
        )
        string_40.first_appear(self, time=0.1)

        self.wait(1)

        # ============================

        self.remove(
            string_20,
            string_25,
            string_35,
            string_40,
        )

        string_20 = String(
            s,
            mob_center=string,
            vector=mn.UP * 2.8,
            font_size=25,
            align_edge="right",
        )
        string_20.first_appear(self, time=0.1)

        string_25 = String(
            s,
            mob_center=string,
            vector=mn.UP * 1.4,
            font_size=30,
            align_edge="right",
        )
        string_25.first_appear(self, time=0.1)

        string_35 = String(
            s,
            mob_center=string,
            vector=mn.DOWN * 1.5,
            font_size=37,
            align_edge="right",
        )
        string_35.first_appear(self, time=0.1)

        string_40 = String(
            s,
            mob_center=string,
            vector=mn.DOWN * 3.0,
            font_size=40,
            align_edge="right",
        )
        string_40.first_appear(self, time=0.1)

        self.wait(1)

        self.remove(
            string_20,
            string_25,
            string_35,
            string_40,
        )

        # ============================

        string.update_value(self, "follow the rabbit", left_aligned=False)

        top_text = RelativeText(
            "update_value()",
            vector=mn.UP * 2,
        )
        top_text.first_appear(self)

        string.pointers([4, 5, 6])
        string.highlight_containers_1to3([4, 5, 6])

        self.wait(1)
        string.update_value(self, "follow the rabbit")
        self.wait(pause)
        string.update_value(self, "follow the")
        self.wait(pause)
        string.update_value(self, "follow")
        self.wait(pause)
        string.update_value(self, "")
        self.wait(pause)
        string.update_value(self, "")
        self.wait(pause)
        string.update_value(self, "follow")
        self.wait(1)
        string.update_value(self, "follow the", animate=True)
        string.highlight_containers_1to3([4, 5, 6])
        string.highlight_containers_1to3([4, 5, 6])
        self.wait(pause)
        string.update_value(self, "follow the rabbit", animate=True)
        self.wait(pause)
        string.update_value(self, "rabbit follow the", animate=True)
        self.wait(pause)
        string.update_value(self, "the rabbit follow", animate=True)
        self.wait(pause)
        string.update_value(self, "follow the rabbit", animate=True)
        self.wait(pause)
        string.update_value(self, "follow the", animate=True)
        self.wait(pause)
        string.update_value(self, "follow", animate=True)
        self.wait(pause)
        string.update_value(self, "", animate=True)
        self.wait(pause)
        string.update_value(self, "follow", animate=True)
        self.wait(1)

        self.remove(top_text)

        # ============================

        top_text = RelativeText(
            "pointers()   highlight_containers()",
            vector=mn.UP * 2,
        )
        top_text.first_appear(self)

        string.update_value(self, "follow the rabbit", left_aligned=False)
        self.wait(1)
        string.pointers([0, 3, 6])
        string.highlight_containers_1to3([0, 3, 6])
        self.wait(pause)
        string.pointers([1, 3, 5])
        string.highlight_containers_1to3([1, 3, 5])
        self.wait(pause)
        string.pointers([2, 3, 4])
        string.highlight_containers_1to3([2, 3, 4])
        self.wait(pause)
        string.pointers([3, 3, 3])
        string.highlight_containers_1to3([3, 3, 3])
        self.wait(pause)
        string.pointers([2, 3, 4])
        string.highlight_containers_1to3([2, 3, 4])
        self.wait(pause)
        string.pointers([2, 2, 4])
        string.highlight_containers_1to3([2, 2, 4])
        self.wait(pause)
        string.pointers([2, 3, 4])
        string.highlight_containers_1to3([2, 3, 4])
        self.wait(pause)
        string.pointers([2, 4, 4])
        string.highlight_containers_1to3([2, 4, 4])
        self.wait(pause)
        string.pointers([2, 4, 3])
        string.highlight_containers_1to3([2, 4, 3])
        self.wait(pause)
        string.pointers([2, 40, 2])
        string.highlight_containers_1to3([2, 40, 2])
        self.wait(1)
        self.remove(top_text)
        string.clear_pointers_highlights(0)
        string.clear_containers_highlights()

        # ============================

        top_text = RelativeText(
            "highlight_containers_with_value()   pointers_on_value()",
            vector=mn.UP * 2,
        )
        top_text.first_appear(self)

        string.update_value(self, "follow the rabbit", left_aligned=False)
        self.wait(1)
        string.highlight_containers_with_value("f")
        string.pointers_on_value("f")
        self.wait(pause)
        string.highlight_containers_with_value("t")
        string.pointers_on_value("t")
        self.wait(pause)
        string.highlight_containers_with_value("a", color=mn.LIGHT_BROWN)
        string.pointers_on_value("a", color=mn.LIGHT_BROWN)
        self.wait(pause)
        string.highlight_containers_with_value("b", color=mn.LIGHT_BROWN)
        string.pointers_on_value("b", color=mn.LIGHT_BROWN)
        self.wait(pause)
        string.highlight_containers_with_value("l", color=mn.PURPLE)
        string.pointers_on_value("l", color=mn.PURPLE)
        self.wait(pause)
        string.highlight_containers_with_value("w", color=mn.PURPLE)
        string.pointers_on_value("w", color=mn.PURPLE)
        self.wait(pause)
        string.highlight_containers_with_value(" ", color=mn.PINK)
        string.pointers_on_value(" ", color=mn.PINK)
        self.wait(1)
        self.remove(top_text)

        # ============================

        top_text = RelativeText(
            "mix",
            vector=mn.UP * 2,
        )
        top_text.first_appear(self)

        string.update_value(self, "follow the rabbit", left_aligned=False)
        self.wait(1)
        string.highlight_containers_1to3([0, 2, 4])
        string.pointers([0, 2, 4])
        self.wait(pause)

        string.update_value(self, "follow the")
        string.clear_pointers_highlights(0)
        string.pointers_on_value("f", color=mn.PINK)
        string.highlight_containers_with_value("f", color=mn.PINK)
        self.wait(pause)

        string.update_value(self, "follow")
        string.clear_pointers_highlights(1)
        string.highlight_containers_1to3([0, 2, 4])
        string.pointers([0, 2, 4])
        self.wait(pause)

        string.update_value(self, "", animate=True)
        string.clear_pointers_highlights(0)
        string.highlight_containers_with_value("b", color=mn.PINK)
        string.pointers_on_value("b", color=mn.PINK)
        self.wait(1)

        string.update_value(self, "rabbit", left_aligned=False, animate=True)
        self.wait(1)

        string.update_value(self, "rabbit", left_aligned=False, animate=True)
        string.highlight_containers_with_value("b", color=mn.PINK)
        string.pointers_on_value("b", color=mn.PINK)
        self.wait(1)

        string.update_value(self, "white rabbit", left_aligned=False, animate=True)
        string.clear_pointers_highlights(1)
        string.highlight_containers_1to3([0, 1, 2])
        string.pointers([0, 1, 2])
        self.wait(pause)

        string.update_value(self, "rabbit white", left_aligned=False, animate=True)
        string.clear_pointers_highlights(0)
        string.highlight_containers_with_value("t", color=mn.PINK)
        string.pointers_on_value("t", color=mn.PINK)
        self.wait(pause)

        string.update_value(self, "rabbit the white", left_aligned=False, animate=True)
        string.clear_pointers_highlights(1)
        string.highlight_containers_1to3([0, 2, 2])
        string.pointers([0, 2, 2])
        self.wait(pause)

        string.update_value(self, "white the rabbit", animate=True)
        string.clear_pointers_highlights(0)
        string.pointers_on_value(" ", color=mn.PINK)
        string.highlight_containers_with_value(" ", color=mn.PINK)
        self.wait(pause)

        string.update_value(self, "rab follow rab", animate=True)
        string.highlight_containers_1to3([90, 90, 90])
        string.pointers([90, 90, 90])
        string.highlight_containers_with_value("a", color=mn.PINK)
        string.pointers_on_value("a", color=mn.PINK)
        self.wait(1)

        # ========== FINISH ==============

        self.wait(pause)
        self.renderer.file_writer.output_file = f"./{self.__class__.__name__}.mp4"


class ExampleLinkedlist(mn.Scene):
    def construct(self):
        self.camera.background_color = mn.GREY  # type: ignore
        pause = 0.3
        cll = LinkedList.create_linked_list

        arr = Array([letter for letter in "mob_center"], vector=mn.UP * 3)
        arr.first_appear(self)

        # ======== rotation ============

        ll = LinkedList(
            cll([0, 1, 2]),
            mob_center=arr,
            vector=mn.DOWN * 3.5,
        )
        ll.appear(self)
        self.wait(pause)

        self.remove(ll)
        ll = LinkedList(
            cll([0, 1, 2]),
            mob_center=arr,
            vector=mn.DOWN * 3.5,
            direction=np.array([10, -10, 0]),
        )
        ll.appear(self)
        self.wait(pause)

        self.remove(ll)
        ll = LinkedList(
            cll([0, 1, 2]),
            mob_center=arr,
            vector=mn.DOWN * 3.5,
            direction=np.array([0, -10, 0]),
        )
        ll.appear(self)
        self.wait(pause)

        self.remove(ll)
        ll = LinkedList(
            cll([0, 1, 2]),
            mob_center=arr,
            vector=mn.DOWN * 3.5,
            direction=np.array([-10, -10, 0]),
        )
        ll.appear(self)
        self.wait(pause)

        self.remove(ll)
        ll = LinkedList(
            cll([0, 1, 2]),
            mob_center=arr,
            vector=mn.DOWN * 3.5,
            direction=np.array([-10, 0, 0]),
        )
        ll.appear(self)
        self.wait(pause)

        self.remove(ll)
        ll = LinkedList(
            cll([0, 1, 2]),
            mob_center=arr,
            vector=mn.DOWN * 3.5,
            direction=np.array([-10, 10, 0]),
        )
        ll.appear(self)
        self.wait(pause)

        self.remove(ll)
        ll = LinkedList(
            cll([0, 1, 2]),
            mob_center=arr,
            vector=mn.DOWN * 3.5,
            direction=np.array([0, 10, 0]),
        )
        ll.appear(self)
        self.wait(pause)

        self.remove(ll)
        ll = LinkedList(
            cll([0, 1, 2]),
            mob_center=arr,
            vector=mn.DOWN * 3.5,
            direction=np.array([10, 10, 0]),
        )
        ll.appear(self)
        self.wait(pause)

        self.remove(ll)
        ll = LinkedList(
            cll([0, 1, 2]),
            mob_center=arr,
            vector=mn.DOWN * 3.5,
        )
        ll.appear(self)
        self.wait(1)
        self.remove(ll)

        # ======== left | right alignment ============

        ll1 = LinkedList(
            cll([0, 1, 2]),
            mob_center=arr,
            vector=mn.DOWN * 2,
            align_edge="right",
        )
        ll2 = LinkedList(
            cll([0, 1, 2]),
            mob_center=arr,
            vector=mn.DOWN * 2,
            align_edge="left",
        )

        rt1 = RelativeText(
            "align_edge=right",
            mob_center=ll1,
            vector=mn.DOWN * 2,
        )
        rt2 = RelativeText(
            "align_edge=left",
            mob_center=ll2,
            vector=mn.DOWN * 2,
        )

        self.play(
            mn.FadeIn(ll1),
            mn.FadeIn(ll2),
            mn.FadeIn(rt1),
            mn.FadeIn(rt2),
            run_time=0.5,
        )

        self.wait(1)
        self.remove(ll1, ll2, rt1, rt2)

        # ======== up | down alignment ============

        self.play(arr.animate.move_to(mn.ORIGIN))

        ll1 = LinkedList(
            cll([0, 1]),
            radius=0.8,
            mob_center=arr,
            vector=mn.LEFT * 5.3,
            align_edge="up",
            direction=mn.UP,
        )
        ll2 = LinkedList(
            cll([0, 1]),
            radius=0.8,
            mob_center=arr,
            vector=mn.RIGHT * 5.3,
            align_edge="down",
            direction=mn.UP,
        )

        rt1 = RelativeText(
            "align_edge=up",
            mob_center=ll1,
            vector=mn.DOWN * 3,
            align_edge="left",
        )
        rt2 = RelativeText(
            "align_edge=down",
            mob_center=ll2,
            vector=mn.DOWN * 3.9,
            align_edge="right",
        )

        self.play(
            mn.FadeIn(ll1),
            mn.FadeIn(ll2),
            mn.FadeIn(rt1),
            mn.FadeIn(rt2),
            run_time=0.5,
        )

        self.wait(1)
        self.clear()

        # ======== update value ============

        pause = 0.5

        ll = LinkedList(
            cll([0, 12, 12345, "'", '^"', ".", "_.,", "Aa", "acv", "gjy", "gyp"]),
            direction=np.array([10, 2, 0]),
            vector=mn.LEFT * 5.85 + mn.DOWN * 2,
            # pointers=False,
        )

        ll.highlight_containers_1to3([0, 2, 4])
        ll.pointers([0, 2, 4])

        rt = RelativeText(
            "update_value()",
            mob_center=ll,
            vector=mn.UP * 3,
        )

        self.play(mn.FadeIn(ll), mn.FadeIn(rt))
        self.wait(pause)

        ll.update_value(
            self,
            cll([0, 12, 12345, "'", '^"', ".", "_.,", "Aa"]),
        )
        self.wait(pause)
        ll.update_value(
            self,
            cll([0, 12, 12345, "'", '^"']),
        )
        self.wait(pause)
        ll.update_value(
            self,
            cll([0, 12]),
        )
        self.wait(pause)
        ll.update_value(self, cll([0]))
        self.wait(pause)
        ll.update_value(self, cll([]))
        self.wait(pause)
        ll.update_value(
            self,
            cll([0]),
            animate=True,
        )
        self.wait(pause)
        ll.update_value(
            self,
            cll([0, 12]),
            animate=True,
        )
        self.wait(pause)
        ll.update_value(
            self,
            cll([0, 12, 12345, "'", '^"']),
            animate=True,
        )
        self.wait(pause)
        ll.update_value(
            self,
            cll([0, 12, 12345, "'", '^"', ".", "_.,", "Aa"]),
            animate=True,
        )
        self.wait(pause)
        ll.update_value(
            self,
            cll([0, 12, 12345, "'", '^"', ".", "_.,", "Aa", "acv", "gjy", "gyp"]),
            animate=True,
        )
        self.wait(1)
        self.remove(rt)

        # ======== highlight on index ============

        lln = LinkedList(
            cll([1, 0, 2, 0, 3, 0, 4, 0, 5]),
            vector=mn.LEFT * 4.8,
        )
        self.play(mn.ReplacementTransform(ll, lln, run_time=0.5))

        rt = RelativeText(
            "pointers()   highlight_containers()",
            mob_center=ll,
            vector=mn.UP * 2,
        )
        rt.first_appear(self)

        lln.pointers([2, 4, 6])
        lln.highlight_containers_1to3([2, 4, 6])
        self.wait(pause)
        lln.pointers([3, 4, 5])
        lln.highlight_containers_1to3([3, 4, 5])
        self.wait(pause)
        lln.pointers([4, 4, 4])
        lln.highlight_containers_1to3([4, 4, 4])
        self.wait(pause)
        lln.pointers([5, 4, 3])
        lln.highlight_containers_1to3([5, 4, 3])
        self.wait(pause)
        lln.pointers([5, 3, 3])
        lln.highlight_containers_1to3([5, 3, 3])
        self.wait(pause)
        lln.pointers([5, 4, 3])
        lln.highlight_containers_1to3([5, 4, 3])
        self.wait(pause)
        lln.pointers([5, 5, 3])
        lln.highlight_containers_1to3([5, 5, 3])
        self.wait(pause)
        lln.pointers([5, 5, 60])
        lln.highlight_containers_1to3([5, 5, 60])
        self.wait(pause)
        lln.clear_containers_highlights()
        lln.clear_pointers_highlights(0)
        self.remove(rt)
        self.wait(1)

        # ======== highlight on value ============

        ll = LinkedList(
            cll([10, 2, 3000, 2, 100, 2, 40]),
            vector=mn.LEFT * 4,
        )
        self.play(mn.ReplacementTransform(lln, ll, run_time=0.5))

        rt = RelativeText(
            "highlight_containers_with_value()   pointers_on_value()",
            vector=mn.UP * 2,
        )
        rt.first_appear(self)
        self.wait(pause)

        ll.highlight_containers_with_value(2)
        ll.pointers_on_value(2)
        self.wait(pause)
        ll.update_value(self, cll([22, 0, 22, 0, 22, 0]))
        ll.highlight_containers_with_value(0)
        ll.pointers_on_value(0)
        self.wait(pause)
        ll.update_value(self, cll([0, 22, 0, 22, 0, 22]))
        ll.highlight_containers_with_value(0, color=mn.LIGHT_BROWN)
        ll.pointers_on_value(0, color=mn.LIGHT_BROWN)
        self.wait(pause)
        ll.update_value(self, cll([22, 0, 22, 0, 22, 0]), animate=True)
        ll.highlight_containers_with_value(0, color=mn.LIGHT_BROWN)
        ll.pointers_on_value(0, color=mn.LIGHT_BROWN)
        self.wait(pause)
        ll.update_value(self, cll([0, 22, 0, 22, 0, 22]), animate=True)
        ll.highlight_containers_with_value(0, color=mn.PURPLE)
        ll.pointers_on_value(0, color=mn.PURPLE)
        self.wait(pause)
        ll.update_value(self, cll([22, 0, 22, 0, 22]), animate=True)
        ll.highlight_containers_with_value(0, color=mn.PURPLE)
        ll.pointers_on_value(0, color=mn.PURPLE)
        self.wait(pause)
        ll.update_value(self, cll([0, 22, 0, 22, 0, 22]), animate=True)
        ll.highlight_containers_with_value(0, color=mn.PINK)
        ll.pointers_on_value(0, color=mn.PINK)
        self.wait(pause)
        ll.update_value(self, cll([22, 0, 22, 0, 22]), animate=True)
        ll.highlight_containers_with_value(0, color=mn.PINK)
        ll.pointers_on_value(0, color=mn.PINK)
        self.wait(1)

        # ========== FINISH ==============

        self.wait(pause)
        self.renderer.file_writer.output_file = f"./{self.__class__.__name__}.mp4"


class ExampleCodeblock(mn.Scene):
    def construct(self):
        self.camera.background_color = mn.DARK_GREY  # type: ignore
        pause = 1

        # ======== INPUTS ============

        pre_code_lines = [
            "This is pre_code_lines.",
            "They have the same..",
            "..functionality.",
        ]

        code_lines = [
            "This is code_lines.",  # 0
            "It is possible to highlight them",  # 1
            "one by one,",  # 2
            "or",  # 3
            "│",  # 4
            "several",  # 5
            "│",  # 6
            "at once.",  # 7
            "When highlight(...) calls,",  # 8
            "or calls without args,",  # 9
            "the old highlight clears.",  # 10
        ]

        # ======== main mob ============

        # Construction code_block
        cb = CodeBlock(
            code_lines,
            pre_code_lines=pre_code_lines,
            vector=mn.RIGHT * 3 + mn.DOWN * 0.5,
            font_size=25,
        )
        # Animation code_block
        cb.first_appear(self)

        # ======== highlight line ============

        title = RelativeText(
            "highlight()",
            vector=mn.UP * 3.2 + mn.LEFT * 5.0,
            font_size=30,
        )
        title.first_appear(self)
        self.wait(pause)

        def highlight_with_title(
            self: mn.Scene,
            code_block: CodeBlock,
            old_title: mn.Mobject,
            *code_indices: int,
            precode: tuple[int, ...] | None = None,
            pause=2,
        ):
            code_block.highlight(*code_indices, precode_indices=precode)

            left_point = old_title.get_left()
            self.remove(old_title)

            args_str = f"({', '.join(map(str, code_indices))}"
            if precode:
                args_str += f", precode_indices={precode}"
            args_str += ")"

            new_title = RelativeText(
                f"highlight{args_str}",
                font_size=30,
            )
            vector = left_point - new_title.get_left()
            new_title.shift(vector)
            new_title.appear(self)
            self.wait(pause)
            return new_title

        title = highlight_with_title(self, cb, title, 0)
        title = highlight_with_title(self, cb, title, 1)
        title = highlight_with_title(self, cb, title, 2)
        title = highlight_with_title(self, cb, title, 3, 5, 7, pause=3)
        title = highlight_with_title(self, cb, title, 8, 9, 10, pause=3)
        title = highlight_with_title(self, cb, title, precode=(0,))
        title = highlight_with_title(self, cb, title, precode=(1, 2))
        title = highlight_with_title(self, cb, title, 1, 3, 5, 7, 9, precode=(0, 2))
        title = highlight_with_title(self, cb, title, 0, 2, 4, 6, 8, 10, precode=(1,))

        # ========== FINISH ==============

        self.wait(pause)
        self.renderer.file_writer.output_file = f"./{self.__class__.__name__}.mp4"
