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
    RelativeTextValueGroup,
    RelativeTextActive,
    RelativeText,
    CodeBlock,
    CodeBlockLense,
    TitleText,
    LinkedList,
    SemiRoundedRectangle,
    grid,
    AlgoManimBase,
)

group_appear = AlgoManimBase.group_appear


class Stub:
    a = [grid]


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

        head = """
        def selection_sort(arr: list[int]) -> list[int]:
        """
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
            head=head,
            vector=mn.DOWN * 0.3 + mn.RIGHT * 2.6,
            font="Monospace",
        )

        array = Array(
            lambda: arr,
            align_bottom=code_block,
            vector=mn.LEFT * 4.4,
            font_size=35,
        )

        length_text = RelativeTextValue(
            ("length", lambda: length, mn.WHITE),
            mob_center=array,
            align_top=code_block,
        )

        i_text = RelativeTextValue(
            ("i", lambda: i, mn.RED),
            mob_center=array,
            align_left=array,
            vector=mn.UP * 2.2,
        )

        k_text = RelativeTextValue(
            ("k", lambda: k, mn.GREEN),
            align_right=array,
            align_bottom=i_text,
        )

        min_text = RelativeTextValue(
            ("min_index", lambda: min_index, mn.BLUE),
            mob_center=array,
            vector=mn.UP * 1.4,
        )

        # ======== PRE-CYCLE LOGIC =============

        title.appear(self)
        array.first_appear(self)
        code_block.first_appear(self)

        code_block.highlight(0)
        length_text.first_appear(self)
        self.wait(pause)

        # self.add(
        #     length_text,
        #     i_text,
        #     min_text,
        #     k_text,
        # )

        # grid(self)

        # ===== ALGORITHM CYCLE ==========

        for i in range(length - 1):
            code_block.highlight(2)
            i_text.update_value(self)
            array.highlight_pointers(i)
            array.highlight_containers(i)
            self.wait(pause)

            min_index = i
            code_block.highlight(3)
            array.highlight_pointers(i, min_index)
            array.highlight_containers(i, min_index)
            min_text.update_value(self)
            self.wait(pause)

            for k in range(i + 1, length):
                code_block.highlight(4)
                array.highlight_pointers(i, min_index, k)
                array.highlight_containers(i, min_index, k)
                k_text.update_value(self)
                self.wait(pause)

                code_block.highlight(5)
                self.wait(pause)
                if arr[k] < arr[min_index]:
                    #
                    min_index = k
                    code_block.highlight(6)
                    array.highlight_pointers(i, min_index, k)
                    array.highlight_containers(i, min_index, k)
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
            font_size=35,
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

        vl = mn.LEFT * 3.5
        vr = mn.RIGHT * 3.5
        vu = mn.UP * 1.3
        vd = mn.DOWN * 1.3
        vmc = mn.DOWN * 1
        type_font_size = 30
        mobs_font_size = 30

        type1 = RelativeText(
            "RelativeText",
            font_size=type_font_size,
            text_color=mn.BLACK,
            vector=vu + vl,
        )

        type2 = RelativeText(
            "RelativeTextActive",
            font_size=type_font_size,
            text_color=mn.BLACK,
            vector=vd + vl,
        )

        type3 = RelativeText(
            "RelativeTextValue",
            font_size=type_font_size,
            text_color=mn.BLACK,
            vector=vu + vr,
        )

        type4 = RelativeText(
            "RelativeTextValueGroup",
            font_size=type_font_size,
            text_color=mn.BLACK,
            vector=vd + vr,
        )

        s = "abc"

        t1 = RelativeText(
            s,
            font_size=mobs_font_size,
            mob_center=type1,
            vector=vmc,
        )

        t2 = RelativeTextActive(
            lambda: s,
            font_size=mobs_font_size,
            mob_center=type2,
            vector=vmc,
            anchor=None,
        )

        t3 = RelativeTextValue(
            ("text", lambda: s, mn.WHITE),
            font_size=mobs_font_size,
            mob_center=type3,
            vector=vmc,
            anchor=None,
        )

        t4 = RelativeTextValueGroup(
            # ("text", lambda: s, mn.DARK_BROWN),
            ("text", lambda: s, mn.LOGO_GREEN),
            ("text", lambda: s, mn.BLUE),
            font_size=mobs_font_size,
            mob_center=type4,
            vector=vmc,
            anchor=None,
        )

        def first_appear(self):
            pause = 1

            title = RelativeText(
                "first_appear() + remove()",
                font_size=50,
                text_color=mn.BLACK,
                align_screen=mn.UP,
                screen_buff=0.5,
            )
            title.first_appear(self)

            group_appear(self, type1, type2, type3, type4)
            self.wait(pause)

            p_text = RelativeTextValue(
                ("input", lambda: s, mn.BLACK),
                font_size=35,
                mob_center=title,
                vector=mn.DOWN * 1.0,
                anchor=None,
            )
            p_text.first_appear(self)
            self.wait(pause)

            t1.first_appear(self)
            t2.first_appear(self)
            t3.first_appear(self)
            t4.first_appear(self)
            self.wait(pause)
            self.remove(t1, t2, t3, t4)
            self.wait(pause)

            def cycle(new_val):
                nonlocal s
                s = new_val
                p_text.update_value(self)
                self.wait(pause)
                t1.first_appear(self)
                t2.first_appear(self)
                t3.first_appear(self)
                t4.first_appear(self)
                self.wait(pause)
                self.remove(t1, t2, t3, t4)
                self.wait(pause)

            cycle("ab")
            cycle("a")
            cycle("")
            cycle([1, 2, 3])
            cycle({"a": 1})

            self.clear()

        def groupp_appear(self):
            pause = 1
            nonlocal s
            s = "abc"

            title = RelativeText(
                "group_appear()",
                font_size=50,
                text_color=mn.BLACK,
                align_screen=mn.UP,
                screen_buff=0.5,
            )
            title.first_appear(self)

            group_appear(self, type1, type2, type3, type4)
            self.wait(pause)

            p_text = RelativeTextValue(
                ("input", lambda: s, mn.BLACK),
                font_size=35,
                mob_center=title,
                anchor=None,
                vector=mn.DOWN * 1.0,
            )
            p_text.first_appear(self)
            self.wait(pause)

            group_appear(self, t1, t2, t3, t4)
            self.wait(pause)
            self.remove(t1, t2, t3, t4)
            self.wait(pause)

            def cycle(
                new_val,
            ):
                nonlocal s
                s = new_val
                p_text.update_value(self)
                self.wait(pause)
                group_appear(self, t1, t2, t3, t4)
                self.wait(pause)
                self.remove(t1, t2, t3, t4)
                self.wait(pause)

            cycle("ab")
            cycle("a")
            cycle("")
            cycle("a")

            self.clear()

        def update(self):
            pause = 1
            nonlocal s
            s = "abc"

            title = RelativeText(
                "update_value()",
                font_size=50,
                text_color=mn.BLACK,
                align_screen=mn.UP,
                screen_buff=0.5,
            )
            title.first_appear(self)

            group_appear(self, type1, type2, type3, type4, animate=False)
            self.wait(pause)

            p_text = RelativeTextValue(
                ("input", lambda: s, mn.BLACK),
                font_size=35,
                mob_center=title,
                anchor=None,
                vector=mn.DOWN * 1.0,
            )
            p_text.first_appear(self)
            self.wait(pause)

            group_appear(self, t1, t2, t3, t4)
            self.wait(pause)

            def cycle(
                new_val,
            ):
                nonlocal s
                s = new_val
                p_text.update_value(self)
                self.wait(pause)
                t2.update_value(self)
                t3.update_value(self)
                t4.update_value(self)
                self.wait(pause)

            cycle("ab")
            cycle("a")
            cycle("")
            cycle([1, 2, 3])
            cycle({"a": 1})

            self.wait(pause)
            self.clear()

        def position(self):
            pause = 1
            s = "abc"

            title = RelativeText(
                "positioning",
                font_size=50,
                text_color=mn.BLACK,
                align_screen=mn.UP,
                screen_buff=0.5,
            )
            title.first_appear(self)

            group_appear(self, type1, type2, type3, type4)
            self.wait(pause)

            vd = mn.DOWN * 1

            p = None
            p_text = RelativeTextValue(
                ("alignment", lambda: p, mn.BLACK),
                font_size=35,
                mob_center=title,
                vector=mn.DOWN * 1.0,
                anchor=None,
            )

            p_text.update_value(self)
            self.wait(pause)
            t1 = RelativeText(
                s,
                font_size=mobs_font_size,
                mob_center=type1,
                vector=vd,
            )
            t2 = RelativeTextActive(
                lambda: s,
                font_size=mobs_font_size,
                mob_center=type2,
                vector=vd,
            )
            t3 = RelativeTextValue(
                ("text", lambda: s, mn.WHITE),
                font_size=mobs_font_size,
                mob_center=type3,
                vector=vd,
            )
            t4 = RelativeTextValueGroup(
                ("text", lambda: s, mn.LOGO_GREEN),
                ("text", lambda: s, mn.BLUE),
                font_size=mobs_font_size,
                mob_center=type4,
                vector=vd,
            )
            group_appear(self, t1, t2, t3, t4)
            self.wait(pause)
            self.remove(t1, t2, t3, t4)
            self.wait(pause)

            p = "align_left"
            p_text.update_value(self)
            self.wait(pause)
            t1 = RelativeText(
                s,
                font_size=mobs_font_size,
                mob_center=type1,
                align_left=type1,
                vector=vd,
            )
            t2 = RelativeTextActive(
                lambda: s,
                font_size=mobs_font_size,
                mob_center=type2,
                align_left=type2,
                vector=vd,
            )
            t3 = RelativeTextValue(
                ("text", lambda: s, mn.WHITE),
                font_size=mobs_font_size,
                mob_center=type3,
                align_left=type3,
                vector=vd,
            )
            t4 = RelativeTextValueGroup(
                ("text", lambda: s, mn.LOGO_GREEN),
                ("text", lambda: s, mn.BLUE),
                font_size=mobs_font_size,
                mob_center=type4,
                align_left=type4,
                vector=vd,
            )
            group_appear(self, t1, t2, t3, t4)
            self.wait(pause)
            self.remove(t1, t2, t3, t4)
            self.wait(pause)

            p = "align_right"
            p_text.update_value(self)
            self.wait(pause)
            t1 = RelativeText(
                s,
                font_size=mobs_font_size,
                mob_center=type1,
                align_right=type1,
                vector=vd,
            )
            t2 = RelativeTextActive(
                lambda: s,
                font_size=mobs_font_size,
                mob_center=type2,
                align_right=type2,
                vector=vd,
            )
            t3 = RelativeTextValue(
                ("text", lambda: s, mn.WHITE),
                font_size=mobs_font_size,
                mob_center=type3,
                align_right=type3,
                vector=vd,
            )
            t4 = RelativeTextValueGroup(
                ("text", lambda: s, mn.LOGO_GREEN),
                ("text", lambda: s, mn.BLUE),
                font_size=mobs_font_size,
                mob_center=type4,
                align_right=type4,
                vector=vd,
            )
            group_appear(self, t1, t2, t3, t4)
            self.wait(pause)
            self.remove(t1, t2, t3, t4)
            self.wait(pause)

            self.clear()

        # ========== calls ==============

        first_appear(self)
        groupp_appear(self)
        update(self)
        position(self)

        # ========== finish ==============

        self.wait(1)
        self.renderer.file_writer.output_file = f"./{self.__class__.__name__}.mp4"  # type: ignore


