class Grid:
    """
    Represents a two-dimensional cellular automaton grid for Conway's Game of Life
    and other Life-like rulesets. The grid is internally stored as a flat,
    one-dimensional list.

    Each cell is either alive (1) or dead (0). The grid supports both wrapping
    (toroidal) and non-wrapping boundary behavior. When wrapping is enabled,
    out-of-bounds neighbor lookups wrap around to the opposite edge. When disabled,
    out-of-bounds neighbors are treated as dead.

    Parameters
    ----------
    grid: list[int] | None
        An optional list representing the initial grid state. Must have
        length `grid_size * grid_size` if provided. If omitted, a zero-filled
        grid is created and initialized with a glider pattern.
    grid_wrap: bool, default=True
        Whether the grid should wrap around at the edges (toroidal topology).
        If False, neighbor lookups outside the grid return 0.
    grid_size: int, default=10
        Width and height of the square grid.
    """

    def __init__(self, grid=None, grid_wrap: bool = True, grid_size: int = 10) -> None:
        self.grid_size = grid_size

        self.grid = [0] * (grid_size * grid_size)

        self.grid_wrap = grid_wrap

        self.set_cell(1, 0, 1)
        self.set_cell(2, 1, 1)
        self.set_cell(0, 2, 1)
        self.set_cell(1, 2, 1)
        self.set_cell(2, 2, 1)

    def set_cell(self, x: int, y: int, state: int) -> None:
        """
        Set the state of a specific cell in the grid.

        Parameters
        ----------
        x: int
            The x-coordinate (column index) of the cell.
        y: int
            The y-coordinate (row index) of the cell.
        state: int
            The new state of the cell: 1 for alive, 0 for dead.
        """

        self.grid[y * self.grid_size + x] = state

    def get_cell(self, x: int, y: int) -> int:
        """
        Retrieve the state of a cell, applying wrapping or boundary checks as needed.

        If wrapping is enabled, coordinates are taken modulo the grid size.
        If wrapping is disabled, attempts to access out-of-bounds coordinates
        return 0.

        Parameters
        ----------
        x : int
            The x-coordinate of the cell to retrieve.
        y : int
            The y-coordinate of the cell to retrieve.

        Returns
        -------
        int
            The state of the cell at (x, y): 1 if alive, 0 if dead.
        """

        if self.grid_wrap:
            x %= self.grid_size
            y %= self.grid_size
        else:
            if x < 0 or x >= self.grid_size or y < 0 or y >= self.grid_size:
                return 0

        return self.grid[y * self.grid_size + x]

    def count_neighbors(self, x: int, y: int) -> int:
        """
        Count the number of alive neighbors surrounding the cell at (x, y).

        Uses Moore neighborhood (the eight surrounding cells). Neighbor lookups
        respect the grid's wrapping mode as implemented in `get_cell`.

        Parameters
        ----------
        x : int
            The x-coordinate of the target cell.
        y : int
            The y-coordinate of the target cell.

        Returns
        -------
        int
            The number of neighboring cells that are alive.
        """

        count = 0
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                if self.get_cell(x + dx, y + dy):
                    count += 1

        return count

    def evolve(self, ruleset):
        """
        Advance the grid by one generation using the provided ruleset.

        For each cell, the method determines:
            - whether the cell is currently alive,
            - how many neighbors it has, and
            - what action the ruleset prescribes (“die”, “survive”, or “born”).

        A new grid state is computed and then replaces the current one.

        Parameters
        ----------
        ruleset : RuleSet
            A `RuleSet` object that determines the state a cell evolves into based on
            the count of neighboring cells.
        """

        new_grid = self.grid.copy()
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                index = y * self.grid_size + x
                is_alive = self.grid[index] == 1
                neighbor_count = self.count_neighbors(x, y)
                action = ruleset.evaluate(is_alive, neighbor_count)

                if action == "die":
                    new_grid[index] = 0
                elif action in "survive" and is_alive:
                    new_grid[index] = 1
                elif action == "born":
                    new_grid[index] = 1

        self.grid = new_grid
