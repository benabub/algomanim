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
            vector=mn.LEFT * 4.1 + mn.DOWN * 0.35,
            font_size=40,
            # font=Vars.font,
        )
        # Animation
        array.first_appear(self)

        # ========== CODE BLOCK ============

        code = """
for i in range(len(arr)):
    for j in range(len(arr) - i - 1):
        k = j + 1
    if arr[j] > arr[k]:
        arr[j], arr[k] = arr[k], arr[j]
"""
        code_lines = CodeBlock.format_code_lines(code)

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

        # ========== TEXT MOBS ============

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

        # ========== finish ==============

        self.wait(pause)
        self.renderer.file_writer.output_file = f"media/{self.__class__.__name__}.mp4"


class ExampleArray(mn.Scene):
    def construct(self):
        self.camera.background_color = mn.GREY  # type: ignore

        def pyramid(self):
            arr = [0, "\"'`^", "ace", "ygpj", "ABC", ":*#", "."]

            array = Array(
                arr,
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

            self.remove(
                array_20,
                array_30,
                array_40,
                array_50,
            )

            # ============================

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

            self.remove(
                array_20,
                array_30,
                array_40,
                array_50,
            )

            # ============================

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

        def positioning(self):
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

        def updatevalue(self):
            pause = 1
            center = Array(list("mob_center"), font_size=50)
            text_title = RelativeText(
                "update_value()",
                vector=mn.LEFT * 4.4 + mn.UP * 3.2,
                text_color=mn.BLACK,
                font_size=50,
            )
            center.group_appear(self, text_title)

            arr_1 = Array(
                [1, 2, 3],
                mob_center=center,
                vector=mn.UP * 1.5,
                anchor=None,
                pointers=False,
            )
            arr_2 = Array(
                [1, 2, 3],
                mob_center=arr_1,
                vector=mn.UP * 0.7,
                anchor=mn.RIGHT,
                pointers=False,
            )
            arr_3 = Array(
                [1, 2, 3],
                mob_center=arr_2,
                vector=mn.UP * 0.7,
                anchor=mn.LEFT,
                pointers=False,
            )

            text_no_align = RelativeText(
                "no align_sides:", align_bottom=arr_2, vector=mn.LEFT * 4.6
            )
            text_arr_1 = RelativeText(
                "anchor=None", mob_center=arr_1, vector=mn.RIGHT * 4.0
            )
            text_arr_2 = RelativeText(
                "anchor=mn.RIGHT", mob_center=arr_2, vector=mn.RIGHT * 4.6
            )
            text_arr_3 = RelativeText(
                "anchor=mn.LEFT", mob_center=arr_3, vector=mn.RIGHT * 4.4
            )

            arr_4 = Array(
                [1, 2, 3],
                align_left=center,
                vector=mn.DOWN * 1.5,
                pointers=False,
            )
            arr_5 = Array(
                [1, 2, 3],
                align_right=center,
                vector=mn.DOWN * 1.5,
                pointers=False,
            )

            text_arr_4 = RelativeText(
                "align_left=center",
                align_left=arr_4,
                mob_center=arr_4,
                vector=mn.DOWN * 1.0,
            )
            text_arr_5 = RelativeText(
                "align_right=center",
                align_right=arr_5,
                mob_center=arr_5,
                vector=mn.DOWN * 1.0,
            )

            arr_1.group_appear(
                self,
                arr_2,
                arr_3,
                arr_4,
                arr_5,
                text_no_align,
                text_arr_1,
                text_arr_2,
                text_arr_3,
                text_arr_4,
                text_arr_5,
            )
            self.wait(2)

            arr_1.highlight_containers_1to3([0, 1, 2])
            arr_2.highlight_containers_1to3([0, 1, 2])
            arr_3.highlight_containers_1to3([0, 1, 2])
            arr_4.highlight_containers_1to3([0, 1, 2])
            arr_5.highlight_containers_1to3([0, 1, 2])
            self.wait(pause)

            arr = [1, 2]
            arr_1.update_value(self, arr)
            arr_2.update_value(self, arr)
            arr_3.update_value(self, arr)
            arr_4.update_value(self, arr)
            arr_5.update_value(self, arr)
            self.wait(pause)

            arr = [1]
            arr_1.update_value(self, arr)
            arr_2.update_value(self, arr)
            arr_3.update_value(self, arr)
            arr_4.update_value(self, arr)
            arr_5.update_value(self, arr)
            self.wait(pause)

            arr = []
            arr_1.update_value(self, arr)
            arr_2.update_value(self, arr)
            arr_3.update_value(self, arr)
            arr_4.update_value(self, arr)
            arr_5.update_value(self, arr)
            self.wait(pause)

            arr = [1]
            arr_1.update_value(self, arr)
            arr_2.update_value(self, arr)
            arr_3.update_value(self, arr)
            arr_4.update_value(self, arr)
            arr_5.update_value(self, arr)
            self.wait(pause)

            arr = [1, 2]
            arr_1.update_value(self, arr)
            arr_2.update_value(self, arr)
            arr_3.update_value(self, arr)
            arr_4.update_value(self, arr)
            arr_5.update_value(self, arr)
            self.wait(pause)

            arr = [1, 2, 3]
            arr_1.update_value(self, arr)
            arr_2.update_value(self, arr)
            arr_3.update_value(self, arr)
            arr_4.update_value(self, arr)
            arr_5.update_value(self, arr)
            self.wait(pause)

            arr = [1, 2, 3, 4]
            arr_1.update_value(self, arr)
            arr_2.update_value(self, arr)
            arr_3.update_value(self, arr)
            arr_4.update_value(self, arr)
            arr_5.update_value(self, arr)
            self.wait(pause)

            self.clear()

        def highlights_1to3(self):
            pause = 0.5

            array = Array([10, 2, 3000, 2, 100, 1, 40])
            top_text = RelativeText(
                "pointers()   highlight_containers_1to3()",
                vector=mn.UP * 2,
            )
            array.group_appear(self, top_text)
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

            self.clear()

        def monocolor(self):
            pause = 0.5
            array = Array([1, 2, 3, 4, 5, 6, 7, 8, 9])
            top_text = RelativeText(
                "highlight_containers_monocolor()",
                vector=mn.UP * 2,
            )
            array.group_appear(self, top_text)
            self.wait(1)

            array.highlight_containers_monocolor([0, 2, 4, 6, 8])
            self.wait(pause)
            array.highlight_containers_monocolor([0, 1, 2, 3, 4])
            self.wait(pause)
            array.highlight_containers_monocolor([5, 6, 7, 8])
            self.wait(pause)
            self.remove(top_text)
            array.clear_containers_highlights()

            self.clear()

        def highlight_on_value(self):
            pause = 0.5
            array = Array([10, 2, 3000, 2, 100, 1, 40])
            top_text = RelativeText(
                "highlight_containers_with_value()   pointers_on_value()",
                vector=mn.UP * 2,
            )
            array.group_appear(self, top_text)
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

            self.clear()

        def mix(self):
            pause = 0.5
            array = Array([0, 1, 22, 333, 4444, 55555])
            top_text = RelativeText(
                "mix",
                vector=mn.UP * 2,
            )
            array.group_appear(self, top_text)
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

        # ========== calls ==============

        pyramid(self)
        positioning(self)
        updatevalue(self)
        highlights_1to3(self)
        monocolor(self)
        highlight_on_value(self)
        mix(self)

        # ========== finish ==============

        self.wait(1)
        self.renderer.file_writer.output_file = f"./{self.__class__.__name__}.mp4"


class ExampleString(mn.Scene):
    def construct(self):
        self.camera.background_color = mn.GREY  # type: ignore

        def pyramid(self):
            s = "0agA-/*&.^`~"
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
                align_left=string,
            )
            string_20.first_appear(self, time=0.1)

            string_25 = String(
                s,
                mob_center=string,
                vector=mn.UP * 1.4,
                font_size=30,
                align_left=string,
            )
            string_25.first_appear(self, time=0.1)

            string_35 = String(
                s,
                mob_center=string,
                vector=mn.DOWN * 1.5,
                font_size=37,
                align_left=string,
            )
            string_35.first_appear(self, time=0.1)

            string_40 = String(
                s,
                mob_center=string,
                vector=mn.DOWN * 3.0,
                font_size=40,
                align_left=string,
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
                align_right=string,
            )
            string_20.first_appear(self, time=0.1)

            string_25 = String(
                s,
                mob_center=string,
                vector=mn.UP * 1.4,
                font_size=30,
                align_right=string,
            )
            string_25.first_appear(self, time=0.1)

            string_35 = String(
                s,
                mob_center=string,
                vector=mn.DOWN * 1.5,
                font_size=37,
                align_right=string,
            )
            string_35.first_appear(self, time=0.1)

            string_40 = String(
                s,
                mob_center=string,
                vector=mn.DOWN * 3.0,
                font_size=40,
                align_right=string,
            )
            string_40.first_appear(self, time=0.1)

            self.wait(1)
            self.clear()

        def positioning(self):
            pause = 1
            string = "str"

            center = String("mob_center", font_size=40)
            center.first_appear(self)

            top_text = RelativeText(
                "mob_center=mob_center\nvector=mn.UP * 1",
                vector=mn.DOWN * 2 + mn.RIGHT * 0,
            )
            s = String(string, mob_center=center, vector=mn.UP * 2)
            s.group_appear(self, top_text)
            self.wait(pause)

            self.remove(s, top_text)

            top_text = RelativeText(
                "mob_center=mob_center\nalign_left=mob_center\nvector=mn.UP * 1",
                vector=mn.DOWN * 2 + mn.RIGHT * 0,
            )
            s = String(string, mob_center=center, align_left=center, vector=mn.UP * 2)
            s.group_appear(self, top_text)
            self.wait(pause)

            self.remove(s, top_text)

            top_text = RelativeText(
                "mob_center=mob_center\nalign_right=mob_center\nvector=mn.UP * 1",
                vector=mn.DOWN * 2 + mn.RIGHT * 0,
            )
            s = String(string, mob_center=center, align_right=center, vector=mn.UP * 2)
            s.group_appear(self, top_text)
            self.wait(pause)

            self.clear()

            one = String("one", font_size=60, vector=mn.UP * 2.7 + mn.LEFT * 4)
            two = String("two", font_size=60, vector=mn.DOWN * 2.4 + mn.RIGHT * 3)
            one.group_appear(self, two)
            self.wait(pause)

            # -----------------------

            top_text = RelativeText(
                "align_left=one\nalign_bottom=two",
                vector=mn.UP * 1 + mn.RIGHT * 2,
            )
            s = String(string, align_left=one, align_bottom=two)
            s.group_appear(self, top_text)
            self.wait(pause)
            self.remove(s, top_text)

            top_text = RelativeText(
                "align_left=one\nalign_top=two",
                vector=mn.UP * 1 + mn.RIGHT * 2,
            )
            s = String(string, align_left=one, align_top=two)
            s.group_appear(self, top_text)
            self.wait(pause)
            self.remove(s, top_text)

            top_text = RelativeText(
                "align_right=one\nalign_top=two",
                vector=mn.UP * 1 + mn.RIGHT * 2,
            )
            s = String(string, align_right=one, align_top=two)
            s.group_appear(self, top_text)
            self.wait(pause)
            self.remove(s, top_text)

            top_text = RelativeText(
                "align_right=one\nalign_bottom=two",
                vector=mn.UP * 1 + mn.RIGHT * 2,
            )
            s = String(string, align_right=one, align_bottom=two)
            s.group_appear(self, top_text)
            self.wait(pause)
            self.remove(s, top_text)

            top_text = RelativeText(
                "align_left=one\nalign_bottom=two\nvector=mn.UP * 1 + mn.RIGHT * 1",
                vector=mn.UP * 0.7 + mn.RIGHT * 2,
            )
            s = String(
                string,
                align_left=one,
                align_bottom=two,
                vector=mn.UP * 1 + mn.RIGHT * 1,
            )
            s.group_appear(self, top_text)
            self.wait(pause)
            self.clear()

        def updatevalue(self):
            pause = 0.5
            string = String("follow the rabbit")
            string.first_appear(self)

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

        def highlights_1to3(self):
            pause = 0.5
            string = String("follow the rabbit")
            top_text = RelativeText(
                "pointers()   highlight_containers()",
                vector=mn.UP * 2,
            )
            string.group_appear(self, top_text)
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
            self.clear()

        def highlight_on_value(self):
            pause = 0.5
            string = String("follow the rabbit")
            top_text = RelativeText(
                "highlight_containers_with_value()   pointers_on_value()",
                vector=mn.UP * 2,
            )
            string.group_appear(self, top_text)
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
            self.clear()

        def mix(self):
            pause = 0.5
            string = String("follow the rabbit")
            top_text = RelativeText(
                "mix",
                vector=mn.UP * 2,
            )
            string.group_appear(self, top_text)
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

            string.update_value(
                self, "rabbit the white", left_aligned=False, animate=True
            )
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

        # ========== calls ==============

        pyramid(self)
        positioning(self)
        updatevalue(self)
        highlights_1to3(self)
        highlight_on_value(self)
        mix(self)

        # ========== finish ==============

        self.wait(1)
        self.renderer.file_writer.output_file = f"./{self.__class__.__name__}.mp4"


