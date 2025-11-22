import pytest

def test_evolve_grid():
    grid = [0, 1, 0, 0, 1, 0, 0, 1, 0]
    new_grid = evolve_grid(grid)
    assert new_grid[4] == 1 # blinker persist

