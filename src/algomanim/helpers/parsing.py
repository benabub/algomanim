def indent_cutter(lines: list[str]) -> list[str]:
    """Remove base indentation from code lines recursively.

    Recursively strips 4 spaces from the beginning of each line until
    the first line no longer starts with 4 spaces.

    Args:
        lines: List of code lines with consistent indentation.

    Returns:
        List of code lines with base indentation removed.
    """
    if lines[0].startswith("    "):
        lines = [line[4:] for line in lines]
        return indent_cutter(lines)
    return lines


def code_to_lines(code: str) -> list[str]:
    """Convert a code string into a list of properly indented lines.

    Strips surrounding whitespace, splits into lines, validates that the
    first line is not empty, and removes common base indentation.

    Args:
        code: Multiline string containing Python code.

    Returns:
        List of code lines with consistent base indentation removed.

    Raises:
        ValueError: If the first line is empty after stripping.
    """
    lines = code.strip().split("\n")

    if not lines[0].strip():
        raise ValueError("code string problem: first line cannot be empty")

    return indent_cutter(lines)
