import pygame
import sys


pygame.init()
WIDTH, HEIGHT = 900, 600
FONT = pygame.font.SysFont(None, 36)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Adjacency list — defines which nodes connect to which
graph = {
    'A': ['B','C'],
    'B': ['A','D','E'],
    'C': ['A','E'],
    'D': ['B'],
    'E': ['C','B']
}

# Screen positions for each node
nodes = {
    'A': (200, 300),
    'B': (400, 150),
    'C': (300, 450),
    'D': (600, 200),
    'E': (600, 400)
}

# Colours for ease of implementation
SteelBlue = (50, 150, 200)
radius = 25
White = (255, 255, 255)
Red = (255, 100, 100)
Green = (100, 255, 100)
Black = (0, 0, 0)
Yellow = (225, 225, 0)
LightBlue = (200, 200, 250)
MutedBlue = (150, 150, 200)
Orange = (255, 163, 0)


# Draws all edges between connected nodes
def draw_graph():
    selected_node = None
    for node, neighbours in graph.items():
        for neighbour in neighbours:
            start_pos = nodes[node]
            end_pos = nodes[neighbour]
            pygame.draw.line(screen, SteelBlue, start_pos, end_pos, 2)


# Draws each node as a circle — colour indicates its state
# White = unvisited, Yellow = selected, Red = current, Green = visited
def draw_node(visited=[], current=None, selected_node=None):
    for node, pos in nodes.items():
        if node == selected_node:
            colour = Yellow
        elif node == current:
            colour = Red
        elif node in visited:
            colour = Green
        else:
            colour = White
        pygame.draw.circle(screen, colour, pos, radius)
        draw_text(node, (pos[0] - 9, pos[1] - 11))


# Shows text on the screen at the set position
def draw_text(text, pos, font=None, colour=Black):
    if font is None:
        font = FONT
    txt = font.render(text, True, colour)
    screen.blit(txt, pos)


# Highlights the traversal path from the start node to the current node
def draw_path(current, parent):
    node = current
    while node and parent.get(node):
        start = nodes[parent[node]]
        end = nodes[node]
        pygame.draw.line(screen, Orange, start, end, 4)
        node = parent[node]


# BFS — explores nodes level by level using a queue (first in, first out)
def bfs(start):
    queue = [start]
    visited = []
    parent = {start: None}
    while queue:
        node = queue.pop(0)
        visited.append(node)
        yield visited[:], node, parent
        for neighbour in graph[node]:
            if neighbour not in visited and neighbour not in parent:
                queue.append(neighbour)
                parent[neighbour] = node
    yield visited[:], None, parent


# DFS — explores as far as possible along each branch using a stack (last in, first out)
def dfs(start):
    stack = [start]
    visited = []
    parent = {start: None}
    while stack:
        node = stack.pop()
        visited.append(node)
        yield visited[:], node, parent
        for neighbour in graph[node]:
            if neighbour not in visited and neighbour not in parent:
                stack.append(neighbour)
                parent[neighbour] = node
    yield visited[:], None, parent


# Main Loop
def main():
    generator = None
    animating = False
    anim_delay = 500          # Milliseconds between each traversal step
    last_step = pygame.time.get_ticks()
    visited = []
    current = None
    running = True

   # Programs state: idle, selecting, searching
    mode = 'idle'
    algorithm = None
    selected_node = None
    parent = {}
    status = ""

    # Buttons along the top of the screen
    back_btn    = pygame.Rect(20,  20, 150, 38)
    bfs_btn     = pygame.Rect(190, 20, 150, 38)
    dfs_btn     = pygame.Rect(360, 20, 150, 38)
    reset_btn   = pygame.Rect(530, 20, 150, 38)

    # Confirm and cancel buttons shown during node selection
    confirm_btn = pygame.Rect(300, 550, 150, 38)
    cancel_btn  = pygame.Rect(500, 550, 150, 38)

    while running:
        now = pygame.time.get_ticks()

        # plays the traversal with a set delay for ease of viewing
        if animating and generator and now - last_step >= anim_delay:
            try:
                visited, current, parent = next(generator)
                last_step = now
            except StopIteration:
                animating = False
                current = None
                status = "complete"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if bfs_btn.collidepoint(event.pos) and mode == 'idle':
                    mode = 'selecting'
                    algorithm = 'bfs'
                    status = ""
                elif dfs_btn.collidepoint(event.pos) and mode == 'idle':
                    mode = 'selecting'
                    algorithm = 'dfs'
                    status = ""
                elif back_btn.collidepoint(event.pos):
                    return
                elif reset_btn.collidepoint(event.pos):
                    generator = None
                    animating = False
                    visited = []
                    current = None
                    mode = 'idle'
                    algorithm = None
                    selected_node = None
                    status = "reset"
                elif confirm_btn.collidepoint(event.pos) and mode == 'selecting' and selected_node:
                    generator = bfs(selected_node) if algorithm == 'bfs' else dfs(selected_node)
                    animating = True
                    visited = []
                    current = None
                    mode = 'searching'
                elif cancel_btn.collidepoint(event.pos) and mode == 'selecting':
                    mode = 'idle'
                    selected_node = None
                    algorithm = None
                elif mode == 'selecting':
                    # Check if click landed on a node
                    for node, pos in nodes.items():
                        dx = event.pos[0] - pos[0]
                        dy = event.pos[1] - pos[1]
                        if (dx*dx + dy*dy) ** 0.5 < radius:
                            selected_node = node

        screen.fill(LightBlue)

        # Back button — returns to main menu
        pygame.draw.rect(screen, Red, back_btn)
        draw_text("Main Menu", (back_btn.x + 10, back_btn.y + 8))

        # Show confirm/cancel and instructions during node selection
        if mode == 'selecting':
            pygame.draw.rect(screen, Green, confirm_btn)
            draw_text("Confirm", (confirm_btn.x + 10, confirm_btn.y + 8))
            pygame.draw.rect(screen, Green, cancel_btn)
            draw_text("Cancel", (cancel_btn.x + 10, cancel_btn.y + 8))
            draw_text(f" - Click a starting node for {algorithm}: ", (20, 90))
            if selected_node:
                draw_text(f" - {selected_node} selected", (20, 130))

        # BFS and DFS buttons
        for btn, label in [(bfs_btn, "BFS Search"), (dfs_btn, "DFS Search")]:
            pygame.draw.rect(screen, MutedBlue, btn)
            draw_text(label, (btn.x + 8, btn.y + 8))

        # Reset button — clears traversal and returns to idle
        pygame.draw.rect(screen, Green, reset_btn)
        draw_text("Reset", (reset_btn.x + 40, reset_btn.y + 8))

        # Status of the program
        if status == "reset":
            draw_text("Graph Reset", (20, 130))
        elif status == "complete":
            draw_text("Algorithm Complete", (20, 130))

        draw_graph()
        draw_path(current, parent)
        draw_node(visited, current, selected_node)
        pygame.display.flip()

    clock.tick(60)


if __name__ == "__main__":
    main()