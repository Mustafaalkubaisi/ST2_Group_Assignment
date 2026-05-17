import pygame
import sys
import sorting_module
import graphs_module
import heap_module
import puzzles_module
import assignment_phase1


pygame.init()
WIDTH, HEIGHT = 800, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

def draw_text(text, pos):
    txt = FONT.render(text, True, (0, 0, 0))
    screen.blit(txt, pos)

def main_menu():
    screen.fill((200, 200, 250))
    draw_text("Algorithm Explorer", (WIDTH // 3, 50))
    buttons = {
        'Data Structures': pygame.Rect(270, 150, 220, 50),
        'Sorting':         pygame.Rect(270, 230, 220, 50),
        'Graphs':          pygame.Rect(270, 310, 220, 50),
        'Heap':            pygame.Rect(270, 390, 220, 50),
        'Puzzles':         pygame.Rect(270, 470, 220, 50)
    }

    for text, rect in buttons.items():
        pygame.draw.rect(screen, (150, 150, 200), rect)
        draw_text(text, (rect.x + 20, rect.y + 10))
    pygame.display.flip()
    return buttons

def data_structures_module():
    assignment_phase1.run(screen)


def main():
    running = True
    current_module = None

    while running:
        buttons = main_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and current_module is None:
                for name, rect in buttons.items():
                    if rect.collidepoint(event.pos):
                        current_module = name
                        break

                # Run modules based on button pressed
                if current_module:
                    if current_module == 'Data Structures':
                        data_structures_module()
                    elif current_module == 'Sorting':
                        sorting_module.main()
                    elif current_module == 'Graphs':
                        graphs_module.main()
                    elif current_module == 'Heap':
                        heap_module.main()
                    elif current_module == 'Puzzles':
                        puzzles_module.main()
                    current_module = None

        clock.tick(30)
    pygame.quit()


if __name__ == "__main__":
    main()



