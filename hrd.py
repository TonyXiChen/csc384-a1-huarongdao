import collections
import heapq
import math
import sys


def locations_of_empty(game_board: list) -> list:
    """Return all the coordinates of the empty squares"""
    result = []
    for i in range(20):
        if game_board[i // 4][i % 4] == 0:
            result.append(((i // 4), (i % 4)))
    return result


def location_of_2x2(game_board: list) -> tuple:
    """Return the upper-leftmost coordinate of the 2x2 piece"""
    for i in range(20):
        if game_board[i // 4][i % 4] == 1:
            return (i // 4), (i % 4)
    return 0, 0


def locations_of_1x1(game_board: list) -> list:
    """Return all the coordinates of 1x1 pieces"""
    result = []
    for i in range(20):
        if game_board[i // 4][i % 4] == 7:
            result.append(((i // 4), (i % 4)))
    return result


def locations_of_horizontal(game_board: list) -> list:
    """Return all the leftmost coordinates of horizontal 1x2 pieces"""
    result = []
    for i in range(20):
        if (i % 4 + 1 <= 3) and (game_board[i // 4][i % 4]) in {2, 3, 4, 5, 6} and (game_board[i // 4][i % 4] == game_board[i // 4][i % 4 + 1]):
            result.append(((i // 4), (i % 4)))
    return result


def locations_of_vertical(game_board: list) -> list:
    """Return all the upper coordinates of vertical 1x2 pieces"""
    result = []
    for i in range(20):
        if (i // 4 + 1 <= 4) and (game_board[i // 4][i % 4]) in {2, 3, 4, 5, 6} and (game_board[i // 4][i % 4] == game_board[i // 4 + 1][i % 4]):
            result.append(((i // 4), (i % 4)))
    return result


class State:
    """A state in the search graph"""
    zero: list  # empty
    one: tuple  # 2x2 piece, only one so use tuple
    two: list  # horizontal 1x2 piece
    three: list  # vertical 2x1 piece
    four: list  # 1x1 piece

    def __init__(self, zero=None, one=(), two=None, three=None, four=None, board_only=None) -> None:
        self.zero = zero
        self.one = one
        self.two = two
        self.three = three
        self.four = four
        if board_only is not None:
            self.zero = locations_of_empty(board_only)
            self.one = location_of_2x2(board_only)
            self.two = locations_of_horizontal(board_only)
            self.three = locations_of_vertical(board_only)
            self.four = locations_of_1x1(board_only)

    def is_goal_state(self) -> bool:
        if self.one == (3, 1):
            return True
        else:
            return False

    def print_state(self) -> list:
        result = list(range(20))
        for single_zero in self.zero:
            result[single_zero[0] * 4 + single_zero[1]] = 0
        one_coordinates = [self.one, (self.one[0], self.one[1] + 1), (self.one[0] + 1, self.one[1]), (self.one[0] + 1, self.one[1] + 1)]
        for single_one in one_coordinates:
            result[single_one[0] * 4 + single_one[1]] = 1
        for horizontal in self.two:
            horizontal_coordinates = [horizontal, (horizontal[0], horizontal[1] + 1)]
            for single_horizontal in horizontal_coordinates:
                result[single_horizontal[0] * 4 + single_horizontal[1]] = 2
        for vertical in self.three:
            vertical_coordinates = [vertical, (vertical[0] + 1, vertical[1])]
            for single_vertical in vertical_coordinates:
                result[single_vertical[0] * 4 + single_vertical[1]] = 3
        for single_four in self.four:
            result[single_four[0] * 4 + single_four[1]] = 4
        return result


def all_to_the(coordinates: list, direction: str) -> list:
    result = []
    if direction == "up":
        for coordinate in coordinates:
            result.append((coordinate[0] - 1, coordinate[1]))
    elif direction == "down":
        for coordinate in coordinates:
            result.append((coordinate[0] + 1, coordinate[1]))
    elif direction == "left":
        for coordinate in coordinates:
            result.append((coordinate[0], coordinate[1] - 1))
    elif direction == "right":
        for coordinate in coordinates:
            result.append((coordinate[0], coordinate[1] + 1))
    return result


def successors(s: State) -> list:
    zero, one, two, three, four, result, new_zero, new_one = set(s.zero.copy()), s.one, s.two.copy(), s.three.copy(), s.four.copy(), [], [], []

    one_coordinates = [one, (one[0], one[1] + 1), (one[0] + 1, one[1]), (one[0] + 1, one[1] + 1)]
    if {all_to_the(one_coordinates, "up")[0], all_to_the(one_coordinates, "up")[1]} == zero:
        new_zero = [one_coordinates[2], one_coordinates[3]]
        new_one = all_to_the([one], "up")[0]
    elif {all_to_the(one_coordinates, "down")[2], all_to_the(one_coordinates, "down")[3]} == zero:
        new_zero = [one_coordinates[0], one_coordinates[1]]
        new_one = all_to_the([one], "down")[0]
    elif {all_to_the(one_coordinates, "left")[0], all_to_the(one_coordinates, "left")[2]} == zero:
        new_zero = [one_coordinates[1], one_coordinates[3]]
        new_one = all_to_the([one], "left")[0]
    elif {all_to_the(one_coordinates, "right")[1], all_to_the(one_coordinates, "right")[3]} == zero:
        new_zero = [one_coordinates[0], one_coordinates[2]]
        new_one = all_to_the([one], "right")[0]
    if len(new_zero) == 2:
        result.append(State(new_zero, new_one, two, three, four))

    for horizontal in two:
        horizontal_coordinates = [horizontal, (horizontal[0], horizontal[1] + 1)]
        for direction in ["up", "down"]:
            if set(all_to_the(horizontal_coordinates, direction)) == zero:
                new_zero = horizontal_coordinates
                new_two = [all_to_the(horizontal_coordinates, direction)[0] if h == horizontal_coordinates[0] else h for h in two]
                result.append(State(new_zero, one, new_two, three, four))
        if all_to_the(horizontal_coordinates, "left")[0] in zero:
            new_zero = [(horizontal[0], horizontal[1] + 1) if all_to_the(horizontal_coordinates, "left")[0] == old_zero else old_zero for old_zero in zero]
            new_two = [all_to_the(horizontal_coordinates, "left")[0] if h == horizontal_coordinates[0] else h for h in two]
            result.append(State(new_zero, one, new_two, three, four))
        if all_to_the(horizontal_coordinates, "right")[1] in zero:
            new_zero = [horizontal if all_to_the(horizontal_coordinates, "right")[1] == old_zero else old_zero for old_zero in zero]
            new_two = [all_to_the(horizontal_coordinates, "right")[0] if h == horizontal_coordinates[0] else h for h in two]
            result.append(State(new_zero, one, new_two, three, four))

    for vertical in three:
        vertical_coordinates = [vertical, (vertical[0] + 1, vertical[1])]
        for direction in ["left", "right"]:
            if set(all_to_the(vertical_coordinates, direction)) == zero:
                new_zero = vertical_coordinates
                new_three = [all_to_the(vertical_coordinates, direction)[0] if v == vertical_coordinates[0] else v for v in three]
                result.append(State(new_zero, one, two, new_three, four))
        if all_to_the(vertical_coordinates, "up")[0] in zero:
            new_zero = [(vertical[0] + 1, vertical[1]) if all_to_the(vertical_coordinates, "up")[0] == old_zero else old_zero for old_zero in zero]
            new_three = [all_to_the(vertical_coordinates, "up")[0] if v == vertical_coordinates[0] else v for v in three]
            result.append(State(new_zero, one, two, new_three, four))
        if all_to_the(vertical_coordinates, "down")[1] in zero:
            new_zero = [vertical if all_to_the(vertical_coordinates, "down")[1] == old_zero else old_zero for old_zero in zero]
            new_three = [all_to_the(vertical_coordinates, "down")[0] if v == vertical_coordinates[0] else v for v in three]
            result.append(State(new_zero, one, two, new_three, four))

    for single in four:
        for direction in ["up", "down", "left", "right"]:
            for some_zero in zero:
                if all_to_the([single], direction)[0] == some_zero:
                    new_zero = [single if old_empty == some_zero else old_empty for old_empty in zero]
                    new_four = [some_zero if old_single == single else old_single for old_single in four]
                    result.append(State(new_zero, one, two, three, new_four))

    return result


class Node:
    item: State
    prev_node = None
    next_node = None
    cost = 0
    heuristic = math.inf

    def __init__(self, item=None, prev_node=None, cost=0, heuristic=math.inf):
        self.item = item
        self.prev_node = prev_node
        self.cost = cost
        self.heuristic = heuristic

    def __lt__(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)

    def print_from_initial_node(self) -> str:
        result = "Cost of the solution: " + str(self.cost) + "\n"
        text = collections.deque()
        curr = self
        while (curr is not None) and (curr.item is not None):
            index = 0
            text_block = ""
            for number in curr.item.print_state():
                text_block += str(number)
                if index % 4 == 3:
                    text_block += "\n"
                index += 1
            text_block += "\n"
            text.append(text_block)
            curr = curr.prev_node
        while text:
            result += text.pop()
        return result


def manhattan_heuristic(s: State) -> int:
    return abs(s.one[0] - 3) + abs(s.one[1] - 1)


def manhattan_heuristic_pro_max(s: State) -> int:
    """manhattan plus the number of other characters in the target region"""
    two, three, four, count = s.two.copy(), s.three.copy(), s.four.copy(), 0
    target_region = {(3, 1), (3, 2), (4, 1), (4, 2)}

    for horizontal in two:
        horizontal_coordinates = {horizontal, (horizontal[0], horizontal[1] + 1)}
        if horizontal_coordinates.intersection(target_region) != set():
            count += 1
    for vertical in three:
        vertical_coordinates = {vertical, (vertical[0] + 1, vertical[1])}
        if vertical_coordinates.intersection(target_region) != set():
            count += 1
    for single_four in four:
        if single_four in target_region:
            count += 1

    return manhattan_heuristic(s) + count


def successor_nodes(n: Node, heuristic="manhattan") -> list:
    result = []
    for successor in successors(n.item):
        if heuristic == "manhattan":
            successor_node = Node(item=successor, prev_node=n, cost=n.cost+1, heuristic=manhattan_heuristic(successor))
        elif heuristic == "manhattan_pro_max":
            successor_node = Node(item=successor, prev_node=n, cost=n.cost+1, heuristic=manhattan_heuristic_pro_max(successor))
        else:
            successor_node = Node(item=successor, prev_node=n, cost=n.cost + 1, heuristic=0)
        result.append(successor_node)
    return result


def manhattan_heuristic_search_solution(initial_n: Node) -> Node:
    frontier = [initial_n]
    pruning = set()
    while len(frontier) > 0:
        current_node = heapq.heappop(frontier)
        pruning.add(hash(tuple(current_node.item.print_state())))
        if current_node.item.is_goal_state():
            return current_node
        for next_move in successor_nodes(current_node, heuristic="manhattan"):
            if hash(tuple(next_move.item.print_state())) not in pruning:
                pruning.add(hash(tuple(next_move.item.print_state())))
                heapq.heappush(frontier, next_move)
    return initial_n


def manhattan_heuristic_pro_max_search_solution(initial_n: Node) -> Node:
    frontier = [initial_n]
    pruning = set()
    while len(frontier) > 0:
        current_node = heapq.heappop(frontier)
        pruning.add(hash(tuple(current_node.item.print_state())))
        if current_node.item.is_goal_state():
            return current_node
        for next_move in successor_nodes(current_node, heuristic="manhattan_pro_max"):
            if hash(tuple(next_move.item.print_state())) not in pruning:
                pruning.add(hash(tuple(next_move.item.print_state())))
                heapq.heappush(frontier, next_move)
    return initial_n


def dfs_solution(initial_n: Node) -> Node:
    frontier = collections.deque()
    frontier.append(initial_n)
    pruning = set()
    while len(frontier) > 0:
        current_node = frontier.pop()
        pruning.add(hash(tuple(current_node.item.print_state())))
        if current_node.item.is_goal_state():
            return current_node
        for next_move in successor_nodes(current_node, heuristic="dfs"):
            if hash(tuple(next_move.item.print_state())) not in pruning:
                pruning.add(hash(tuple(next_move.item.print_state())))
                frontier.append(next_move)
    return initial_n


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python3 hrd.py  <input file>  <DFS output file>  <A* output file>")
        sys.exit()

    input_file = open(sys.argv[1], "r")
    dfs_output_file = open(sys.argv[2], "w")
    a_star_output_file = open(sys.argv[3], "w")

    empty_board = [[8, 8, 8, 8], [8, 8, 8, 8], [8, 8, 8, 8], [8, 8, 8, 8], [8, 8, 8, 8]]
    """Game board initialized with 8's, coordinate wise, upper-leftmost is 0,0 and lower-rightmost is 4,3"""

    c = input_file.read(1)
    input_index = 0
    while input_index <= 19:
        if c.isdigit():
            empty_board[input_index // 4][input_index % 4] = int(c)
            input_index += 1
            c = input_file.read(1)
        else:
            c = input_file.read(1)
    initial_board = empty_board.copy()
    initial_state = State(board_only=initial_board)
    initial_node = Node(item=initial_state, heuristic=manhattan_heuristic(initial_state))

    dfs_solution_node = dfs_solution(initial_node)
    dfs_output_file.write(dfs_solution_node.print_from_initial_node())
    dfs_output_file.close()

    a_star_solution_node = manhattan_heuristic_search_solution(initial_node)
    a_star_output_file.write(a_star_solution_node.print_from_initial_node())
    a_star_output_file.close()

    a_star_solution_node = manhattan_heuristic_pro_max_search_solution(initial_node)
