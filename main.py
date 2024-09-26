from collections import deque
import heapq
import random

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def is_empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

def initialize_grid():
    # Get user input for the search algorithm, number of rows, and columns
    search_algorithm = int(input("Enter the search algorithm you want to use \n1. Depth First Search\n2. Uninformed Cost Search\n3. Breadth First Search\n4. Greedy Best-First Algorithm\n5. A* Search Algorithm\nPlease enter between 1-5: "))
    rows = int(input("Enter the number of rows: "))
    cols = int(input("Enter the number of columns: "))

    algorithm_names = ['dfs', 'ucs', 'bfs', 'gbf', 'A*']
    if search_algorithm not in [1, 2, 3, 4, 5]:
        raise Exception("Input should be between 1 and 5")
    if rows < 1 or cols < 1:
        raise Exception("Rows and columns must be positive integers")

    # Initialize a 2D array with spaces
    grid = [[" " for _ in range(cols)] for _ in range(rows)]

    # Prompt user for the starting position
    while True:
        start_row = int(input("Enter the starting row (0 to {}): ".format(rows - 1)))
        start_col = int(input("Enter the starting column (0 to {}): ".format(cols - 1)))
        if 0 <= start_row < rows and 0 <= start_col < cols:
            grid[start_row][start_col] = "S"  # Mark the starting position on the grid
            break
        else:
            print("Invalid starting position. Please enter again.")

    # Prompt user for the goal position
    while True:
        goal_row = int(input("Enter the goal row (0 to {}): ".format(rows - 1)))
        goal_col = int(input("Enter the goal column (0 to {}): ".format(cols - 1)))
        if 0 <= goal_row < rows and 0 <= goal_col < cols:
            grid[goal_row][goal_col] = "G"  # Mark the goal position on the grid
            break
        else:
            print("Invalid goal position. Please enter again.")

    # Prompt user for the number of obstacles
    num_obstacles = int(input("Enter the number of obstacles: "))
    for _ in range(num_obstacles):
        obstacle_row = random.randint(0, rows - 1)
        obstacle_col = random.randint(0, cols - 1)
        while grid[obstacle_row][obstacle_col] != " ":
            obstacle_row = random.randint(0, rows - 1)
            obstacle_col = random.randint(0, cols - 1)
        grid[obstacle_row][obstacle_col] = "X"

    return grid, (start_row, start_col), (goal_row, goal_col), algorithm_names[search_algorithm - 1]



def display_grid(grid, start_pos, goal_pos, path=None):
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if (i, j) == start_pos:
                print(f" S ", end="")
            elif (i, j) == goal_pos:
                print(f" G ", end="")
            elif path and (i, j) in path:
                print(" * ", end="")
            elif cell == "X":
                print(" # ", end="")  # Print blockage symbol
            else:
                print(f" . ", end="")
        print('')

def dfs(grid, start, goal):
    movements = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    stack = PriorityQueue()
    stack.put(start, 0)

    visited = set()
    visited.add(start)

    parent = {}

    while not stack.is_empty():
        current_node = stack.get()

        if current_node == goal:
            path = []
            while current_node:
                path.append(current_node)
                current_node = parent.get(current_node)
            return path[::-1], len(path), len(visited)

        row, col = current_node

        for move in movements:
            new_row, new_col = row + move[0], col + move[1]
            if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]) and grid[new_row][new_col] != "X" and (new_row, new_col) not in visited:
                stack.put((new_row, new_col), 0)  # Priority doesn't affect DFS
                visited.add((new_row, new_col))
                parent[(new_row, new_col)] = current_node

    return None, 0, len(visited)


def bfs(grid, start, goal):
    movements = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    queue = PriorityQueue()
    queue.put(start, 0)

    visited = set()
    visited.add(start)

    parent = {}

    while not queue.is_empty():
        current_node = queue.get()

        if current_node == goal:
            path = []
            while current_node:
                path.append(current_node)
                current_node = parent.get(current_node)
            return path[::-1], len(path), len(visited)

        row, col = current_node

        for move in movements:
            new_row, new_col = row + move[0], col + move[1]
            if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]) and grid[new_row][new_col] != "X" and (new_row, new_col) not in visited:
                queue.put((new_row, new_col), 0)  # Priority doesn't affect BFS
                visited.add((new_row, new_col))
                parent[(new_row, new_col)] = current_node

    return None, 0, len(visited)




