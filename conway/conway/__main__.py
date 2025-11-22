import time
from rules import RuleSet
from grid import Grid

def main():
    print("\x1b[2J\x1b[?25l")

    rules = RuleSet("./rules")
    print(rules)

    grid = Grid(grid_size=20)
    print(grid)
    try:
        while True:
            time.sleep(0.5)
            grid.evolve(rules)
            grid.refresh()
    except KeyboardInterrupt:
        print("\x1b[?25h")
        print("Ended simulation.")


if __name__ == "__main__":
    main()
