import pygame
import random
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)
WATER_BLUE = (0, 191, 255)
START_COLOR = (255, 0, 0)  # Orange
END_COLOR = (255, 0, 0)  # Red
ALGORITHM_COLOR = (255, 0, 0)  # Yellow

class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_passable(self):
        return self.color == GREEN

    def is_impassable(self):
        return self.color == BLUE

    def is_start(self):
        return self.color == START_COLOR

    def is_end(self):
        return self.color == END_COLOR

    def reset(self):
        self.color = WHITE

    def make_passable(self):
        self.color = GREEN

    def make_impassable(self):
        self.color = BLUE

    def make_start(self):
        self.color = START_COLOR

    def make_end(self):
        self.color = END_COLOR

    def make_algorithm_path(self):
        self.color = ALGORITHM_COLOR

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_impassable():  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_impassable():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_impassable():  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_impassable():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        if not current.is_start():
            current.make_algorithm_path()
        draw()

def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_algorithm_path()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    if not neighbor.is_start():
                        neighbor.make_algorithm_path()

        draw()

        if current != start:
            current.make_impassable()

    return False

def make_random_map(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)

    # Make everything grass initially
    for i in range(rows):
        for j in range(rows):
            grid[i][j].make_passable()

    # Add water randomly
    for _ in range(500):  # Adjust the number of water tiles as needed
        i, j = random.randint(0, rows - 1), random.randint(0, rows - 1)
        grid[i][j].make_impassable()

    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
    win.fill(BLACK)

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()

def main(win, width):
    ROWS = 50
    grid = make_random_map(ROWS, width)

    # Set random start and end points
    start_row, start_col = random.randint(0, ROWS - 1), random.randint(0, ROWS - 1)
    end_row, end_col = random.randint(0, ROWS - 1), random.randint(0, ROWS - 1)

    start = grid[start_row][start_col]
    end = grid[end_row][end_col]

    start.make_passable()
    end.make_passable()

    run = True
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_random_map(ROWS, width)

                    start_row, start_col = random.randint(0, ROWS - 1), random.randint(0, ROWS - 1)
                    end_row, end_col = random.randint(0, ROWS - 1), random.randint(0, ROWS - 1)

                    start = grid[start_row][start_col]
                    end = grid[end_row][end_col]

                    start.make_passable()
                    end.make_passable()

    pygame.quit()

# Call the main function
main(WIN, WIDTH)
