"""
Example scenes demonstrating algomanim functionality and serving as visual tests.

This module contains Example classes that:
  - Showcase algomanim features in action
  - Serve as visual tests to verify classes work correctly
  - Help identify rendering issues on different systems

Note: Uses default Manim fonts. For better visual results, consider installing
and specifying custom fonts in the scene configurations.
"""

import manim as mn

import numpy as np
from algomanim import (
    Array,
    String,
    RelativeTextValue,
    RelativeText,
    CodeBlock,
    TitleText,
)

# from algomanim import utils
from algomanim.algomanim import LinkedList


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
        array.highlight_containers([i, j, k])

        # ======== PRE-CYCLE =============

        self.wait(pause)

        # ===== ALGORITHM CYCLE ==========

        for i in range(len(arr)):
            code_block.highlight_line(0)
            bubble -= 1
            array.pointers([i, j, k])
            array.highlight_containers([i, j, k])
            top_text.update_text(self)
            self.wait(pause)

            for j in range(n - i - 1):
                code_block.highlight_line(1)
                array.pointers([i, j, k])
                array.highlight_containers([i, j, k])
                array.pointers_on_value(bubble, color=mn.WHITE)
                top_text.update_text(self)
                bottom_text.update_text(self, animate=False)
                self.wait(pause)

                k = j + 1
                code_block.highlight_line(2)
                array.pointers([i, j, k])
                array.highlight_containers([i, j, k])
                top_text.update_text(self)
                self.wait(pause)

                code_block.highlight_line(3)
                self.wait(pause)
                if arr[j] > arr[k]:
                    arr[j], arr[k] = arr[k], arr[j]
                    code_block.highlight_line(4)
                    array.update_value(self, arr, animate=False)
                    array.pointers_on_value(bubble, color=mn.WHITE)
                    array.pointers([i, j, k])
                    array.highlight_containers([i, j, k])
                    top_text.update_text(self)
                    self.wait(pause)

        # ========== FINISH ==============

        self.wait(pause)
        self.renderer.file_writer.output_file = f"media/{self.__class__.__name__}.mp4"


