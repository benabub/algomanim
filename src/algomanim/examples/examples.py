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
    CodeBlockLense,
    TitleText,
    LinkedList,
)


class Example_selection_sort(mn.Scene):
    def construct(self):
        self.camera.background_color = mn.DARK_GRAY  # type: ignore

        # ======== INPUTS ============

        pause = 1

        arr = [1, 3, 5, 4, 5, 2]
        length = len(arr)
        i = 0
        min_index = i
        k = i + 1

        code = """
length = len(arr)

for i in range(length - 1):
    min_index = i
    for k in range(i + 1, length):
        if arr[min_index] > arr[k]:
            min_index = k
    if min_index != i:
        arr[i], arr[min_index] = arr[min_index], arr[i]
return arr
"""

        # ======== MOBJECTS CONSTRUCTION ============

        title = TitleText(
            "Selection Sort",
            vector=mn.UP * 3.3,
            flourish=True,
        )

        code_block = CodeBlock(
            code,
            vector=mn.DOWN * 0.3 + mn.RIGHT * 2.6,
            font="Monospace",
        )

        length_text = RelativeTextValue(
            ("length", lambda: length, mn.WHITE),
            align_top=code_block,
            vector=mn.LEFT * 5,
        )

        i_text = RelativeTextValue(
            ("i", lambda: i, mn.RED),
            mob_center=length_text,
            align_left=length_text,
            vector=mn.DOWN * 0.7,
        )

        min_text = RelativeTextValue(
            ("min_index", lambda: min_index, mn.BLUE),
            mob_center=i_text,
            align_left=length_text,
            vector=mn.DOWN * 0.7,
        )

        k_text = RelativeTextValue(
            ("k", lambda: k, mn.GREEN),
            mob_center=min_text,
            align_left=length_text,
            vector=mn.DOWN * 0.7,
        )

        array = Array(
            lambda: arr,
            mob_center=k_text,
            align_bottom=code_block,
            vector=mn.RIGHT * 1.2,
            font_size=40,
        )

        # ======== PRE-CYCLE LOGIC =============

        title.appear(self)
        array.first_appear(self)
        code_block.first_appear(self)

        code_block.highlight(0)
        length_text.first_appear(self)
        self.wait(pause)

        # ===== ALGORITHM CYCLE ==========

        for i in range(length - 1):
            code_block.highlight(2)
            i_text.update_value(self)
            array.pointers(i)
            array.highlight_containers_1to3(i)
            self.wait(pause)

            min_index = i
            code_block.highlight(3)
            array.pointers(i, min_index)
            array.highlight_containers_1to3(i, min_index)
            min_text.update_value(self)
            self.wait(pause)

            for k in range(i + 1, length):
                code_block.highlight(4)
                array.pointers(i, min_index, k)
                array.highlight_containers_1to3(i, min_index, k)
                k_text.update_value(self)
                self.wait(pause)

                code_block.highlight(5)
                self.wait(pause)
                if arr[k] < arr[min_index]:
                    #
                    min_index = k
                    code_block.highlight(6)
                    array.pointers(i, min_index, k)
                    array.highlight_containers_1to3(i, min_index, k)
                    min_text.update_value(self)
                    self.wait(pause)

            code_block.highlight(7)
            self.wait(pause)
            if min_index != i:
                #
                arr[i], arr[min_index] = arr[min_index], arr[i]
                array.update_value(self)
                code_block.highlight(8)
                self.wait(pause)

        # return arr
        code_block.highlight(9)
        return_text = RelativeTextValue(
            ("return", lambda: arr, mn.ORANGE),
            mob_center=code_block,
            align_left=code_block,
            vector=mn.DOWN * 3.0,
            equal_sign=False,
        )
        return_text.first_appear(self)

        # ========== FINISH ==============

        self.wait(pause)
        self.renderer.file_writer.output_file = f"media/{self.__class__.__name__}.mp4"  # type: ignore


class Example_text(mn.Scene):
    def construct(self):
        self.camera.background_color = mn.GREY  # type: ignore

        def first_appear(self):
            pause = 0.5
            s = "abc"

            title = RelativeText(
                "first_appear() + remove()",
                font_size=50,
                text_color=mn.BLACK,
                align_screen=mn.DOWN,
                screen_buff=1,
            )
            title.first_appear(self)

            text = RelativeTextValue(
                ("text", lambda: s, mn.WHITE),
                font_size=40,
            )

            top_text = RelativeTextValue(
                ("text", lambda: s, mn.WHITE),
                mob_center=text,
                vector=mn.UP * 1.5,
                font_size=30,
            )

            top_text.first_appear(self)
            self.wait(pause)
            text.first_appear(self)
            self.wait(pause)
            self.remove(text)
            self.wait(pause)

            s = "ab"
            top_text.update_value(self)
            self.wait(pause)
            text.first_appear(self)
            self.wait(pause)
            self.remove(text)
            self.wait(pause)

            s = "a"
            top_text.update_value(self)
            self.wait(pause)
            text.first_appear(self)
            self.wait(pause)
            self.remove(text)
            self.wait(pause)

            s = ""
            top_text.update_value(self)
            self.wait(pause)
            text.first_appear(self)
            self.wait(pause)
            self.remove(text)
            self.wait(pause)

            s = "a"
            top_text.update_value(self)
            self.wait(pause)
            text.first_appear(self)
            self.wait(1)

            self.clear()

        def group_appear(self):
            pause = 0.5
            s = "abc"

            title = RelativeText(
                "first_appear() + remove()",
                font_size=50,
                text_color=mn.BLACK,
                align_screen=mn.DOWN,
                screen_buff=1,
            )
            title.first_appear(self)

            text_1 = RelativeTextValue(
                ("text", lambda: s, mn.RED),
                font_size=40,
                vector=mn.UP,
            )
            text_2 = RelativeTextValue(
                ("text", lambda: s, mn.BLUE),
                font_size=40,
            )
            text_3 = RelativeTextValue(
                ("text", lambda: s, mn.GREEN),
                ("text", lambda: s, mn.GREEN),
                vector=mn.DOWN,
                font_size=40,
            )

            top_text = RelativeTextValue(
                ("text", lambda: s, mn.BLACK),
                font_size=40,
                align_screen=mn.UP,
                screen_buff=1,
            )

            top_text.first_appear(self)
            self.wait(pause)
            text_1.group_appear(self, text_2, text_3)
            self.wait(pause)
            self.remove(text_1, text_2, text_3)
            self.wait(pause)

            s = "ab"
            top_text.update_value(self)
            self.wait(pause)
            text_1.group_appear(self, text_2, text_3)
            self.wait(pause)
            self.remove(text_1, text_2, text_3)
            self.wait(pause)

            s = "a"
            top_text.update_value(self)
            self.wait(pause)
            text_1.group_appear(self, text_2, text_3)
            self.wait(pause)
            self.remove(text_1, text_2, text_3)
            self.wait(pause)

            s = ""
            top_text.update_value(self)
            self.wait(pause)
            text_1.group_appear(self, text_2, text_3)
            self.wait(pause)
            self.remove(text_1, text_2, text_3)
            self.wait(pause)

            s = "a"
            top_text.update_value(self)
            self.wait(pause)
            text_1.group_appear(self, text_2, text_3)
            self.wait(1)

            self.clear()

        # ========== calls ==============

        first_appear(self)
        group_appear(self)

        # ========== finish ==============

        self.wait(1)
        self.renderer.file_writer.output_file = f"./{self.__class__.__name__}.mp4"  # type: ignore


