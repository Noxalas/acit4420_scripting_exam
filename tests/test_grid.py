import pytest
from conway.grid import Grid
from conway.rules import RuleSet

conway_rule = RuleSet("B3/S23")


def test_set_and_get_cell():
    grid = Grid(grid_size=5)
    grid.set_cell(3, 3, 1)
    assert grid.get_cell(3, 3) == 1
    grid.set_cell(3, 3, 0)
    assert grid.get_cell(3, 3) == 0


def test_count_neighbors_no_wrap():
    grid = Grid(grid_size=3, grid_wrap=False)
    grid.set_cell(0, 0, 1)
    grid.set_cell(0, 1, 1)
    grid.set_cell(1, 0, 1)
    assert grid.count_neighbors(1, 1) == 3
    assert grid.count_neighbors(2, 2) == 0


def test_count_neighbors_with_wrap():
    grid = Grid(grid_size=3, grid_wrap=True)
    grid.set_cell(0, 0, 1)
    assert grid.count_neighbors(2, 2) == 1


def test_evolve_blinker():
    grid = Grid(grid_size=4)
    grid.set_cell(0, 1, 1)
    grid.set_cell(1, 1, 1)
    grid.set_cell(2, 1, 1)

    grid.evolve(conway_rule)
    expected = [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
    assert grid.grid == expected


def test_get_cell_out_of_bounds_no_wrap():
    grid = Grid(grid_size=3, grid_wrap=False)
    assert grid.get_cell(-1, 0) == 0
    assert grid.get_cell(0, -1) == 0
    assert grid.get_cell(3, 0) == 0
    assert grid.get_cell(0, 3) == 0
