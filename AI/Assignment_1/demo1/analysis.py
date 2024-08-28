# Alp Önder Yener -- 31183

import heapq  # for priority queue
import tracemalloc  # for memory consumption
import time  # for time consumption
import sys

######################################################################################################################

# Levels defined
EASY1 = "000000000000\n0XXXXXXXXXX0\n00000XXXXXX0\nXXXXXXXXXXX0\n0XXXXXXXXXX0\n0XXXXXXXXXX0\n0XXXXXXXXXX0\n0XXXXXXXXXX0\n0XXXXXXXXXX0\n0XXXXXXXXXX0\n0XXXXXXXXXX0\nS00000000000"
EASY2 = "000000000000\n0S0000XXXXX0\n00000XXXXXX0\nXXXXXXXXXXX0\n0XXXXXXXXXX0\n0XXXXXXXXXX0\n0XXXXXXXXXX0\n0XXXXXXXXXX0\n0XXXXXXXXXX0\n0XXXXXXXXXX0\n0XXXXXXXXXX0\n000000000000"
EASY3 = "X00000000000\n000000XXXXX0\n000000XXXXX0\nXXXXXXXXXXX0\n0XXXS00000X0\n0XXXXXXXX0X0\n0XXXXXXXX0X0\n0XXXXXXXX000\n0XXXXXXXXXX0\n0XXXXXXXXXX0\n0XXXXXXXXXX0\n000000000000"
EASY4 = "000000000000\n0XXXXXXXXXX0\n000000XXXXX0\nXXXXXXXXXXX0\n0XXXS00000X0\n0XXXXXXXX0X0\n0XXXXXXXX0X0\n0XXXXXXXX000\n0XXXXXXXXXX0\n0XXXXXXXXXX0\n00000000XXX0\n000000X00000"
EASY5 = "000000000000\n0XXXXXXXXXX0\n0000000000X0\nXXXXXXXXX0X0\n0XS0000000X0\n0XXXXXXXX0X0\n0XXXXXXXX0X0\n0XXXXXXXX000\n0XXXXXXXXXX0\n0XXXXXXXXXX0\n00000000XXX0\n00XXXXX00000"

EASY_LEVELS = [EASY1, EASY2, EASY3, EASY4, EASY5]

MEDIUM1 = "X00000000000\n000000XXXXX0\n000000XXXXX0\nXXXXXXXXXXX0\n0XXXS00000X0\n0XXXXXXXX0X0\n0XXXXXXXX0X0\n0XXXXXXXX000\n0XXXXXXXXXX0\n0XXXXXXXXXX0\n000000000000\n0X0000000000"
MEDIUM2 = "X00000X00000\n000000XXXXX0\n000000XXXXX0\n0XXXXXXXXXX0\n0XXXS00000X0\n0XXXXXXXX0X0\n0XXXXXXXX0X0\n0XXXXXXXX000\n0XXXXXXXXXX0\n0XXXXXXXXXX0\n000000000000\n0X0000000000"
MEDIUM3 = "XXXXXXX00000\n000000XXXXX0\n000000XXXXX0\n0XXXXXXXXXX0\n0XXXS00000X0\n0XXXXXXXX0X0\n0XXXXXXXX0X0\n0XXXXXXXX0X0\n000000000000\n0XXXXXXXXXX0\n000000000000\n0X0000000000"
MEDIUM3 = "XXXXXXX00000\n000000XXXXX0\n000000XXXXX0\n0XXXXXXXXXX0\n0XXXS00000X0\n0XXXXXXXX0X0\n0XXXXXXXX0X0\n0XXXXXXXX0X0\n000000000000\n0XXXXXXXXXX0\n000000000000\n0X0000000000"
MEDIUM4 = "0XXX00000000\n0XXXXXXXXXX0\n0XXXXXXXXXX0\n0XXXXXXXXXX0\n0X00S00000X0\n0XXX0XXXX0X0\n0XXX0XXXX0X0\n0XXXXXXXX0X0\n000000000000\n0XXXXXXXXXX0\n000000000000\n0X0000000000"
MEDIUM5 = "0X0000000000\n0XXXXXXXXXX0\n0XXXXXXXXXX0\n0XXXXXXXXXX0\n0X00S00000X0\n0XXX0XXXX0X0\n0XXX0XXXX0X0\n0XXX0XXXX0X0\n000000000000\n0XXXXXXXXXX0\n000000000000\n0XXX00000000"

