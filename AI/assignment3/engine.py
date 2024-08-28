from pathlib import Path

from helper import center_two_strings

# Folder including the grid configurations
MAP_DIR = Path("maps")

# Symbols for representing the bridges
SINGLE_H_BRIDGE = "-"
DOUBLE_H_BRIDGE = "="
SINGLE_V_BRIDGE = "|"
DOUBLE_V_BRIDGE = "X"


class Island:
    def __init__(self, x: int, y: int, bridges_required: int, label: str) -> None:
        self.x = x  # X coordinate on the grid
        self.y = y  # Y coordinate on the grid
        self.label = label
        self.bridges_required = bridges_required  # Number of bridges to connect
        self.bridges_connected = 0  # Number of bridges currently connected
        self.neighbors: list["Island" | None] = [
            None,  # UP
            None,  # DOWN
            None,  # LEFT
            None,  # RIGHT
        ]

    def is_numbered(self) -> bool:
        return self.bridges_required != 0

    def is_full(self) -> bool:
        return self.bridges_required == self.bridges_connected

    def __repr__(self) -> str:
        return f"Island({self.x}, {self.y}, {self.bridges_required})"

    def __eq__(self, island: "Island") -> bool:
        return self.x == island.x and self.y == island.y


class Grid:
    """This class represents the hashi game map and include methods to interact with the map

    Properties:
        map (list[list[str]]): Represents the map of the game
        mapping (dict[str, tuple[int, int]]): Mappings for labels of the islands
        islands (dict[tuple[int, int], Island]): Dictionary of islands corresponding to the coordinates
        width (int): Length of the rows of map
        island_count (int): Number of islands in the map
        score (int): Score of the player


    Raises:
        ValueError: Inconsistent grid row lengths. Each row should be of the same length.
        ValueError: Grid file can only consist of dots (.) and integers between 0 and 4.
        ValueError: Too many islands. At most 26 is allowed.
        ValueError: No two islands cannot be adjacent.
        ValueError: Empty grid configuration file.
        ValueError: Empty grid configuration. No islands exist.
        ValueError: There are no possible actions for this grid configuration start.

    """

    map: list[list[str]]
    mapping: dict[str, tuple[int, int]]
    islands: dict[tuple[int, int], Island]
    width: int
    island_count: int
    score: int

    # A very long constructor with constraint checks for grid setup
    def __init__(self, level: int) -> None:
        self.map = []
        self.mapping = {}
        self.islands = {}
        self.score = 0
        counter = 0
        map_path = MAP_DIR / f"map{level}.txt"
        neighbor_exists = False
        with map_path.open("r", encoding="utf-8") as file:
            for x, row in enumerate(file):
                self.map.append([])
                col = row.strip().split(" ")
                if x > 0 and len(self.map[x - 1]) != len(col):
                    raise ValueError(
                        "Inconsistent grid row lengths. Each row should be of the same length."
                    )
                h_neighbor = None
                if x == 0:
                    self.width = len(col)
                    v_neighbors = [None for _ in range(len(col))]
                for y, column in enumerate(col):
                    self.map[x].append(column)
                    if column != ".":
                        if not column.isnumeric() or int(column) < 0 or int(column) > 4:
                            raise ValueError(
                                f'Grid file can only consist of dots (.) and integers between 0 and 4: Invalid char "{column}".'
                            )
                        if counter > 25:
                            raise ValueError("Too many islands. At most 26 is allowed.")
                        char = chr(ord("A") + counter)
                        self.mapping[char] = (x, y)
                        new_island = Island(x, y, int(column), char)
                        if h_neighbor is not None:
                            if y - h_neighbor < 2:
                                raise ValueError("No two islands cannot be adjacent.")
                            neighbor_exists = True
                            new_island.neighbors[2] = self.islands[(x, h_neighbor)]
                            self.islands[(x, h_neighbor)].neighbors[3] = new_island
                        if v_neighbors[y] is not None:
                            if x - v_neighbors[y] < 2:
                                raise ValueError("No two islands cannot be adjacent.")
                            neighbor_exists = True
                            new_island.neighbors[0] = self.islands[(v_neighbors[y], y)]
                            self.islands[(v_neighbors[y], y)].neighbors[1] = new_island
                            pass
                        self.islands[(x, y)] = new_island
                        h_neighbor = y
                        v_neighbors[y] = x
                        counter += 1
                        continue

        if len(self.map) == 0:
            raise ValueError("Empty grid configuration file.")
        if counter == 0:
            raise ValueError("Empty grid configuration. No islands exist.")
        self.height = len(self.map)
        self.island_count = counter
        if not self.action_left() or not neighbor_exists:
            raise ValueError(
                "There are no possible actions for this grid configuration start"
            )

    def get_from_label(self, label: str) -> Island:
        coordinates = self.mapping[label]
        island = self.islands[(coordinates[0], coordinates[1])]
        return island

    # TODO Consider rewriting the class so that possible actions are stored from the start
    # and updated with each action (build_bridge and number_island) for optimization.
    def get_possible_actions(self) -> list[tuple[str, str]]:
        """Get the possible actions that can be taken in the current state of game (grid).
        Mind that some of these actions can be mutually exclusive meaning these actions cannot be
        trusted to taken one after another. This function should be called again to get new accurate
        possible actions.

        Returns:
            list[tuple[str, str]]: Possible actions that can be taken
        """
        possible_actions: list[tuple[str, str]] = []
        checked_islands: list[Island] = []  # To prevent multiple checking

        for island in self.islands.values():
            # Check if the island number is unset
            if island.bridges_required == 0:
                checked_islands.append(island)
                possible_actions.append((island.label, "3"))
                possible_actions.append((island.label, "4"))
                continue
            # Check if the island has reached its bridge limit
            if island.is_full():
                checked_islands.append(island)
                continue
            # Check if the neighbors are eligable for bridge building
            for i, neighbor in enumerate(island.neighbors):
                if not neighbor or neighbor in checked_islands or neighbor.is_full():
                    continue
                horizontal = True if i > 1 else False
                direction = -1 if i == 0 or i == 2 else 1
                check = True
                if horizontal:
                    y_coor = island.y + direction
                    if self.map[island.x][y_coor] == DOUBLE_H_BRIDGE:
                        continue
                    while neighbor.y != y_coor:
                        symbol = self.map[island.x][y_coor]
                        if symbol == SINGLE_V_BRIDGE or symbol == DOUBLE_V_BRIDGE:
                            check = False
                            break
                        y_coor += direction
                else:
                    x_coor = island.x + direction
                    if self.map[x_coor][island.y] == DOUBLE_V_BRIDGE:
                        continue
                    while neighbor.x != x_coor:
                        symbol = self.map[x_coor][island.y]
                        if symbol == SINGLE_H_BRIDGE or symbol == DOUBLE_H_BRIDGE:
                            check = False
                            break
                        x_coor += direction
                if check:
                    possible_actions.append((island.label, neighbor.label))
            checked_islands.append(island)
        return possible_actions

    def action_left(self) -> bool:
        """Checks if there are actions left in the grid

        Returns:
            bool: True if there is at least one action left
        """
        # Check if there are bridges that can be built or there are unnumbered islands
        checked_islands: list[Island] = []
        for island in self.islands.values():
            if island.bridges_required == 0:
                return True
            if island.is_full():
                checked_islands.append(island)
                continue
            for i, neighbor in enumerate(island.neighbors):
                if not neighbor or neighbor in checked_islands or neighbor.is_full():
                    continue
                horizontal = True if i > 1 else False
                direction = -1 if i == 0 or i == 2 else 1
                check = True
                if horizontal:
                    y_coor = island.y + direction
                    if self.map[island.x][y_coor] == DOUBLE_H_BRIDGE:
                        continue
                    while neighbor.y != y_coor:
                        symbol = self.map[island.x][y_coor]
                        if symbol == SINGLE_V_BRIDGE or symbol == DOUBLE_V_BRIDGE:
                            check = False
                            break
                        y_coor += direction
                else:
                    x_coor = island.x + direction
                    if self.map[x_coor][island.y] == DOUBLE_V_BRIDGE:
                        continue
                    while neighbor.x != x_coor:
                        symbol = self.map[x_coor][island.y]
                        if symbol == SINGLE_H_BRIDGE or symbol == DOUBLE_H_BRIDGE:
                            check = False
                            break
                        x_coor += direction
                if check:
                    return True
            checked_islands.append(island)
        return False

    def number_island(self, label: str, number: int) -> None:
        """Number an island that is previously not numbered

        Args:
            label (str): Letter of the island that is to be numbered
            number (int): Number to be set to the island

        Raises:
            ValueError: Island is already numbered
        """
        island = self.get_from_label(label)
        if island.is_numbered():
            raise ValueError(f"Island ({label}) is already numbered.")
        island.bridges_required = number
        self.map[island.x][island.y] = str(number)

    def build_bridge(self, source: str, destination: str, players_turn: bool) -> None:
        """Adds a bridge between two islands, while considering the restrictions. Updates the score according
        to the two islands that are given in the arguments. Check exceptions below for the restrictions.

        Args:
            source (str): Label for the source island
            destination (str): Label for the destination island
            players_turn (bool): Should be true if the action is taken by the player and not the AI

        Raises:
            ValueError: Source island has no room for additional bridges.
            ValueError: Destination island has no room for additional bridges.
            ValueError: Islands are not neighbors
            ValueError: Cannot have more then two bridges between two islands.
            ValueError: Cannot cross vertical and horizontal bridges.
        """
        src = self.get_from_label(source)
        # Check if the source island is not full
        if src.is_full():
            raise ValueError(
                f"Source island ({source}) has no room for additional bridges."
            )
        des = self.get_from_label(destination)
        # Check if the destination island is not full
        if des.is_full():
            raise ValueError(
                f"Destination island ({destination}) has no room for additional bridges."
            )
        # Check if the two islands are neighbors
        check = False
        for neighbor in src.neighbors:
            if neighbor and neighbor == des:
                check = True
                break
        if not check:
            raise ValueError(f"Islands ({source} and {destination}) are not neighbors")
        horizontal = True if src.x == des.x else False
        score = 0
        # Check if there are no cross-bridging and bridge overflow
        if horizontal:
            direction = 1 if src.y < des.y else -1
            y_coor = src.y + direction
            if self.map[src.x][y_coor] == DOUBLE_H_BRIDGE:
                raise ValueError(
                    "Cannot have more then two bridges between two islands."
                )
            while des.y != y_coor:
                symbol = self.map[src.x][y_coor]
                if symbol == SINGLE_V_BRIDGE or symbol == DOUBLE_V_BRIDGE:
                    raise ValueError("Cannot cross vertical and horizontal bridges.")
                y_coor += direction
            # Set the changes
            y_coor = src.y + direction
            while des.y != y_coor:
                self.map[src.x][y_coor] = (
                    DOUBLE_H_BRIDGE
                    if self.map[src.x][y_coor] == SINGLE_H_BRIDGE
                    else SINGLE_H_BRIDGE
                )
                y_coor += direction
        else:
            direction = 1 if src.x < des.x else -1
            x_coor = src.x + direction
            if self.map[x_coor][src.y] == DOUBLE_V_BRIDGE:
                raise ValueError(
                    "Cannot have more then two bridges between two islands."
                )
            while des.x != x_coor:
                symbol = self.map[x_coor][src.y]
                if symbol == SINGLE_H_BRIDGE or symbol == DOUBLE_H_BRIDGE:
                    raise ValueError("Cannot cross vertical and horizontal bridges.")
                x_coor += direction
            # Set the changes
            x_coor = src.x + direction
            while des.x != x_coor:
                self.map[x_coor][src.y] = (
                    DOUBLE_V_BRIDGE
                    if self.map[x_coor][src.y] == SINGLE_V_BRIDGE
                    else SINGLE_V_BRIDGE
                )
                x_coor += direction
        src.bridges_connected += 1
        des.bridges_connected += 1
        # Calculate score change
        if src.is_full():
            score += src.bridges_required
        if des.is_full():
            score += des.bridges_required
        self.score += score if players_turn else -score

    def take_action(self, first: str, second: str, players_turn: bool) -> None:
        """Wrapper function for building a bridge between two islands or
        numbering an unnumbered island

        Args:
            first (str): First parameter, label of an island
            second (str): Second paramter, can be either a label of an island or 3 or 4
            players_turn (bool): Should be true if the action is taken by the player and not the AI
        """
        if second.isnumeric():
            self.number_island(first, int(second))
        else:
            self.build_bridge(first, second, players_turn)

    def display_grid(self, width: int) -> None:
        """Display numbered and labeled grid side by side

        Args:
            width (int): Width of the line to be printed
        """
        print(center_two_strings("Grid", "Labels", width))
        count = ord("A")
        for row in range(self.height):
            grid = ""
            labeled_grid = ""
            for col in range(self.width):
                symbol = self.map[row][col]
                grid += symbol + " "
                if symbol.isnumeric():
                    labeled_grid += chr(count)
                    count += 1
                else:
                    labeled_grid += symbol
                labeled_grid += " "
            print(center_two_strings(grid, labeled_grid, width))