class Example_array(mn.Scene):
    def construct(self):
        self.camera.background_color = mn.GREY  # type: ignore

        pause = 1

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
            array_20.first_appear(self, appear_time=0.1)

            array_30 = Array(
                lambda: arr,
                mob_center=array,
                vector=mn.UP * 1.4,
                font_size=30,
            )
            array_30.first_appear(self, appear_time=0.1)

            array_40 = Array(
                lambda: arr,
                mob_center=array,
                vector=mn.DOWN * 1.5,
                font_size=40,
            )
            array_40.first_appear(self, appear_time=0.1)

            array_50 = Array(
                lambda: arr,
                mob_center=array,
                vector=mn.DOWN * 3.0,
                font_size=50,
            )
            array_50.first_appear(self, appear_time=0.1)

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
            array_20.first_appear(self, appear_time=0.1)

            array_30 = Array(
                lambda: arr,
                mob_center=array,
                align_left=array,
                vector=mn.UP * 1.4,
                font_size=30,
            )
            array_30.first_appear(self, appear_time=0.1)

            array_40 = Array(
                lambda: arr,
                mob_center=array,
                align_left=array,
                vector=mn.DOWN * 1.5,
                font_size=40,
            )
            array_40.first_appear(self, appear_time=0.1)

            array_50 = Array(
                lambda: arr,
                mob_center=array,
                align_left=array,
                vector=mn.DOWN * 3.0,
                font_size=50,
            )
            array_50.first_appear(self, appear_time=0.1)

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
            array_20.first_appear(self, appear_time=0.1)

            array_30 = Array(
                lambda: arr,
                mob_center=array,
                align_right=array,
                vector=mn.UP * 1.4,
                font_size=30,
            )
            array_30.first_appear(self, appear_time=0.1)

            array_40 = Array(
                lambda: arr,
                mob_center=array,
                align_right=array,
                vector=mn.DOWN * 1.5,
                font_size=40,
            )
            array_40.first_appear(self, appear_time=0.1)

            array_50 = Array(
                lambda: arr,
                mob_center=array,
                align_right=array,
                vector=mn.DOWN * 3.0,
                font_size=50,
            )
            array_50.first_appear(self, appear_time=0.1)

            self.wait(1)

            self.remove(
                array,
                array_20,
                array_30,
                array_40,
                array_50,
            )

        def first_appear(self):
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
            array.first_appear(self)
            self.wait(1.5)
            self.remove(array)

            def cycle(
                self,
                text: str,
            ):
                top_text = RelativeText(
                    text,
                    mob_center=array,
                    vector=mn.UP * 1.5,
                    font_size=30,
                )
                top_text.first_appear(self, hl_time=0.5)
                array.first_appear(self)
                self.wait(1.5)
                self.remove(array, top_text)
                self.wait(0.5)

            arr = [1, 2]
            cycle(self, "arr = [1,2]")

            arr = [1, 2, 3]
            cycle(self, "arr = [1,2,3]")

            array.highlight_containers(0, 1, 2)
            array.highlight_pointers(0, 1, 2)
            cycle(
                self,
                "array.highlight_containers(0,1,2)\narray.highlight_pointers(0,1,2)",
            )

            arr = []
            cycle(self, "arr = []")

            arr = [1, 2]
            cycle(self, "arr = [1,2]")

            array.clear_containers_highlights()
            array.clear_pointers_highlights()
            cycle(
                self,
                "array.clear_containers_highlights()\narray.clear_pointers_highlights()",
            )

            self.wait(pause)
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
            group_appear(self, array1, text1)
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
            group_appear(self, array2, text2)
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
            group_appear(self, array3, text3)
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
            group_appear(self, text1, array1, array2)
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
            group_appear(self, text2, array3, array4)
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
                pointers="both",
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
            group_appear(self, array1, text1)
            self.wait(pause)

            array2 = Array(
                lambda: arr,
                pointers="both",
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
            group_appear(self, array2, text2)
            self.wait(pause)

            array3 = Array(
                lambda: arr,
                pointers="both",
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
            group_appear(self, array3, text3)
            self.wait(pause)

            array1.highlight_pointers(0, 1, 2)
            array1.highlight_pointers(1, pos=1, color_1=mn.PINK)
            array2.highlight_pointers(0, 1, 2)
            array2.highlight_pointers(1, pos=1, color_1=mn.PINK)
            array3.highlight_pointers(0, 1, 2)
            array3.highlight_pointers(1, pos=1, color_1=mn.PINK)
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

            array1.highlight_pointers(0, 1, 2)
            array1.highlight_pointers(1, pos=1, color_1=mn.PINK)
            array2.highlight_pointers(0, 1, 2)
            array2.highlight_pointers(1, pos=1, color_1=mn.PINK)
            array3.highlight_pointers(0, 1, 2)
            array3.highlight_pointers(1, pos=1, color_1=mn.PINK)
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

            array1.highlight_pointers(0, 1, 2)
            array1.highlight_pointers(1, pos=1, color_1=mn.PINK)
            array2.highlight_pointers(0, 1, 2)
            array2.highlight_pointers(1, pos=1, color_1=mn.PINK)
            array3.highlight_pointers(0, 1, 2)
            array3.highlight_pointers(1, pos=1, color_1=mn.PINK)
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

            array1.highlight_pointers(0, 1, 2)
            array1.highlight_pointers(1, pos=1, color_1=mn.PINK)
            array2.highlight_pointers(0, 1, 2)
            array2.highlight_pointers(1, pos=1, color_1=mn.PINK)
            array3.highlight_pointers(0, 1, 2)
            array3.highlight_pointers(1, pos=1, color_1=mn.PINK)
            self.wait(1)

            self.wait(1)
            self.clear()

        def highlights(self):
            pause = 1

            title = RelativeText(
                "pointers_mode param; highlight_containers(); higlight_pointers()",
                font_size=30,
                text_color=mn.BLACK,
                align_screen=mn.UP,
                screen_buff=0.7,
            )
            title.first_appear(self)
            self.wait(1)

            command_text = RelativeText(
                "pointers_mode = 3",
                font_size=35,
                mob_center=title,
                vector=mn.DOWN * 1.2,
            )
            command_text.first_appear(self)
            self.wait(1)

            array = Array(
                lambda: [0, 0, 0, 0, 0],
                font_size=45,
            )
            array.first_appear(self)
            self.wait(1)

            indices = ()

            param_text = RelativeTextValue(
                ("indices_param", lambda: indices, mn.WHITE),
                font_size=35,
                mob_center=array,
                align_left=array,
                vector=mn.DOWN * 1.5,
            )

            def cycle(
                scene: mn.Scene,
                array: Array,
                text: RelativeTextValue,
                new_indices,
            ):
                nonlocal indices
                indices = new_indices
                text.update_value(scene, animate=False)
                array.highlight_containers(*new_indices)
                array.highlight_pointers(*new_indices)
                self.wait(pause)

            cycle(self, array, param_text, (0, 1, 2))
            cycle(self, array, param_text, (0, 0, 2))
            cycle(self, array, param_text, (0, 2, 2))
            cycle(self, array, param_text, (1, 2, 1))
            cycle(self, array, param_text, (1, 1, 1))

            array.clear_containers_highlights()
            array.clear_pointers_highlights()
            self.remove(command_text, array, param_text)
            self.wait(1)

            command_text = RelativeText(
                "pointers_mode = 5",
                font_size=35,
                mob_center=title,
                vector=mn.DOWN * 1.2,
            )
            command_text.first_appear(self)
            self.wait(1)

            array = Array(
                lambda: [0, 0, 0, 0, 0],
                font_size=45,
                pointers_mode=5,
            )
            array.first_appear(self)
            self.wait(1)

            cycle(self, array, param_text, (0, 1, 2, 3, 4))
            cycle(self, array, param_text, (0, 0, 2, 2, 5))
            cycle(self, array, param_text, (0, 0, 0, 2, 2))
            cycle(self, array, param_text, (0, 0, 0, 0))
            cycle(self, array, param_text, (0, 0, 0, 0, 0))
            cycle(self, array, param_text, (0, 0, 2, 3, 4))
            cycle(self, array, param_text, (0, 1, 0, 3, 4))
            cycle(self, array, param_text, (0, 1, 2, 0, 4))
            cycle(self, array, param_text, (0, 1, 2, 3, 0))
            cycle(self, array, param_text, (0, 1, 1, 3, 4))
            cycle(self, array, param_text, (0, 1, 2, 1, 4))
            cycle(self, array, param_text, (0, 1, 2, 3, 1))
            cycle(self, array, param_text, (0, 1, 2, 2, 4))
            cycle(self, array, param_text, (0, 1, 2, 3, 2))
            cycle(self, array, param_text, (0, 1, 2, 3, 3))
            cycle(self, array, param_text, (0, 1, 2, 3, 4))

            self.wait(1)
            self.remove(title)
            array.clear_pointers_highlights(0)
            array.clear_containers_highlights()

            self.clear()

        def positioning(self):
            pause = 1

            title = RelativeText(
                "positioning",
                font_size=40,
                text_color=mn.BLACK,
                align_screen=mn.UP + mn.RIGHT,
            )
            title.first_appear(self)

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
            group_appear(self, array, top_text)
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
            group_appear(self, array, top_text)
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
            group_appear(self, array, top_text)
            self.wait(pause)

            self.clear()
            self.add(title)

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
            group_appear(self, one, two)
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
            group_appear(self, array, top_text)
            self.wait(pause)
            self.remove(array, top_text)

            top_text = RelativeText(
                "align_left=one\nalign_top=two",
                vector=mn.UP * 1 + mn.RIGHT * 2,
                font_size=30,
            )
            array = Array(lambda: arr, align_left=one, align_top=two)
            group_appear(self, array, top_text)
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
            group_appear(self, array, top_text)
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
            group_appear(self, array, top_text)
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
            group_appear(self, array, top_text)
            self.wait(pause)
            self.clear()

        def update_value(self):
            pause = 0.5
            center = Array(lambda: list("mob_center"), font_size=50)
            title = RelativeText(
                "update_value()",
                vector=mn.LEFT * 4.4 + mn.UP * 3.2,
                text_color=mn.BLACK,
                font_size=50,
            )
            group_appear(self, center, title)

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

            group_appear(
                self,
                arr_1,
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

            def highlight_containers():
                arr_1.highlight_containers(0, 1, 2, 3)
                arr_2.highlight_containers(0, 1, 2, 3)
                arr_3.highlight_containers(0, 1, 2, 3)
                arr_4.highlight_containers(0, 1, 2, 3)
                arr_5.highlight_containers(0, 1, 2, 3)
                self.wait(pause)

            highlight_containers()

            def cycle(self, new_arr: list):
                nonlocal arr
                arr = new_arr
                arr_1.update_value(self)
                arr_2.update_value(self)
                arr_3.update_value(self)
                arr_4.update_value(self)
                arr_5.update_value(self)
                self.wait(pause)

            cycle(self, [1, 2])
            cycle(self, [1])
            cycle(self, [])
            cycle(self, [1])
            cycle(self, [1, 2])
            cycle(self, [1, 2, 3])
            cycle(self, [1, 2, 3, 4])

            self.remove(
                arr_1,
                arr_2,
                arr_3,
                arr_4,
                arr_5,
            )
            self.wait(pause)

            arr = []

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

            highlight_containers()

            group_appear(
                self,
                arr_1,
                arr_2,
                arr_3,
                arr_4,
                arr_5,
            )
            self.wait(1)

            cycle(self, [1])
            cycle(self, [])
            cycle(self, [1, 2])
            cycle(self, [1, 2, 3])

            self.wait(1)
            self.clear()

        def frame_import(self):
            pause = 0.5

            title = RelativeText(
                "frame_from param",
                font_size=50,
                text_color=mn.BLACK,
                align_screen=mn.UP,
                screen_buff=1,
            )
            self.add(title)

            donor_val = [100, 100, 100, 100, 100]
            donor = Array(
                lambda: donor_val,  # type: ignore
                font_size=35,
                vector=mn.UP * 1 + mn.RIGHT * 1,
                container_color=mn.BLUE,
                fill_color=mn.PINK,
            )
            donor_text = RelativeText("donor Array", font_size=30, mob_center=donor)
            donor_text.next_to(donor, mn.LEFT, buff=0.5)
            group_appear(self, donor, donor_text)
            self.wait(pause)

            rec_val = [0, 0, 0, 0, 0]
            recipient = Array(
                lambda: rec_val,
                font_size=25,
                mob_center=donor,
                align_left=donor,
                vector=mn.DOWN * 2,
                frame_from=donor,
                fill_color=mn.DARK_BROWN,
            )
            rec_text = RelativeText("recipient Array", font_size=30, mob_center=donor)
            rec_text.next_to(recipient, mn.LEFT, buff=0.5)
            group_appear(self, recipient, rec_text)
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

            rec_val = [10, 10, 10, 10, 10]
            recipient.update_value(self)
            self.wait(pause)

            rec_val = [100, 100, 100, 100, 100]
            recipient.update_value(self)
            self.wait(pause)

            rec_val = [1000, 1000, 1000, 1000, 1000]
            recipient.update_value(self)
            self.wait(pause)

            rec_val = [10000, 10000, 10000, 10000, 10000]
            recipient.update_value(self)
            self.wait(pause)

            rec_val = [0, 0, 0, 0, 0]
            recipient.update_value(self)
            self.wait(pause)

            donor_val = [10, 10, 10, 10, 10]
            donor.update_value(self)
            recipient.update_value(self)
            self.wait(pause)

            donor_val = [1, 1, 1, 1, 1]
            donor.update_value(self)
            recipient.update_value(self)
            self.wait(pause)

            donor_val = [10, 10, 10, 10, 10]
            donor.update_value(self)
            recipient.update_value(self)
            self.wait(1)

            self.remove(
                donor,
                recipient,
                func_text,
                donor_text,
                rec_text,
            )
            self.wait(1)

            # ---------------------------

            donor_val = "AAAAA"
            donor = String(
                lambda: donor_val,  # type: ignore
                font_size=35,
                vector=mn.UP * 1 + mn.RIGHT * 1,
                container_color=mn.BLUE,
                fill_color=mn.PINK,
            )
            donor_text = RelativeText(
                "donor String",
                font_size=30,
                mob_center=donor,
            )
            donor_text.next_to(donor, mn.LEFT, buff=0.5)
            group_appear(self, donor, donor_text)
            self.wait(pause)

            rec_val = [0, 0, 0, 0, 0]
            recipient = Array(
                lambda: rec_val,
                font_size=25,
                mob_center=donor,
                align_left=donor,
                vector=mn.DOWN * 2,
                frame_from=donor,
                fill_color=mn.DARK_BROWN,
            )
            rec_text = RelativeText(
                "recipient Array",
                font_size=30,
                mob_center=donor,
            )
            rec_text.next_to(recipient, mn.LEFT, buff=0.5)
            group_appear(self, recipient, rec_text)
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

            rec_val = [10, 10, 10, 10, 10]
            recipient.update_value(self)
            self.wait(pause)

            rec_val = [100, 100, 100, 100, 100]
            recipient.update_value(self)
            self.wait(pause)

            rec_val = [1000, 1000, 1000, 1000, 1000]
            recipient.update_value(self)
            self.wait(pause)

            rec_val = [0, 0, 0, 0, 0]
            recipient.update_value(self)
            self.wait(1)

            self.clear()

        def monocolor(self):
            pause = 1

            title = RelativeText(
                "highlight_containers_monocolor()",
                font_size=35,
                text_color=mn.BLACK,
                align_screen=mn.UP,
                screen_buff=0.7,
            )
            title.first_appear(self)
            self.wait(1)

            array = Array(
                lambda: [1, 2, 3, 4, 5, 6, 7, 8, 9],
                font_size=35,
            )
            array.first_appear(self)
            self.wait(1)

            indices = ()

            param_text = RelativeTextValue(
                ("indices_param", lambda: indices, mn.WHITE),
                font_size=35,
                mob_center=array,
                align_left=array,
                vector=mn.DOWN * 1.5,
            )

            def cycle(
                scene: mn.Scene,
                array: Array,
                text: RelativeTextValue,
                new_indices,
            ):
                nonlocal indices
                indices = new_indices
                text.update_value(scene, animate=False)
                array.highlight_containers_monocolor(new_indices)
                self.wait(pause)

            cycle(self, array, param_text, (0, 2, 4, 6, 8))
            cycle(self, array, param_text, (0, 1, 2, 3, 4))
            cycle(self, array, param_text, (5, 6, 7, 8))

            self.remove(title)
            array.clear_containers_highlights()

            self.clear()

        def highlight_containers_with_value(self):
            pause = 0.5
            arr = [10, 2, 3000, 2, 100, 1, 40]

            title = RelativeText(
                "highlight_containers_with_value()\nhighlight_pointers_above_value()",
                font_size=35,
                text_color=mn.BLACK,
                align_screen=mn.UP,
                screen_buff=0.7,
            )
            title.first_appear(self)
            self.wait(1)

            array = Array(
                lambda: arr,
                font_size=35,
            )
            array.first_appear(self)
            self.wait(1)

            def cycle(
                scene: mn.Scene,
                val: int,
                arr_new: list,
                color=None,
            ):
                nonlocal arr
                arr = arr_new
                array.update_value(scene)
                array.highlight_containers_with_value(val, color=color)
                array.highlight_pointers_above_value(val, 0, color)
                self.wait(pause)

            cycle(self, 0, [22, 0, 22, 0, 22, 0])
            cycle(self, 22, [22, 0, 22, 0, 22, 0, 22], mn.LIGHT_BROWN)
            cycle(self, 0, [22, 0, 22, 0, 22, 0], mn.LIGHT_BROWN)
            cycle(self, 22, [22, 0, 22, 0, 22, 0, 22], mn.PURPLE)
            cycle(self, 0, [22, 0, 22, 0, 22], mn.PURPLE)
            cycle(self, 22, [22, 0, 22, 0, 22, 0, 22], mn.PINK)
            cycle(self, 0, [22, 0, 22, 0, 22], mn.PINK)

            self.remove(title)

            self.clear()

        def highlight_containers_with_values(self):
            pause = 0.5

            title = RelativeText(
                "highlight_containers_with_values();  text_color_with_values()",
                font_size=35,
                text_color=mn.BLACK,
                align_screen=mn.UP,
                screen_buff=0.7,
            )
            title.first_appear(self)
            self.wait(1)

            arr = [0, 1, 2, 0, 1, 2]

            cont_mapp = {
                0: "#FF0000",
                1: "#FFFFFF",
                2: "#0000FF",
            }
            text_mapp = {
                1: "#000000",
                2: mn.YELLOW,
            }

            array = Array(
                lambda: arr,
                font_size=35,
                weight="BOLD",
            )
            array.first_appear(self)
            self.wait(1)

            array.highlight_containers_with_values(cont_mapp)
            array.text_color_with_values(text_mapp)
            self.wait(pause)

            arr = [2, 2, 1, 1, 0, 0]
            array.update_value(self)
            array.highlight_containers_with_values(cont_mapp)
            array.text_color_with_values(text_mapp)
            self.wait(pause)

            arr = [0, 0, 1, 1, 2, 2]
            array.update_value(self)
            array.highlight_containers_with_values(cont_mapp)
            array.text_color_with_values(text_mapp)
            self.wait(1)

            arr = [0, 1, 2, 0, 1, 2]
            array.update_value(self, animate=False)
            array.highlight_containers_with_values(cont_mapp)
            array.text_color_with_values(text_mapp)
            self.wait(pause)

            arr = [2, 2, 1, 1, 0, 0]
            array.update_value(self, animate=False)
            array.highlight_containers_with_values(cont_mapp)
            array.text_color_with_values(text_mapp)
            self.wait(pause)

            arr = [0, 0, 1, 1, 2, 2]
            array.update_value(self, animate=False)
            array.highlight_containers_with_values(cont_mapp)
            array.text_color_with_values(text_mapp)
            self.wait(1)

            self.remove(title)

            self.clear()

        def pointers_on_values(self):
            pause = 0.5
            arr = ["A", 0, "B", 1, "C", 2, "D"]
            st = [0, 1, 2]

            title = RelativeText(
                "pointers_on_values()",
                font_size=35,
                text_color=mn.BLACK,
                align_screen=mn.UP,
                screen_buff=0.7,
            )
            title.first_appear(self)
            self.wait(1)

            array = Array(
                lambda: arr,
                font_size=35,
                weight="BOLD",
            )
            array.first_appear(self)
            self.wait(1)

            set_text = RelativeTextValue(
                ("collection", lambda: st, mn.BLACK),
                font_size=30,
                mob_center=title,
                vector=mn.DOWN * 1,
            )
            set_text.first_appear(self)
            self.wait(1)

            array.highlight_pointers_above_values(st, 1, mn.ORANGE)
            self.wait(1)

            array.highlight_containers(0, 2, 4)
            array.highlight_pointers(0, 2, 4)
            self.wait(pause)

            arr = [0, "B", 1, "C", 2, "D"]
            array.update_value(self)
            self.wait(pause)

            arr = ["B", 1, "C", 2, "D"]
            array.update_value(self)
            self.wait(pause)

            arr = ["A", "B", "C", "D"]
            array.update_value(self)
            self.wait(1)

            self.remove(array)

            self.clear()

        # ========== calls ==============

        pyramid(self)
        first_appear(self)
        direction(self)
        lockwidth(self)
        pointers(self)
        highlights(self)
        positioning(self)
        update_value(self)
        frame_import(self)
        monocolor(self)
        highlight_containers_with_value(self)
        highlight_containers_with_values(self)
        pointers_on_values(self)

        # ========== finish ==============

        self.wait(1)
        self.renderer.file_writer.output_file = f"./{self.__class__.__name__}.mp4"  # type: ignore


class Example_string(mn.Scene):
    def construct(self):
        self.camera.background_color = mn.GREY  # type: ignore

        pause = 1

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
            string_20.first_appear(self, appear_time=0.1)

            string_25 = String(
                lambda: s,
                mob_center=string,
                vector=mn.UP * 1.4,
                font_size=30,
            )
            string_25.first_appear(self, appear_time=0.1)

            string_35 = String(
                lambda: s,
                mob_center=string,
                vector=mn.DOWN * 1.5,
                font_size=37,
            )
            string_35.first_appear(self, appear_time=0.1)

            string_40 = String(
                lambda: s,
                mob_center=string,
                vector=mn.DOWN * 3.0,
                font_size=40,
            )
            string_40.first_appear(self, appear_time=0.1)

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
            string_20.first_appear(self, appear_time=0.1)

            string_25 = String(
                lambda: s,
                mob_center=string,
                vector=mn.UP * 1.4,
                font_size=30,
                align_left=string,
            )
            string_25.first_appear(self, appear_time=0.1)

            string_35 = String(
                lambda: s,
                mob_center=string,
                vector=mn.DOWN * 1.5,
                font_size=37,
                align_left=string,
            )
            string_35.first_appear(self, appear_time=0.1)

            string_40 = String(
                lambda: s,
                mob_center=string,
                vector=mn.DOWN * 3.0,
                font_size=40,
                align_left=string,
            )
            string_40.first_appear(self, appear_time=0.1)

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
            string_20.first_appear(self, appear_time=0.1)

            string_25 = String(
                lambda: s,
                mob_center=string,
                vector=mn.UP * 1.4,
                font_size=30,
                align_right=string,
            )
            string_25.first_appear(self, appear_time=0.1)

            string_35 = String(
                lambda: s,
                mob_center=string,
                vector=mn.DOWN * 1.5,
                font_size=37,
                align_right=string,
            )
            string_35.first_appear(self, appear_time=0.1)

            string_40 = String(
                lambda: s,
                mob_center=string,
                vector=mn.DOWN * 3.0,
                font_size=40,
                align_right=string,
            )
            string_40.first_appear(self, appear_time=0.1)

            self.wait(1)
            self.clear()

        def first_appear(self):

            from typing import cast, Callable

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
                cast(Callable[[], str], lambda: s),
                font_size=40,
            )
            string.first_appear(self)
            self.wait(1.5)
            self.remove(string)

            def cycle(
                self,
                text: str,
            ):
                top_text = RelativeText(
                    text,
                    mob_center=string,
                    vector=mn.UP * 1.5,
                    font_size=30,
                )
                top_text.first_appear(self, hl_time=0.5)
                string.first_appear(self)
                self.wait(1.5)
                self.remove(string, top_text)
                self.wait(0.5)

            s = "ab"
            cycle(self, "s = 'ab'")

            s = ""
            cycle(self, "s = ''")

            s = "abc"
            cycle(self, "s = 'abc'")

            string.highlight_containers(0, 1, 2)
            string.highlight_pointers(0, 1, 2)
            cycle(
                self,
                "string.highlight_containers(0,1,2)\nstring.highlight_pointers(0,1,2)",
            )

            s = ""
            cycle(self, "s = ''")

            s = "abc"
            cycle(self, "s = 'abc'")

            string.clear_containers_highlights()
            string.clear_pointers_highlights()
            cycle(
                self,
                "string.clear_containers_highlights()\nstring.clear_pointers_highlights()",
            )

            self.wait(pause)
            self.clear()

        def pointers(self):

            s = "abc"

            title = RelativeText(
                "pointers param",
                font_size=50,
                text_color=mn.BLACK,
                align_screen=mn.DOWN,
                screen_buff=1,
            )
            title.first_appear(self)

            string1 = String(
                lambda: s,
                pointers="both",
                align_screen=mn.LEFT,
                screen_buff=0.7,
            )
            text1 = RelativeText(
                'pointers="both"',
                font_size=30,
                mob_center=string1,
                vector=mn.UP * 1.3,
            )

            string2 = String(
                lambda: s,
                pointers="top",
                vector=mn.LEFT * 1.8,
            )
            text2 = RelativeText(
                'pointers="top"',
                font_size=30,
                mob_center=string2,
                vector=mn.DOWN * 1.3,
            )

            string3 = String(
                lambda: s,
                pointers="bottom",
                vector=mn.RIGHT * 1.8,
            )
            text3 = RelativeText(
                'pointers="bottom"',
                font_size=30,
                mob_center=string3,
                vector=mn.UP * 1.3,
            )

            string4 = String(
                lambda: s,
                pointers=None,
                align_screen=mn.RIGHT,
                screen_buff=0.7,
            )
            text4 = RelativeText(
                "pointers=None",
                font_size=30,
                mob_center=string4,
                vector=mn.DOWN * 1.3,
            )

            group_appear(
                self,
                string1,
                string2,
                string3,
                string4,
                text1,
                text2,
                text3,
                text4,
            )
            self.wait(1)

            string1.highlight_pointers(0, 1, 2)
            string1.highlight_pointers(1, pos=1, color_1=mn.PINK)
            string2.highlight_pointers(0, 1, 2)
            string2.highlight_pointers(1, pos=1, color_1=mn.PINK)
            string3.highlight_pointers(0, 1, 2)
            string3.highlight_pointers(1, pos=1, color_1=mn.PINK)
            string4.highlight_pointers(0, 1, 2)
            string4.highlight_pointers(1, pos=1, color_1=mn.PINK)
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
            group_appear(self, s, top_text)
            self.wait(pause)

            self.remove(s, top_text)

            top_text = RelativeText(
                "mob_center=mob_center\nalign_left=mob_center\nvector=mn.UP * 1",
                vector=mn.DOWN * 2 + mn.RIGHT * 0,
            )
            s = String(
                lambda: string, mob_center=center, align_left=center, vector=mn.UP * 2
            )
            group_appear(self, s, top_text)
            self.wait(pause)

            self.remove(s, top_text)

            top_text = RelativeText(
                "mob_center=mob_center\nalign_right=mob_center\nvector=mn.UP * 1",
                vector=mn.DOWN * 2 + mn.RIGHT * 0,
            )
            s = String(
                lambda: string, mob_center=center, align_right=center, vector=mn.UP * 2
            )
            group_appear(self, s, top_text)
            self.wait(pause)

            self.clear()

            one = String(lambda: "one", font_size=60, vector=mn.UP * 2.7 + mn.LEFT * 4)
            two = String(
                lambda: "two", font_size=60, vector=mn.DOWN * 2.4 + mn.RIGHT * 3
            )
            group_appear(self, one, two)
            self.wait(pause)

            # -----------------------

            top_text = RelativeText(
                "align_left=one\nalign_bottom=two",
                vector=mn.UP * 1 + mn.RIGHT * 2,
            )
            s = String(lambda: string, align_left=one, align_bottom=two)
            group_appear(self, s, top_text)
            self.wait(pause)
            self.remove(s, top_text)

            top_text = RelativeText(
                "align_left=one\nalign_top=two",
                vector=mn.UP * 1 + mn.RIGHT * 2,
            )
            s = String(lambda: string, align_left=one, align_top=two)
            group_appear(self, s, top_text)
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
            group_appear(self, s, top_text)
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
            group_appear(self, s, top_text)
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
            group_appear(self, s, top_text)
            self.wait(pause)
            self.clear()

        def update_value(self):
            pause = 0.5
            center = String(lambda: "mob_center", font_size=50)
            text_title = RelativeText(
                "update_value()",
                vector=mn.LEFT * 4.4 + mn.UP * 3.2,
                text_color=mn.BLACK,
                font_size=50,
            )
            group_appear(self, center, text_title)

            s = "123"
            str_1 = String(
                lambda: s,
                mob_center=center,
                vector=mn.UP * 1.5,
                anchor=None,
                pointers=None,
            )
            str_2 = String(
                lambda: s,
                mob_center=str_1,
                vector=mn.UP * 0.7,
                anchor="end",
                pointers=None,
            )
            str_3 = String(
                lambda: s,
                mob_center=str_2,
                vector=mn.UP * 0.7,
                anchor="start",
                pointers=None,
            )

            text_no_align = RelativeText(
                "no align_sides:", align_bottom=str_2, vector=mn.LEFT * 4.6
            )
            text_str_1 = RelativeText(
                "anchor=None", mob_center=str_1, vector=mn.RIGHT * 4.0
            )
            text_str_2 = RelativeText(
                'anchor="end"', mob_center=str_2, vector=mn.RIGHT * 4.6
            )
            text_str_3 = RelativeText(
                'anchor="start"', mob_center=str_3, vector=mn.RIGHT * 4.4
            )

            str_4 = String(
                lambda: s,
                align_left=center,
                vector=mn.DOWN * 1.5,
                pointers=None,
            )
            str_5 = String(
                lambda: s,
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

            group_appear(
                self,
                str_1,
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

            def highlight_containers():
                str_1.highlight_containers(0, 1, 2, 3)
                str_2.highlight_containers(0, 1, 2, 3)
                str_3.highlight_containers(0, 1, 2, 3)
                str_4.highlight_containers(0, 1, 2, 3)
                str_5.highlight_containers(0, 1, 2, 3)
                self.wait(pause)

            highlight_containers()

            def cycle(self, new_str: str):
                nonlocal s
                s = new_str
                str_1.update_value(self)
                str_2.update_value(self)
                str_3.update_value(self)
                str_4.update_value(self)
                str_5.update_value(self)
                self.wait(pause)

            cycle(self, "12")
            cycle(self, "1")
            cycle(self, "")
            cycle(self, "1")
            cycle(self, "12")
            cycle(self, "123")
            cycle(self, "1234")

            self.remove(
                str_1,
                str_2,
                str_3,
                str_4,
                str_5,
            )
            self.wait(pause)

            s = ""
            str_1 = String(
                lambda: s,
                mob_center=center,
                vector=mn.UP * 1.5,
                anchor=None,
                pointers=None,
            )
            str_2 = String(
                lambda: s,
                mob_center=str_1,
                vector=mn.UP * 0.7,
                anchor="end",
                pointers=None,
            )
            str_3 = String(
                lambda: s,
                mob_center=str_2,
                vector=mn.UP * 0.7,
                anchor="start",
                pointers=None,
            )
            str_4 = String(
                lambda: s,
                align_left=center,
                vector=mn.DOWN * 1.5,
                pointers=None,
            )
            str_5 = String(
                lambda: s,
                align_right=center,
                vector=mn.DOWN * 1.5,
                pointers=None,
            )

            highlight_containers()

            group_appear(
                self,
                str_1,
                str_2,
                str_3,
                str_4,
                str_5,
            )
            self.wait(1)

            cycle(self, "1")
            cycle(self, "")
            cycle(self, "12")
            cycle(self, "123")

            self.wait(1)
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
            title.first_appear(self)

            donor_val = [100, 100, 100, 100, 100]
            donor = Array(
                lambda: donor_val,  # type: ignore
                font_size=35,
                vector=mn.UP * 1 + mn.RIGHT * 1,
                container_color=mn.BLUE,
                fill_color=mn.PINK,
            )
            donor_text = RelativeText(
                "donor Array",
                font_size=30,
                mob_center=donor,
            )
            donor_text.next_to(donor, mn.LEFT, buff=0.5)
            group_appear(self, donor, donor_text)
            self.wait(pause)

            rec_val = "AAAAA"
            recipient = String(
                lambda: rec_val,
                font_size=25,
                mob_center=donor,
                align_left=donor,
                vector=mn.DOWN * 2,
                frame_from=donor,
                fill_color=mn.DARK_BROWN,
            )
            rec_text = RelativeText(
                "recipient String",
                font_size=30,
                mob_center=donor,
            )
            rec_text.next_to(recipient, mn.LEFT, buff=0.5)
            group_appear(self, recipient, rec_text)
            self.wait(pause)

            func_text = RelativeText(
                "update_value()",
                font_size=40,
                text_color=mn.BLACK,
                align_screen=mn.DOWN,
                screen_buff=1,
            )
            func_text.first_appear(self)
            self.wait(pause)

            donor_val = [10, 10, 10, 10, 10]
            donor.update_value(self)
            recipient.update_value(self)
            self.wait(pause)

            donor_val = [1, 1, 1, 1, 1]
            donor.update_value(self)
            recipient.update_value(self)
            self.wait(pause)

            donor_val = [10, 10, 10, 10, 10]
            donor.update_value(self)
            recipient.update_value(self)
            self.wait(1)

            self.remove(
                donor,
                recipient,
                func_text,
                donor_text,
                rec_text,
            )
            self.wait(1)

            # -------------------

            donor_val = "AAAAA"
            donor = String(
                lambda: donor_val,
                font_size=40,
                vector=mn.UP * 1 + mn.RIGHT * 1,
                container_color=mn.BLUE,
                fill_color=mn.PINK,
            )
            donor_text = RelativeText(
                "donor String",
                font_size=30,
                mob_center=donor,
            )
            donor_text.next_to(donor, mn.LEFT, buff=0.5)
            group_appear(self, donor, donor_text)
            self.wait(pause)

            rec_val = "AAAAA"
            recipient = String(
                lambda: rec_val,
                font_size=25,
                mob_center=donor,
                align_left=donor,
                vector=mn.DOWN * 2,
                frame_from=donor,
                fill_color=mn.DARK_BROWN,
            )
            rec_text = RelativeText(
                "recipient String",
                font_size=30,
                mob_center=donor,
            )
            rec_text.next_to(recipient, mn.LEFT, buff=0.5)
            group_appear(self, recipient, rec_text)
            self.wait(1)

            self.clear()

        def highlights(self):
            pause = 1

            title = RelativeText(
                "pointers()   highlight_containers()   higlight_pointers()",
                font_size=35,
                text_color=mn.BLACK,
                align_screen=mn.UP,
                screen_buff=0.7,
            )
            title.first_appear(self)
            self.wait(1)

            command_text = RelativeText(
                "pointers_mode = 3",
                font_size=35,
                mob_center=title,
                vector=mn.DOWN * 1.2,
            )
            command_text.first_appear(self)
            self.wait(1)

            string = String(
                lambda: "00000",
                font_size=45,
            )
            string.first_appear(self)
            self.wait(1)

            indices = ()

            param_text = RelativeTextValue(
                ("indices_param", lambda: indices, mn.WHITE),
                font_size=35,
                mob_center=string,
                align_left=string,
                vector=mn.DOWN * 1.5,
            )

            def cycle(
                scene: mn.Scene,
                string: String,
                text: RelativeTextValue,
                new_indices,
            ):
                nonlocal indices
                indices = new_indices
                text.update_value(scene, animate=False)
                string.highlight_containers(*new_indices)
                string.highlight_pointers(*new_indices)
                self.wait(pause)

            cycle(self, string, param_text, (0, 1, 2))
            cycle(self, string, param_text, (0, 0, 2))
            cycle(self, string, param_text, (0, 2, 2))
            cycle(self, string, param_text, (1, 2, 1))
            cycle(self, string, param_text, (1, 1, 1))

            string.clear_containers_highlights()
            string.clear_pointers_highlights()
            self.remove(command_text, string, param_text)
            self.wait(1)

            command_text = RelativeText(
                "pointers_mode = 5",
                font_size=35,
                mob_center=title,
                vector=mn.DOWN * 1.2,
            )
            command_text.first_appear(self)
            self.wait(1)

            string = String(
                lambda: "00000",
                font_size=45,
                pointers_mode=5,
            )
            string.first_appear(self)
            self.wait(1)

            cycle(self, string, param_text, (0, 1, 2, 3, 4))
            cycle(self, string, param_text, (0, 0, 2, 2, 5))
            cycle(self, string, param_text, (0, 0, 0, 2, 2))
            cycle(self, string, param_text, (0, 0, 0, 0))
            cycle(self, string, param_text, (0, 0, 0, 0, 0))
            cycle(self, string, param_text, (0, 0, 2, 3, 4))
            cycle(self, string, param_text, (0, 1, 0, 3, 4))
            cycle(self, string, param_text, (0, 1, 2, 0, 4))
            cycle(self, string, param_text, (0, 1, 2, 3, 0))
            cycle(self, string, param_text, (0, 1, 1, 3, 4))
            cycle(self, string, param_text, (0, 1, 2, 1, 4))
            cycle(self, string, param_text, (0, 1, 2, 3, 1))
            cycle(self, string, param_text, (0, 1, 2, 2, 4))
            cycle(self, string, param_text, (0, 1, 2, 3, 2))
            cycle(self, string, param_text, (0, 1, 2, 3, 3))
            cycle(self, string, param_text, (0, 1, 2, 3, 4))

            self.wait(1)
            self.remove(title)
            string.clear_pointers_highlights(0)
            string.clear_containers_highlights()

            self.clear()

        def highlights_monocolor(self):
            pause = 1
            s = "follow rab"
            string = String(lambda: s, anchor=None)
            top_text = RelativeText(
                "highlight_containers_monocolor()",
                vector=mn.UP * 2,
            )
            group_appear(self, string, top_text)
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
                "highlight_containers_with_value()\nhighlight_pointers_above_value()",
                vector=mn.UP * 2,
            )
            group_appear(self, string, top_text)
            self.wait(1)

            string.highlight_containers_with_value("f")
            string.highlight_pointers_above_value("f", pos=0)
            self.wait(pause)
            string.highlight_containers_with_value("t")
            string.highlight_pointers_above_value("t", pos=0)
            self.wait(pause)
            string.highlight_containers_with_value("a", color=mn.LIGHT_BROWN)
            string.highlight_pointers_above_value("a", color=mn.LIGHT_BROWN, pos=0)
            self.wait(pause)
            string.highlight_containers_with_value("b", color=mn.LIGHT_BROWN)
            string.highlight_pointers_above_value("b", color=mn.LIGHT_BROWN, pos=0)
            self.wait(pause)
            string.highlight_containers_with_value("l", color=mn.PURPLE)
            string.highlight_pointers_above_value("l", color=mn.PURPLE, pos=0)
            self.wait(pause)
            string.highlight_containers_with_value("w", color=mn.PURPLE)
            string.highlight_pointers_above_value("w", color=mn.PURPLE, pos=0)
            self.wait(pause)
            string.highlight_containers_with_value(" ", color=mn.PINK)
            string.highlight_pointers_above_value(" ", color=mn.PINK, pos=0)
            self.wait(1)
            self.clear()

        def pointers_on_values(self):
            pause = 0.5
            s = "A0B1C2D"
            st = {"0", "1", "2"}

            string = String(
                lambda: s,
                font_size=35,
                weight="BOLD",
            )
            title = RelativeText(
                "pointers_on_values()",
                text_color=mn.BLACK,
                font_size=50,
                align_screen=mn.UP,
                screen_buff=0.5,
            )
            group_appear(self, string, title)
            self.wait(1)

            set_text = RelativeTextValue(
                ("collection", lambda: st, mn.BLACK),
                font_size=30,
                mob_center=title,
                vector=mn.DOWN * 1,
            )
            set_text.first_appear(self)
            self.wait(1)

            string.highlight_pointers_above_values(st, 1, mn.ORANGE)
            self.wait(1)

            string.highlight_containers(0, 2, 4)
            string.highlight_pointers(0, 2, 4)
            self.wait(pause)

            s = "0B1C2D"
            string.update_value(self)
            self.wait(pause)

            s = "B1C2D"
            string.update_value(self)
            self.wait(pause)

            s = "ABCD"
            string.update_value(self)
            self.wait(1)

            self.remove(string)

            self.clear()

        # ========== calls ==============

        pyramid(self)
        first_appear(self)
        pointers(self)
        positioning(self)
        update_value(self)
        frame_import(self)
        highlights(self)
        highlights_monocolor(self)
        highlight_on_value(self)
        pointers_on_values(self)

        # ========== finish ==============

        self.wait(1)
        self.renderer.file_writer.output_file = f"./{self.__class__.__name__}.mp4"  # type: ignore


class Example_linked_list(mn.Scene):
    def construct(self):
        self.camera.background_color = mn.GREY  # type: ignore

        cll = LinkedList.create_linked_list
        pause = 1

        def first_appear(self):

            from typing import Callable, cast
            from algomanim.helpers.datastructures import ListNode

            ln = cll([1, 2, 3])

            title = RelativeText(
                "first_appear() + remove()",
                font_size=50,
                text_color=mn.BLACK,
                align_screen=mn.DOWN,
                screen_buff=1,
            )
            title.first_appear(self)

            ll = LinkedList(
                cast(Callable[[], ListNode | None], lambda: ln),
                radius=0.35,
            )
            ll.first_appear(self)
            self.wait(1.5)
            self.remove(ll)

            def cycle(
                self,
                text: str,
            ):
                top_text = RelativeText(
                    text,
                    mob_center=ll,
                    vector=mn.UP * 1.5,
                    font_size=30,
                )
                top_text.first_appear(self, hl_time=0.5)
                ll.first_appear(self)
                self.wait(1.5)
                self.remove(ll, top_text)
                self.wait(0.5)

            ln = cll([1, 2])
            cycle(self, "ln = cll([1, 2])")

            ln = cll([1, 2, 3])
            cycle(self, "ln = cll([1, 2, 3])")

            ll.highlight_containers(0, 1, 2)
            ll.highlight_pointers(0, 1, 2)
            cycle(
                self,
                "ll.highlight_containers(0,1,2)\nll.highlight_pointers(0,1,2)",
            )

            ln = cll([])
            cycle(self, "ln = cll([])")

            ln = cll([1, 2])
            cycle(self, "ln = cll([1, 2])")

            ll.clear_containers_highlights()
            ll.clear_pointers_highlights()
            cycle(
                self,
                "ll.clear_containers_highlights()\nll.clear_pointers_highlights()",
            )

            self.wait(pause)
            self.clear()

        def positioning(self):

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
            group_appear(self, ll, top_text)
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
            group_appear(self, ll, top_text)
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
            group_appear(self, ll, top_text)
            self.wait(pause)

            self.clear()

            one = Array(
                lambda: list("one"), font_size=60, vector=mn.UP * 2.7 + mn.LEFT * 4
            )
            two = Array(
                lambda: list("two"), font_size=60, vector=mn.DOWN * 2.4 + mn.RIGHT * 3
            )
            group_appear(self, one, two)
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
            group_appear(self, ll, top_text)
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
            group_appear(self, ll, top_text)
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
            group_appear(self, ll, top_text)
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
            group_appear(self, ll, top_text)
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
            group_appear(self, ll, top_text)
            self.wait(pause)
            self.clear()

        def pointers(self):

            ln = cll([1, 2, 3])

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

            ll1 = LinkedList(
                lambda: ln,
                pointers="both",
                align_screen=mn.LEFT,
                screen_buff=0.5,
            )

            text1 = RelativeText(
                "direction=mn.RIGHT",
                font_size=30,
                mob_center=ll1,
                align_left=ll1,
                vector=mn.UP * 2,
            )
            group_appear(self, ll1, text1)
            self.wait(pause)

            ll2 = LinkedList(
                lambda: ln,
                pointers="both",
                direction=mn.UP,
                vector=mn.LEFT * 1,
            )
            text2 = RelativeText(
                "direction=mn.UP",
                font_size=30,
                align_bottom=text1,
                align_left=ll2,
            )
            group_appear(self, ll2, text2)
            self.wait(pause)

            ll3 = LinkedList(
                lambda: ln,
                pointers="both",
                direction=mn.DOWN,
                vector=mn.RIGHT * 3,
            )
            text3 = RelativeText(
                "direction=mn.DOWN",
                font_size=30,
                align_bottom=text1,
                align_left=ll3,
            )
            group_appear(self, ll3, text3)
            self.wait(pause)

            ll1.highlight_pointers(0, 1, 2)
            ll1.highlight_pointers(1, pos=1, color_1=mn.PINK)
            ll2.highlight_pointers(0, 1, 2)
            ll2.highlight_pointers(1, pos=1, color_1=mn.PINK)
            ll3.highlight_pointers(0, 1, 2)
            ll3.highlight_pointers(1, pos=1, color_1=mn.PINK)
            self.wait(1)

            self.remove(
                ll1,
                ll2,
                ll3,
            )
            self.wait(pause)

            s = "top"
            p_text.update_value(self)
            self.wait(pause)

            ll1 = LinkedList(
                lambda: ln,
                pointers="top",
                align_screen=mn.LEFT,
                screen_buff=0.5,
            )
            ll1.first_appear(self)
            self.wait(pause)

            ll2 = LinkedList(
                lambda: ln,
                pointers="top",
                direction=mn.UP,
                vector=mn.LEFT * 1,
            )
            ll2.first_appear(self)
            self.wait(pause)

            ll3 = LinkedList(
                lambda: ln,
                pointers="top",
                direction=mn.DOWN,
                vector=mn.RIGHT * 3,
            )
            ll3.first_appear(self)
            self.wait(pause)

            ll1.highlight_pointers(0, 1, 2)
            ll1.highlight_pointers(1, pos=1, color_1=mn.PINK)
            ll2.highlight_pointers(0, 1, 2)
            ll2.highlight_pointers(1, pos=1, color_1=mn.PINK)
            ll3.highlight_pointers(0, 1, 2)
            ll3.highlight_pointers(1, pos=1, color_1=mn.PINK)
            self.wait(1)

            self.remove(
                ll1,
                ll2,
                ll3,
            )
            self.wait(pause)

            s = "bottom"
            p_text.update_value(self)
            self.wait(pause)

            ll1 = LinkedList(
                lambda: ln,
                pointers="bottom",
                align_screen=mn.LEFT,
                screen_buff=0.5,
            )
            ll1.first_appear(self)
            self.wait(pause)

            ll2 = LinkedList(
                lambda: ln,
                pointers="bottom",
                direction=mn.UP,
                vector=mn.LEFT * 1,
            )
            ll2.first_appear(self)
            self.wait(pause)

            ll3 = LinkedList(
                lambda: ln,
                pointers="bottom",
                direction=mn.DOWN,
                vector=mn.RIGHT * 3,
            )
            ll3.first_appear(self)
            self.wait(pause)

            ll1.highlight_pointers(0, 1, 2)
            ll1.highlight_pointers(1, pos=1, color_1=mn.PINK)
            ll2.highlight_pointers(0, 1, 2)
            ll2.highlight_pointers(1, pos=1, color_1=mn.PINK)
            ll3.highlight_pointers(0, 1, 2)
            ll3.highlight_pointers(1, pos=1, color_1=mn.PINK)
            self.wait(1)

            self.remove(
                ll1,
                ll2,
                ll3,
            )
            self.wait(pause)

            s = "None"
            p_text.update_value(self)
            self.wait(pause)

            ll1 = LinkedList(
                lambda: ln,
                pointers=None,
                align_screen=mn.LEFT,
                screen_buff=0.5,
            )
            ll1.first_appear(self)
            self.wait(pause)

            ll2 = LinkedList(
                lambda: ln,
                pointers=None,
                direction=mn.UP,
                vector=mn.LEFT * 1,
            )
            ll2.first_appear(self)
            self.wait(pause)

            ll3 = LinkedList(
                lambda: ln,
                pointers=None,
                direction=mn.DOWN,
                vector=mn.RIGHT * 3,
            )
            ll3.first_appear(self)
            self.wait(pause)

            ll1.highlight_pointers(0, 1, 2)
            ll1.highlight_pointers(1, pos=1, color_1=mn.PINK)
            ll2.highlight_pointers(0, 1, 2)
            ll2.highlight_pointers(1, pos=1, color_1=mn.PINK)
            ll3.highlight_pointers(0, 1, 2)
            ll3.highlight_pointers(1, pos=1, color_1=mn.PINK)

            self.wait(1)
            self.clear()

        def highlights(self):
            pause = 1

            title = RelativeText(
                "pointers_mode param; highlight_containers(); highlight_pointers()",
                font_size=30,
                text_color=mn.BLACK,
                align_screen=mn.UP,
                screen_buff=0.7,
            )
            title.first_appear(self)
            self.wait(1)

            command_text = RelativeText(
                "pointers_mode = 3",
                font_size=35,
                mob_center=title,
                vector=mn.DOWN * 1.2,
            )
            command_text.first_appear(self)
            self.wait(1)

            ll = LinkedList(
                lambda: cll([0, 0, 0, 0, 0]),
            )
            ll.first_appear(self)
            self.wait(1)

            indices = ()

            param_text = RelativeTextValue(
                ("indices_param", lambda: indices, mn.WHITE),
                font_size=35,
                mob_center=ll,
                align_left=ll,
                vector=mn.DOWN * 1.5,
            )

            def cycle(
                scene: mn.Scene,
                text: RelativeTextValue,
                new_indices,
            ):
                nonlocal indices
                indices = new_indices
                text.update_value(scene, animate=False)
                ll.highlight_containers(*new_indices)
                ll.highlight_pointers(*new_indices)
                self.wait(pause)

            cycle(self, param_text, (0, 1, 2))
            cycle(self, param_text, (0, 0, 2))
            cycle(self, param_text, (0, 2, 2))
            cycle(self, param_text, (1, 2, 1))
            cycle(self, param_text, (1, 1, 1))

            ll.clear_containers_highlights()
            ll.clear_pointers_highlights()
            self.remove(command_text, ll, param_text)
            self.wait(1)

            command_text = RelativeText(
                "pointers_mode = 5",
                font_size=35,
                mob_center=title,
                vector=mn.DOWN * 1.2,
            )
            command_text.first_appear(self)
            self.wait(1)

            ll = LinkedList(
                lambda: cll([0, 0, 0, 0, 0]),
                pointers_mode=5,
            )
            ll.first_appear(self)
            self.wait(1)

            cycle(self, param_text, (0, 1, 2, 3, 4))
            cycle(self, param_text, (0, 0, 2, 2, 5))
            cycle(self, param_text, (0, 0, 0, 2, 2))
            cycle(self, param_text, (0, 0, 0, 0))
            cycle(self, param_text, (0, 0, 0, 0, 0))
            cycle(self, param_text, (0, 0, 2, 3, 4))
            cycle(self, param_text, (0, 1, 0, 3, 4))
            cycle(self, param_text, (0, 1, 2, 0, 4))
            cycle(self, param_text, (0, 1, 2, 3, 0))
            cycle(self, param_text, (0, 1, 1, 3, 4))
            cycle(self, param_text, (0, 1, 2, 1, 4))
            cycle(self, param_text, (0, 1, 2, 3, 1))
            cycle(self, param_text, (0, 1, 2, 2, 4))
            cycle(self, param_text, (0, 1, 2, 3, 2))
            cycle(self, param_text, (0, 1, 2, 3, 3))
            cycle(self, param_text, (0, 1, 2, 3, 4))

            self.wait(1)
            self.remove(title)
            ll.clear_pointers_highlights(0)
            ll.clear_containers_highlights()

            self.clear()

        def rotation(self):
            pause = 0.3

            ll = LinkedList(
                lambda: cll([0, 1, 2]),
            )
            ll.appear(self)
            ll.highlight_pointers(0, 1, 2)
            self.wait(pause)

            self.remove(ll)
            ll = LinkedList(
                lambda: cll([0, 1, 2]),
                direction=np.array([10, -10, 0]),
            )
            ll.appear(self)
            ll.highlight_pointers(0, 1, 2)
            self.wait(pause)

            self.remove(ll)
            ll = LinkedList(
                lambda: cll([0, 1, 2]),
                direction=np.array([0, -10, 0]),
            )
            ll.appear(self)
            ll.highlight_pointers(0, 1, 2)
            self.wait(pause)

            self.remove(ll)
            ll = LinkedList(
                lambda: cll([0, 1, 2]),
                direction=np.array([-10, -10, 0]),
            )
            ll.appear(self)
            ll.highlight_pointers(0, 1, 2)
            self.wait(pause)

            self.remove(ll)
            ll = LinkedList(
                lambda: cll([0, 1, 2]),
                direction=np.array([-10, 0, 0]),
            )
            ll.appear(self)
            ll.highlight_pointers(0, 1, 2)
            self.wait(pause)

            self.remove(ll)
            ll = LinkedList(
                lambda: cll([0, 1, 2]),
                direction=np.array([-10, 10, 0]),
            )
            ll.appear(self)
            ll.highlight_pointers(0, 1, 2)
            self.wait(pause)

            self.remove(ll)
            ll = LinkedList(
                lambda: cll([0, 1, 2]),
                direction=np.array([0, 10, 0]),
            )
            ll.appear(self)
            ll.highlight_pointers(0, 1, 2)
            self.wait(pause)

            self.remove(ll)
            ll = LinkedList(
                lambda: cll([0, 1, 2]),
                direction=np.array([10, 10, 0]),
            )
            ll.appear(self)
            ll.highlight_pointers(0, 1, 2)
            self.wait(pause)

            self.remove(ll)
            ll = LinkedList(
                lambda: cll([0, 1, 2]),
            )
            ll.appear(self)
            ll.highlight_pointers(0, 1, 2)
            self.wait(1)
            self.remove(ll)

            self.wait(1)
            self.clear()

        def alignment(self):

            # ======== left | right alignment ============

            mob_center = Array(
                lambda: list("mob_center"),
                vector=mn.UP * 3,
                font_size=35,
            )
            mob_center.first_appear(self)

            ll1 = LinkedList(
                lambda: cll([0, 1, 2]),
                radius=0.3,
                mob_center=mob_center,
                align_right=mob_center,
                vector=mn.DOWN * 2,
            )
            ll2 = LinkedList(
                lambda: cll([0, 1, 2]),
                radius=0.3,
                mob_center=mob_center,
                align_left=mob_center,
                vector=mn.DOWN * 2,
            )

            rt1 = RelativeText(
                "mob_center=mob_center\nalign_right=mob_center\nvector=mn.DOWN * 2",
                mob_center=ll1,
                align_left=ll1,
                vector=mn.DOWN * 2 + mn.LEFT * 0.5,
            )
            rt2 = RelativeText(
                "mob_center=mob_center\nalign_left=mob_center\nvector=mn.DOWN * 2",
                mob_center=ll2,
                align_right=ll2,
                vector=mn.DOWN * 2 + mn.RIGHT * 0.5,
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
                vector=mn.UP * 0.3,
            )
            rt2 = RelativeText(
                "mob_center=mob_center\nalign_bottom=mob_center\nvector=mn.RIGHT * 5.3",
                align_right=mob_center,
                align_top=ll2,
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

        def update_value(self):

            from typing import cast, Callable
            from algomanim.helpers.datastructures import ListNode

            pause = 0.5
            center = Array(lambda: list("mob_center"), font_size=50)
            title = RelativeText(
                "update_value()",
                vector=mn.LEFT * 4.4 + mn.UP * 3.2,
                text_color=mn.BLACK,
                font_size=50,
            )
            group_appear(self, center, title)

            ln = cll([1, 2, 3])

            radius = 0.3

            ll_1 = LinkedList(
                cast(Callable[[], ListNode | None], lambda: ln),
                radius=radius,
                mob_center=center,
                vector=mn.UP * 1.5,
                anchor=None,
                pointers=None,
            )
            ll_2 = LinkedList(
                cast(Callable[[], ListNode | None], lambda: ln),
                radius=radius,
                mob_center=ll_1,
                vector=mn.UP * 0.7,
                anchor="end",
                pointers=None,
            )
            ll_3 = LinkedList(
                cast(Callable[[], ListNode | None], lambda: ln),
                radius=radius,
                mob_center=ll_2,
                vector=mn.UP * 0.7,
                anchor="start",
                pointers=None,
            )

            text_no_align = RelativeText(
                "no align_sides:",
                align_bottom=ll_2,
                vector=mn.LEFT * 4.6,
                font_size=30,
            )
            text_arr_3 = RelativeText(
                "anchor='start'",
                mob_center=ll_3,
                vector=mn.RIGHT * 4.4,
                font_size=30,
            )
            text_arr_1 = RelativeText(
                "anchor=None",
                mob_center=ll_1,
                align_left=text_arr_3,
                font_size=30,
            )
            text_arr_2 = RelativeText(
                "anchor='end'",
                mob_center=ll_2,
                align_left=text_arr_3,
                font_size=30,
            )

            ll_4 = LinkedList(
                cast(Callable[[], ListNode | None], lambda: ln),
                radius=radius,
                align_left=center,
                vector=mn.DOWN * 1.5,
                pointers=None,
            )
            ll_5 = LinkedList(
                cast(Callable[[], ListNode | None], lambda: ln),
                radius=radius,
                align_right=center,
                vector=mn.DOWN * 1.5,
                pointers=None,
            )

            text_arr_4 = RelativeText(
                "align_left=mob_center",
                align_left=ll_4,
                mob_center=ll_4,
                vector=mn.DOWN * 1.0 + mn.LEFT * 1,
                font_size=30,
            )
            text_arr_5 = RelativeText(
                "align_right=mob_center",
                align_right=ll_5,
                mob_center=ll_5,
                vector=mn.DOWN * 1.0 + mn.RIGHT * 1,
                font_size=30,
            )

            group_appear(
                self,
                ll_1,
                ll_2,
                ll_3,
                ll_4,
                ll_5,
                text_no_align,
                text_arr_1,
                text_arr_2,
                text_arr_3,
                text_arr_4,
                text_arr_5,
            )
            self.wait(2)

            def highlight_containers():
                ll_1.highlight_containers(0, 1, 2, 3)
                ll_2.highlight_containers(0, 1, 2, 3)
                ll_3.highlight_containers(0, 1, 2, 3)
                ll_4.highlight_containers(0, 1, 2, 3)
                ll_5.highlight_containers(0, 1, 2, 3)
                self.wait(pause)

            highlight_containers()

            def cycle(self, new_list: list):
                nonlocal ln
                ln = cll(new_list)
                ll_1.update_value(self)
                ll_2.update_value(self)
                ll_3.update_value(self)
                ll_4.update_value(self)
                ll_5.update_value(self)
                self.wait(pause)

            cycle(self, [1, 2])
            cycle(self, [1])
            cycle(self, [])
            cycle(self, [1])
            cycle(self, [1, 2])
            cycle(self, [1, 2, 3])
            cycle(self, [1, 2, 3, 4])

            self.remove(
                ll_1,
                ll_2,
                ll_3,
                ll_4,
                ll_5,
            )
            self.wait(pause)

            ln = cll([])
            ll_1 = LinkedList(
                cast(Callable[[], ListNode | None], lambda: ln),
                radius=radius,
                mob_center=center,
                vector=mn.UP * 1.5,
                anchor=None,
                pointers=None,
            )
            ll_2 = LinkedList(
                cast(Callable[[], ListNode | None], lambda: ln),
                radius=radius,
                mob_center=ll_1,
                vector=mn.UP * 0.7,
                anchor="end",
                pointers=None,
            )
            ll_3 = LinkedList(
                cast(Callable[[], ListNode | None], lambda: ln),
                radius=radius,
                mob_center=ll_2,
                vector=mn.UP * 0.7,
                anchor="start",
                pointers=None,
            )
            ll_4 = LinkedList(
                cast(Callable[[], ListNode | None], lambda: ln),
                radius=radius,
                align_left=center,
                vector=mn.DOWN * 1.5,
                pointers=None,
            )
            ll_5 = LinkedList(
                cast(Callable[[], ListNode | None], lambda: ln),
                radius=radius,
                align_right=center,
                vector=mn.DOWN * 1.5,
                pointers=None,
            )

            highlight_containers()

            group_appear(
                self,
                ll_1,
                ll_2,
                ll_3,
                ll_4,
                ll_5,
            )
            self.wait(1)

            cycle(self, [1])
            cycle(self, [])
            cycle(self, [1, 2])
            cycle(self, [1, 2, 3])

            self.wait(1)
            self.clear()

        def update_value_direction(self):

            ln = cll([0, 12, 12345, "'", '^"', ".", "_.,", "Aa", "acv", "gjy", "gyp"])

            title = RelativeText(
                "anchor='start'\ndirection=np.array([10, 2, 0])\nupdate_value()",
                align_screen=mn.LEFT + mn.UP,
                screen_buff=0.5,
            )
            title.first_appear(self)
            self.wait(pause)

            ll = LinkedList(
                lambda: ln,
                direction=np.array([10, 2, 0]),
                vector=mn.DOWN * 1,
                anchor="start",
            )
            ll.highlight_containers(0, 2, 4)
            ll.highlight_pointers(0, 2, 4)
            ll.first_appear(self)
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
                anchor="end",
            )
            ll.highlight_containers(0, 2, 4)
            ll.highlight_pointers(0, 2, 4)
            title = RelativeText(
                "anchor='end'\ndirection=np.array([10, 2, 0])\nupdate_value()",
                align_left=ll,
                vector=mn.UP * 3,
            )
            group_appear(self, ll, title)
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
                anchor="end",
            )
            ll.highlight_containers(0, 2, 4)
            ll.highlight_pointers(0, 2, 4)
            title = RelativeText(
                "anchor='end'\ndirection=np.array([-10, -2, 0])\nupdate_value()",
                align_left=ll,
                vector=mn.UP * 3,
            )
            group_appear(self, ll, title)
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
            ll.highlight_containers(0, 2, 4)
            ll.highlight_pointers(0, 2, 4)
            title = RelativeText(
                "anchor=None\ndirection=np.array([10, 2, 0])\nupdate_value()",
                align_left=ll,
                vector=mn.UP * 3,
            )
            group_appear(self, ll, title)
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
                "highlight_pointers()   highlight_containers()",
                mob_center=lln,
                vector=mn.UP * 2,
            )
            group_appear(self, lln, rt)

            lln.highlight_pointers(2, 4, 6)
            lln.highlight_containers(2, 4, 6)
            self.wait(pause)
            lln.highlight_pointers(3, 4, 5)
            lln.highlight_containers(3, 4, 5)
            self.wait(pause)
            lln.highlight_pointers(4, 4, 4)
            lln.highlight_containers(4, 4, 4)
            self.wait(pause)
            lln.highlight_pointers(5, 4, 3)
            lln.highlight_containers(5, 4, 3)
            self.wait(pause)
            lln.highlight_pointers(5, 3, 3)
            lln.highlight_containers(5, 3, 3)
            self.wait(pause)
            lln.highlight_pointers(5, 4, 3)
            lln.highlight_containers(5, 4, 3)
            self.wait(pause)
            lln.highlight_pointers(5, 5, 3)
            lln.highlight_containers(5, 5, 3)
            self.wait(pause)
            lln.highlight_pointers(5, 5, 60)
            lln.highlight_containers(5, 5, 60)
            self.wait(pause)
            lln.clear_containers_highlights()
            lln.clear_pointers_highlights(0)
            self.wait(1)
            self.clear()

        def highlights_monocolor(self):
            ln = cll([0, 1, 2, 3, 4, 5])
            lln = LinkedList(
                lambda: ln,
            )
            rt = RelativeText(
                "highlight_containers_monocolor()",
                mob_center=lln,
                vector=mn.UP * 2,
            )
            group_appear(self, lln, rt)

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

            title = RelativeText(
                "highlight_containers_with_value()   highlight_pointers_above_value()",
                vector=mn.UP * 2,
            )
            title.first_appear(self)
            self.wait(pause)

            ln = cll([10, 2, 3000, 2, 100, 2, 40])
            ll = LinkedList(lambda: ln)
            ll.first_appear(self)
            self.wait(pause)

            def cycle(
                scene: mn.Scene,
                val: int,
                list_new: list,
                color=None,
            ):
                nonlocal ln
                ln = cll(list_new)
                ll.update_value(scene)
                ll.highlight_containers_with_value(val, color=color)
                ll.highlight_pointers_above_value(val, 0, color=color)
                self.wait(pause)

            cycle(self, 0, [22, 0, 22, 0, 22, 0])
            cycle(self, 22, [22, 0, 22, 0, 22, 0, 22], mn.LIGHT_BROWN)
            cycle(self, 0, [22, 0, 22, 0, 22, 0], mn.LIGHT_BROWN)
            cycle(self, 22, [22, 0, 22, 0, 22, 0, 22], mn.PURPLE)
            cycle(self, 0, [22, 0, 22, 0, 22], mn.PURPLE)
            cycle(self, 22, [22, 0, 22, 0, 22, 0, 22], mn.PINK)
            cycle(self, 0, [22, 0, 22, 0, 22], mn.PINK)

            self.wait(pause)
            self.clear()

        def append(self):

            title = RelativeText(
                "append()",
                vector=mn.UP * 2,
            )
            title.first_appear(self)
            self.wait(pause)

            ll = LinkedList(lambda: cll([0]), vector=mn.LEFT * 1.7)
            ll.highlight_containers(0, 1, 2, 3)
            ll.first_appear(self)
            self.wait(pause)

            ll_1 = LinkedList(lambda: cll([1]))
            ll_2 = LinkedList(lambda: cll([2]))
            ll_3 = LinkedList(lambda: cll([3]))

            ll.append(self, ll_1)
            self.wait(pause)

            ll.append(self, ll_2)
            self.wait(pause)

            ll.append(self, ll_3)
            self.wait(pause)

            self.wait(pause)
            self.clear()

        # ========== calls ==============

        first_appear(self)
        positioning(self)
        pointers(self)
        rotation(self)
        highlights(self)
        alignment(self)
        update_value(self)
        update_value_direction(self)
        highlights_1to3(self)
        highlights_monocolor(self)
        highlight_on_value(self)
        append(self)

        # ========== finish ==============

        self.wait(1)
        self.renderer.file_writer.output_file = f"./{self.__class__.__name__}.mp4"  # type: ignore


class Example_code_block(mn.Scene):
    def construct(self):
        self.camera.background_color = mn.DARK_GREY  # type: ignore
        pause = 1

        def main(self):

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
            self.wait(0.5)
            self.clear()
            self.wait(1)

        def head(self):

            title = RelativeText(
                "head param",
                font_size=50,
                align_screen=mn.UP,
                screen_buff=0.5,
            )
            title.first_appear(self)
            self.wait(0.5)

            head1 = """
            def function(
                ---- dominant width ----
            ):
            """
            code1 = """
            0
            1
            2
            3
            4
            """

            head2 = """
            def func():
            """
            code2 = """
            0
            1
            2 ---- dominant width ----
            3
            4
            """

            cb1 = CodeBlock(
                code1,
                head=head1,
                vector=mn.LEFT * 3,
            )
            cb2 = CodeBlock(
                code2,
                head=head2,
                vector=mn.RIGHT * 3,
                align_bottom=cb1,
            )
            group_appear(self, cb1, cb2)
            self.wait(0.5)

            def highlight(*indices: int):
                cb1.highlight(*indices)
                cb2.highlight(*indices)
                self.wait(1)

            highlight(0)
            highlight(2)
            highlight(4)
            highlight(1, 3)
            highlight(0, 2, 4)
            highlight()

            self.remove(cb1, cb2)
            self.wait(0.5)
            self.clear()

        # ========== calls ==============

        main(self)
        head(self)

        # ========== FINISH ==============

        self.wait(pause)
        self.renderer.file_writer.output_file = f"./{self.__class__.__name__}.mp4"  # type: ignore


class Example_code_block_lense(mn.Scene):
    def construct(self):
        self.camera.background_color = mn.DARK_GREY  # type: ignore

        # ========== INPUTS ==============
        pause = 1

        def main(scene):

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
                - a bounded area, depending on the lines limit. #23

            As in CodeBlock, # 25
                empty lines # 26
                    are not highlighted. # 27

            As in CodeBlock, # 29
            passing no indices will clear highlighting. # 30
            Like in this one. # 31
            And back again. # 32

            Also, there is a `pre` param in highlight(). # 34
            It helps when you need to add mobs to the scene # 35
            that are not directly provided by the code. # 36
            """

            cb = CodeBlockLense(
                code,
                vector=mn.DOWN * 0.3 + mn.RIGHT * 2.0,
                font="Monospace",
            )
            cb.first_appear(scene)
            scene.wait(pause)

            param = "highlight(0)"

            title = RelativeTextActive(
                lambda: param,
                vector=mn.UP * 3.2 + mn.LEFT * 5.5,
                font_size=30,
            )

            def cycle(
                scene: mn.Scene,
                title: mn.Mobject,
                *indices: int,
                pre: bool = False,
            ):
                nonlocal param
                if not pre:
                    new_param = f"highlight({', '.join(map(str, indices))})"
                else:
                    new_param = f"highlight({', '.join(map(str, indices))}, pre=True)"
                param = new_param
                title.update_value(scene, animate=False)
                if not pre:
                    cb.highlight(*indices)
                else:
                    cb.highlight(*indices, pre=True)
                scene.wait(1)

            cycle(scene, title, 0)

            cycle(scene, title, 2)
            cycle(scene, title, 3)
            cycle(scene, title, 4)
            cycle(scene, title, 5)
            cycle(scene, title, 6)

            cycle(scene, title, 8)
            cycle(scene, title, 9)
            cycle(scene, title, 10)

            cycle(scene, title, 12, 13)
            cycle(scene, title, 14)
            cycle(scene, title, 15)
            cycle(scene, title, 16)

            cycle(scene, title, 18, 19, 20)
            cycle(scene, title, 21, 22)
            cycle(scene, title, 23)

            cycle(scene, title, 24, 25)
            cycle(scene, title, 26, 27)

            cycle(scene, title, 29)
            cycle(scene, title, 30)
            cycle(scene, title)
            cycle(scene, title, 32)

            cycle(scene, title, 34, pre=True)
            cycle(scene, title, 35, 36, pre=True)
            cycle(scene, title, 35, 36)

            scene.remove(cb)
            scene.wait(0.5)
            scene.clear()
            scene.wait(pause)

        def head(self):

            title = RelativeText(
                "head param",
                font_size=50,
                align_screen=mn.UP,
                screen_buff=0.5,
            )
            title.first_appear(self)
            self.wait(0.5)

            head1 = """
            def function(
                ---- dominant width ----
            ):
            """
            code1 = """
            0
            1
            2
            3
            4
            5
            6
            7
            8
            """

            head2 = """
            def func():
            """
            code2 = """
            0
            1
            2 ---- dominant width ----
            3
            4
            5
            6
            7
            8
            """

            cb1 = CodeBlockLense(
                code1,
                limit=8,
                head=head1,
                vector=mn.LEFT * 3,
            )
            cb2 = CodeBlockLense(
                code2,
                limit=8,
                head=head2,
                vector=mn.RIGHT * 3,
                align_bottom=cb1,
            )
            group_appear(self, cb1, cb2)
            self.wait(0.5)

            def highlight(*indices: int):
                cb1.highlight(*indices)
                cb2.highlight(*indices)
                self.wait(1)

            highlight(0, 1, 2)
            highlight(3, 4, 5)
            highlight(7)
            highlight(8)
            highlight(7)
            highlight(1)
            highlight()
            highlight(1)

            self.remove(cb1, cb2)
            self.wait(0.5)
            self.clear()

        # ========== calls ==============

        main(self)
        head(self)

        # ========== FINISH ==============

        self.wait(pause)
        self.renderer.file_writer.output_file = f"./{self.__class__.__name__}.mp4"  # type: ignore


class Example_semi_rounded_rectangle(mn.Scene):
    def construct(self):
        self.camera.background_color = mn.DARK_GREY  # type: ignore
        pause = 1

        def default(self):

            title = RelativeText(
                "default SemiRoundedRectangle",
                font_size=50,
                text_color=mn.WHITE,
                align_screen=mn.UP,
            )
            params = RelativeText(
                "width=3\nheight=2",
                font_size=40,
                text_color=mn.WHITE,
                align_screen=mn.DOWN,
                screen_buff=1.3,
            )
            group_appear(self, title, params)

            rect = SemiRoundedRectangle(
                width=3,
                height=2,
            )

            self.add(rect)

            self.wait(2)

            self.clear()
            self.wait(0.5)

        def non_default(self):

            font_size = 30

            title = RelativeText(
                "non-default SemiRoundedRectangle",
                font_size=50,
                text_color=mn.WHITE,
                align_screen=mn.UP,
            )

            params = RelativeText(
                "width=3\nheight=2\ncorner_radius=1\nfill_color = mn.GRAY_BROWN\nstroke_color = mn.PINK\nstroke_width = 10",
                font_size=25,
                text_color=mn.WHITE,
                vector=mn.UP * 1.5,
            )
            group_appear(self, title, params)

            corner_radius = 1
            fill_color = mn.GRAY_BROWN
            stroke_color = mn.PINK
            stroke_width = 10

            side = 4.5
            up = 1.5
            down = 1.5
            text_vector = mn.DOWN * 1.5

            rect1 = SemiRoundedRectangle(
                width=3,
                height=2,
                direction=mn.UP,
                corner_radius=corner_radius,
                fill_color=fill_color,
                stroke_color=stroke_color,
                stroke_width=stroke_width,
            )
            rect1.move_to(mn.LEFT * side + mn.UP * up)
            text1 = RelativeText(
                "direction=mn.UP",
                font_size=font_size,
                text_color=mn.WHITE,
                mob_center=rect1,
                vector=text_vector,
            )

            rect2 = SemiRoundedRectangle(
                width=3,
                height=2,
                direction=mn.DOWN,
                corner_radius=corner_radius,
                fill_color=fill_color,
                stroke_color=stroke_color,
                stroke_width=stroke_width,
            )
            rect2.move_to(mn.LEFT * side + mn.DOWN * down)
            text2 = RelativeText(
                "direction=mn.DOWN",
                font_size=font_size,
                text_color=mn.WHITE,
                mob_center=rect2,
                vector=text_vector,
            )

            rect3 = SemiRoundedRectangle(
                width=3,
                height=2,
                direction=mn.LEFT,
                corner_radius=corner_radius,
                fill_color=fill_color,
                stroke_color=stroke_color,
                stroke_width=stroke_width,
            )
            rect3.move_to(mn.RIGHT * side + mn.UP * up)
            text3 = RelativeText(
                "direction=mn.LEFT",
                font_size=font_size,
                text_color=mn.WHITE,
                mob_center=rect3,
                vector=text_vector,
            )

            rect4 = SemiRoundedRectangle(
                width=3,
                height=2,
                direction=mn.RIGHT,
                corner_radius=corner_radius,
                fill_color=fill_color,
                stroke_color=stroke_color,
                stroke_width=stroke_width,
            )
            rect4.move_to(mn.RIGHT * side + mn.DOWN * down)
            text4 = RelativeText(
                "direction=mn.RIGHT",
                font_size=font_size,
                text_color=mn.WHITE,
                mob_center=rect4,
                vector=text_vector,
            )

            self.add(
                rect1,
                rect2,
                rect3,
                rect4,
                text1,
                text2,
                text3,
                text4,
            )

            self.wait(2)

            self.clear()
            self.wait(0.5)

        # ========== calls ==============

        default(self)
        non_default(self)

        # ========== FINISH ==============

        self.wait(pause)
        self.renderer.file_writer.output_file = f"./{self.__class__.__name__}.mp4"  # type: ignore