MEDIUM_LEVELS = [MEDIUM1, MEDIUM2, MEDIUM3, MEDIUM4, MEDIUM5]

HARD1 = "X00000X00000\n000000XXXXX0\n000000XXXXX0\n0XXXXXXXXXX0\n0XXXS00000X0\n0XXXXXXXX0X0\n0XXXXXXXX0X0\n0XXXXXXXX0X0\n000000000000\n0XXXXXXXXXX0\n000000000000\n0X0000000000"
HARD2 = "XXX000X00000\n000000XXXXX0\n00000XXXXXX0\n0XXX0XXXXXX0\n0XXXS00000X0\n0XXX0XXXX0X0\n0XXX000000X0\n0XXXXXXXX0X0\n000000000000\n0XXXXXXXXXX0\n000000000000\n0X0000000000"
HARD3 = "XXX000X00000\n000000XXXXX0\n00000XXXXXX0\n0XXX0XXXXXX0\n0XXXS00000X0\n0XXX0XXXX0X0\n0XXX000000X0\n0XXXXXXXX0X0\n000000000000\n0XXXXXXXXXX0\n0X0000000000\n0X000000X000"
HARD4 = "XXX000X00000\n000000XXXXX0\n00000XXXXXX0\n0XXX0XXXXXX0\n0XXXS00000X0\n0XXX0XXXX0X0\n0XXX000000X0\n0XXXXXXXX0X0\n0X0X00000000\n0X0XXXXXXXX0\n0X0000000000\n0X000000X000"
HARD5 = "XXX000X00000\n000000XXXXX0\n00000XXXXXX0\n0XXX0XXXXXX0\n0X00S00000X0\n0XXX0XXXX0X0\n0XXX000000X0\n0XXXXXXXX0X0\n0X0X00000000\n0X0XXXXXXXX0\n0X0000000000\n0X000000X000"

HARD_LEVELS = [HARD1, HARD2, HARD3, HARD4, HARD5]

######################################################################################################################

# Helper Functions

# given the board, finds available directions for the agent to move towards
def find_available_directions(node):
    board = node.state
    column_number = board.find("\n")  # how many columns there are
    agent_idx = board.strip().find("S")  # where the agent is, starting from 0

    # check if right is OK
    if agent_idx + 1 < len(board):
        if board[agent_idx + 1] == "0" or board[agent_idx + 1] == "C":
            right = True
        else:
            right = False
    else:
        right = False

    # check if left is OK
    if agent_idx - 1 >= 0:
        if board[agent_idx - 1] == "0" or board[agent_idx - 1] == "C":
            left = True
        else:
            left = False
    else:
        left = False

    # check if up is OK
    if agent_idx - column_number - 1 >= 0:
        if (
            board[agent_idx - column_number - 1] == "0"
            or board[agent_idx - column_number - 1] == "C"
        ):
            up = True
        else:
            up = False
    else:
        up = False

    # check if down is OK
    if agent_idx + column_number + 1 < len(board):
        if (
            board[agent_idx + column_number + 1] == "0"
            or board[agent_idx + column_number + 1] == "C"
        ):
            down = True
        else:
            down = False
    else:
        down = False

    return up, down, left, right  # , column_number, agent_idx

