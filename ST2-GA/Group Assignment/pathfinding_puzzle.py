import pygame
import sys
import collections



pygame.init()

WIDTH = 800
HEIGHT = 700
ROWS = 40
CELL_SIZE = WIDTH // ROWS

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinding Puzzle")

FONT = pygame.font.SysFont(None, 28)
clock = pygame.time.Clock()

grid = []
start_pos = None
end_pos = None


for row in range(ROWS):
    grid.append([])
    for col in range(ROWS):
        grid[row].append(0)

# 0 = empty
# 1 = obstacle
# 2 = start
# 3 = end

# Draws the grid and adds the colours for the obtacles, nodes and final path
def draw_grid():
    screen.fill((255, 255, 255))

    for row in range(ROWS):
        for col in range(ROWS):

            color = (255, 255, 255)

            if grid[row][col] == 1:
                color = (0, 0, 0)

            elif grid[row][col] == 2:
                color = (0, 255, 0)

            elif grid[row][col] == 3:
                color = (255, 0, 0)

            elif grid[row][col] == 4:
                color = (100, 200, 255)

            elif grid[row][col] == 5:
                color = (0, 128, 0)

            rect = pygame.Rect(
                col * CELL_SIZE,
                row * CELL_SIZE + 40,
                CELL_SIZE,
                CELL_SIZE
            )

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)
    instructions = FONT.render("Left click: Start, End, Obstacles| Space: Run| Right click: Erase| C: Clear| ESC: Back", True, (0, 0, 0))
    screen.blit(instructions, (10, 10))
    pygame.display.flip()


# Returns the cell clicked by the user
def cell_clicked(pos):
    x, y = pos
    row = (y-40) // CELL_SIZE
    col = x // CELL_SIZE

    if 0 <= row < ROWS and 0 <= col < ROWS:
        return row, col
    return None

# Returns valid neighbouring cells that aren't obstacles
def get_neighbors(row, col):
    neighbors = []

    directions = [
        (-1, 0),  # up
        (1, 0),   # down
        (0, -1),  # left
        (0, 1)    # right
    ]

    for dr, dc in directions:
        new_row = row + dr
        new_col = col + dc

        if 0 <= new_row < ROWS and 0 <= new_col < ROWS:
            if grid[new_row][new_col] != 1:
                neighbors.append((new_row, new_col))

    return neighbors

# BFS pathfinding that explores neighbouring cells using a queue
def bfs_pathfinding():
    if start_pos is None or end_pos is None:
        print("Please place both a start and end point.")
        return

    queue = collections.deque()
    queue.append(start_pos)

    visited = set()
    visited.add(start_pos)

    came_from = {}

    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        current = queue.popleft()

        if current == end_pos:
            reconstruct_path(came_from)
            return

        row, col = current

        for neighbor in get_neighbors(row, col):
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.append(neighbor)

                n_row, n_col = neighbor
                if grid[n_row][n_col] == 0:
                    grid[n_row][n_col] = 4
                    draw_grid()
                    pygame.time.wait(20)

# Rebuilds and displays the shortest path
def reconstruct_path(came_from):
    current = end_pos

    while current != start_pos:
        current = came_from[current]

        if current != start_pos:
            row, col = current
            grid[row][col] = 5

            draw_grid()
            pygame.time.wait(40)

# Main loop
def main():
    global start_pos, end_pos, grid

    running = True

    while running:
        draw_grid()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_c:
                    grid = [[0 for col in range(ROWS)] for row in range(ROWS)]
                    start_pos = None
                    end_pos = None

                elif event.key == pygame.K_SPACE:
                    bfs_pathfinding()


            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked_cell = cell_clicked(event.pos)

                if clicked_cell is not None:
                    row, col = clicked_cell

                    if event.button == 1:  # left click
                        if start_pos is None:
                            start_pos = (row, col)
                            grid[row][col] = 2

                        elif end_pos is None and (row, col) != start_pos:
                            end_pos = (row, col)
                            grid[row][col] = 3

                        elif (row, col) != start_pos and (row, col) != end_pos:
                            grid[row][col] = 1

                    elif event.button == 3:  # right click
                        if (row, col) == start_pos:
                            start_pos = None

                        if (row, col) == end_pos:
                            end_pos = None

                        grid[row][col] = 0

        clock.tick(30)


if __name__ == "__main__":
    main()