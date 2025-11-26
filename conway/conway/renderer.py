import sys

BLACK = "\x1b[30m"
WHITE = "\x1b[37m"
BLACK_BG = "\x1b[40m"
WHITE_BG = "\x1b[47m"
RESET = "\x1b[0m"

BLOCK = "▀"


def grid_to_string(grid) -> str:
    """
    Convert a Grid object into a colored Unicode string suitable for terminal display.

    The function renders the grid two rows at a time using the Unicode "upper half block"
    character (▀). Each character encodes:
        - the top cell as the foreground color
        - the bottom cell as the background color

    Alive cells are rendered in white; dead cells are rendered in black.

    Parameters
    ----------
    grid: Grid
        A Grid instance providing `grid_size` and a `get_cell(x, y)` method.

    Returns
    -------
    str
        A multi-line string containing ANSI escape sequences for color and the
        block characters representing the grid. Intended for direct terminal output.
    """

    size = grid.grid_size
    lines = []

    for y in range(0, size, 2):
        line = []
        for x in range(size):
            top = grid.get_cell(x, y)
            bottom = grid.get_cell(x, y + 1) if y + 1 < size else 0

            fg = WHITE if top else BLACK
            bg = WHITE_BG if bottom else BLACK_BG

            line.append(f"{fg}{bg}{BLOCK}{RESET}")

        lines.append("".join(line))

    return "\n".join(lines)


def refresh(grid) -> None:
    """
    Update the terminal display with the current grid state.

    This function clears the previously printed grid by moving the cursor upward
    by the number of lines printed, then prints the current grid rendering.
    It relies on ANSI escape codes.

    Parameters
    ----------
    grid: Grid
        The Grid object to display. Rendering is handled by `grid_to_string`.

    Returns
    -------
    None
        The updated grid is written directly to stdout.
    """

    output = grid_to_string(grid)
    lines = output.count("\n") + 1

    sys.stdout.write(f"\x1b[{lines}A")
    sys.stdout.write(output + "\n")
    sys.stdout.flush()
