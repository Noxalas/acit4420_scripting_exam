import time
import sys

BLACK = "\x1b[30m"
WHITE = "\x1b[37m"

BLACK_BG = "\x1b[40m"
WHITE_BG = "\x1b[47m"

RESET = "\x1b[0m"

# TODO: Usse trick from minecraftty (minecraft in terminal) to draw 1x2 tiles for every character (colored background and character).
BLOCK = "▀"


class Grid:
    def __init__(self, grid=[], grid_size: int = 10) -> None:
        self.grid_size = grid_size
        self.grid = [0] * (grid_size * grid_size)

        self.set_cell(1, 0, 1)
        self.set_cell(2, 1, 1)
        self.set_cell(0, 2, 1)
        self.set_cell(1, 2, 1)
        self.set_cell(2, 2, 1)

    def set_cell(self, x: int, y: int, state: int) -> None:
        self.grid[y * self.grid_size + x] = state

    def get_cell(self, x: int, y: int) -> int:
        x %= self.grid_size
        y %= self.grid_size
        return self.grid[y * self.grid_size + x]

    def count_neighbors(self, x: int, y: int) -> int:
        count = 0
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                if self.get_cell(x + dx, y + dy):
                    count += 1
        return count

    def evolve(self, ruleset):
        new_grid = self.grid.copy()
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                idx = y * self.grid_size + x
                is_alive = self.grid[idx] == 1
                neighbor_count = self.count_neighbors(x, y)
                action = ruleset.evaluate(is_alive, neighbor_count)

                if action == "die":
                    new_grid[idx] = 0
                elif action in ("survive", "unchanged") and is_alive:
                    new_grid[idx] = 1
                elif action == "born":
                    new_grid[idx] = 1
        self.grid = new_grid

    def to_string(self) -> str:
        lines = []
        size = self.grid_size

        for y in range(0, size, 2):
            line = []
            for x in range(size):
                top = self.get_cell(x, y)
                bottom = self.get_cell(x, y + 1) if y + 1 < size else 0
                if y + 1 < size:
                    bottom = self.grid[(y + 1) * size + x]

                fg = WHITE if top else BLACK
                bg = WHITE_BG if bottom else BLACK_BG

                line.append(f"{fg}{bg}{BLOCK}{RESET}")
            lines.append("".join(line))
        return "\n".join(lines)

    def refresh(self) -> None:
        output = self.to_string()
        lines = output.count("\n") + 1

        sys.stdout.write(f"\x1b[{lines}A")
        sys.stdout.write(output + "\n")
        sys.stdout.flush()

    def __str__(self) -> str:
        return self.to_string()

