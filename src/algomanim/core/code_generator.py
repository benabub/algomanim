import pyperclip
from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Config:
    commands_dict = {
        "a": {  # appear
            "with_line": "with sound(appear, offset_appear",
            "code_line": "# .first_appear(self)\n",
        },
        "u": {  # update with var change check -> choose sound
            "with_line": "with sound(curr_sound, curr_offset",
            "code_line": "# .update_value(self)\n",
        },
        "U": {  # update with standard sound
            "with_line": "with sound(update, offset_update",
            "code_line": "# .update_value(self)\n",
        },
        "p": {  # point
            "with_line": "with sound(point, offset_point",
            "code_line": "# .highlight_containers_1to3()\n",
        },
        "s": {  # slide
            "with_line": "with sound(slide, offset_slide",
            "code_line": "# .highlight_containers_1to3()\n",
        },
    }
    suffix_dict = {
        False: "):\n",
        True: ", pause):\n",
    }
    tab = "    "
    base_tab = tab * 2


class CodeGenerator:
    """
    ...
    """

    CONFIG = Config()

    def __init__(
        self,
        code: str,
        commands_dict=CONFIG.commands_dict,
        suffix_dict=CONFIG.suffix_dict,
        tab=CONFIG.tab,
        base_tab=CONFIG.base_tab,
    ) -> None:
        self._code = code
        self._commands_dict = commands_dict
        self._suffix_dict = suffix_dict
        self._tab = tab
        self._base_tab = base_tab

    def _get_command_pair(
        self,
        command: str,
        indent: str,
        if_last: bool,
        pass_line: bool,
    ) -> str:

        curr_command_dict = self._commands_dict[command]
        with_line = indent + curr_command_dict["with_line"] + self._suffix_dict[if_last]
        code_line = indent + self._tab + curr_command_dict["code_line"]

        if not pass_line:
            return with_line + code_line
        else:
            dots = indent + self._tab + "...\n"
            return with_line + code_line + dots

    def _get_highlight_pair(
        self,
        indent: str,
        sound: str,
        offset: str,
        scene_arg: str,
        line_number: int,
        if_last: bool,
    ) -> str:
        with_line = (
            indent + f"with sound({sound}, {offset}{self._suffix_dict[if_last]}\n"
        )
        code_line = (
            indent + self._tab + f"code_block.highlight({scene_arg}{line_number})\n"
        )
        return with_line + code_line

    def generate(
        self,
        scene_param: bool = False,
    ) -> None:
        """Generate animation scaffolding with sound blocks from algorithm code.
        ...
        """

        # commands_dict = self._commands_dict
        # suffix_dict = self._suffix_dict

        tab = self._tab
        base_tab = self._base_tab

        if scene_param:
            scene_arg = "self, "
        else:
            scene_arg = ""

        code_lines = self._code.strip().split("\n")
        res = ""
        line_number = 0

        add_block_list = []

        # --------- main iterating -------------

        for line in code_lines:
            line = line.lstrip()
            indent = line[: len(line) - len(line)]

            if not line or line.startswith("#"):
                line_number += 1
                continue

            if re.search(r"=.$", line):
                main_part, tail = line.rsplit(" ", 1)
                commands = tail.split("=")[1:]
                line = main_part
                inline_commands = True
            else:
                inline_commands = False
                commands = ""

            # --------- head block -------------

            if (  # pre-highlight line - same indent
                line.startswith("if ")
                or line.startswith("break")
                or line.startswith("continue")
            ):
                if line.startswith("if "):
                    sound = "cycle"
                    offset = "offset_cycle"
                else:
                    sound = "step"
                    offset = "offset_step"

                highlight_pair = self._get_highlight_pair(
                    base_tab + indent,
                    sound,
                    offset,
                    scene_arg,
                    line_number,
                    not inline_commands,
                )

                line_3 = base_tab + line + "\n"
                line_4 = base_tab + indent + tab + "#\n"
                head_block = highlight_pair + line_3 + line_4

            elif (  # after-highlight line - plus indent
                line.startswith("else")
                or line.startswith("elif ")
                or line.startswith("while ")
            ):
                if line.startswith("for ") or line.startswith("while "):
                    sound = "cycle"
                    offset = "offset_cycle"
                else:
                    sound = "step"
                    offset = "offset_step"

                line_1 = base_tab + line + "\n"

                highlight_pair = self._get_highlight_pair(
                    base_tab + indent + tab,
                    sound,
                    offset,
                    scene_arg,
                    line_number,
                    not inline_commands,
                )

                line_4 = base_tab + indent + tab + "#\n"
                head_block = line_1 + highlight_pair + line_4

            elif (  # after-highlight line - plus indent
                line.startswith("for ")
            ):
                line_1 = base_tab + line + "\n"

                highlight_pair = self._get_highlight_pair(
                    base_tab + indent + tab,
                    "cycle",
                    "offset_cycle",
                    scene_arg,
                    line_number,
                    not inline_commands,
                )

                command_pair = self._get_command_pair(
                    command="p",
                    indent=base_tab + indent + tab,
                    if_last=not inline_commands,
                    pass_line=True,
                )

                line_7 = base_tab + indent + tab + "#\n"
                head_block = line_1 + highlight_pair + command_pair + line_7

            elif line.startswith("return "):  # return lines only - same indent
                line_1 = base_tab + indent + "# " + line + "\n"

                line_2 = base_tab + indent + "with sound(step, offset_step):\n"
                line_3 = (
                    base_tab
                    + tab
                    + indent
                    + f"code_block.highlight({scene_arg}{line_number})\n"
                )

                highlight_pair = self._get_highlight_pair(
                    base_tab + indent,
                    "step",
                    "offset_step",
                    scene_arg,
                    line_number,
                    not inline_commands,
                )

                line_4 = base_tab + indent + "with sound(rtn, offset_return, 3):\n"
                line_5 = base_tab + indent + tab + "...\n"
                line_6 = "\n"
                head_block = line_1 + line_2 + line_3 + line_4 + line_5 + line_6
            else:
                head_block = ""

            add_block_list.append(head_block)

            # --------- bottom block -------------

            if inline_commands:
                commands_lines_list = []

                if "u" not in commands:
                    sound_diff_line = ""
                else:
                    operands = line.split("=", 1)
                    val1 = operands[0].strip()
                    val2 = operands[1].strip()
                    sound_diff_line = (
                        base_tab
                        + indent
                        + f"curr_sound, curr_offset = sound_diff({val1}, {val2})"
                        + "\n"
                    )

                for j in range(len(commands)):
                    if j == len(commands) - 1:
                        if_last = True
                    else:
                        if_last = False

                    command_pair = self._get_command_pair(
                        command=commands[j],
                        indent=base_tab + indent,
                        if_last=if_last,
                        pass_line=True,
                    )
                    commands_lines_list.append(command_pair)

                commands_block = "".join(commands_lines_list)

                line_1 = base_tab + line + "\n"
                line_2 = base_tab + indent + "with sound(step, offset_step):\n"
                line_3 = (
                    base_tab
                    + indent
                    + tab
                    + f"code_block.highlight({scene_arg}{line_number})\n"
                )
                line_5 = "\n"
                bottom_block = (
                    sound_diff_line + line_1 + line_2 + line_3 + commands_block + line_5
                )

            else:
                line_1 = base_tab + line + "\n"
                line_2 = base_tab + indent + "with sound(step, offset_step):\n"
                line_3 = (
                    base_tab
                    + indent
                    + tab
                    + f"code_block.highlight({scene_arg}{line_number})\n"
                )
                line_4 = "\n"
                bottom_block = line_1 + line_2 + line_3 + line_4

            add_block_list.append(bottom_block)

            # --------- cycle finish -------------

        add_block = "".join(add_block_list)
        res += add_block
        line_number += 1

        pyperclip.copy(res)

    def generate_with_no_sound(
        self,
        scene_param: bool = False,
    ) -> None:
        """Generate animation scaffolding from algorithm code.

        This static method converts algorithm code into a template for Manim
        animation construction. It parses the code structure and generates
        corresponding highlight calls and wait statements.

        The generated template is copied to the system clipboard for easy
        insertion into Manim scene construct() method.

        Important:
            The CodeBlock instance in the scene must be named `code_block`
            for the generated template to work correctly.

        Args:
            code: Multiline string containing the algorithm code to animate.
            self_param: If True, includes `self,` as first argument in highlight()
                        calls (for CodeBlockLense). Default False (for CodeBlock).
        """

        if scene_param:
            scene_arg = "self, "
        else:
            scene_arg = ""

        code_lines = self._code.strip().split("\n")
        res = ""
        tab = "    "
        base_tab = tab * 2
        i = 0

        for line in code_lines:
            line_lstrip = line.lstrip()
            indent = line[: len(line) - len(line_lstrip)]

            if not line_lstrip or line_lstrip.startswith("#"):
                i += 1
                continue
            elif (  # pre-highlight line - same indent
                line_lstrip.startswith("if ")
                or line_lstrip.startswith("break")
                or line_lstrip.startswith("continue")
            ):
                line_1 = base_tab + indent + f"code_block.highlight({scene_arg}{i})\n"
                line_2 = base_tab + indent + "self.wait(pause)\n"
                line_3 = base_tab + line + "\n"
                line_4 = base_tab + indent + tab + "#\n"
                add_block = line_1 + line_2 + line_3 + line_4
            elif (  # after-highlight line - plus indent
                line_lstrip.startswith("for ")
                or line_lstrip.startswith("else")
                or line_lstrip.startswith("elif ")
                or line_lstrip.startswith("while ")
            ):
                line_1 = base_tab + line + "\n"
                line_2 = (
                    base_tab + indent + tab + f"code_block.highlight({scene_arg}{i})\n"
                )
                line_3 = base_tab + indent + tab + "self.wait(pause)\n"
                line_4 = base_tab + indent + tab + "#\n"
                add_block = line_1 + line_2 + line_3 + line_4
            elif line_lstrip.startswith("return "):  # return lines only - same indent
                line_1 = base_tab + indent + "# " + line_lstrip + "\n"
                line_2 = base_tab + indent + f"code_block.highlight({scene_arg}{i})\n"
                line_3 = "\n"
                add_block = line_1 + line_2 + line_3
            else:
                line_1 = base_tab + line + "\n"
                line_2 = base_tab + indent + f"code_block.highlight({scene_arg}{i})\n"
                line_3 = base_tab + indent + "self.wait(pause)\n"
                line_4 = "\n"
                add_block = line_1 + line_2 + line_3 + line_4

            res += add_block
            i += 1

        pyperclip.copy(res)