class ExampleArray(mn.Scene):
    def construct(self):
        self.camera.background_color = mn.GREY  # type: ignore
        pause = 0.5

        # ======== INPUTS ============

        arr = [0, "\"'`^", "ace", "ygpj", "ABC", ":*#", "."]

        # ============================

        array = Array(arr)
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

        top_text = RelativeText(
            "update_value()",
            vector=mn.UP * 2,
        )
        top_text.first_appear(self)

        array.update_value(self, [1, 12, 123, 1234, 12345, 123456], left_aligned=False)
        array.pointers([0, 1, 2])
        array.highlight_containers([0, 1, 2])
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
        array.highlight_containers([0, 1, 2])
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
            "pointers()   highlight_containers()",
            vector=mn.UP * 2,
        )
        top_text.first_appear(self)

        array.update_value(self, [10, 2, 3000, 2, 100, 1, 40], left_aligned=False)
        self.wait(1)
        array.pointers([0, 3, 6])
        array.highlight_containers([0, 3, 6])
        self.wait(pause)
        array.pointers([1, 3, 5])
        array.highlight_containers([1, 3, 5])
        self.wait(pause)
        array.pointers([2, 3, 4])
        array.highlight_containers([2, 3, 4])
        self.wait(pause)
        array.pointers([3, 3, 3])
        array.highlight_containers([3, 3, 3])
        self.wait(pause)
        array.pointers([2, 3, 4])
        array.highlight_containers([2, 3, 4])
        self.wait(pause)
        array.pointers([2, 2, 4])
        array.highlight_containers([2, 2, 4])
        self.wait(pause)
        array.pointers([2, 3, 4])
        array.highlight_containers([2, 3, 4])
        self.wait(pause)
        array.pointers([2, 4, 4])
        array.highlight_containers([2, 4, 4])
        self.wait(pause)
        array.pointers([2, 4, 3])
        array.highlight_containers([2, 4, 3])
        self.wait(pause)
        array.pointers([2, 4, 2])
        array.highlight_containers([2, 4, 2])
        self.wait(1)
        self.remove(top_text)
        array.clear_pointers_highlights(0)
        array.clear_containers_highlights()

        # ============================

        top_text = RelativeText(
            "highlight_cells_with_value()   pointers_on_value()",
            vector=mn.UP * 2,
        )
        top_text.first_appear(self)

        array.update_value(self, [10, 2, 3000, 2, 100, 1, 40], left_aligned=False)
        self.wait(1)
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
        array.highlight_containers([0, 2, 4])
        array.pointers([0, 2, 4])
        # array.highlight_cells_with_value(0, color=mn.PINK)
        array.pointers_on_value(0, color=mn.PINK)
        self.wait(pause)

        array.update_value(self, [1, 0, 55555, 333])
        # array.highlight_containers([0, 2, 4])
        # array.pointers([0, 2, 4])
        array.clear_pointers_highlights(0)
        array.highlight_containers_with_value(0, color=mn.PINK)
        array.pointers_on_value(0, color=mn.PINK)
        self.wait(pause)

        array.update_value(self, [0, 333, 0])
        array.highlight_containers([0, 2, 4])
        array.pointers([0, 2, 4])
        # array.highlight_cells_with_value(0, color=mn.PINK)
        array.pointers_on_value(0, color=mn.PINK)
        self.wait(pause)

        array.update_value(self, [0, 0])
        # array.highlight_containers([0, 2, 4])
        # array.pointers([0, 2, 4])
        array.clear_pointers_highlights(0)
        array.highlight_containers_with_value(0, color=mn.PINK)
        array.pointers_on_value(0, color=mn.PINK)
        self.wait(pause)

        array.update_value(self, [0])
        array.highlight_containers([0, 2, 4])
        array.pointers([0, 2, 4])
        # array.highlight_cells_with_value(0, color=mn.PINK)
        array.pointers_on_value(0, color=mn.PINK)
        self.wait(pause)

        array.update_value(self, [], animate=True)
        array.highlight_containers([0, 2, 4])
        array.pointers([0, 2, 4])
        # array.highlight_containers_with_value(0, color=mn.PINK)
        array.pointers_on_value(0, color=mn.PINK)
        self.wait(pause)

        array.update_value(self, [0, 0, 0, 0], animate=True)
        # array.highlight_containers([0, 2, 4])
        # array.pointers([0, 2, 4])
        # array.highlight_cells_with_value(0, color=mn.PINK)
        # array.pointers_on_value(0, color=mn.PINK)
        self.wait(pause)

        array.update_value(self, [1, 0, 22, 0, 333, 0], animate=True)
        # array.highlight_containers([0, 1, 2])
        # array.pointers([0, 1, 2])
        array.clear_pointers_highlights(0)
        array.highlight_containers_with_value(0, color=mn.PINK)
        array.pointers_on_value(0, color=mn.PINK)
        self.wait(pause)

        array.update_value(self, [0, 22, 0, 333, 0], animate=True)
        array.clear_pointers_highlights(1)
        array.highlight_containers([1, 1, 2])
        array.pointers([1, 1, 2])
        # array.highlight_cells_with_value(0, color=mn.PINK)
        # array.pointers_on_value(0, color=mn.PINK)
        self.wait(pause)

        array.update_value(self, [1, 0, 22, 0, 333, 0, 22], animate=True)
        # array.highlight_containers([0, 2, 2])
        # array.pointers([0, 2, 2])
        array.clear_pointers_highlights(0)
        array.highlight_containers_with_value(0, color=mn.PINK)
        array.pointers_on_value(0, color=mn.PINK)
        self.wait(pause)

        array.update_value(self, [0, 22, 0, 333, 0, 55555], animate=True)
        array.clear_pointers_highlights(1)
        array.highlight_containers([3, 5, 3])
        array.pointers([3, 5, 3])
        # array.highlight_cells_with_value(0, color=mn.PINK)
        # array.pointers_on_value(0, color=mn.PINK)
        self.wait(pause)

        array.update_value(self, [1, 0], animate=True)
        array.highlight_containers([0, 0, 0])
        array.pointers([0, 0, 0])
        # array.highlight_cells_with_value(0, color=mn.PINK)
        # array.pointers_on_value(0, color=mn.PINK)
        self.wait(pause)

        array.update_value(self, [0, 0, 0, 0, 0, 0], animate=True)
        # array.update_value(self, [0, 0, 0, 0, 0, 0], animate=False)
        # array.highlight_containers([9, 9, 9])
        # array.pointers([9, 9, 9])
        array.clear_pointers_highlights(0)
        array.highlight_containers_with_value(0, color=mn.PINK)
        array.pointers_on_value(0, color=mn.PINK)
        self.wait(1)
        # self.remove(top_text)

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

        string = String(s)
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
        string.highlight_containers([4, 5, 6])

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
        string.highlight_containers([4, 5, 6])
        string.highlight_containers([4, 5, 6])
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
        string.highlight_containers([0, 3, 6])
        self.wait(pause)
        string.pointers([1, 3, 5])
        string.highlight_containers([1, 3, 5])
        self.wait(pause)
        string.pointers([2, 3, 4])
        string.highlight_containers([2, 3, 4])
        self.wait(pause)
        string.pointers([3, 3, 3])
        string.highlight_containers([3, 3, 3])
        self.wait(pause)
        string.pointers([2, 3, 4])
        string.highlight_containers([2, 3, 4])
        self.wait(pause)
        string.pointers([2, 2, 4])
        string.highlight_containers([2, 2, 4])
        self.wait(pause)
        string.pointers([2, 3, 4])
        string.highlight_containers([2, 3, 4])
        self.wait(pause)
        string.pointers([2, 4, 4])
        string.highlight_containers([2, 4, 4])
        self.wait(pause)
        string.pointers([2, 4, 3])
        string.highlight_containers([2, 4, 3])
        self.wait(pause)
        string.pointers([2, 40, 2])
        string.highlight_containers([2, 40, 2])
        self.wait(1)
        self.remove(top_text)
        string.clear_pointers_highlights(0)
        string.clear_containers_highlights()

        # ============================

        top_text = RelativeText(
            "highlight_cells_with_value()   pointers_on_value()",
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
        string.highlight_containers([0, 2, 4])
        string.pointers([0, 2, 4])
        # string.pointers_on_value("f", color=mn.PINK)
        # string.highlight_containers_with_value("f", color=mn.PINK)
        self.wait(pause)

        string.update_value(self, "follow the")
        # string.highlight_containers([0, 2, 4])
        # string.pointers([0, 2, 4])
        string.clear_pointers_highlights(0)
        string.pointers_on_value("f", color=mn.PINK)
        string.highlight_containers_with_value("f", color=mn.PINK)
        self.wait(pause)

        string.update_value(self, "follow")
        string.clear_pointers_highlights(1)
        string.highlight_containers([0, 2, 4])
        string.pointers([0, 2, 4])
        # string.highlight_containers_with_value("f", color=mn.PINK)
        # string.pointers_on_value("f", color=mn.PINK)
        self.wait(pause)

        string.update_value(self, "", animate=True)
        # string.highlight_containers([0, 2, 4])
        # string.pointers([0, 2, 4])
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
        string.highlight_containers([0, 1, 2])
        string.pointers([0, 1, 2])
        # string.highlight_containers_with_value("t", color=mn.PINK)
        # string.pointers_on_value("t", color=mn.PINK)
        self.wait(pause)

        string.update_value(self, "rabbit white", left_aligned=False, animate=True)
        # string.highlight_containers([1, 1, 2])
        # string.pointers([1, 1, 2])
        string.clear_pointers_highlights(0)
        string.highlight_containers_with_value("t", color=mn.PINK)
        string.pointers_on_value("t", color=mn.PINK)
        self.wait(pause)

        string.update_value(self, "rabbit the white", left_aligned=False, animate=True)
        string.clear_pointers_highlights(1)
        string.highlight_containers([0, 2, 2])
        string.pointers([0, 2, 2])
        # string.highlight_containers_with_value("t", color=mn.PINK)
        # string.pointers_on_value("t", color=mn.PINK)
        self.wait(pause)

        string.update_value(self, "white the rabbit", animate=True)
        # string.highlight_containers([3, 5, 3])
        # string.pointers([3, 5, 3])
        string.clear_pointers_highlights(0)
        string.pointers_on_value(" ", color=mn.PINK)
        string.highlight_containers_with_value(" ", color=mn.PINK)
        self.wait(pause)

        string.update_value(self, "rab follow rab", animate=True)
        string.highlight_containers([90, 90, 90])
        string.pointers([90, 90, 90])
        string.highlight_containers_with_value("a", color=mn.PINK)
        string.pointers_on_value("a", color=mn.PINK)
        self.wait(1)
        # self.remove(top_text)

        # ========== FINISH ==============

        self.wait(pause)
        self.renderer.file_writer.output_file = f"./{self.__class__.__name__}.mp4"


class ExampleLinkedlist(mn.Scene):
    def construct(self):
        self.camera.background_color = mn.GREY  # type: ignore
        pause = 0.3
        cll = LinkedList.create_linked_list

        # arr = Array([letter for letter in "mob_center"], vector=mn.UP * 3)
        # arr.first_appear(self)

        # ======== rotation ============

        # ll = LinkedList(
        #     cll([0, 1, 2]),
        #     mob_center=arr,
        #     vector=mn.DOWN * 3.5,
        # )
        # ll.appear(self)
        # self.pause(pause)
        #
        # self.remove(ll)
        # ll = LinkedList(
        #     cll([0, 1, 2]),
        #     mob_center=arr,
        #     vector=mn.DOWN * 3.5,
        #     direction=np.array([10, -10, 0]),
        # )
        # ll.appear(self)
        # self.pause(pause)
        #
        # self.remove(ll)
        # ll = LinkedList(
        #     cll([0, 1, 2]),
        #     mob_center=arr,
        #     vector=mn.DOWN * 3.5,
        #     direction=np.array([0, -10, 0]),
        # )
        # ll.appear(self)
        # self.pause(pause)
        #
        # self.remove(ll)
        # ll = LinkedList(
        #     cll([0, 1, 2]),
        #     mob_center=arr,
        #     vector=mn.DOWN * 3.5,
        #     direction=np.array([-10, -10, 0]),
        # )
        # ll.appear(self)
        # self.pause(pause)
        #
        # self.remove(ll)
        # ll = LinkedList(
        #     cll([0, 1, 2]),
        #     mob_center=arr,
        #     vector=mn.DOWN * 3.5,
        #     direction=np.array([-10, 0, 0]),
        # )
        # ll.appear(self)
        # self.pause(pause)
        #
        # self.remove(ll)
        # ll = LinkedList(
        #     cll([0, 1, 2]),
        #     mob_center=arr,
        #     vector=mn.DOWN * 3.5,
        #     direction=np.array([-10, 10, 0]),
        # )
        # ll.appear(self)
        # self.pause(pause)
        #
        # self.remove(ll)
        # ll = LinkedList(
        #     cll([0, 1, 2]),
        #     mob_center=arr,
        #     vector=mn.DOWN * 3.5,
        #     direction=np.array([0, 10, 0]),
        # )
        # ll.appear(self)
        # self.pause(pause)
        #
        # self.remove(ll)
        # ll = LinkedList(
        #     cll([0, 1, 2]),
        #     mob_center=arr,
        #     vector=mn.DOWN * 3.5,
        #     direction=np.array([10, 10, 0]),
        # )
        # ll.appear(self)
        # self.pause(pause)
        #
        # self.remove(ll)
        # ll = LinkedList(
        #     cll([0, 1, 2]),
        #     mob_center=arr,
        #     vector=mn.DOWN * 3.5,
        # )
        # ll.appear(self)
        # self.pause(1)
        # self.remove(ll)

        # ======== left | right alignment ============

        # ll1 = LinkedList(
        #     cll([0, 1, 2]),
        #     mob_center=arr,
        #     vector=mn.DOWN * 2,
        #     align_edge="right",
        # )
        # ll2 = LinkedList(
        #     cll([0, 1, 2]),
        #     mob_center=arr,
        #     vector=mn.DOWN * 2,
        #     align_edge="left",
        # )
        #
        # rt1 = RelativeText(
        #     "align_edge=right",
        #     mob_center=ll1,
        #     vector=mn.DOWN * 2,
        # )
        # rt2 = RelativeText(
        #     "align_edge=left",
        #     mob_center=ll2,
        #     vector=mn.DOWN * 2,
        # )
        #
        # self.play(
        #     mn.FadeIn(ll1),
        #     mn.FadeIn(ll2),
        #     mn.FadeIn(rt1),
        #     mn.FadeIn(rt2),
        #     run_time=0.5,
        # )
        #
        # self.pause(1)
        # self.remove(ll1, ll2, rt1, rt2)

        # ======== up | down alignment ============

        # self.play(arr.animate.move_to(mn.ORIGIN))
        #
        # ll1 = LinkedList(
        #     cll([0, 1]),
        #     radius=0.8,
        #     mob_center=arr,
        #     vector=mn.LEFT * 5.3,
        #     align_edge="up",
        #     direction=mn.UP,
        # )
        # ll2 = LinkedList(
        #     cll([0, 1]),
        #     radius=0.8,
        #     mob_center=arr,
        #     vector=mn.RIGHT * 5.3,
        #     align_edge="down",
        #     direction=mn.UP,
        # )
        #
        # rt1 = RelativeText(
        #     "align_edge=up",
        #     mob_center=ll1,
        #     vector=mn.DOWN * 3,
        #     align_edge="left",
        # )
        # rt2 = RelativeText(
        #     "align_edge=down",
        #     mob_center=ll2,
        #     vector=mn.DOWN * 3.9,
        #     align_edge="right",
        # )
        #
        # self.play(
        #     mn.FadeIn(ll1),
        #     mn.FadeIn(ll2),
        #     mn.FadeIn(rt1),
        #     mn.FadeIn(rt2),
        #     run_time=0.5,
        # )
        #
        # self.pause(1)
        # self.clear()

        # ======== update value ============

        pause = 0.5

        ll = LinkedList(
            cll([0, 12, 12345, "'", '^"', ".", "_.,", "Aa", "acv", "gjy", "gyp"]),
            direction=np.array([10, 2, 0]),
            vector=mn.LEFT * 5.85 + mn.DOWN * 2,
        )

        ll.highlight_containers([0, 2, 4])
        ll.pointers([0, 2, 4])

        rt = RelativeText(
            "update_value()",
            mob_center=ll,
            vector=mn.UP * 3,
        )

        self.play(mn.FadeIn(ll), mn.FadeIn(rt))
        self.pause(pause)

        ll.update_value(
            self,
            cll([0, 12, 12345, "'", '^"', ".", "_.,", "Aa"]),
        )
        self.pause(pause)
        ll.update_value(
            self,
            cll([0, 12, 12345, "'", '^"']),
        )
        self.pause(pause)
        ll.update_value(
            self,
            cll([0, 12]),
        )
        self.pause(pause)
        ll.update_value(self, cll([0]))
        self.pause(pause)
        ll.update_value(self, cll([]))
        self.pause(pause)
        ll.update_value(
            self,
            cll([0]),
            animate=True,
        )
        self.pause(pause)
        ll.update_value(
            self,
            cll([0, 12]),
            animate=True,
        )
        self.pause(pause)
        ll.update_value(
            self,
            cll([0, 12, 12345, "'", '^"']),
            animate=True,
        )
        self.pause(pause)
        ll.update_value(
            self,
            cll([0, 12, 12345, "'", '^"', ".", "_.,", "Aa"]),
            animate=True,
        )
        self.pause(pause)
        ll.update_value(
            self,
            cll([0, 12, 12345, "'", '^"', ".", "_.,", "Aa", "acv", "gjy", "gyp"]),
            animate=True,
        )
        self.pause(1)
        self.remove(rt)

        # ======== highlight on index ============

        lln = LinkedList(
            cll([1, 0, 2, 0, 3, 0, 4, 0, 5]),
            vector=mn.LEFT * 4.8,
        )
        self.play(mn.ReplacementTransform(ll, lln, time=0.5))

        rt = RelativeText(
            "pointers()   highlight_containers()",
            mob_center=ll,
            vector=mn.UP * 2,
        )
        rt.first_appear(self)

        lln.pointers([2, 4, 6])
        lln.highlight_containers([2, 4, 6])
        self.pause(pause)
        lln.pointers([3, 4, 5])
        lln.highlight_containers([3, 4, 5])
        self.pause(pause)
        lln.pointers([4, 4, 4])
        lln.highlight_containers([4, 4, 4])
        self.pause(pause)
        lln.pointers([5, 4, 3])
        lln.highlight_containers([5, 4, 3])
        self.pause(pause)
        lln.pointers([5, 3, 3])
        lln.highlight_containers([5, 3, 3])
        self.pause(pause)
        lln.pointers([5, 4, 3])
        lln.highlight_containers([5, 4, 3])
        self.pause(pause)
        lln.pointers([5, 5, 3])
        lln.highlight_containers([5, 5, 3])
        self.pause(pause)
        lln.pointers([5, 5, 60])
        lln.highlight_containers([5, 5, 60])
        self.pause(1)

        # ======== highlight on value ============

        # ======== mix ============

        # ll_2 = LinkedList(
        #     cll([0, 1, 2]),
        #     direction=np.array([-1, 0, 0]),
        #     mob_center=arr,
        #     vector=mn.DOWN * 3.5,
        #     align_edge="right",
        # )

        # self.play(mn.FadeIn(ll_1), mn.FadeIn(ll_2), run_time=0.5)

        # linked_list = cll(
        #     [0, 12, 12345, "'", '^"', ".", "_.,", "Aa", "acv", "gjy", "gyp"]
        # )

        # ll = LinkedList(
        #     [0, 12, 12345, "'", '^"', ".", "_.,", "Aa", "acv", "gjy", "gyp"],
        #     radius=0.4,
        #     # direction=mn.RIGHT + mn.DOWN,
        #     direction=np.array([-100, 40, 0]),
        #     vector=mn.LEFT * 3 + mn.UP * 2,
        # )

        # ll.first_appear(self)
        # ll.pointers([3, 5, 7])
        # ll.highlight_containers([3, 5, 7])

        # ll.update_value(self, [12345, "'", '^"', ".", "_.,", "Aa", "acv", "gjy", "gyp"])
        # self.pause(pause)
        # ll.update_value(self, [".", "_.,", "Aa", "acv", "gjy", "gyp"])

        # ========== FINISH ==============

        self.wait(pause)
        self.renderer.file_writer.output_file = f"./{self.__class__.__name__}.mp4"
