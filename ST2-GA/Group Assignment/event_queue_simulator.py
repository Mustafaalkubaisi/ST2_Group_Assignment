import pygame
import sys
import math



pygame.init()

WIDTH = 800
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Event Queue Simulator")

FONT = pygame.font.SysFont(None, 30)
clock = pygame.time.Clock()

event_queue = []

event_counter = 1
processed_event = "No event processed yet"

# Draws the heap as a binary tree and highlights nodes
def draw_heap(highlight_indices):
    if not event_queue:
        empty_text = FONT.render("Heap is empty", True, (0, 0, 0))
        screen.blit(empty_text, (320, 300))
        return

    node_positions = []

    for i in range(len(event_queue)):
        level = int(math.floor(math.log2(i + 1)))
        index_in_level = i - (2 ** level - 1)
        gap = WIDTH // (2 ** level + 1)

        x = gap * (index_in_level + 1)
        y = 230 + level * 80

        node_positions.append((x, y))

    for i in range(len(event_queue)):
        left = 2 * i + 1
        right = 2 * i + 2

        if left < len(event_queue):
            pygame.draw.line(screen, (0, 0, 0), node_positions[i], node_positions[left], 2)

        if right < len(event_queue):
            pygame.draw.line(screen, (0, 0, 0), node_positions[i], node_positions[right], 2)

    for i, event in enumerate(event_queue):
        event_time, description = event

        color = (100, 200, 250)

        if i in highlight_indices:
            color = (255, 100, 100)

        pygame.draw.circle(screen, color, node_positions[i], 28)

        text = FONT.render(str(event_time), True, (0, 0, 0))
        text_rect = text.get_rect(center=node_positions[i])
        screen.blit(text, text_rect)

# Draws the screen including instructions and visualisation
def draw_screen(highlight_indices=[]):
    screen.fill((255, 255, 255))

    title = FONT.render("Event Queue Simulator", True, (0, 0, 0))
    screen.blit(title, (260, 40))

    instructions = FONT.render("A: Add Event | S: Process Event | C:Clear | ESC: Back", True, (0, 0, 0))
    screen.blit(instructions, (180, 90))

    draw_heap(highlight_indices)


    processed_text = FONT.render(f"Processed: {processed_event}", True, (0, 0, 0))
    screen.blit(processed_text, (40, 660))

    pygame.display.flip()

# Restores order after a new event
def heapify_up(heap, index):

    while index > 0:

        parent = (index - 1) // 2

        if heap[parent][0] > heap[index][0]:

            heap[parent], heap[index] = heap[index], heap[parent]
            draw_screen([parent,index])
            pygame.time.wait(400)

            index = parent

        else:
            break


# Restores order after root event
def heapify_down(heap, index):

    n = len(heap)

    while True:

        left = 2 * index + 1
        right = 2 * index + 2

        smallest = index

        if left < n and heap[left][0] < heap[smallest][0]:
            smallest = left

        if right < n and heap[right][0] < heap[smallest][0]:
            smallest = right

        if smallest != index:

            heap[index], heap[smallest] = heap[smallest], heap[index]
            draw_screen([index,smallest])
            pygame.time.wait(400)

            index = smallest

        else:
            break

# Adds an event to the priority queue
def add_event():

    global event_counter

    event_time = event_counter
    description = f"Event {event_counter}"

    event_queue.append((event_time, description))
    draw_screen([len(event_queue) - 1])
    pygame.time.wait(300)

    heapify_up(event_queue, len(event_queue) - 1)

    event_counter += 1

# Removes the highest priority event
def process_event():

    global processed_event

    if len(event_queue) == 0:
        processed_event = "Queue is empty"
        return

    root = event_queue[0]

    event_queue[0] = event_queue[-1]

    event_queue.pop()

    if len(event_queue) > 0:
        heapify_down(event_queue, 0)

    processed_event = f"Time {root[0]}: {root[1]}"

# Resets the event queue
def clear_events():
    global event_queue, event_counter, processed_event

    event_queue = []
    event_counter = 1
    processed_event = "No event processed yet"


# Main loop
def main():
    running = True

    while running:
        draw_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_a:
                    add_event()

                elif event.key == pygame.K_s:
                    process_event()

                elif event.key == pygame.K_c:
                    clear_events()

        clock.tick(30)


if __name__ == "__main__":
    main()