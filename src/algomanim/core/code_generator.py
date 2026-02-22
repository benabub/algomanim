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
    base_indent = tab * 2


class CodeGenerator:
    """Generates Manim animation templates from algorithm code.

    This class parses algorithm code and produces structured templates for
    Manim animations, including proper indentation, highlight calls, and
    sound effect blocks. It supports two output formats: with sound effects
    (for audio-enhanced animations) and without sound (for silent animations).

    The generator recognizes special inline commands in the format "=x" where
    x is one command character (a, u, U, p, s) that determine which
    animation blocks to generate for that line.

    Attributes:
        CONFIG: Default configuration instance with template strings.
    """

    CONFIG = Config()

    def __init__(
        self,
        code: str,
        commands_dict=CONFIG.commands_dict,
        suffix_dict=CONFIG.suffix_dict,
        tab=CONFIG.tab,
        base_indent=CONFIG.base_indent,
    ) -> None:
        """Initialize CodeGenerator with source code and optional template overrides.

        Args:
            code: Multiline string containing the algorithm code to animate.
            commands_dict: Optional custom command templates. If not provided,
                uses defaults from CONFIG.
            suffix_dict: Optional custom suffix mappings. If not provided,
                uses defaults from CONFIG.
            tab: Indentation string (typically four spaces). If not provided,
                uses default from CONFIG.
            base_indent: Base indentation level (typically eight spaces).
                If not provided, uses default from CONFIG.
        """
        self._code = code
        self._commands_dict = commands_dict
        self._suffix_dict = suffix_dict
        self._tab = tab
        self._base_indent = base_indent

    def _get_command_pair(
        self,
        command: str,
        indent: str,
        is_last: bool,
        pass_line: bool,
    ) -> str:
        """Generate a command block for a specific animation action.

        Args:
            command: Command character.
            indent: Indentation string for the block.
            is_last: Whether this is the last command in a sequence.
            pass_line: Whether to include a "..." placeholder line.

        Returns:
            Formatted string containing the command block.
        """
        curr_command_dict = self._commands_dict[command]
        with_line = indent + curr_command_dict["with_line"] + self._suffix_dict[is_last]
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
        is_last: bool,
    ) -> str:
        """Generate a code block for highlighting a line in CodeBlock.

        Args:
            indent: Indentation string for the block.
            sound: Sound type ('step', 'cycle', etc.).
            offset: Offset parameter name for the sound.
            scene_arg: Scene argument string (empty or "self, ").
            line_number: Line number to highlight.
            is_last: Whether this is the last highlight in a sequence.

        Returns:
            Formatted string containing the highlight block.
        """
        with_line = indent + f"with sound({sound}, {offset}{self._suffix_dict[is_last]}"
        code_line = (
            indent + self._tab + f"code_block.highlight({scene_arg}{line_number})\n"
        )
        return with_line + code_line

    def _get_custom_line(
        self,
        clean_line: str,
        indent,
    ) -> str:
        """Generate a simple indented line of code.

        Args:
            clean_line: The code line content (without indentation).
            indent: Indentation string to prepend.

        Returns:
            Indented line with newline character.
        """
        return indent + clean_line + "\n"

    def generate_with_no_sound(
        self,
        scene_param: bool = False,
    ) -> None:
        """Generate a silent animation template without sound effects.

        Parses the algorithm code and produces a template with code_block.highlight()
        calls and self.wait() statements. The output is copied to the clipboard.

        Important:
            The CodeBlock instance in the scene must be named `code_block`.

        Args:
            scene_param: If True, prepends 'self, ' to highlight() arguments
                for CodeBlockLense compatibility. Defaults to False.
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

    def generate(
        self,
        scene_param: bool = False,
    ) -> None:
        """Generate an animation template with sound effects blocks.

        Parses the algorithm code and produces a structured template with
        'with sound' context managers, code_block.highlight() calls, and
        command blocks for various animation actions. The output is copied
        to the clipboard.

        Important:
            1. The CodeBlock instance in the scene must be named `code_block`.
            2. The scene must have an alias `sound = self.sound_block`.
            3. Global variables for sounds must be available:
               - step (highlight line in CodeBlock)
               - cycle (highlight cycle-start line in CodeBlock)
               - slide (pointers/highlights move)
               - update (mobjects update)
               - appear (animation structures appear)
               - point (pointers appear)
               - rtn (return mobject appear)

        Args:
            scene_param: If True, prepends 'self, ' to highlight() arguments
                for CodeBlockLense compatibility. Defaults to False.

        Raises:
            ValueError: If an unknown command (not a, u, U, p, s) is found in
                a line ending with '=.' pattern.
        """

        tab = self._tab

        if scene_param:
            scene_arg = "self, "
        else:
            scene_arg = ""

        code_lines = self._code.strip().split("\n")
        line_number = 0

        add_block_list = []

        # --------- main iterating -------------

        for line in code_lines:
            line_lstrip = line.lstrip()
            indent = line[: len(line) - len(line_lstrip)]
            edge_indent = self._base_indent + indent
            line = line.strip()

            # --------- line analyse -------------

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

            if (  # pre-highlight line - same indent
                line_lstrip.startswith("if ")
                or line.startswith("for")
                or line.startswith("while")
                or line.startswith("return")
                or line.startswith("else")
                or line.startswith("elif")
            ):
                statement_line = True
            else:
                statement_line = False

            # --------- head block -------------

            # sound_diff line
            if inline_commands and "u" in commands:
                operands = line.split("=", 1)
                val1 = operands[0].strip()
                val2 = operands[1].strip()
                add_block_list.append(
                    edge_indent
                    + f"curr_sound, curr_offset = sound_diff({val1}, {val2})\n"
                )

            if statement_line:
                if (  # pre-highlight line - edge_indent
                    line.startswith("if ")
                ):
                    highlight_pair = self._get_highlight_pair(
                        edge_indent,
                        "cycle",
                        "offset_cycle",
                        scene_arg,
                        line_number,
                        not inline_commands,
                    )
                    add_block_list.append(highlight_pair)

                    add_block_list.append(edge_indent + line + "\n")
                    add_block_list.append(edge_indent + tab + "#\n")

                elif (  # after-highlight line - edge_indent plus tab
                    line.startswith("else ") or line.startswith("elif ")
                ):
                    add_block_list.append(edge_indent + line + "\n")

                    highlight_pair = self._get_highlight_pair(
                        edge_indent + tab,
                        "step",
                        "offset_step",
                        scene_arg,
                        line_number,
                        not inline_commands,
                    )
                    add_block_list.append(highlight_pair)

                    if not inline_commands:
                        add_block_list.append("\n")

                elif (  # after-highlight line - edge_indent plus tab
                    line.startswith("for ") or line.startswith("while ")
                ):
                    add_block_list.append(edge_indent + line + "\n")

                    highlight_pair = self._get_highlight_pair(
                        edge_indent + tab,
                        "cycle",
                        "offset_cycle",
                        scene_arg,
                        line_number,
                        False,
                    )
                    add_block_list.append(highlight_pair)

                    add_block_list.append(
                        self._get_custom_line(
                            "if i == 0:",
                            edge_indent + tab,
                        )
                    )

                    appear_pair = self._get_command_pair(
                        command="a",
                        indent=edge_indent + tab * 2,
                        is_last=False,
                        pass_line=True,
                    )
                    add_block_list.append(appear_pair)

                    point_pair = self._get_command_pair(
                        command="p",
                        indent=edge_indent + tab * 2,
                        is_last=not inline_commands,
                        pass_line=True,
                    )
                    add_block_list.append(point_pair)

                    add_block_list.append(
                        self._get_custom_line(
                            "else:",
                            edge_indent + tab,
                        )
                    )

                    update_pair = self._get_command_pair(
                        command="U",
                        indent=edge_indent + tab * 2,
                        is_last=False,
                        pass_line=True,
                    )
                    add_block_list.append(update_pair)

                    slide_pair = self._get_command_pair(
                        command="s",
                        indent=edge_indent + tab * 2,
                        is_last=not inline_commands,
                        pass_line=True,
                    )
                    add_block_list.append(slide_pair)

                    if not inline_commands:
                        add_block_list.append("\n")

                elif line_lstrip.startswith(
                    "return "
                ):  # return lines only - edge_indent
                    add_block_list.append(edge_indent + "# " + line + "\n")

                    highlight_pair = self._get_highlight_pair(
                        edge_indent,
                        "step",
                        "offset_step",
                        scene_arg,
                        line_number,
                        False,
                    )
                    add_block_list.append(highlight_pair)

                    line_1 = edge_indent + "with sound(rtn, offset_return, 3):\n"
                    line_2 = edge_indent + tab + "...\n"
                    add_block_list.append(line_1 + line_2)

                    if not inline_commands:
                        add_block_list.append("\n")

            else:  # if not statement_line -> start of block
                add_block_list.append(edge_indent + line + "\n")
                add_block_list.append(
                    self._get_highlight_pair(
                        edge_indent,
                        "step",
                        "offset_step",
                        scene_arg,
                        line_number,
                        not inline_commands,
                    )
                )

            # --------- bottom block -------------

            if inline_commands:
                for j in range(len(commands)):
                    if j == len(commands) - 1:
                        is_last = True
                    else:
                        is_last = False

                    command_pair = self._get_command_pair(
                        command=commands[j],
                        indent=edge_indent,
                        is_last=is_last,
                        pass_line=True,
                    )
                    add_block_list.append(command_pair)

                add_block_list.append("\n")

            # add_block_list.append("\n")
            line_number += 1
            # --------- cycle finish -------------

        add_block = "".join(add_block_list)

        pyperclip.copy(add_block)