class ExampleLinkedlist(mn.Scene):
    def construct(self):
        self.camera.background_color = mn.GREY  # type: ignore

        cll = LinkedList.create_linked_list

        # ============================

        pause = 1

        center = Array(list("mob_center"), font_size=40)
        center.first_appear(self)

        top_text = RelativeText(
            "mob_center=mob_center\nvector=mn.UP * 2",
            vector=mn.DOWN * 2 + mn.RIGHT * 0,
        )
        ll = LinkedList(
            cll([0, 1]),
            mob_center=center,
            vector=mn.UP * 2,
        )
        ll.group_appear(self, top_text)
        self.wait(pause)

        self.remove(ll, top_text)

        top_text = RelativeText(
            "mob_center=mob_center\nalign_left=mob_center\nvector=mn.UP * 2",
            vector=mn.DOWN * 2 + mn.RIGHT * 0,
        )
        ll = LinkedList(
            cll([0, 1]),
            mob_center=center,
            align_left=center,
            vector=mn.UP * 2,
        )
        ll.group_appear(self, top_text)
        self.wait(pause)

        self.remove(ll, top_text)

        top_text = RelativeText(
            "mob_center=mob_center\nalign_right=mob_center\nvector=mn.UP * 2",
            vector=mn.DOWN * 2 + mn.RIGHT * 0,
        )
        ll = LinkedList(
            cll([0, 1]),
            mob_center=center,
            align_right=center,
            vector=mn.UP * 2,
        )
        ll.group_appear(self, top_text)
        self.wait(pause)

        self.clear()

        one = Array(list("one"), font_size=60, vector=mn.UP * 2.7 + mn.LEFT * 4)
        two = Array(list("two"), font_size=60, vector=mn.DOWN * 2.4 + mn.RIGHT * 3)
        one.group_appear(self, two)
        self.wait(0.5)

        # -----------------------

        top_text = RelativeText(
            "align_left=one\nalign_bottom=two",
            vector=mn.UP * 1 + mn.RIGHT * 2,
        )
        ll = LinkedList(
            cll([0, 1]),
            align_left=one,
            align_bottom=two,
        )
        ll.group_appear(self, top_text)
        self.wait(pause)
        self.remove(ll, top_text)

        top_text = RelativeText(
            "align_left=one\nalign_top=two",
            vector=mn.UP * 1 + mn.RIGHT * 2,
        )
        ll = LinkedList(
            cll([0, 1]),
            align_left=one,
            align_top=two,
        )
        ll.group_appear(self, top_text)
        self.wait(pause)
        self.remove(ll, top_text)

        top_text = RelativeText(
            "align_right=one\nalign_top=two",
            vector=mn.UP * 1 + mn.RIGHT * 2,
        )
        ll = LinkedList(
            cll([0, 1]),
            align_right=one,
            align_top=two,
        )
        ll.group_appear(self, top_text)
        self.wait(pause)
        self.remove(ll, top_text)

        top_text = RelativeText(
            "align_right=one\nalign_bottom=two",
            vector=mn.UP * 1 + mn.RIGHT * 2,
        )
        ll = LinkedList(
            cll([0, 1]),
            align_right=one,
            align_bottom=two,
        )
        ll.group_appear(self, top_text)
        self.wait(pause)
        self.remove(ll, top_text)

        top_text = RelativeText(
            "align_left=one\nalign_bottom=two\nvector=mn.UP * 1 + mn.RIGHT * 1",
            vector=mn.UP * 0.7 + mn.RIGHT * 2,
        )
        ll = LinkedList(
            cll([0, 1]),
            align_left=one,
            align_bottom=two,
            vector=mn.UP * 1 + mn.RIGHT * 1,
        )
        ll.group_appear(self, top_text)
        self.wait(pause)
        self.clear()

        # ======== rotation ============

        pause = 0.3
        cll = LinkedList.create_linked_list

        arr = Array(list("mob_center"), vector=mn.UP * 3)
        arr.first_appear(self)

        ll = LinkedList(
            cll([0, 1, 2]),
            mob_center=arr,
            vector=mn.DOWN * 3.5,
        )
        ll.appear(self)
        ll.pointers([0, 1, 2])
        self.wait(pause)

        self.remove(ll)
        ll = LinkedList(
            cll([0, 1, 2]),
            mob_center=arr,
            vector=mn.DOWN * 3.5,
            direction=np.array([10, -10, 0]),
        )
        ll.appear(self)
        ll.pointers([0, 1, 2])
        self.wait(pause)

        self.remove(ll)
        ll = LinkedList(
            cll([0, 1, 2]),
            mob_center=arr,
            vector=mn.DOWN * 3.5,
            direction=np.array([0, -10, 0]),
        )
        ll.appear(self)
        ll.pointers([0, 1, 2])
        self.wait(pause)

        self.remove(ll)
        ll = LinkedList(
            cll([0, 1, 2]),
            mob_center=arr,
            vector=mn.DOWN * 3.5,
            direction=np.array([-10, -10, 0]),
        )
        ll.appear(self)
        ll.pointers([0, 1, 2])
        self.wait(pause)

        self.remove(ll)
        ll = LinkedList(
            cll([0, 1, 2]),
            mob_center=arr,
            vector=mn.DOWN * 3.5,
            direction=np.array([-10, 0, 0]),
        )
        ll.appear(self)
        ll.pointers([0, 1, 2])
        self.wait(pause)

        self.remove(ll)
        ll = LinkedList(
            cll([0, 1, 2]),
            mob_center=arr,
            vector=mn.DOWN * 3.5,
            direction=np.array([-10, 10, 0]),
        )
        ll.appear(self)
        ll.pointers([0, 1, 2])
        self.wait(pause)

        self.remove(ll)
        ll = LinkedList(
            cll([0, 1, 2]),
            mob_center=arr,
            vector=mn.DOWN * 3.5,
            direction=np.array([0, 10, 0]),
        )
        ll.appear(self)
        ll.pointers([0, 1, 2])
        self.wait(pause)

        self.remove(ll)
        ll = LinkedList(
            cll([0, 1, 2]),
            mob_center=arr,
            vector=mn.DOWN * 3.5,
            direction=np.array([10, 10, 0]),
        )
        ll.appear(self)
        ll.pointers([0, 1, 2])
        self.wait(pause)

        self.remove(ll)
        ll = LinkedList(
            cll([0, 1, 2]),
            mob_center=arr,
            vector=mn.DOWN * 3.5,
        )
        ll.appear(self)
        ll.pointers([0, 1, 2])
        self.wait(1)
        self.remove(ll)

        # ======== left | right alignment ============

        ll1 = LinkedList(
            cll([0, 1, 2]),
            mob_center=arr,
            align_right=arr,
            vector=mn.DOWN * 2,
        )
        ll2 = LinkedList(
            cll([0, 1, 2]),
            mob_center=arr,
            align_left=arr,
            vector=mn.DOWN * 2,
        )

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

        self.play(
            mn.FadeIn(ll1),
            mn.FadeIn(ll2),
            # mn.FadeIn(rt1),
            # mn.FadeIn(rt2),
            run_time=0.5,
        )

        self.wait(1)
        self.remove(
            ll1,
            ll2,
            # rt1,
            # rt2,
        )

        # ======== up | down alignment ============

        self.play(arr.animate.move_to(mn.ORIGIN))

        ll1 = LinkedList(
            cll([0, 1]),
            radius=0.8,
            mob_center=arr,
            align_top=arr,
            vector=mn.LEFT * 5.3,
            direction=mn.UP,
        )
        ll2 = LinkedList(
            cll([0, 1]),
            radius=0.8,
            mob_center=arr,
            align_bottom=arr,
            vector=mn.RIGHT * 5.3,
            direction=mn.UP,
        )

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

        self.play(
            mn.FadeIn(ll1),
            mn.FadeIn(ll2),
            # mn.FadeIn(rt1),
            # mn.FadeIn(rt2),
            run_time=0.5,
        )

        self.wait(1)
        self.clear()

        # ======== update value ============

        pause = 0.5

        ll = LinkedList(
            cll([0, 12, 12345, "'", '^"', ".", "_.,", "Aa", "acv", "gjy", "gyp"]),
            direction=np.array([10, 2, 0]),
            vector=mn.DOWN * 2,
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
            # vector=mn.LEFT * 4.8,
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
            # vector=mn.LEFT * 4,
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

        precode = """
This is precode_lines.
They have the same..
..functionality.
"""
        code = """
This is code_lines.
It is possible to highlight them
one by one,
or
│
several
│
at once.
When highlight(...) calls,
or calls without args,
the old highlight clears.
"""
        precode_lines = CodeBlock.format_code_lines(precode)
        code_lines = CodeBlock.format_code_lines(code)

        # ======== main mob ============

        # Construction code_block
        cb = CodeBlock(
            code_lines,
            pre_code_lines=precode_lines,
            vector=mn.RIGHT * 3 + mn.DOWN * 0.5,
            font_size=25,
        )
        # Animation code_block
        cb.first_appear(self)

        # ======== highlight line ============

        title = RelativeText(
            "highlight(0)",
            vector=mn.UP * 3.2 + mn.LEFT * 5.0,
            font_size=30,
        )
        title.first_appear(self)

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
