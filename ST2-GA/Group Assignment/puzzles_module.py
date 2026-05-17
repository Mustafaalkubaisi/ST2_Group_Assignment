import pygame
import sys
import pathfinding_puzzle
import event_queue_simulator
import dp_puzzle


pygame.init()

WIDTH, HEIGHT = 800, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()


White = (255, 255, 255)
Red = (255, 100, 100)
Green = (100, 255, 100)
Black = (0, 0, 0)
Yellow = (225, 225, 0)
LightBlue = (200, 200, 250)
MutedBlue = (150, 150, 200)
OffWhite = (230, 230, 235)
LimeGreen = (50, 205, 50)
Crimson = (220, 50, 50)
Orange = (255, 140, 0)

# shows text on the screen
def draw_text(text, pos):
    txt = FONT.render(text, True, (0, 0, 0))
    screen.blit(txt, pos)

# Main menu for the puzzles
def puzzles_menu():
    screen.fill(LightBlue)
    draw_text("Phase 3: Puzzle Challenges", (210, 50))

    # Puzzles available
    buttons = {
        'Pathfinding Puzzle': pygame.Rect(170, 150, 460, 50),
        'Event Queue Simulator': pygame.Rect(170, 230, 460, 50),
        'Dynamic Programming Puzzle': pygame.Rect(170, 310, 460, 50),
        'Back': pygame.Rect(170, 390, 460, 50)
    }

    # Draw buttons
    for text, rect in buttons.items():
        pygame.draw.rect(screen, MutedBlue, rect)
        draw_text(text, (rect.x + 20, rect.y + 10))

    pygame.display.flip()
    return buttons

# Main loop
def main():
    running = True

    while running:
        buttons = puzzles_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for name, rect in buttons.items():

                    # Run puzzles based on button pressed
                    if rect.collidepoint(event.pos):
                        if name == 'Pathfinding Puzzle':
                            pathfinding_puzzle.main()

                        elif name == 'Event Queue Simulator':
                            event_queue_simulator.main()

                        elif name == 'Dynamic Programming Puzzle':
                            dp_puzzle.main()

                        elif name == 'Back':
                            running = False

        clock.tick(30)


if __name__ == "__main__":
    main()