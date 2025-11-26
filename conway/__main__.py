import argparse
import time

from rules import RuleSet
from grid import Grid
from renderer import refresh


def main(args):
    # Clear screen + hide cursor
    print("\x1b[2J\x1b[?25l", end="")

    rules = RuleSet(args.ruleset)

    grid = Grid(grid_size=50)

    try:
        while True:
            grid.evolve(rules)
            refresh(grid)
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\x1b[?25h")
        print("Ended simulation.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Tool to simulate Life-like cellular automatons"
    )
    parser.add_argument(
        "--ruleset",
        required=False,
        default="B3/S23",
        help="Input Life-like ruleset (e.g. B3/S23)",
    )

    args = parser.parse_args()
    main(args)