# moves the agent on the board, given the direction
## returns the cost and the new state
def move(direction, node):
    board = node.state
    agent_idx = board.strip().find("S")
    column_number = board.find("\n")

    cells_traveled = 0
    if direction == "up":
        stop_idx = agent_idx - column_number - 1
        while stop_idx >= 0 and (board[stop_idx] == "0" or board[stop_idx] == "C"):
            board = (
                board[:stop_idx] + "S" + board[stop_idx + 1 :]
            )  # symbolizing that the cell is colored
            previous_cell_idx = stop_idx + column_number + 1
            board = board[:previous_cell_idx] + "C" + board[previous_cell_idx + 1 :]
            stop_idx = stop_idx - column_number - 1
            cells_traveled += 1

    if direction == "down":
        stop_idx = agent_idx + column_number + 1
        while stop_idx < len(board) and (
            board[stop_idx] == "0" or board[stop_idx] == "C"
        ):
            board = (
                board[:stop_idx] + "S" + board[stop_idx + 1 :]
            )  # symbolizing that the cell is colored
            previous_cell_idx = stop_idx - column_number - 1
            board = board[:previous_cell_idx] + "C" + board[previous_cell_idx + 1 :]
            stop_idx = stop_idx + column_number + 1
            cells_traveled += 1

    if direction == "left":
        stop_idx = agent_idx - 1
        while stop_idx >= 0 and (board[stop_idx] == "0" or board[stop_idx] == "C"):
            board = (
                board[:stop_idx] + "S" + board[stop_idx + 1 :]
            )  # symbolizing that the cell is colored
            previous_cell_idx = stop_idx + 1
            board = board[:previous_cell_idx] + "C" + board[previous_cell_idx + 1 :]
            stop_idx = stop_idx - 1
            cells_traveled += 1

    if direction == "right":
        stop_idx = agent_idx + 1
        while stop_idx < len(board) and (
            board[stop_idx] == "0" or board[stop_idx] == "C"
        ):
            board = (
                board[:stop_idx] + "S" + board[stop_idx + 1 :]
            )  # symbolizing that the cell is colored
            previous_cell_idx = stop_idx - 1
            board = board[:previous_cell_idx] + "C" + board[previous_cell_idx + 1 :]
            stop_idx = stop_idx + 1
            cells_traveled += 1

    return board, cells_traveled

######################################################################################################################

# Functions used on A* and the Node class

# each state will be represented as a Node
class Node:
    def __init__(self, state, parent=None, g=0, direction=None):
        self.parent = parent
        self.state = state
        self.g = g
        self.direction = direction

# simple goal test
def goal_test(node):
    if node.state.count("0") == 0:
        return True
    return False

# returns a list of successor states, given the node
## also, calculates g(n') for each successor state
### each element is of type list, [n', g(n'), direction taken to get to n'] where n' is the new state
def succ(node):
    succ_states = []
    up, down, left, right = find_available_directions(node)
    directions = [up, down, left, right]
    direction_names = ["up", "down", "left", "right"]

    for idx in range(len(directions)):
        if directions[idx]:
            new_state, cost = move(direction_names[idx], node)

            new_state_g = node.g + cost # calculate g for new state

            succ_states.append([new_state, new_state_g, direction_names[idx]])

    return succ_states

# calculates h2
def calculate_h2(node):
    board = node.state
    return 3*(board.count("0"))

# calculates h1
def calculate_h1(node):
    up, down, left, right = find_available_directions(node)
    directions = [up, down, left, right]
    direction_names = ["up", "down", "left", "right"]

    max_cost = 0
    for idx in range(len(directions)):
        if directions[idx]:
            _, cost = move(direction_names[idx], node)
            if cost > max_cost:
                max_cost = cost

    return max_cost * node.state.count("0")

# check if the state is in frontier
def check_if_in_frontier(queue, s):
    for node in queue:
        if node[2].state == s:
            return node[2]
    return False

# check if the state is in closed
def check_if_in_closed(queue, s):
    for node in queue:
        if node.state == s:
            return node
    return False


######################################################################################################################

# A* searches, using h1 and h2