class Example_array(mn.Scene):
    def construct(self):
        self.camera.background_color = mn.GREY  # type: ignore

        def pyramid(self):
            arr = [0, "\"'`^", "ace", "ygpj", "ABC", ":*#", "."]

            array = Array(
                lambda: arr,
                font_size=35,
            )
            array.first_appear(self)

            array_20 = Array(
                lambda: arr,
                mob_center=array,
                vector=mn.UP * 2.8,
                font_size=20,
            )
            array_20.first_appear(self, time=0.1)

            array_30 = Array(
                lambda: arr,
                mob_center=array,
                vector=mn.UP * 1.4,
                font_size=30,
            )
            array_30.first_appear(self, time=0.1)

            array_40 = Array(
                lambda: arr,
                mob_center=array,
                vector=mn.DOWN * 1.5,
                font_size=40,
            )
            array_40.first_appear(self, time=0.1)

            array_50 = Array(
                lambda: arr,
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
                lambda: arr,
                mob_center=array,
                align_left=array,
                vector=mn.UP * 2.8,
                font_size=20,
            )
            array_20.first_appear(self, time=0.1)

            array_30 = Array(
                lambda: arr,
                mob_center=array,
                align_left=array,
                vector=mn.UP * 1.4,
                font_size=30,
            )
            array_30.first_appear(self, time=0.1)

            array_40 = Array(
                lambda: arr,
                mob_center=array,
                align_left=array,
                vector=mn.DOWN * 1.5,
                font_size=40,
            )
            array_40.first_appear(self, time=0.1)

            array_50 = Array(
                lambda: arr,
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
                lambda: arr,
                mob_center=array,
                align_right=array,
                vector=mn.UP * 2.8,
                font_size=20,
            )
            array_20.first_appear(self, time=0.1)

            array_30 = Array(
                lambda: arr,
                mob_center=array,
                align_right=array,
                vector=mn.UP * 1.4,
                font_size=30,
            )
            array_30.first_appear(self, time=0.1)

            array_40 = Array(
                lambda: arr,
                mob_center=array,
                align_right=array,
                vector=mn.DOWN * 1.5,
                font_size=40,
            )
            array_40.first_appear(self, time=0.1)

            array_50 = Array(
                lambda: arr,
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

        def first_appear(self):
            pause = 0.5
            arr = [1, 2, 3]

            title = RelativeText(
                "first_appear() + remove()",
                font_size=50,
                text_color=mn.BLACK,
                align_screen=mn.DOWN,
                screen_buff=1,
            )
            title.first_appear(self)

            array = Array(
                lambda: arr,
                font_size=40,
            )
            top_text = RelativeTextValue(
                ("arr", lambda: arr, mn.WHITE),
                mob_center=array,
                vector=mn.UP * 1.5,
                font_size=30,
            )

            top_text.first_appear(self)
            self.wait(pause)
            array.first_appear(self)
            self.wait(pause)
            self.remove(array)
            self.wait(pause)

            arr = [1, 2]
            top_text.update_value(self)
            self.wait(pause)
            array.first_appear(self)
            self.wait(pause)
            self.remove(array)
            self.wait(pause)

            arr = [1]
            top_text.update_value(self)
            self.wait(pause)
            array.first_appear(self)
            self.wait(pause)
            self.remove(array)
            self.wait(pause)

            arr = []
            top_text.update_value(self)
            self.wait(pause)
            array.first_appear(self)
            self.wait(pause)
            self.remove(array)
            self.wait(pause)

            arr = [1]
            top_text.update_value(self)
            self.wait(pause)
            array.first_appear(self)
            self.wait(1)

            self.clear()

        def direction(self):

            pause = 0.5
            arr = [1, 2, 3]

            title = RelativeText(
                "direction param",
                font_size=50,
                text_color=mn.BLACK,
                align_screen=mn.DOWN,
                screen_buff=1,
            )
            title.first_appear(self)

            arr_text = RelativeTextValue(
                ("arr", lambda: arr, mn.WHITE),
                font_size=30,
                align_screen=mn.UP,
                screen_buff=0.5,
            )
            arr_text.first_appear(self)
            self.wait(pause)

            array1 = Array(
                lambda: arr,
                font_size=40,
                align_screen=mn.LEFT,
                screen_buff=0.5,
            )
            text1 = RelativeText(
                "mn.RIGHT",
                font_size=30,
                mob_center=array1,
                align_left=array1,
                vector=mn.UP * 2,
            )
            array1.group_appear(self, text1)
            self.wait(pause)

            array2 = Array(
                lambda: arr,
                direction=mn.UP,
                font_size=40,
                vector=mn.LEFT * 1,
            )
            text2 = RelativeText(
                "mn.UP",
                font_size=30,
                align_bottom=text1,
                align_left=array2,
            )
            array2.group_appear(self, text2)
            self.wait(pause)

            array3 = Array(
                lambda: arr,
                direction=mn.DOWN,
                font_size=40,
                vector=mn.RIGHT * 3,
            )
            text3 = RelativeText(
                "mn.DOWN",
                font_size=30,
                align_bottom=text1,
                align_left=array3,
            )
            array3.group_appear(self, text3)
            self.wait(pause)

            update_text = RelativeText(
                "update_value()",
                font_size=30,
                text_color=mn.BLACK,
                mob_center=title,
                vector=mn.DOWN,
            )
            update_text.first_appear(self)
            self.wait(pause)

            arr = [1, 2]
            arr_text.update_value(self)
            self.wait(pause)
            array1.update_value(self)
            array2.update_value(self)
            array3.update_value(self)
            self.wait(pause)

            arr = [1]
            arr_text.update_value(self)
            self.wait(pause)
            array1.update_value(self)
            array2.update_value(self)
            array3.update_value(self)
            self.wait(pause)

            arr = []
            arr_text.update_value(self)
            self.wait(pause)
            array1.update_value(self)
            array2.update_value(self)
            array3.update_value(self)
            self.wait(pause)

            arr = [1]
            arr_text.update_value(self)
            self.wait(pause)
            array1.update_value(self)
            array2.update_value(self)
            array3.update_value(self)
            self.wait(1)

            arr = [1, 2]
            arr_text.update_value(self)
            self.wait(pause)
            array1.update_value(self)
            array2.update_value(self)
            array3.update_value(self)
            self.wait(1)

            arr = [1, 2, 3]
            arr_text.update_value(self)
            self.wait(pause)
            array1.update_value(self)
            array2.update_value(self)
            array3.update_value(self)
            self.wait(1)

            self.clear()

        def lockwidth(self):
            pause = 0.5
            arr = [1, 2, 3]

            title = RelativeText(
                "lock_width param",
                font_size=50,
                text_color=mn.BLACK,
                align_screen=mn.DOWN,
                screen_buff=1,
            )
            title.first_appear(self)

            arr_text = RelativeTextValue(
                ("arr", lambda: arr, mn.WHITE),
                font_size=30,
                align_screen=mn.UP,
                screen_buff=0.5,
            )
            arr_text.first_appear(self)
            self.wait(pause)

            array1 = Array(
                lambda: arr,
                pointers=None,
                font_size=40,
                align_screen=mn.LEFT,
                screen_buff=1.5,
                direction=mn.UP,
            )
            array2 = Array(
                lambda: arr,
                pointers=None,
                font_size=40,
                mob_center=array1,
                vector=mn.RIGHT * 2.8,
            )
            text1 = RelativeText(
                "lock_width = False",
                font_size=30,
                vector=mn.UP * 2,
                align_left=array1,
            )
            text1.group_appear(self, array1, array2)
            self.wait(pause)

            array3 = Array(
                lambda: arr,
                pointers=None,
                font_size=40,
                align_screen=mn.RIGHT,
                screen_buff=1.5,
                direction=mn.UP,
                lock_width=True,
            )
            array4 = Array(
                lambda: arr,
                pointers=None,
                font_size=40,
                mob_center=array3,
                vector=mn.LEFT * 2.8,
                lock_width=True,
            )
            text2 = RelativeText(
                "lock_width = True",
                font_size=30,
                vector=mn.UP * 2,
                align_right=array3,
            )
            text2.group_appear(self, array3, array4)
            self.wait(pause)

            update_text = RelativeText(
                "update_value()",
                font_size=30,
                text_color=mn.BLACK,
                mob_center=title,
                vector=mn.DOWN,
            )
            update_text.first_appear(self)
            self.wait(pause)

            arr = [1, 22, 333]
            arr_text.update_value(self)
            self.wait(pause)
            array1.update_value(self)
            array2.update_value(self)
            array3.update_value(self)
            array4.update_value(self)
            self.wait(pause)

            arr = [1111, 22, 333]
            arr_text.update_value(self)
            self.wait(pause)
            array1.update_value(self)
            array2.update_value(self)
            array3.update_value(self)
            array4.update_value(self)
            self.wait(pause)

            arr = [1, 2, 3]
            arr_text.update_value(self)
            self.wait(pause)
            array1.update_value(self)
            array2.update_value(self)
            array3.update_value(self)
            array4.update_value(self)
            self.wait(1)

            self.clear()

        def pointers(self):

            pause = 0.5
            arr = [1, 2, 3]

            title = RelativeText(
                "pointers param",
                font_size=50,
                text_color=mn.BLACK,
                align_screen=mn.DOWN,
                screen_buff=1,
            )
            title.first_appear(self)

            s = "both"
            p_text = RelativeTextValue(
                ("pointers", lambda: s, mn.WHITE),
                font_size=30,
                align_screen=mn.UP,
                screen_buff=0.5,
            )
            p_text.first_appear(self)
            self.wait(pause)

            array1 = Array(
                lambda: arr,
                font_size=40,
                align_screen=mn.LEFT,
                screen_buff=0.5,
            )
            text1 = RelativeText(
                "direction=mn.RIGHT",
                font_size=30,
                mob_center=array1,
                align_left=array1,
                vector=mn.UP * 2,
            )
            array1.group_appear(self, text1)
            self.wait(pause)

            array2 = Array(
                lambda: arr,
                direction=mn.UP,
                font_size=40,
                vector=mn.LEFT * 1,
            )
            text2 = RelativeText(
                "direction=mn.UP",
                font_size=30,
                align_bottom=text1,
                align_left=array2,
            )
            array2.group_appear(self, text2)
            self.wait(pause)

            array3 = Array(
                lambda: arr,
                direction=mn.DOWN,
                font_size=40,
                vector=mn.RIGHT * 3,
            )
            text3 = RelativeText(
                "direction=mn.DOWN",
                font_size=30,
                align_bottom=text1,
                align_left=array3,
            )
            array3.group_appear(self, text3)
            self.wait(pause)

            array1.pointers(0, 1, 2)
            array1.pointers(1, pos=1, color_1=mn.PINK)
            array2.pointers(0, 1, 2)
            array2.pointers(1, pos=1, color_1=mn.PINK)
            array3.pointers(0, 1, 2)
            array3.pointers(1, pos=1, color_1=mn.PINK)
            self.wait(1)

            self.remove(
                array1,
                array2,
                array3,
            )
            self.wait(pause)

            s = "top"
            p_text.update_value(self)
            self.wait(pause)

            array1 = Array(
                lambda: arr,
                pointers="top",
                font_size=40,
                align_screen=mn.LEFT,
                screen_buff=0.5,
            )
            array1.first_appear(self)
            self.wait(pause)

            array2 = Array(
                lambda: arr,
                pointers="top",
                direction=mn.UP,
                font_size=40,
                vector=mn.LEFT * 1,
            )
            array2.first_appear(self)
            self.wait(pause)

            array3 = Array(
                lambda: arr,
                pointers="top",
                direction=mn.DOWN,
                font_size=40,
                vector=mn.RIGHT * 3,
            )
            array3.first_appear(self)
            self.wait(pause)

            array1.pointers(0, 1, 2)
            array1.pointers(1, pos=1, color_1=mn.PINK)
            array2.pointers(0, 1, 2)
            array2.pointers(1, pos=1, color_1=mn.PINK)
            array3.pointers(0, 1, 2)
            array3.pointers(1, pos=1, color_1=mn.PINK)
            self.wait(1)

            self.remove(
                array1,
                array2,
                array3,
            )
            self.wait(pause)

            s = "bottom"
            p_text.update_value(self)
            self.wait(pause)

            array1 = Array(
                lambda: arr,
                pointers="bottom",
                font_size=40,
                align_screen=mn.LEFT,
                screen_buff=0.5,
            )
            array1.first_appear(self)
            self.wait(pause)

            array2 = Array(
                lambda: arr,
                pointers="bottom",
                direction=mn.UP,
                font_size=40,
                vector=mn.LEFT * 1,
            )
            array2.first_appear(self)
            self.wait(pause)

            array3 = Array(
                lambda: arr,
                pointers="bottom",
                direction=mn.DOWN,
                font_size=40,
                vector=mn.RIGHT * 3,
            )
            array3.first_appear(self)
            self.wait(pause)

            array1.pointers(0, 1, 2)
            array1.pointers(1, pos=1, color_1=mn.PINK)
            array2.pointers(0, 1, 2)
            array2.pointers(1, pos=1, color_1=mn.PINK)
            array3.pointers(0, 1, 2)
            array3.pointers(1, pos=1, color_1=mn.PINK)
            self.wait(1)

            self.remove(
                array1,
                array2,
                array3,
            )
            self.wait(pause)

            s = "None"
            p_text.update_value(self)
            self.wait(pause)

            array1 = Array(
                lambda: arr,
                pointers=None,
                font_size=40,
                align_screen=mn.LEFT,
                screen_buff=0.5,
            )
            array1.first_appear(self)
            self.wait(pause)

            array2 = Array(
                lambda: arr,
                pointers=None,
                direction=mn.UP,
                font_size=40,
                vector=mn.LEFT * 1,
            )
            array2.first_appear(self)
            self.wait(pause)

            array3 = Array(
                lambda: arr,
                pointers=None,
                direction=mn.DOWN,
                font_size=40,
                vector=mn.RIGHT * 3,
            )
            array3.first_appear(self)
            self.wait(pause)

            array1.pointers(0, 1, 2)
            array1.pointers(1, pos=1, color_1=mn.PINK)
            array2.pointers(0, 1, 2)
            array2.pointers(1, pos=1, color_1=mn.PINK)
            array3.pointers(0, 1, 2)
            array3.pointers(1, pos=1, color_1=mn.PINK)
            self.wait(1)

            self.wait(1)
            self.clear()

        def positioning(self):
            pause = 1
            arr = list("arr")

            center = Array(lambda: list("mob_center"), font_size=40)
            center.first_appear(self)

            top_text = RelativeText(
                "mob_center=mob_center\nvector=mn.UP * 1",
                vector=mn.DOWN * 2 + mn.RIGHT * 0,
                font_size=30,
            )
            array = Array(
                lambda: arr,
                mob_center=center,
                vector=mn.UP * 2,
                font_size=35,
            )
            array.group_appear(self, top_text)
            self.wait(pause)

            self.remove(array, top_text)

            top_text = RelativeText(
                "mob_center=mob_center\nalign_left=mob_center\nvector=mn.UP * 1",
                vector=mn.DOWN * 2 + mn.RIGHT * 0,
                font_size=30,
            )
            array = Array(
                lambda: arr,
                mob_center=center,
                align_left=center,
                vector=mn.UP * 2,
                font_size=35,
            )
            array.group_appear(self, top_text)
            self.wait(pause)

            self.remove(array, top_text)

            top_text = RelativeText(
                "mob_center=mob_center\nalign_right=mob_center\nvector=mn.UP * 1",
                vector=mn.DOWN * 2 + mn.RIGHT * 0,
                font_size=30,
            )
            array = Array(
                lambda: arr,
                mob_center=center,
                align_right=center,
                vector=mn.UP * 2,
                font_size=35,
            )
            array.group_appear(self, top_text)
            self.wait(pause)

            self.clear()

            one = Array(
                lambda: list("one"),
                font_size=60,
                vector=mn.UP * 2.7 + mn.LEFT * 4,
            )
            two = Array(
                lambda: list("two"),
                font_size=60,
                vector=mn.DOWN * 2.4 + mn.RIGHT * 3,
            )
            one.group_appear(self, two)
            self.wait(0.5)

            top_text = RelativeText(
                "align_left=one\nalign_bottom=two",
                vector=mn.UP * 1 + mn.RIGHT * 2,
                font_size=30,
            )
            array = Array(
                lambda: arr,
                align_left=one,
                align_bottom=two,
                font_size=35,
            )
            array.group_appear(self, top_text)
            self.wait(pause)
            self.remove(array, top_text)

            top_text = RelativeText(
                "align_left=one\nalign_top=two",
                vector=mn.UP * 1 + mn.RIGHT * 2,
                font_size=30,
            )
            array = Array(lambda: arr, align_left=one, align_top=two)
            array.group_appear(self, top_text)
            self.wait(pause)
            update_text = RelativeText(
                "update_value()",
                mob_center=top_text,
                align_left=top_text,
                vector=mn.DOWN * 1,
                font_size=30,
            )
            update_text.first_appear(self)

            arr = [1, 2, 3]
            array.update_value(self)
            self.wait(0.5)
            arr = [1]
            array.update_value(self)
            self.wait(0.5)
            arr = []
            array.update_value(self)
            self.wait(0.5)
            arr = [1, 2]
            array.update_value(self)
            self.wait(0.5)

            self.remove(array, top_text, update_text)

            top_text = RelativeText(
                "align_right=one\nalign_top=two",
                vector=mn.UP * 1 + mn.RIGHT * 2,
                font_size=30,
            )
            array = Array(
                lambda: arr,
                align_right=one,
                align_top=two,
                font_size=35,
            )
            array.group_appear(self, top_text)
            self.wait(pause)

            update_text = RelativeText(
                "update_value()",
                mob_center=top_text,
                align_left=top_text,
                vector=mn.DOWN * 1,
                font_size=30,
            )
            update_text.first_appear(self)

            arr = [1, 2, 3]
            array.update_value(self)
            self.wait(0.5)
            arr = [1]
            array.update_value(self)
            self.wait(0.5)
            arr = []
            array.update_value(self)
            self.wait(0.5)
            arr = [1, 2]
            array.update_value(self)
            self.wait(0.5)

            self.remove(array, top_text, update_text)

            top_text = RelativeText(
                "align_right=one\nalign_bottom=two",
                vector=mn.UP * 1 + mn.RIGHT * 2,
                font_size=30,
            )
            array = Array(
                lambda: arr,
                align_right=one,
                align_bottom=two,
                font_size=35,
            )
            array.group_appear(self, top_text)
            self.wait(pause)
            self.remove(array, top_text)

            top_text = RelativeText(
                "align_left=one\nalign_bottom=two\nvector=mn.UP * 1 + mn.RIGHT * 1",
                vector=mn.UP * 0.7 + mn.RIGHT * 2,
                font_size=30,
            )
            array = Array(
                lambda: arr,
                align_left=one,
                align_bottom=two,
                vector=mn.UP * 1 + mn.RIGHT * 1,
                font_size=35,
            )
            array.group_appear(self, top_text)
            self.wait(pause)
            self.clear()

        def update_value(self):
            pause = 0.5
            center = Array(lambda: list("mob_center"), font_size=50)
            text_title = RelativeText(
                "update_value()",
                vector=mn.LEFT * 4.4 + mn.UP * 3.2,
                text_color=mn.BLACK,
                font_size=50,
            )
            center.group_appear(self, text_title)

            arr = [1, 2, 3]

            arr_1 = Array(
                lambda: arr,
                mob_center=center,
                vector=mn.UP * 1.5,
                anchor=None,
                pointers=None,
                font_size=35,
            )
            arr_2 = Array(
                lambda: arr,
                mob_center=arr_1,
                vector=mn.UP * 0.7,
                anchor="end",
                pointers=None,
                font_size=35,
            )
            arr_3 = Array(
                lambda: arr,
                mob_center=arr_2,
                vector=mn.UP * 0.7,
                anchor="start",
                pointers=None,
                font_size=35,
            )

            text_no_align = RelativeText(
                "no align_sides:",
                align_bottom=arr_2,
                vector=mn.LEFT * 4.6,
                font_size=30,
            )
            text_arr_3 = RelativeText(
                "anchor='start'",
                mob_center=arr_3,
                vector=mn.RIGHT * 4.4,
                font_size=30,
            )
            text_arr_1 = RelativeText(
                "anchor=None",
                mob_center=arr_1,
                align_left=text_arr_3,
                font_size=30,
            )
            text_arr_2 = RelativeText(
                "anchor='end'",
                mob_center=arr_2,
                align_left=text_arr_3,
                font_size=30,
            )

            arr_4 = Array(
                lambda: arr,
                align_left=center,
                vector=mn.DOWN * 1.5,
                pointers=None,
                font_size=35,
            )
            arr_5 = Array(
                lambda: arr,
                align_right=center,
                vector=mn.DOWN * 1.5,
                pointers=None,
                font_size=35,
            )

            text_arr_4 = RelativeText(
                "align_left=mob_center",
                align_left=arr_4,
                mob_center=arr_4,
                vector=mn.DOWN * 1.0 + mn.LEFT * 1,
                font_size=30,
            )
            text_arr_5 = RelativeText(
                "align_right=mob_center",
                align_right=arr_5,
                mob_center=arr_5,
                vector=mn.DOWN * 1.0 + mn.RIGHT * 1,
                font_size=30,
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

            arr_1.highlight_containers_1to3(0, 1, 2)
            arr_2.highlight_containers_1to3(0, 1, 2)
            arr_3.highlight_containers_1to3(0, 1, 2)
            arr_4.highlight_containers_1to3(0, 1, 2)
            arr_5.highlight_containers_1to3(0, 1, 2)
            self.wait(pause)

            arr = [1, 2]
            arr_1.update_value(self)
            arr_2.update_value(self)
            arr_3.update_value(self)
            arr_4.update_value(self)
            arr_5.update_value(self)
            self.wait(pause)

            arr = [1]
            arr_1.update_value(self)
            arr_2.update_value(self)
            arr_3.update_value(self)
            arr_4.update_value(self)
            arr_5.update_value(self)
            self.wait(pause)

            arr = []
            arr_1.update_value(self)
            arr_2.update_value(self)
            arr_3.update_value(self)
            arr_4.update_value(self)
            arr_5.update_value(self)
            self.wait(pause)

            arr = [1]
            arr_1.update_value(self)
            arr_2.update_value(self)
            arr_3.update_value(self)
            arr_4.update_value(self)
            arr_5.update_value(self)
            self.wait(pause)

            arr = [1, 2]
            arr_1.update_value(self)
            arr_2.update_value(self)
            arr_3.update_value(self)
            arr_4.update_value(self)
            arr_5.update_value(self)
            self.wait(pause)

            arr = [1, 2, 3]
            arr_1.update_value(self)
            arr_2.update_value(self)
            arr_3.update_value(self)
            arr_4.update_value(self)
            arr_5.update_value(self)
            self.wait(pause)

            arr = [1, 2, 3, 4]
            arr_1.update_value(self)
            arr_2.update_value(self)
            arr_3.update_value(self)
            arr_4.update_value(self)
            arr_5.update_value(self)
            self.wait(pause)

            self.clear()

        def frame_import(self):
            pause = 0.5

            title = RelativeText(
                "frame_from import",
                font_size=50,
                text_color=mn.BLACK,
                align_screen=mn.UP,
                screen_buff=1,
            )
            self.add(title)

            base_list = [100, 100, 100, 100, 100]
            base = Array(
                lambda: base_list,
                font_size=35,
                vector=mn.UP * 1 + mn.RIGHT * 1,
                container_color=mn.BLUE,
                fill_color=mn.PINK,
            )
            base_text = RelativeText("base array", font_size=30, mob_center=base)
            base_text.next_to(base, mn.LEFT, buff=0.5)
            base.group_appear(self, base_text)
            self.wait(pause)

            donor_list = [0, 0, 0, 0, 0]
            donor = Array(
                lambda: donor_list,
                font_size=35,
                mob_center=base,
                align_left=base,
                vector=mn.DOWN * 2,
                frame_from=base,
                fill_color=mn.DARK_BROWN,
            )
            donor_text = RelativeText(
                "frame donor array", font_size=30, mob_center=base
            )
            donor_text.next_to(donor, mn.LEFT, buff=0.5)
            donor.group_appear(self, donor_text)
            self.wait(pause)

            func_text = RelativeText(
                "update_value()",
                font_size=40,
                text_color=mn.BLACK,
                align_screen=mn.DOWN,
                screen_buff=1,
            )
            self.add(func_text)
            self.wait(pause)

            donor_list = [10, 10, 10, 10, 10]
            donor.update_value(self)
            self.wait(pause)

            donor_list = [100, 100, 100, 100, 100]
            donor.update_value(self)
            self.wait(pause)

            donor_list = [1000, 1000, 1000, 1000, 1000]
            donor.update_value(self)
            self.wait(pause)

            donor_list = [0, 0, 0, 0, 0]
            donor.update_value(self)
            self.wait(pause)

            base_list = [10, 10, 10, 10, 10]
            base.update_value(self)
            donor.update_value(self)
            self.wait(pause)

            base_list = [1, 1, 1, 1, 1]
            base.update_value(self)
            donor.update_value(self)
            self.wait(pause)

            base_list = [10, 10, 10, 10, 10]
            base.update_value(self)
            donor.update_value(self)
            self.wait(1)

            self.clear()

        def highlights_1to3(self):
            pause = 0.5

            array = Array(
                lambda: [10, 2, 3000, 2, 100, 1, 40],
                font_size=35,
            )
            top_text = RelativeText(
                "pointers()   highlight_containers_1to3()",
                vector=mn.UP * 2,
                font_size=30,
            )
            array.group_appear(self, top_text)
            self.wait(1)

            array.pointers(0, 3, 6)
            array.highlight_containers_1to3(0, 3, 6)
            self.wait(pause)
            array.pointers(1, 3, 5)
            array.highlight_containers_1to3(1, 3, 5)
            self.wait(pause)
            array.pointers(2, 3, 4)
            array.highlight_containers_1to3(2, 3, 4)
            self.wait(pause)
            array.pointers(3, 3, 3)
            array.highlight_containers_1to3(3, 3, 3)
            self.wait(pause)
            array.pointers(2, 3, 4)
            array.highlight_containers_1to3(2, 3, 4)
            self.wait(pause)
            array.pointers(2, 2, 4)
            array.highlight_containers_1to3(2, 2, 4)
            self.wait(pause)
            array.pointers(2, 3, 4)
            array.highlight_containers_1to3(2, 3, 4)
            self.wait(pause)
            array.pointers(2, 4, 4)
            array.highlight_containers_1to3(2, 4, 4)
            self.wait(pause)
            array.pointers(2, 4, 3)
            array.highlight_containers_1to3(2, 4, 3)
            self.wait(pause)
            array.pointers(2, 4, 2)
            array.highlight_containers_1to3(2, 4, 2)
            self.wait(1)
            self.remove(top_text)
            array.clear_pointers_highlights(0)
            array.clear_containers_highlights()

            self.clear()

        def monocolor(self):
            pause = 0.5
            array = Array(
                lambda: [1, 2, 3, 4, 5, 6, 7, 8, 9],
                font_size=35,
            )
            top_text = RelativeText(
                "highlight_containers_monocolor()",
                vector=mn.UP * 2,
                font_size=30,
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
            arr = [10, 2, 3000, 2, 100, 1, 40]
            array = Array(
                lambda: arr,
                font_size=35,
            )
            top_text = RelativeText(
                "highlight_containers_with_value()   pointers_on_value()",
                vector=mn.UP * 2,
                font_size=30,
            )
            array.group_appear(self, top_text)
            self.wait(1)

            array.highlight_containers_with_value(0)
            array.pointers_on_value(0)
            self.wait(pause)
            arr = [22, 0, 22, 0, 22, 0]
            array.update_value(self)
            array.highlight_containers_with_value(0)
            array.pointers_on_value(0)
            self.wait(pause)
            arr = [0, 22, 0, 22, 0, 22]
            array.update_value(self)
            array.highlight_containers_with_value(0, color=mn.LIGHT_BROWN)
            array.pointers_on_value(0, color=mn.LIGHT_BROWN)
            self.wait(pause)
            arr = [22, 0, 22, 0, 22, 0]
            array.update_value(self)
            array.highlight_containers_with_value(0, color=mn.LIGHT_BROWN)
            array.pointers_on_value(0, color=mn.LIGHT_BROWN)
            self.wait(pause)
            arr = [0, 22, 0, 22, 0, 22]
            array.update_value(self)
            array.highlight_containers_with_value(0, color=mn.PURPLE)
            array.pointers_on_value(0, color=mn.PURPLE)
            self.wait(pause)
            arr = [22, 0, 22, 0, 22]
            array.update_value(self)
            array.highlight_containers_with_value(0, color=mn.PURPLE)
            array.pointers_on_value(0, color=mn.PURPLE)
            self.wait(pause)
            arr = [0, 22, 0, 22, 0, 22]
            array.update_value(self)
            array.highlight_containers_with_value(0, color=mn.PINK)
            array.pointers_on_value(0, color=mn.PINK)
            self.wait(pause)
            arr = [22, 0, 22, 0, 22]
            array.update_value(self)
            array.highlight_containers_with_value(0, color=mn.PINK)
            array.pointers_on_value(0, color=mn.PINK)
            self.wait(1)
            self.remove(top_text)

            self.clear()

        def mix(self):
            pause = 0.5
            arr = [0, 1, 22, 333, 4444, 55555]
            array = Array(
                lambda: arr,
                font_size=35,
            )
            top_text = RelativeText(
                "mix",
                vector=mn.UP * 2,
                font_size=30,
            )
            array.group_appear(self, top_text)
            self.wait(1)

            array.highlight_containers_1to3(0, 2, 4)
            array.pointers(0, 2, 4)
            array.pointers_on_value(0, color=mn.PINK)
            self.wait(pause)

            arr = [1, 0, 55555, 333]
            array.update_value(self)
            array.clear_pointers_highlights(0)
            array.highlight_containers_with_value(0, color=mn.PINK)
            array.pointers_on_value(0, color=mn.PINK)
            self.wait(pause)

            arr = [0, 333, 0]
            array.update_value(self)
            array.highlight_containers_1to3(0, 2, 4)
            array.pointers(0, 2, 4)
            array.pointers_on_value(0, color=mn.PINK)
            self.wait(pause)

            arr = [0, 0]
            array.update_value(self)
            array.clear_pointers_highlights(0)
            array.highlight_containers_with_value(0, color=mn.PINK)
            array.pointers_on_value(0, color=mn.PINK)
            self.wait(pause)

            arr = [0]
            array.update_value(self)
            array.highlight_containers_1to3(0, 2, 4)
            array.pointers(0, 2, 4)
            array.pointers_on_value(0, color=mn.PINK)
            self.wait(pause)

            arr = []
            array.update_value(self, animate=True)
            array.highlight_containers_1to3(0, 2, 4)
            array.pointers(0, 2, 4)
            array.pointers_on_value(0, color=mn.PINK)
            self.wait(pause)

            arr = [0, 0, 0, 0]
            array.update_value(self, animate=True)
            self.wait(pause)

            arr = [1, 0, 22, 0, 333, 0]
            array.update_value(self, animate=True)
            array.clear_pointers_highlights(0)
            array.highlight_containers_with_value(0, color=mn.PINK)
            array.pointers_on_value(0, color=mn.PINK)
            self.wait(pause)

            arr = [0, 22, 0, 333, 0]
            array.update_value(self, animate=True)
            array.clear_pointers_highlights(1)
            array.highlight_containers_1to3(1, 1, 2)
            array.pointers(1, 1, 2)
            self.wait(pause)

            arr = [1, 0, 22, 0, 333, 0, 22]
            array.update_value(self, animate=True)
            array.clear_pointers_highlights(0)
            array.highlight_containers_with_value(0, color=mn.PINK)
            array.pointers_on_value(0, color=mn.PINK)
            self.wait(pause)

            arr = [0, 22, 0, 333, 0, 55555]
            array.update_value(self, animate=True)
            array.clear_pointers_highlights(1)
            array.highlight_containers_1to3(3, 5, 3)
            array.pointers(3, 5, 3)
            self.wait(pause)

            arr = [1, 0]
            array.update_value(self, animate=True)
            array.highlight_containers_1to3(0, 0, 0)
            array.pointers(0, 0, 0)
            self.wait(pause)

            arr = [0, 0, 0, 0, 0, 0]
            array.update_value(self, animate=True)
            array.clear_pointers_highlights(0)
            array.highlight_containers_with_value(0, color=mn.PINK)
            array.pointers_on_value(0, color=mn.PINK)
            self.wait(1)

        # ========== calls ==============

        pyramid(self)
        first_appear(self)
        direction(self)
        lockwidth(self)
        pointers(self)
        positioning(self)
        update_value(self)
        frame_import(self)
        highlights_1to3(self)
        monocolor(self)
        highlight_on_value(self)
        mix(self)

        # ========== finish ==============

        self.wait(1)
        self.renderer.file_writer.output_file = f"./{self.__class__.__name__}.mp4"  # type: ignore


class Example_string(mn.Scene):
    def construct(self):
        self.camera.background_color = mn.GREY  # type: ignore

        def pyramid(self):
            s = "0agA-/*&.^`~"
            string = String(
                lambda: s,
                # pointers=False,
            )
            string.first_appear(self)

            string_20 = String(
                lambda: s,
                mob_center=string,
                vector=mn.UP * 2.8,
                font_size=25,
            )
            string_20.first_appear(self, time=0.1)

            string_25 = String(
                lambda: s,
                mob_center=string,
                vector=mn.UP * 1.4,
                font_size=30,
            )
            string_25.first_appear(self, time=0.1)

            string_35 = String(
                lambda: s,
                mob_center=string,
                vector=mn.DOWN * 1.5,
                font_size=37,
            )
            string_35.first_appear(self, time=0.1)

            string_40 = String(
                lambda: s,
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
                lambda: s,
                mob_center=string,
                vector=mn.UP * 2.8,
                font_size=25,
                align_left=string,
            )
            string_20.first_appear(self, time=0.1)

            string_25 = String(
                lambda: s,
                mob_center=string,
                vector=mn.UP * 1.4,
                font_size=30,
                align_left=string,
            )
            string_25.first_appear(self, time=0.1)

            string_35 = String(
                lambda: s,
                mob_center=string,
                vector=mn.DOWN * 1.5,
                font_size=37,
                align_left=string,
            )
            string_35.first_appear(self, time=0.1)

            string_40 = String(
                lambda: s,
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
                lambda: s,
                mob_center=string,
                vector=mn.UP * 2.8,
                font_size=25,
                align_right=string,
            )
            string_20.first_appear(self, time=0.1)

            string_25 = String(
                lambda: s,
                mob_center=string,
                vector=mn.UP * 1.4,
                font_size=30,
                align_right=string,
            )
            string_25.first_appear(self, time=0.1)

            string_35 = String(
                lambda: s,
                mob_center=string,
                vector=mn.DOWN * 1.5,
                font_size=37,
                align_right=string,
            )
            string_35.first_appear(self, time=0.1)

            string_40 = String(
                lambda: s,
                mob_center=string,
                vector=mn.DOWN * 3.0,
                font_size=40,
                align_right=string,
            )
            string_40.first_appear(self, time=0.1)

            self.wait(1)
            self.clear()

        def first_appear(self):
            pause = 0.5
            s = "abc"

            title = RelativeText(
                "first_appear() + remove()",
                font_size=50,
                text_color=mn.BLACK,
                align_screen=mn.DOWN,
                screen_buff=1,
            )
            title.first_appear(self)

            string = String(
                lambda: s,
                font_size=40,
            )
            top_text = RelativeTextValue(
                ("string", lambda: s, mn.WHITE),
                mob_center=string,
                vector=mn.UP * 1.5,
                font_size=30,
            )

            top_text.first_appear(self)
            self.wait(pause)
            string.first_appear(self)
            self.wait(pause)
            self.remove(string)
            self.wait(pause)

            s = "ab"
            top_text.update_value(self)
            self.wait(pause)
            string.first_appear(self)
            self.wait(pause)
            self.remove(string)
            self.wait(pause)

            s = "a"
            top_text.update_value(self)
            self.wait(pause)
            string.first_appear(self)
            self.wait(pause)
            self.remove(string)
            self.wait(pause)

            s = ""
            top_text.update_value(self)
            self.wait(pause)
            string.first_appear(self)
            self.wait(pause)
            self.remove(string)
            self.wait(pause)

            s = "a"
            top_text.update_value(self)
            self.wait(pause)
            string.first_appear(self)
            self.wait(1)

            self.clear()

        def positioning(self):
            pause = 1
            string = "str"

            center = String(lambda: "mob_center", font_size=40)
            center.first_appear(self)

            top_text = RelativeText(
                "mob_center=mob_center\nvector=mn.UP * 1",
                vector=mn.DOWN * 2 + mn.RIGHT * 0,
            )
            s = String(lambda: string, mob_center=center, vector=mn.UP * 2)
            s.group_appear(self, top_text)
            self.wait(pause)

            self.remove(s, top_text)

            top_text = RelativeText(
                "mob_center=mob_center\nalign_left=mob_center\nvector=mn.UP * 1",
                vector=mn.DOWN * 2 + mn.RIGHT * 0,
            )
            s = String(
                lambda: string, mob_center=center, align_left=center, vector=mn.UP * 2
            )
            s.group_appear(self, top_text)
            self.wait(pause)

            self.remove(s, top_text)

            top_text = RelativeText(
                "mob_center=mob_center\nalign_right=mob_center\nvector=mn.UP * 1",
                vector=mn.DOWN * 2 + mn.RIGHT * 0,
            )
            s = String(
                lambda: string, mob_center=center, align_right=center, vector=mn.UP * 2
            )
            s.group_appear(self, top_text)
            self.wait(pause)

            self.clear()

            one = String(lambda: "one", font_size=60, vector=mn.UP * 2.7 + mn.LEFT * 4)
            two = String(
                lambda: "two", font_size=60, vector=mn.DOWN * 2.4 + mn.RIGHT * 3
            )
            one.group_appear(self, two)
            self.wait(pause)

            # -----------------------

            top_text = RelativeText(
                "align_left=one\nalign_bottom=two",
                vector=mn.UP * 1 + mn.RIGHT * 2,
            )
            s = String(lambda: string, align_left=one, align_bottom=two)
            s.group_appear(self, top_text)
            self.wait(pause)
            self.remove(s, top_text)

            top_text = RelativeText(
                "align_left=one\nalign_top=two",
                vector=mn.UP * 1 + mn.RIGHT * 2,
            )
            s = String(lambda: string, align_left=one, align_top=two)
            s.group_appear(self, top_text)
            self.wait(pause)
            update_text = RelativeText(
                "update_value()",
                mob_center=top_text,
                align_left=top_text,
                vector=mn.DOWN * 1,
            )
            update_text.first_appear(self)

            string = "123"
            s.update_value(self)
            self.wait(0.5)
            string = "1"
            s.update_value(self)
            self.wait(0.5)
            string = ""
            s.update_value(self)
            self.wait(0.5)
            string = "12"
            s.update_value(self)
            self.wait(0.5)

            self.remove(s, top_text, update_text)

            top_text = RelativeText(
                "align_right=one\nalign_top=two",
                vector=mn.UP * 1 + mn.RIGHT * 2,
            )
            s = String(lambda: string, align_right=one, align_top=two)
            s.group_appear(self, top_text)
            self.wait(pause)
            update_text = RelativeText(
                "update_value()",
                mob_center=top_text,
                align_left=top_text,
                vector=mn.DOWN * 1,
            )
            update_text.first_appear(self)

            string = "123"
            s.update_value(self)
            self.wait(0.5)
            string = "1"
            s.update_value(self)
            self.wait(0.5)
            string = ""
            s.update_value(self)
            self.wait(0.5)
            string = "12"
            s.update_value(self)
            self.wait(0.5)

            self.remove(s, top_text, update_text)

            top_text = RelativeText(
                "align_right=one\nalign_bottom=two",
                vector=mn.UP * 1 + mn.RIGHT * 2,
            )
            s = String(lambda: string, align_right=one, align_bottom=two)
            s.group_appear(self, top_text)
            self.wait(pause)
            self.remove(s, top_text)

            top_text = RelativeText(
                "align_left=one\nalign_bottom=two\nvector=mn.UP * 1 + mn.RIGHT * 1",
                vector=mn.UP * 0.7 + mn.RIGHT * 2,
            )
            s = String(
                lambda: string,
                align_left=one,
                align_bottom=two,
                vector=mn.UP * 1 + mn.RIGHT * 1,
            )
            s.group_appear(self, top_text)
            self.wait(pause)
            self.clear()

        def updatevalue(self):
            pause = 0.5
            center = String(lambda: "mob_center", font_size=50)
            text_title = RelativeText(
                "update_value()",
                vector=mn.LEFT * 4.4 + mn.UP * 3.2,
                text_color=mn.BLACK,
                font_size=50,
            )
            center.group_appear(self, text_title)

            string = "123"
            str_1 = String(
                lambda: string,
                mob_center=center,
                vector=mn.UP * 1.5,
                anchor=None,
                pointers=None,
            )
            str_2 = String(
                lambda: string,
                mob_center=str_1,
                vector=mn.UP * 0.7,
                anchor=mn.RIGHT,
                pointers=None,
            )
            str_3 = String(
                lambda: string,
                mob_center=str_2,
                vector=mn.UP * 0.7,
                anchor=mn.LEFT,
                pointers=None,
            )

            text_no_align = RelativeText(
                "no align_sides:", align_bottom=str_2, vector=mn.LEFT * 4.6
            )
            text_str_1 = RelativeText(
                "anchor=None", mob_center=str_1, vector=mn.RIGHT * 4.0
            )
            text_str_2 = RelativeText(
                "anchor=mn.RIGHT", mob_center=str_2, vector=mn.RIGHT * 4.6
            )
            text_str_3 = RelativeText(
                "anchor=mn.LEFT", mob_center=str_3, vector=mn.RIGHT * 4.4
            )

            str_4 = String(
                lambda: string,
                align_left=center,
                vector=mn.DOWN * 1.5,
                pointers=None,
            )
            str_5 = String(
                lambda: string,
                align_right=center,
                vector=mn.DOWN * 1.5,
                pointers=None,
            )

            text_str_4 = RelativeText(
                "align_left=mob_center",
                align_left=str_4,
                mob_center=str_4,
                vector=mn.DOWN * 1.0 + mn.LEFT * 2,
            )
            text_str_5 = RelativeText(
                "align_right=mob_center",
                align_right=str_5,
                mob_center=str_5,
                vector=mn.DOWN * 1.0 + mn.RIGHT * 2,
            )

            str_1.group_appear(
                self,
                str_2,
                str_3,
                str_4,
                str_5,
                text_no_align,
                text_str_1,
                text_str_2,
                text_str_3,
                text_str_4,
                text_str_5,
            )
            self.wait(2)

            str_1.highlight_containers_1to3(0, 1, 2)
            str_2.highlight_containers_1to3(0, 1, 2)
            str_3.highlight_containers_1to3(0, 1, 2)
            str_4.highlight_containers_1to3(0, 1, 2)
            str_5.highlight_containers_1to3(0, 1, 2)
            self.wait(pause)

            string = "12"
            str_1.update_value(self)
            str_2.update_value(self)
            str_3.update_value(self)
            str_4.update_value(self)
            str_5.update_value(self)
            self.wait(pause)

            string = "1"
            str_1.update_value(self)
            str_2.update_value(self)
            str_3.update_value(self)
            str_4.update_value(self)
            str_5.update_value(self)
            self.wait(pause)

            string = ""
            str_1.update_value(self)
            str_2.update_value(self)
            str_3.update_value(self)
            str_4.update_value(self)
            str_5.update_value(self)
            self.wait(pause)

            string = "1"
            str_1.update_value(self)
            str_2.update_value(self)
            str_3.update_value(self)
            str_4.update_value(self)
            str_5.update_value(self)
            self.wait(pause)

            string = "12"
            str_1.update_value(self)
            str_2.update_value(self)
            str_3.update_value(self)
            str_4.update_value(self)
            str_5.update_value(self)
            self.wait(pause)

            string = "123"
            str_1.update_value(self)
            str_2.update_value(self)
            str_3.update_value(self)
            str_4.update_value(self)
            str_5.update_value(self)
            self.wait(pause)

            string = "1234"
            str_1.update_value(self)
            str_2.update_value(self)
            str_3.update_value(self)
            str_4.update_value(self)
            str_5.update_value(self)
            self.wait(pause)

            self.remove(
                str_1,
                str_2,
                str_3,
                str_4,
                str_5,
            )
            self.wait(pause)

            string = ""
            str_1 = String(
                lambda: string,
                mob_center=center,
                vector=mn.UP * 1.5,
                anchor=None,
                pointers=None,
            )
            str_2 = String(
                lambda: string,
                mob_center=str_1,
                vector=mn.UP * 0.7,
                anchor=mn.RIGHT,
                pointers=None,
            )
            str_3 = String(
                lambda: string,
                mob_center=str_2,
                vector=mn.UP * 0.7,
                anchor=mn.LEFT,
                pointers=None,
            )
            str_4 = String(
                lambda: string,
                align_left=center,
                vector=mn.DOWN * 1.5,
                pointers=None,
            )
            str_5 = String(
                lambda: string,
                align_right=center,
                vector=mn.DOWN * 1.5,
                pointers=None,
            )
            str_1.highlight_containers_1to3(0, 1, 2)
            str_2.highlight_containers_1to3(0, 1, 2)
            str_3.highlight_containers_1to3(0, 1, 2)
            str_4.highlight_containers_1to3(0, 1, 2)
            str_5.highlight_containers_1to3(0, 1, 2)
            str_1.group_appear(
                self,
                str_2,
                str_3,
                str_4,
                str_5,
            )
            self.wait(1)

            string = "1"
            str_1.update_value(self)
            str_2.update_value(self)
            str_3.update_value(self)
            str_4.update_value(self)
            str_5.update_value(self)
            self.wait(pause)

            string = ""
            str_1.update_value(self)
            str_2.update_value(self)
            str_3.update_value(self)
            str_4.update_value(self)
            str_5.update_value(self)
            self.wait(pause)

            string = "12"
            str_1.update_value(self)
            str_2.update_value(self)
            str_3.update_value(self)
            str_4.update_value(self)
            str_5.update_value(self)
            self.wait(pause)

            string = "123"
            str_1.update_value(self)
            str_2.update_value(self)
            str_3.update_value(self)
            str_4.update_value(self)
            str_5.update_value(self)
            self.wait(pause)

            self.clear()

        def highlights_1to3(self):
            pause = 0.5
            string = String(lambda: "follow the rabbit")
            top_text = RelativeText(
                "pointers()   highlight_containers()",
                vector=mn.UP * 2,
            )
            string.group_appear(self, top_text)
            self.wait(1)

            string.pointers(0, 3, 6)
            string.highlight_containers_1to3(0, 3, 6)
            self.wait(pause)
            string.pointers(1, 3, 5)
            string.highlight_containers_1to3(1, 3, 5)
            self.wait(pause)
            string.pointers(2, 3, 4)
            string.highlight_containers_1to3(2, 3, 4)
            self.wait(pause)
            string.pointers(3, 3, 3)
            string.highlight_containers_1to3(3, 3, 3)
            self.wait(pause)
            string.pointers(2, 3, 4)
            string.highlight_containers_1to3(2, 3, 4)
            self.wait(pause)
            string.pointers(2, 2, 4)
            string.highlight_containers_1to3(2, 2, 4)
            self.wait(pause)
            string.pointers(2, 3, 4)
            string.highlight_containers_1to3(2, 3, 4)
            self.wait(pause)
            string.pointers(2, 4, 4)
            string.highlight_containers_1to3(2, 4, 4)
            self.wait(pause)
            string.pointers(2, 4, 3)
            string.highlight_containers_1to3(2, 4, 3)
            self.wait(pause)
            string.pointers(2, 40, 2)
            string.highlight_containers_1to3(2, 40, 2)
            self.wait(1)
            self.clear()

        def highlights_monocolor(self):
            pause = 1
            s = "follow rab"
            string = String(lambda: s, anchor=None)
            top_text = RelativeText(
                "highlight_containers_monocolor()",
                vector=mn.UP * 2,
            )
            string.group_appear(self, top_text)
            self.wait(pause)

            string.highlight_containers_monocolor([0, 1, 2, 3, 4, 5])
            self.wait(pause)
            string.highlight_containers_monocolor([7, 8, 9, 10, 11, 12])
            self.wait(pause)
            s = "follow rabbit"
            string.update_value(self)
            self.wait(2)
            self.clear()

        def highlight_on_value(self):
            pause = 0.5
            s = "follow the rabbit"
            string = String(lambda: s)
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
            s = "follow the rabbit"
            string = String(lambda: s)
            top_text = RelativeText(
                "mix",
                vector=mn.UP * 2,
            )
            string.group_appear(self, top_text)
            self.wait(1)

            string.highlight_containers_1to3(0, 2, 4)
            string.pointers(0, 2, 4)
            self.wait(pause)

            s = "follow the"
            string.update_value(
                self,
            )
            string.clear_pointers_highlights(0)
            string.pointers_on_value("f", color=mn.PINK)
            string.highlight_containers_with_value("f", color=mn.PINK)
            self.wait(pause)

            s = "follow"
            string.update_value(self)
            string.clear_pointers_highlights(1)
            string.highlight_containers_1to3(0, 2, 4)
            string.pointers(0, 2, 4)
            self.wait(pause)

            s = ""
            string.update_value(self, animate=True)
            string.clear_pointers_highlights(0)
            string.highlight_containers_with_value("b", color=mn.PINK)
            string.pointers_on_value("b", color=mn.PINK)
            self.wait(1)

            s = "rabbit"
            string.update_value(self, animate=True)
            self.wait(1)

            s = "rabbit"
            string.update_value(self, animate=True)
            string.highlight_containers_with_value("b", color=mn.PINK)
            string.pointers_on_value("b", color=mn.PINK)
            self.wait(1)

            s = "white rabbit"
            string.update_value(self, animate=True)
            string.clear_pointers_highlights(1)
            string.highlight_containers_1to3(0, 1, 2)
            string.pointers(0, 1, 2)
            self.wait(pause)

            s = "rabbit white"
            string.update_value(self, animate=True)
            string.clear_pointers_highlights(0)
            string.highlight_containers_with_value("t", color=mn.PINK)
            string.pointers_on_value("t", color=mn.PINK)
            self.wait(pause)

            s = "rabbit the white"
            string.update_value(self, animate=True)
            string.clear_pointers_highlights(1)
            string.highlight_containers_1to3(0, 2, 2)
            string.pointers(0, 2, 2)
            self.wait(pause)

            s = "white the rabbit"
            string.update_value(self, animate=True)
            string.clear_pointers_highlights(0)
            string.pointers_on_value(" ", color=mn.PINK)
            string.highlight_containers_with_value(" ", color=mn.PINK)
            self.wait(pause)

            s = "rab follow rab"
            string.update_value(self, animate=True)
            string.highlight_containers_1to3(90, 90, 90)
            string.pointers(90, 90, 90)
            string.highlight_containers_with_value("a", color=mn.PINK)
            string.pointers_on_value("a", color=mn.PINK)
            self.wait(1)

        # ========== calls ==============

        pyramid(self)
        first_appear(self)
        positioning(self)
        updatevalue(self)
        highlights_1to3(self)
        highlights_monocolor(self)
        highlight_on_value(self)
        mix(self)

        # ========== finish ==============

        self.wait(1)
        self.renderer.file_writer.output_file = f"./{self.__class__.__name__}.mp4"  # type: ignore


class Example_linked_list(mn.Scene):
    def construct(self):
        self.camera.background_color = mn.GREY  # type: ignore

        cll = LinkedList.create_linked_list

        def positioning(self):
            pause = 1

            center = Array(lambda: list("mob_center"), font_size=40)
            center.first_appear(self)

            top_text = RelativeText(
                "mob_center=mob_center\nvector=mn.UP * 2",
                vector=mn.DOWN * 2 + mn.RIGHT * 0,
            )
            ll = LinkedList(
                lambda: cll([0, 1]),
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
                lambda: cll([0, 1]),
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
                lambda: cll([0, 1]),
                mob_center=center,
                align_right=center,
                vector=mn.UP * 2,
            )
            ll.group_appear(self, top_text)
            self.wait(pause)

            self.clear()

            one = Array(
                lambda: list("one"), font_size=60, vector=mn.UP * 2.7 + mn.LEFT * 4
            )
            two = Array(
                lambda: list("two"), font_size=60, vector=mn.DOWN * 2.4 + mn.RIGHT * 3
            )
            one.group_appear(self, two)
            self.wait(0.5)

            # -----------------------

            top_text = RelativeText(
                "align_left=one\nalign_bottom=two",
                vector=mn.UP * 1 + mn.RIGHT * 2,
            )
            ll = LinkedList(
                lambda: cll([0, 1]),
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
                lambda: cll([0, 1]),
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
                lambda: cll([0, 1]),
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
                lambda: cll([0, 1]),
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
                lambda: cll([0, 1]),
                align_left=one,
                align_bottom=two,
                vector=mn.UP * 1 + mn.RIGHT * 1,
            )
            ll.group_appear(self, top_text)
            self.wait(pause)
            self.clear()

        def rotation(self):
            pause = 0.3
            cll = LinkedList.create_linked_list

            mob_center = Array(lambda: list("mob_center"), vector=mn.UP * 3)
            mob_center.first_appear(self)

            ll = LinkedList(
                lambda: cll([0, 1, 2]),
                mob_center=mob_center,
                vector=mn.DOWN * 3.5,
            )
            ll.appear(self)
            ll.pointers(0, 1, 2)
            self.wait(pause)

            self.remove(ll)
            ll = LinkedList(
                lambda: cll([0, 1, 2]),
                mob_center=mob_center,
                vector=mn.DOWN * 3.5,
                direction=np.array([10, -10, 0]),
            )
            ll.appear(self)
            ll.pointers(0, 1, 2)
            self.wait(pause)

            self.remove(ll)
            ll = LinkedList(
                lambda: cll([0, 1, 2]),
                mob_center=mob_center,
                vector=mn.DOWN * 3.5,
                direction=np.array([0, -10, 0]),
            )
            ll.appear(self)
            ll.pointers(0, 1, 2)
            self.wait(pause)

            self.remove(ll)
            ll = LinkedList(
                lambda: cll([0, 1, 2]),
                mob_center=mob_center,
                vector=mn.DOWN * 3.5,
                direction=np.array([-10, -10, 0]),
            )
            ll.appear(self)
            ll.pointers(0, 1, 2)
            self.wait(pause)

            self.remove(ll)
            ll = LinkedList(
                lambda: cll([0, 1, 2]),
                mob_center=mob_center,
                vector=mn.DOWN * 3.5,
                direction=np.array([-10, 0, 0]),
            )
            ll.appear(self)
            ll.pointers(0, 1, 2)
            self.wait(pause)

            self.remove(ll)
            ll = LinkedList(
                lambda: cll([0, 1, 2]),
                mob_center=mob_center,
                vector=mn.DOWN * 3.5,
                direction=np.array([-10, 10, 0]),
            )
            ll.appear(self)
            ll.pointers(0, 1, 2)
            self.wait(pause)

            self.remove(ll)
            ll = LinkedList(
                lambda: cll([0, 1, 2]),
                mob_center=mob_center,
                vector=mn.DOWN * 3.5,
                direction=np.array([0, 10, 0]),
            )
            ll.appear(self)
            ll.pointers(0, 1, 2)
            self.wait(pause)

            self.remove(ll)
            ll = LinkedList(
                lambda: cll([0, 1, 2]),
                mob_center=mob_center,
                vector=mn.DOWN * 3.5,
                direction=np.array([10, 10, 0]),
            )
            ll.appear(self)
            ll.pointers(0, 1, 2)
            self.wait(pause)

            self.remove(ll)
            ll = LinkedList(
                lambda: cll([0, 1, 2]),
                mob_center=mob_center,
                vector=mn.DOWN * 3.5,
            )
            ll.appear(self)
            ll.pointers(0, 1, 2)
            self.wait(1)
            self.remove(ll)

            # ======== left | right alignment ============

            ll1 = LinkedList(
                lambda: cll([0, 1, 2]),
                mob_center=mob_center,
                align_right=mob_center,
                vector=mn.DOWN * 2,
            )
            ll2 = LinkedList(
                lambda: cll([0, 1, 2]),
                mob_center=mob_center,
                align_left=mob_center,
                vector=mn.DOWN * 2,
            )

            rt1 = RelativeText(
                "mob_center=mob_center\nalign_right=mob_center\nvector=mn.DOWN * 2",
                mob_center=ll1,
                align_left=ll1,
                vector=mn.DOWN * 2,
            )
            rt2 = RelativeText(
                "mob_center=mob_center\nalign_left=mob_center\nvector=mn.DOWN * 2",
                mob_center=ll2,
                align_right=ll2,
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
            self.remove(
                ll1,
                ll2,
                rt1,
                rt2,
            )

            # ======== up | down alignment ============

            self.play(mob_center.animate.move_to(mn.ORIGIN))

            ll1 = LinkedList(
                lambda: cll([0, 1]),
                radius=0.8,
                mob_center=mob_center,
                align_top=mob_center,
                vector=mn.LEFT * 5.3,
                direction=mn.UP,
            )
            ll2 = LinkedList(
                lambda: cll([0, 1]),
                radius=0.8,
                mob_center=mob_center,
                align_bottom=mob_center,
                vector=mn.RIGHT * 5.3,
                direction=mn.UP,
            )

            rt1 = RelativeText(
                "mob_center=mob_center\nalign_top=mob_center\nvector=mn.LEFT * 5.3",
                align_left=mob_center,
                align_bottom=ll1,
                vector=mn.ORIGIN,
            )
            rt2 = RelativeText(
                "mob_center=mob_center\nalign_bottom=mob_center\nvector=mn.RIGHT * 5.3",
                align_right=mob_center,
                align_top=ll2,
                vector=mn.ORIGIN,
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

        def updatevalue(self):
            pause = 0.7

            ln = cll([0, 12, 12345, "'", '^"', ".", "_.,", "Aa", "acv", "gjy", "gyp"])

            ll = LinkedList(
                lambda: ln,
                direction=np.array([10, 2, 0]),
                vector=mn.DOWN * 1,
                anchor=mn.LEFT,
            )
            ll.highlight_containers_1to3(0, 2, 4)
            ll.pointers(0, 2, 4)
            rt = RelativeText(
                "anchor=mn.LEFT\ndirection=np.array([10, 2, 0])\nupdate_value()",
                align_left=ll,
                vector=mn.UP * 3,
            )
            ll.group_appear(self, rt)
            self.wait(pause)

            ln = cll([0, 12, 12345, "'", '^"', ".", "_.,", "Aa"])
            ll.update_value(self)
            self.wait(pause)

            ln = cll([0, 12, 12345, "'", '^"'])
            ll.update_value(self)
            self.wait(pause)

            ln = cll([])
            ll.update_value(self)
            self.wait(pause)

            ln = cll([0, 12])
            ll.update_value(self)
            self.wait(pause)

            ln = cll([0, 12, 12345, "'", '^"'])
            ll.update_value(self)
            self.wait(pause)

            ln = cll([0, 12, 12345, "'", '^"', ".", "_.,", "Aa"])
            ll.update_value(self)
            self.wait(pause)

            ln = cll([0, 12, 12345, "'", '^"', ".", "_.,", "Aa", "acv", "gjy", "gyp"])
            ll.update_value(self)
            self.wait(pause)
            self.clear()

            # ------------------

            ln = cll([0, 12, 12345, "'", '^"', ".", "_.,", "Aa", "acv", "gjy", "gyp"])
            ll = LinkedList(
                lambda: ln,
                direction=np.array([10, 2, 0]),
                vector=mn.DOWN * 1,
                anchor=mn.RIGHT,
            )
            ll.highlight_containers_1to3(0, 2, 4)
            ll.pointers(0, 2, 4)
            rt = RelativeText(
                "anchor=mn.RIGHT\ndirection=np.array([10, 2, 0])\nupdate_value()",
                align_left=ll,
                vector=mn.UP * 3,
            )
            ll.group_appear(self, rt)
            self.wait(pause)

            ln = cll([0, 12, 12345, "'", '^"', ".", "_.,", "Aa"])
            ll.update_value(self)
            self.wait(pause)

            ln = cll([0, 12, 12345, "'", '^"'])
            ll.update_value(self)
            self.wait(pause)

            ln = cll([])
            ll.update_value(self)
            self.wait(pause)

            ln = cll([0, 12])
            ll.update_value(self)
            self.wait(pause)

            ln = cll([0, 12, 12345, "'", '^"'])
            ll.update_value(self)
            self.wait(pause)

            ln = cll([0, 12, 12345, "'", '^"', ".", "_.,", "Aa"])
            ll.update_value(self)
            self.wait(pause)

            ln = cll([0, 12, 12345, "'", '^"', ".", "_.,", "Aa", "acv", "gjy", "gyp"])
            ll.update_value(self)
            self.wait(pause)
            self.clear()

            # ------------------

            ln = cll([0, 12, 12345, "'", '^"', ".", "_.,", "Aa", "acv", "gjy", "gyp"])
            ll = LinkedList(
                lambda: ln,
                direction=np.array([-10, -2, 0]),
                vector=mn.DOWN * 1,
                anchor=mn.RIGHT,
            )
            ll.highlight_containers_1to3(0, 2, 4)
            ll.pointers(0, 2, 4)
            rt = RelativeText(
                "anchor=mn.RIGHT\ndirection=np.array([-10, -2, 0])\nupdate_value()",
                align_left=ll,
                vector=mn.UP * 3,
            )
            ll.group_appear(self, rt)
            self.wait(pause)

            ln = cll([0, 12, 12345, "'", '^"', ".", "_.,", "Aa"])
            ll.update_value(self)
            self.wait(pause)

            ln = cll([0, 12, 12345, "'", '^"'])
            ll.update_value(self)
            self.wait(pause)

            ln = cll([])
            ll.update_value(self)
            self.wait(pause)

            ln = cll([0, 12])
            ll.update_value(self)
            self.wait(pause)

            ln = cll([0, 12, 12345, "'", '^"'])
            ll.update_value(self)
            self.wait(pause)

            ln = cll([0, 12, 12345, "'", '^"', ".", "_.,", "Aa"])
            ll.update_value(self)
            self.wait(pause)

            ln = cll([0, 12, 12345, "'", '^"', ".", "_.,", "Aa", "acv", "gjy", "gyp"])
            ll.update_value(self)
            self.wait(pause)
            self.clear()

            # ------------------

            ln = cll([0, 12, 12345, "'", '^"', ".", "_.,", "Aa", "acv", "gjy", "gyp"])
            ll = LinkedList(
                lambda: ln,
                direction=np.array([10, 2, 0]),
                vector=mn.DOWN * 1,
                anchor=None,
            )
            ll.highlight_containers_1to3(0, 2, 4)
            ll.pointers(0, 2, 4)
            rt = RelativeText(
                "anchor=None\ndirection=np.array([10, 2, 0])\nupdate_value()",
                align_left=ll,
                vector=mn.UP * 3,
            )
            ll.group_appear(self, rt)
            self.wait(pause)

            ln = cll([0, 12, 12345, "'", '^"', ".", "_.,", "Aa"])
            ll.update_value(self)
            self.wait(pause)

            ln = cll([0, 12, 12345, "'", '^"'])
            ll.update_value(self)
            self.wait(pause)

            ln = cll([])
            ll.update_value(self)
            self.wait(pause)

            ln = cll([0, 12])
            ll.update_value(self)
            self.wait(pause)

            ln = cll([0, 12, 12345, "'", '^"'])
            ll.update_value(self)
            self.wait(pause)

            ln = cll([0, 12, 12345, "'", '^"', ".", "_.,", "Aa"])
            ll.update_value(self)
            self.wait(pause)

            ln = cll([0, 12, 12345, "'", '^"', ".", "_.,", "Aa", "acv", "gjy", "gyp"])
            ll.update_value(self)
            self.wait(pause)
            self.clear()

        def highlights_1to3(self):
            pause = 0.5
            lln = LinkedList(
                lambda: cll([1, 0, 2, 0, 3, 0, 4, 0, 5]),
                # vector=mn.LEFT * 4.8,
            )
            rt = RelativeText(
                "pointers()   highlight_containers_1to3()",
                mob_center=lln,
                vector=mn.UP * 2,
            )
            lln.group_appear(self, rt)

            lln.pointers(2, 4, 6)
            lln.highlight_containers_1to3(2, 4, 6)
            self.wait(pause)
            lln.pointers(3, 4, 5)
            lln.highlight_containers_1to3(3, 4, 5)
            self.wait(pause)
            lln.pointers(4, 4, 4)
            lln.highlight_containers_1to3(4, 4, 4)
            self.wait(pause)
            lln.pointers(5, 4, 3)
            lln.highlight_containers_1to3(5, 4, 3)
            self.wait(pause)
            lln.pointers(5, 3, 3)
            lln.highlight_containers_1to3(5, 3, 3)
            self.wait(pause)
            lln.pointers(5, 4, 3)
            lln.highlight_containers_1to3(5, 4, 3)
            self.wait(pause)
            lln.pointers(5, 5, 3)
            lln.highlight_containers_1to3(5, 5, 3)
            self.wait(pause)
            lln.pointers(5, 5, 60)
            lln.highlight_containers_1to3(5, 5, 60)
            self.wait(pause)
            lln.clear_containers_highlights()
            lln.clear_pointers_highlights(0)
            self.wait(1)
            self.clear()

        def highlights_monocolor(self):
            pause = 1
            ln = cll([0, 1, 2, 3, 4, 5])
            lln = LinkedList(
                lambda: ln,
            )
            rt = RelativeText(
                "pointers()   highlight_containers_monocolor()",
                mob_center=lln,
                vector=mn.UP * 2,
            )
            lln.group_appear(self, rt)

            lln.highlight_containers_monocolor([0, 1, 2])
            self.wait(pause)
            lln.highlight_containers_monocolor([3, 4, 5, 6, 7])
            self.wait(pause)

            ln = cll([0, 1, 2, 3, 4, 5, 6, 7])
            lln.update_value(self)
            self.wait(pause)
            lln.highlight_containers_monocolor([0, 2, 4, 6])
            self.wait(pause)
            lln.highlight_containers_monocolor([1, 3, 5, 7])
            self.wait(pause)
            self.clear()

        def highlight_on_value(self):
            pause = 0.5
            ln = cll([10, 2, 3000, 2, 100, 2, 40])
            ll = LinkedList(lambda: ln)
            ll.first_appear(self)

            rt = RelativeText(
                "highlight_containers_with_value()   pointers_on_value()",
                vector=mn.UP * 2,
            )
            rt.first_appear(self)
            self.wait(pause)

            ll.highlight_containers_with_value(2)
            ll.pointers_on_value(2)
            self.wait(pause)

            ln = cll([22, 0, 22, 0, 22, 0])
            ll.update_value(self)
            ll.highlight_containers_with_value(0)
            ll.pointers_on_value(0)
            self.wait(pause)

            ln = cll([0, 22, 0, 22, 0, 22])
            ll.update_value(self)
            ll.highlight_containers_with_value(0, color=mn.LIGHT_BROWN)
            ll.pointers_on_value(0, color=mn.LIGHT_BROWN)
            self.wait(pause)

            ln = cll([22, 0, 22, 0, 22, 0])
            ll.update_value(self, animate=True)
            ll.highlight_containers_with_value(0, color=mn.LIGHT_BROWN)
            ll.pointers_on_value(0, color=mn.LIGHT_BROWN)
            self.wait(pause)

            ln = cll([0, 22, 0, 22, 0, 22])
            ll.update_value(self)
            ll.update_value(self, animate=True)
            ll.highlight_containers_with_value(0, color=mn.PURPLE)
            ll.pointers_on_value(0, color=mn.PURPLE)
            self.wait(pause)

            ln = cll([22, 0, 22, 0, 22])
            ll.update_value(self)
            ll.update_value(self, animate=True)
            ll.highlight_containers_with_value(0, color=mn.PURPLE)
            ll.pointers_on_value(0, color=mn.PURPLE)
            self.wait(pause)

            ln = cll([0, 22, 0, 22, 0, 22])
            ll.update_value(self)
            ll.update_value(self, animate=True)
            ll.highlight_containers_with_value(0, color=mn.PINK)
            ll.pointers_on_value(0, color=mn.PINK)
            self.wait(pause)

            ln = cll([22, 0, 22, 0, 22])
            ll.update_value(self)
            ll.update_value(self, animate=True)
            ll.highlight_containers_with_value(0, color=mn.PINK)
            ll.pointers_on_value(0, color=mn.PINK)
            self.wait(1)

        # ========== calls ==============

        positioning(self)
        rotation(self)
        updatevalue(self)
        highlights_1to3(self)
        highlights_monocolor(self)
        highlight_on_value(self)

        # ========== finish ==============

        self.wait(1)
        self.renderer.file_writer.output_file = f"./{self.__class__.__name__}.mp4"  # type: ignore


class Example_code_block(mn.Scene):
    def construct(self):
        self.camera.background_color = mn.DARK_GREY  # type: ignore
        pause = 1

        # ======== INPUTS ============

        code = """
This is code_lines.  # 0
It is possible to highlight them  # 1
one by one,  # 2
or  # 3

several  # 5

at once.  # 7 

When highlight(...) calls,  # 9
or calls without args,  # 10
the old highlight clears.  # 11

It is impossible to highlight empty lines. # 13
"""

        def main(self):

            # Construction code_block
            cb = CodeBlock(
                code,
                vector=mn.RIGHT * 3,
                font_size=25,
            )
            # Animation code_block
            cb.first_appear(self)

            title = RelativeText(
                "highlight(0)",
                vector=mn.UP * 3.2 + mn.LEFT * 5.5,
                font_size=30,
            )
            title.first_appear(self)

            def highlight_with_title(
                self: mn.Scene,
                code_block: CodeBlock,
                old_title: mn.Mobject,
                *indices: int,
                pause=2,
            ):
                code_block.highlight(*indices)

                left_point = old_title.get_left()
                self.remove(old_title)

                args_str = f"({', '.join(map(str, indices))})"

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
            title = highlight_with_title(self, cb, title, 3, 5, 7, pause=2)
            title = highlight_with_title(self, cb, title, 9, 10, 11, pause=2)
            title = highlight_with_title(self, cb, title, 13)
            title = highlight_with_title(self, cb, title, 0, 2, 4, 6, 8, 10, 12)
            title = highlight_with_title(self, cb, title, 1, 3, 5, 7, 9, 11, 13)

            self.remove(cb)

        # ========== calls ==============

        main(self)

        # ========== FINISH ==============

        self.wait(pause)
        self.renderer.file_writer.output_file = f"./{self.__class__.__name__}.mp4"  # type: ignore


class Example_code_block_lense(mn.Scene):
    def construct(self):
        self.camera.background_color = mn.DARK_GREY  # type: ignore

        # ========== INPUTS ==============
        pause = 1

        code = """
This is CodeBlockLense # 0

It is needed for displaying # 2
    large code blocks # 3
        that do not fit # 4
    entirely in screen height, # 5
and need scrolling. # 6

The limit parameter determines # 8
    how many lines are displayed # 9
        in the block. # 10

There is a restriction on limit: # 12
    7 lines. # 13
If your code is shorter - # 14
    scrolling makes no sense, # 15
        use CodeBlock. # 16

Unlike CodeBlock, # 18
    CodeBlockLense # 19
has restrictions on highlighting: # 20
    - only consecutive lines # 21
        can be highlighted # 22
    - no more than three at once. # 23

As in CodeBlock, # 25
    empty lines # 26
        are not highlighted. # 27
"""

        def main(self):

            cb = CodeBlockLense(
                code,
                vector=mn.DOWN * 0.3 + mn.RIGHT * 2.0,
                font="Monospace",
            )
            cb.first_appear(self)
            self.wait(pause)

            title = RelativeText(
                "highlight(0)",
                vector=mn.UP * 3.2 + mn.LEFT * 5.5,
                font_size=30,
            )
            title.first_appear(self)

            def highlight_with_title(
                self: mn.Scene,
                code_block: CodeBlockLense,
                old_title: mn.Mobject,
                *indices: int,
                pause=1,
            ):
                code_block.highlight(self, *indices)

                left_point = old_title.get_left()
                self.remove(old_title)

                args_str = f"(mn.scene, {', '.join(map(str, indices))})"

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

            title = highlight_with_title(self, cb, title, 2)
            title = highlight_with_title(self, cb, title, 3)
            title = highlight_with_title(self, cb, title, 4)
            title = highlight_with_title(self, cb, title, 5)
            title = highlight_with_title(self, cb, title, 6)

            title = highlight_with_title(self, cb, title, 8)
            title = highlight_with_title(self, cb, title, 9)
            title = highlight_with_title(self, cb, title, 10)

            title = highlight_with_title(self, cb, title, 12, 13)
            title = highlight_with_title(self, cb, title, 14)
            title = highlight_with_title(self, cb, title, 15)
            title = highlight_with_title(self, cb, title, 16)

            title = highlight_with_title(self, cb, title, 18, 19, 20)
            title = highlight_with_title(self, cb, title, 21, 22)
            title = highlight_with_title(self, cb, title, 23)

            title = highlight_with_title(self, cb, title, 24, 25)
            title = highlight_with_title(self, cb, title, 26, 27)

            self.remove(cb)

        # ========== calls ==============

        main(self)

        # ========== FINISH ==============

        self.wait(pause)
        self.renderer.file_writer.output_file = f"./{self.__class__.__name__}.mp4"  # type: ignore
