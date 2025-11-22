import time
from conway.rules import RuleSet
from conway.grid import Grid


if __name__ == "__main__":
    rules = RuleSet("./conway/rules")
    print(rules)

    test_cases = [
            (True, 1),
            (True, 3),
            (False, 3),
            (True, 5),
            (False, 1)
            ]

    for alive, neighbors in test_cases:
        result = rules.evaluate(alive, neighbors)
        print(f"Cell({alive=}, {neighbors=}) -> {result}")


    #size = 10
    #grid = Grid(grid_size=size)
    #grid.set_cell(4, 4, 1)
    #grid.set_cell(5, 4, 1)
    #grid.set_cell(6, 4, 1)

    #print("\x1b[2J\x1b[?25l")

    #try:
    #    while True:
    #        print(grid)
    #        time.sleep(0.5)
    #        grid.evolve()
    #        grid.refresh()
    #except KeyboardInterrupt:
    #    print("\x1b[?25h")
    #    print("Ended simulation.")