def ucs(grid, start, goal):
    movements = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    pq = PriorityQueue()
    pq.put(start, 0)

    visited = set()

    cost_so_far = {start: 0}

    parent = {}

    while not pq.is_empty():
        current_node = pq.get()

        if current_node == goal:
            path = []
            while current_node:
                path.append(current_node)
                current_node = parent.get(current_node)
            return path[::-1], cost_so_far[goal], len(visited)

        visited.add(current_node)
        row, col = current_node

        for move in movements:
            new_row, new_col = current_node[0] + move[0], current_node[1] + move[1]
            if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]) and grid[new_row][new_col] != "X":
                new_cost = cost_so_far[current_node] + 1  # Uniform cost
                if (new_row, new_col) not in cost_so_far or new_cost < cost_so_far[(new_row, new_col)]:
                    cost_so_far[(new_row, new_col)] = new_cost
                    pq.put((new_row, new_col), new_cost)
                    parent[(new_row, new_col)] = current_node

    return None, 0, len(visited)


def gbf(grid, start, goal):
    movements = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    pq = PriorityQueue()
    pq.put(start, heuristic(start, goal))

    visited = set()

    parent = {}

    while not pq.is_empty():
        current_node = pq.get()

        if current_node == goal:
            path = []
            while current_node:
                path.append(current_node)
                current_node = parent.get(current_node)
            return path[::-1], len(path), len(visited)

        visited.add(current_node)
        row, col = current_node

        for move in movements:
            new_row, new_col = current_node[0] + move[0], current_node[1] + move[1]
            if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]) and grid[new_row][new_col] != "X" and (new_row, new_col) not in visited:
                pq.put((new_row, new_col), heuristic((new_row, new_col), goal))
                parent[(new_row, new_col)] = current_node

    return None, 0, len(visited)


def heuristic(current, goal):
    # Manhattan distance heuristic
    return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

def astar(grid, start, goal):
    movements = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    pq = PriorityQueue()
    pq.put(start, heuristic(start, goal))

    visited = set()

    cost_so_far = {start: 0}

    parent = {}

    while not pq.is_empty():
        current_node = pq.get()

        if current_node == goal:
            path = []
            while current_node:
                path.append(current_node)
                current_node = parent.get(current_node)
            return path[::-1], cost_so_far[goal], len(visited)

        visited.add(current_node)
        row, col = current_node

        for move in movements:
            new_row, new_col = current_node[0] + move[0], current_node[1] + move[1]
            if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]) and grid[new_row][new_col] != "X":
                new_cost = cost_so_far[current_node] + 1  # Cost for moving to a neighboring cell
                if (new_row, new_col) not in cost_so_far or new_cost < cost_so_far[(new_row, new_col)]:
                    cost_so_far[(new_row, new_col)] = new_cost
                    pq.put((new_row, new_col), new_cost + heuristic((new_row, new_col), goal))
                    parent[(new_row, new_col)] = current_node

    return None, 0, len(visited)

# Example usage:
import heapq

my_grid, start_pos, goal_pos, searchAlgorithm = initialize_grid()
print("Initialized Grid:")
print(searchAlgorithm)
if searchAlgorithm == 'dfs':
    path, path_length, cells_visited = dfs(my_grid, start_pos, goal_pos)
    if path:
        print("Path found:", path)
    else:
        print("No path found.")
    print("Total cells visited:", cells_visited)
    print()
elif searchAlgorithm == 'ucs':
    path, path_length, cells_visited = ucs(my_grid, start_pos, goal_pos)
    if path:
        print("Path found:", path)
    else:
        print("No path found.")
    print("Total cells visited:", cells_visited)
    print()
elif searchAlgorithm == 'bfs':
    path, path_length, cells_visited = bfs(my_grid, start_pos, goal_pos)
    if path:
        print("Path found:", path)
    else:
        print("No path found.")
    print("Total cells visited:", cells_visited)
    print()
elif searchAlgorithm == 'gbf':
    path, path_length, cells_visited = gbf(my_grid, start_pos, goal_pos)
    if path:
        print("Path found:", path)
    else:
        print("No path found.")
    print("Total cells visited:", cells_visited)
    print()
elif searchAlgorithm == 'A*':
    path, path_length, cells_visited = astar(my_grid, start_pos, goal_pos)
    if path:
        print("Path found:", path)
    else:
        print("No path found.")
    print("Total cells visited:", cells_visited)
    print()

display_grid(my_grid, start_pos, goal_pos, path)
