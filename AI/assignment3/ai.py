from copy import deepcopy

from engine import Grid

MAX = 1000
MIN = -1000

# Global variable
# I hate doing this
best_action: tuple[str, str]


def game_search(grid: Grid, alpha: int, beta: int, isMaximizingPlayer: bool) -> int:
    global best_action
    possible_actions = grid.get_possible_actions()
    # If there are no possible actions left (end of the game simulation)
    if not possible_actions:
        return grid.score

    actions: dict[int, tuple[str, str]] = {}

    if isMaximizingPlayer:
        best_value = MIN
        for action in possible_actions:
            # Taking action
            new_grid = deepcopy(grid)
            new_grid.take_action(action[0], action[1], True)
            # Recursion
            value = game_search(new_grid, alpha, beta, False)
            # To get the best action taken in the tree
            actions[value] = action
            # Get the minimum of all scores that can be obtained from this action
            best_value = max(best_value, value)
            # Pruning
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break
        best_action = actions[best_value]
        return best_value
    else:
        best_value = MAX
        for action in possible_actions:
            # Taking action
            new_grid = deepcopy(grid)
            new_grid.take_action(action[0], action[1], False)
            # Recursion
            value = game_search(new_grid, alpha, beta, True)
            # To get the best action taken in the tree
            actions[value] = action
            # Get the minimum of all scores that can be obtained from this action
            best_value = min(best_value, value)
            # Pruning
            beta = min(beta, best_value)
            if beta <= alpha:
                break
        best_action = actions[best_value]
        return best_value


def get_ai_action(grid: Grid) -> tuple[str, str]:
    global best_action
    best_action = None
    # Score is taken as 0 as the goal is to minimize the player's score
    # from the current state onward. Current score is unnecessary
    game_search(grid, MIN, MAX, False)
    # TODO This function has a side effect of setting the global variable "best_action"
    # Not a good coding practice, this should later be changed
    return best_action