def A_star_search_h1(start):
    closed = []
    frontier = []
    n = Node(state=start)  # no parent, g=0, state is start state
    heapq.heappush(frontier, (0, id(n), n))

    expanded_nodes = 0

    while len(frontier) != 0:

        _, _, n = heapq.heappop(frontier)  # get n such that f(n) is minimum
        expanded_nodes+=1

        goal_achieved = goal_test(n)
        if goal_achieved:
            print("Total distance travelled:", n.g)
            print(
                "Total number of expanded nodes:", expanded_nodes
            )  # +1 is to get the goal node

            print("\n")
            print(n.state)
            print("\n")
            print("Went ", n.direction)
            parent_node = n.parent
            while parent_node != None:
                print(parent_node.state)
                if parent_node.parent != None:
                    print("\n")
                    print("Went ", parent_node.direction)
                parent_node = parent_node.parent
            print("Above is the route taken:")
            return True

        successors = succ(n)  # [successor state, g] for each element

        for element in successors:
            s = element[0]
            g_s = element[1]
            direction = element[2]

            new_node = Node(s, parent=n, g=g_s, direction=direction)  # create new node n'
            new_node_h = calculate_h1(new_node)
            new_node_f = new_node_h + new_node.g

            node_in_frontier = check_if_in_frontier(frontier, s)
            node_in_closed = check_if_in_closed(closed, s)

            if node_in_frontier == False and node_in_closed == False:
                heapq.heappush(frontier, (new_node_f, id(new_node), new_node))

            elif node_in_frontier:
                frontier_node_f = calculate_h1(node_in_frontier) + node_in_frontier.g
                if new_node_f < frontier_node_f:
                    idx = frontier.index(
                        (frontier_node_f, id(node_in_frontier), node_in_frontier)
                    )  # delete the node from the list
                    del frontier[idx]
                    heapq.heappush(frontier, (new_node_f, id(new_node), new_node))

            elif node_in_closed:
                closed_node_f = calculate_h1(node_in_closed) + node_in_closed.g
                if new_node_f < closed_node_f:
                    heapq.heappush(frontier, (new_node_f, id(new_node), new_node))

        closed.append(n)

def A_star_search_h2(start):

    closed = []
    frontier = []
    n = Node(state=start)  # no parent, g=0, state is start state
    heapq.heappush(frontier, (0, id(n), n))

    expanded_nodes = 0

    while len(frontier) != 0:

        _, _, n = heapq.heappop(frontier)  # get n such that f(n) is minimum
        expanded_nodes+=1
        
        goal_achieved = goal_test(n)
        if goal_achieved:
            print("Total distance travelled:", n.g)
            print(
                "Total number of expanded nodes:", expanded_nodes
            )  # +1 is to get the goal node

            print("\n")
            print(n.state)
            print("\n")
            print("Went ", n.direction)
            parent_node = n.parent
            while parent_node != None:
                print(parent_node.state)
                if parent_node.parent != None:
                    print("\n")
                    print("Went ", parent_node.direction)
                parent_node = parent_node.parent

            print("Above is the route taken:")
            return True

        successors = succ(n)  # [successor state, g] for each element

        for element in successors:
            s = element[0]
            g_s = element[1]
            direction = element[2]

            new_node = Node(s, parent=n, g=g_s, direction=direction)  # create new node n'
            new_node_h = calculate_h2(new_node)
            new_node_f = new_node_h + new_node.g

            node_in_frontier = check_if_in_frontier(frontier, s)

            if node_in_frontier == False:
                heapq.heappush(frontier, (new_node_f, id(new_node), new_node))

            else:
                frontier_node_f = calculate_h2(node_in_frontier) + node_in_frontier.g
                if new_node_f < frontier_node_f:
                    idx = frontier.index(
                        (frontier_node_f, id(node_in_frontier), node_in_frontier)
                    )  # delete the node from the list
                    del frontier[idx]
                    heapq.heappush(frontier, (new_node_f, id(new_node), new_node))

        closed.append(n)

######################################################################################################################

level = EASY4


demo3 = "S00\n000\n000"
demo4 = "0000\n0X00\n000X\n0S00"

A_star_search_h2(demo4)


