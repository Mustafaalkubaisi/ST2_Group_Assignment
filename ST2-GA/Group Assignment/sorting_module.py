import pygame
import sys


pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.SysFont(None, 36)
SMALL_FONT = pygame.font.SysFont(None, 28)
clock = pygame.time.Clock()

BAR_AREA = pygame.Rect(50, 150, 700, 380)


# Colours for ease of implementation
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


# Shows text on the screen at a set position
def draw_text(text, pos, font=None, colour=Black):
    if font is None:
        font = FONT
    txt = font.render(text, True, colour)
    screen.blit(txt, pos)

# Draws the list as a bar chart — orange by default, red when comparing, green when sorted
def draw_bars(numbers, highlight=None, green_up_to=-1):
    pygame.draw.rect(screen, OffWhite, BAR_AREA)
    if not numbers:
        return
    max_val = max(abs(n) for n in numbers) or 1
    bar_width = BAR_AREA.width // len(numbers)

    for i, val in enumerate(numbers):
        bar_height = int((abs(val) / max_val) * (BAR_AREA.height - 30))
        x = BAR_AREA.x + i * bar_width
        y = BAR_AREA.bottom - bar_height
        if i <= green_up_to:
            colour = LimeGreen
        elif highlight and i in highlight:
            colour = Crimson
        else:
            colour = Orange
        pygame.draw.rect(screen, colour, (x + 2, y, bar_width - 4, bar_height))
        if bar_width > 30:
            draw_text(str(val), (x + 4, BAR_AREA.bottom + 5), SMALL_FONT)


# Draws the full screen each frame — background, buttons, bars and status text
def draw_screen(numbers, highlight, status, green_up_to,
                back_btn, bubble_btn, select_btn, merge_btn, reset_btn):

    screen.fill(LightBlue)

    # Back button — returns to main menu
    pygame.draw.rect(screen, Red, back_btn)
    draw_text("Main Menu", (back_btn.x + 10, back_btn.y + 8), SMALL_FONT)

    # Sort buttons — each triggers a different sorting algorithm
    for btn, label in [(bubble_btn, "Bubble"), (select_btn, "Selection"), (merge_btn, "Merge")]:
        pygame.draw.rect(screen, MutedBlue, btn)
        draw_text(label, (btn.x + 30, btn.y + 10), SMALL_FONT)

    # Reset button — restores the original unsorted list
    pygame.draw.rect(screen, Green, reset_btn)
    draw_text("Reset", (reset_btn.x + 28, reset_btn.y + 10), SMALL_FONT, Black)

    # Status text showing current sort or instructions
    draw_bars(numbers, highlight, green_up_to)
    draw_text(status, (50, 560), SMALL_FONT, Black)
    pygame.display.flip()


# --- Sorting algorithms ---

# Bubble Sort - repeatedly compares adjacent pairs and swaps if out of order
def bubble_sort(arr):
    arr = arr[:]
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            yield arr[:], {j, j + 1}, -1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                yield arr[:], {j, j + 1}, -1
    # Completion sweep — turns bars green left to right to confirm sorted order
    for i in range(len(arr)):
        yield arr[:], set(), i
    yield arr[:], set(), len(arr) - 1

# Selection Sort — finds the minimum element each pass and places it in position
def selection_sort(arr):
    arr = arr[:]
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            yield arr[:], {j, min_idx}, -1
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            yield arr[:], {i, min_idx}, -1
    # Completion sweep
    for i in range(len(arr)):
        yield arr[:], set(), i
    yield arr[:], set(), len(arr) - 1

# Merge Sort — divides list in half recursively then merges halves back in sorted order
def merge_sort_gen(arr):
    arr = arr[:]
    steps = []

    def merge_sort(a, start):
        if len(a) <= 1:
            return a
        mid = len(a) // 2
        left  = merge_sort(a[:mid], start)
        right = merge_sort(a[mid:], start + mid)
        merged = []
        l, r = 0, 0
        while l < len(left) and r < len(right):
            li, ri = start + l, start + mid + r
            steps.append((arr[:], {li, ri}, -1))
            if left[l] <= right[r]:
                merged.append(left[l]); l += 1
            else:
                merged.append(right[r]); r += 1
        merged.extend(left[l:])
        merged.extend(right[r:])
        for k, val in enumerate(merged):
            arr[start + k] = val
        steps.append((arr[:], set(range(start, start + len(merged))), -1))
        return merged

    merge_sort(arr, 0)
    for step in steps:
        yield step
    # Completion sweep
    for i in range(len(arr)):
        yield arr[:], set(), i
    yield arr[:], set(), len(arr) - 1

# Main Loop
def main():
    original = [5, 3, 8, 1, 2]
    numbers = original[:]
    status = "Choose a sort to animate"
    highlight = set()
    green_up_to = -1
    generator = None
    animating = False
    anim_delay = 125  # Milliseconds between animation steps

    # Button positions along the top of the screen
    back_btn = pygame.Rect(20, 10, 130, 38)
    bubble_btn = pygame.Rect(180, 10, 130, 38)
    select_btn = pygame.Rect(330, 10, 150, 38)
    merge_btn = pygame.Rect(500, 10, 130, 38)
    reset_btn = pygame.Rect(660, 10, 110, 38)

    last_step = pygame.time.get_ticks()

    running = True
    while running:
        now = pygame.time.get_ticks()

        # plays the animation with a set delay for ease of viewing
        if animating and generator and now - last_step >= anim_delay:
            try:
                numbers, highlight, green_up_to = next(generator)
                last_step = now
            except StopIteration:
                animating = False
                highlight = set()
                green_up_to = len(numbers) - 1  # All bars turn green when done
                status = "Done!"

        draw_screen(numbers, highlight, status, green_up_to,
                    back_btn, bubble_btn, select_btn, merge_btn, reset_btn)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if back_btn.collidepoint(pos):
                    return
                elif bubble_btn.collidepoint(pos) and not animating:
                    numbers = original[:]
                    green_up_to = -1
                    generator = bubble_sort(numbers)
                    animating = True
                    status = "Bubble Sort"
                elif select_btn.collidepoint(pos) and not animating:
                    numbers = original[:]
                    green_up_to = -1
                    generator = selection_sort(numbers)
                    animating = True
                    status = "Selection Sort"
                elif merge_btn.collidepoint(pos) and not animating:
                    numbers = original[:]
                    green_up_to = -1
                    generator = merge_sort_gen(numbers)
                    animating = True
                    status = "Merge Sort"
                elif reset_btn.collidepoint(pos):
                    numbers = original[:]
                    generator = None
                    animating = False
                    highlight = set()
                    green_up_to = -1
                    status = "Choose a sort to animate"

        clock.tick(60)


if __name__ == "__main__":
    main()