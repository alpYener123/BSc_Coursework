# Authors:
# Ilhan Yavuz Iskurt 31112
# Alp Önder Yener – 31183

import argparse

from ai import get_ai_action
from engine import Grid
from helper import center_two_strings

# Number of levels that can be loaded
LEVELS = 10


def parse_action(action: str, count: int) -> tuple[str, str]:
    """This function validates the inputs before the action is attempted

    Args:
        action (str): Action to be parsed and semi-validated
        count (int): Number of islands that are present in the grid

    Raises:
        ValueError: Action must have 2 parameters
        ValueError: Parameters must be one character long
        ValueError: First parameter must be a letter
        ValueError: Second parameter must be a letter
        ValueError: Letter must be between A and A + count
        ValueError: Number must be either 3 or 4

    Returns:
        tuple[str, str]: Parsed action
    """
    param = action.strip().split(" ")
    # General checks
    if len(param) != 2:
        raise ValueError("Action must have 2 parameters.")
    if len(param[0]) != 1 or len(param[1]) != 1:
        raise ValueError("Parameters must be one character long.")
    # First parameter check
    if not param[0].isalpha():
        raise ValueError("First parameter must be a letter.")
    char = chr(ord("A") + count - 1)
    if param[0] < "A" or param[0] > char:
        raise ValueError("Letter must be between A and " + char + ".")
    if param[1].isnumeric():
        if param[1] != "3" and param[1] != "4":
            raise ValueError("Number must be either 3 or 4.")
    # Second parameter check
    else:
        if not param[1].isalpha():
            raise ValueError("First parameter must be a letter.")
        if param[1] < "A" or param[1] > char:
            raise ValueError("Letter must be between A and " + char + ".")
        if param[0] == param[1]:
            raise ValueError("First and second letter cannot be the same.")
    return (param[0], param[1])


def main(level: int, start_second: bool):
    """Main function that controls the initialization and the logic of the game

    Args:
        level (int): The level of the grid that should be loaded for the game
        start_second (bool): AI starts the game if this is true
    """
    grid = Grid(level)
    print(
        "Two types of actions are allowed:\n"
        + "--> Building a bridge between two eligable islands. Enter the labels of the islands seperated by space. For example: A B\n"
        + "--> Entering a number to an empty island. Number must be either 3 or 4. For example: C 3\n\n"
        + "Starting board is: Grid "
        + str(level)
        + "\n"
        + (
            "\033[0;36mAI\033[0m starts"
            if start_second
            else "\033[0;32mYou\033[0m start"
        ),
        "first.\n",
    )

    width = max(50, (grid.width * 4) + 20)
    turn = start_second

    # Game Loop
    while grid.action_left():
        if turn:
            print(" \033[0;36mAI\033[0m's Turn ".center(width + 11, "-"))
        else:
            print(" \033[0;32mYour\033[0m Turn ".center(width + 11, "-"))
        grid.display_grid(width)
        print(
            "\n"
            + center_two_strings(
                "\033[0;32mYour\033[0m score: " + str(grid.score),
                " \033[0;36mAI\033[0m's score: " + str(-grid.score),
                width,
            )
        )
        if not turn:
            while True:
                try:
                    action = input("\nAction: ")
                    first, second = parse_action(action, grid.island_count)
                    grid.take_action(first, second, True)
                    break
                except ValueError as e:
                    print("Invalid action:", e)
        else:
            first, second = get_ai_action(grid)
            print("\nAction:", first, second)
            grid.take_action(first, second, False)
        turn = not turn

    # Game Over
    print(" Final Board ".center(width, "-"))
    grid.display_grid(width)
    print(
        "\n"
        + center_two_strings(
            "\033[0;32mYour\033[0m score: " + str(grid.score),
            " \033[0;36mAI\033[0m's score: " + str(-grid.score),
            width,
        )
        + "\n"
    )
    if grid.score > 0:
        print("\033[0;32mCongratulations, you have won!\033[0m")
    elif grid.score < 0:
        print("\033[0;36mAI have won, better luck next time!\033[0m")
    else:
        print("\033[1;33mNo winner this time, game has tied!\033[0m")


# Parse arguments, and initialize and start the game accordingly
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Play hashi against an AI.")

    parser.add_argument(
        "level",
        type=int,
        nargs="?",
        default=0,
        choices=range(LEVELS + 1),
        help=f"Level choices ranging from 0 to {LEVELS}",
    )

    parser.add_argument(
        "--start-second",
        "-s",
        action="store_true",
        help="AI starts first when this flag is set",
    )

    args = parser.parse_args()
    main(args.level, args.start_second)
