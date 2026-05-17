import pygame
import sys

pygame.init()

WIDTH = 600
HEIGHT = 700
ROWS = 6
COLS = 6
CELL_SIZE = WIDTH // COLS

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dynamic Programming Puzzle")

FONT = pygame.font.SysFont(None, 30)
clock = pygame.time.Clock()

dp = [[None for col in range(COLS)] for row in range(ROWS)]
obstacles = set()

path = []

# Draws the grid, obstacles, path and highlighted cells
def draw_grid(highlight=None):
    screen.fill((255, 255, 255))

    instructions = FONT.render("Click: Add obstacle | SPACE: Run DP | C: Clear | ESC: Back", True, (0, 0, 0))
    screen.blit(instructions, (10, 10))

    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(
                col * CELL_SIZE,
                row * CELL_SIZE + 60,
                CELL_SIZE,
                CELL_SIZE
            )

            color = (200, 200, 200)

            if (row, col) == (0,0):
                color = (100, 255, 100)

            elif (row, col) == (ROWS - 1, COLS - 1):
                color = (255, 100, 100)

            if (row, col) in obstacles:
                color = (0, 0, 0)

            if highlight == (row, col):
                color = (255, 180, 180)

            if (row, col) in path:
                color = (255, 255, 0)

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)

            if dp[row][col] is not None and (row, col) not in obstacles:
                text = FONT.render(str(dp[row][col]), True, (0, 0, 0))
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

    pygame.display.flip()

# Returns the cell clicked by the user
def cell_clicked(pos):
    x, y = pos
    row = (y - 60) // CELL_SIZE
    col = x // CELL_SIZE

    if 0 <= row < ROWS and 0 <= col < COLS:
        return row, col

    return None


# Counts all valid paths through the grid
def count_paths():
    global dp
    for row in range(ROWS):
        for col in range(COLS):

            if (row, col) in obstacles:
                dp[row][col] = 0

            elif row == 0 and col == 0:
                dp[row][col] = 1

            else:
                up = dp[row - 1][col] if row > 0 else 0
                left = dp[row][col - 1] if col > 0 else 0
                dp[row][col] = up + left

            draw_grid((row, col))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


            pygame.time.wait(300)


    reconstruct_path()


# Reconstructs valid path from the table
def reconstruct_path():
    path.clear()

    row = ROWS - 1
    col = COLS - 1

    if dp[row][col] == 0 or dp[row][col] is None:
        return

    while row != 0 or col != 0:
        path.append((row, col))

        if row > 0 and dp[row - 1][col] != 0:
            row -= 1

        elif col > 0 and dp[row][col - 1] != 0:
            col -= 1

        else:
            return

        draw_grid((row, col))
        pygame.time.wait(200)

    path.append((0, 0))


# Main loop
def main():
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
                    obstacles.clear()
                    path.clear()

                    for row in range(ROWS):
                        for col in range(COLS):
                            dp[row][col] = None

                elif event.key == pygame.K_SPACE:
                    count_paths()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked_cell = cell_clicked(event.pos)

                if clicked_cell is not None:
                    if clicked_cell != (0,0) and clicked_cell != (ROWS - 1, COLS - 1):
                        obstacles.add(clicked_cell)

        clock.tick(30)


if __name__ == "__main__":
    main()