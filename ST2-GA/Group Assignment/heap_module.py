import pygame
import sys
import math


pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.SysFont('Calibri', 36, bold=False)
SMALL_FONT = pygame.font.SysFont('Calibri', 28, bold=False)
BOLD_FONT = pygame.font.SysFont('Calibri', 28, bold=True)
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

heap = []  # Heap stored as a list — empty to start


# Insert — adds value to end of heap then shifts up to restore heap property
def insert(heap, value):
    heap.append(value)
    i = len(heap) - 1
    while i > 0:
        parent = (i - 1) // 2
        yield heap[:], i, parent
        if heap[i] > heap[parent]:
            heap[i], heap[parent] = heap[parent], heap[i]
            i = parent
        else:
            break
    yield heap[:], -1, -1


# Extract — removes root (max value), moves last item to root then shifts down
def extract(heap):
    if not heap:
        return
    heap[0] = heap[-1]
    heap.pop()
    i = 0
    while True:
        left = 2 * i + 1
        right = 2 * i + 2
        largest = i
        if left < len(heap) and heap[left] > heap[largest]:
            largest = left
        if right < len(heap) and heap[right] > heap[largest]:
            largest = right
        yield heap[:], i, largest
        if largest != i:
            heap[i], heap[largest] = heap[largest], heap[i]
            i = largest
        else:
            break
    yield heap[:], -1, -1


# Calculates screen position of a node based on its level in the tree
def get_node_pos(i, total):
    level = int(math.log2(i + 1))
    level_start = 2 ** level - 1
    pos_in_level = i - level_start
    nodes_in_level = 2 ** level
    x = (pos_in_level + 0.5) * (WIDTH / nodes_in_level)
    y = 120 + level * 100
    return int(x), int(y)


# Shows text on the screen at the set position
def draw_text(text, pos, font=None, colour=Black):
    if font is None:
        font = FONT
    txt = font.render(text, True, colour)
    screen.blit(txt, pos)


# Draws the heap as a binary tree — orange = active node, red = comparison node
def draw_heap(heap, active=-1, compare=-1):
    for i in range(len(heap)):
        pos = get_node_pos(i, len(heap))

        # Draw line to parent (skip root)
        if i > 0:
            parent_pos = get_node_pos((i - 1) // 2, len(heap))
            pygame.draw.line(screen, Black, parent_pos, pos, 2)

        if i == active:
            colour = Orange
        elif i == compare:
            colour = Red
        else:
            colour = MutedBlue

        pygame.draw.circle(screen, colour, pos, 25)
        pygame.draw.circle(screen, Black, pos, 25, 2)

        text = str(heap[i])
        text_surf = SMALL_FONT.render(text, True, Black)
        text_rect = text_surf.get_rect(center=pos)
        screen.blit(text_surf, text_rect)


# Main loop
def main():
    input_text = ""
    input_active = False
    cursor_visible = True
    cursor_timer = 0
    status = ""
    generator = None
    animating = False
    anim_delay = 750  # Milliseconds between animation steps
    last_step = pygame.time.get_ticks()
    active = -1
    compare = -1

    # Button positions along the top of the screen
    back_btn    = pygame.Rect(20,  15, 150, 38)
    insert_btn  = pygame.Rect(185, 15, 120, 38)
    input_box   = pygame.Rect(325, 10, 170, 50)
    extract_btn = pygame.Rect(510, 15, 120, 38)
    reset_btn   = pygame.Rect(645, 15, 120, 38)

    running = True
    while running:
        # Blinking cursor — toggles every 500ms
        cursor_timer += clock.get_time()
        if cursor_timer >= 500:
            cursor_visible = not cursor_visible
            cursor_timer = 0

        # Advance animation one step per anim_delay milliseconds
        now = pygame.time.get_ticks()
        if animating and generator and now - last_step >= anim_delay:
            try:
                heap[:], active, compare = next(generator)
                last_step = now
            except StopIteration:
                animating = False
                active = -1
                compare = -1
                status = "Heap Sorted!"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif input_active:
                    if event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                        status = ""
                    elif event.unicode.isdigit() and len(input_text) < 4:
                        input_text += event.unicode
                    elif len(input_text) >= 4:
                        status = "Max 4 digits allowed"

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if input_box.collidepoint(pos):
                    input_active = True
                elif back_btn.collidepoint(pos):
                    return
                elif insert_btn.collidepoint(pos) and input_text and not animating:
                    generator = insert(heap, int(input_text))
                    animating = True
                    active = -1
                    compare = -1
                    input_text = ""
                    status = ""
                elif extract_btn.collidepoint(pos) and heap and not animating:
                    generator = extract(heap)
                    animating = True
                    active = -1
                    compare = -1
                    status = "Extracting & Updating..."
                elif reset_btn.collidepoint(pos):
                    heap.clear()
                    input_text = ""
                    status = ""
                else:
                    input_active = False

        screen.fill(LightBlue)
        draw_heap(heap, active, compare)

        # Back button — returns to main menu
        pygame.draw.rect(screen, Red, back_btn)
        draw_text("Main Menu", (back_btn.x + 9, back_btn.y + 8), BOLD_FONT, Black)

        # Insert and Extract buttons
        for btn, label in [(insert_btn, "Insert"), (extract_btn, "Extract")]:
            pygame.draw.rect(screen, MutedBlue, btn)
            draw_text(label, (btn.x + 20, btn.y + 8), BOLD_FONT, Black)

        # Reset button — clears the heap
        pygame.draw.rect(screen, Green, reset_btn)
        draw_text("Reset", (reset_btn.x + 25, reset_btn.y + 8), BOLD_FONT, Black)

        # Input box — white when active, off-white when inactive
        pygame.draw.rect(screen, White if input_active else OffWhite, input_box)
        pygame.draw.rect(screen, Black, input_box, 2)
        if not input_text and not input_active:
            draw_text("Enter number", (input_box.x + 5, input_box.y + 12), SMALL_FONT, MutedBlue)
        else:
            draw_text(input_text, (input_box.x + 30, input_box.y + 12), SMALL_FONT, Black)

        # Blinking cursor drawn after typed text
        if input_active and cursor_visible:
            text_width = SMALL_FONT.size(input_text)[0]
            cursor_x = input_box.x + 30 + text_width
            cursor_y = input_box.y + 10
            pygame.draw.line(screen, Black, (cursor_x, cursor_y), (cursor_x, cursor_y + 28), 2)
        else:
            pass

        # Status text — shows current operation or messages
        draw_text(status, (290, 65), SMALL_FONT, Black)
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()