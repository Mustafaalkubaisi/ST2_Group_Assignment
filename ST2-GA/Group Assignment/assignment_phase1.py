import pygame
import sys
import MainMenu
from modules.stack import Stack
from modules.linked_list import DoublyLinkedList
from modules.binary_tree import BST

WIDTH, HEIGHT = 800, 600

# Variables for Stack and Queue blocks
BLOCK_WIDTH, BLOCK_HEIGHT = 200, 40
START_X = (WIDTH - BLOCK_WIDTH) // 2
BASE_Y = HEIGHT - BLOCK_HEIGHT - 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.font.init()
FONT = pygame.font.SysFont(None, 36)


# This function runs the stack visualiser
def stack_visualization(screen, font):
    stack = Stack()

    # Count how many blocks are currently in the stack
    counter = 1

    running = True

    # Error message setup
    warning = pygame.Rect(10, 100, 300, 30)
    warning_text = ""

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()

                # Quit button
                if 220 <= mouse[0] <= 320 and 10 <= mouse[1] <= 60:
                    running = False

                # Push button
                elif 330 <= mouse[0] <= 430 and 10 <= mouse[1] <= 60:
                    warning_text = ''
                    stack.push(counter)
                    counter += 1

                # Pop button
                elif 440 <= mouse[0] <= 540 and 10 <= mouse[1] <= 60:
                    if stack.is_empty():
                        warning_text = 'Cannot pop from empty stack'
                    else:
                        warning_text = ''
                        stack.pop()

            # ESC key returns to menu
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run(screen)

        screen.fill((200, 200, 250))

        # Draw numbered blocks
        for i, val in enumerate(stack._data):
            rect = pygame.Rect(START_X, BASE_Y - i * (BLOCK_HEIGHT + 5), BLOCK_WIDTH, BLOCK_HEIGHT)
            pygame.draw.rect(screen, (100, 150, 250), rect)
            text = font.render(str(val), True, (0, 0, 0))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

        # Title text
        title_text = font.render("Stack visualiser", True, 0)
        screen.blit(title_text, (20, 20))

        # Error message box
        pygame.draw.rect(screen, (200, 200, 250), warning)
        warning_box = font.render(warning_text, True, "red")
        screen.blit(warning_box, warning)

        # Quit button
        buttonQuit = pygame.Rect(220, 10, 100, 50)
        quit_text = font.render("QUIT", True, (0))
        quit_location = quit_text.get_rect(center=buttonQuit.center)
        pygame.draw.rect(screen, (200, 200, 200), buttonQuit)
        screen.blit(quit_text, quit_location)

        # Push button
        buttonPush = pygame.Rect(330, 10, 100, 50)
        push_text = font.render("PUSH", True, (0))
        push_location = quit_text.get_rect(center=buttonPush.center)
        pygame.draw.rect(screen, (200, 200, 200), buttonPush)
        screen.blit(push_text, push_location)

        # Pop button
        buttonPop = pygame.Rect(440, 10, 100, 50)
        pop_text = font.render("POP", True, (0))
        pop_location = quit_text.get_rect(center=buttonPop.center)
        pygame.draw.rect(screen, (200, 200, 200), buttonPop)
        screen.blit(pop_text, pop_location)

        pygame.display.flip()


# This function runs the Queue visualiser
def queue_visualization(screen, font):
    stack = Stack()

    # Count how many blocks are currently in the queue
    counter = 1

    running = True

    # Error message setup
    warning = pygame.Rect(10, 100, 300, 30)
    warning_text = ""

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()

                # Quit button
                if 220 <= mouse[0] <= 320 and 10 <= mouse[1] <= 60:
                    running = False

                # Enqueue button
                elif 330 <= mouse[0] <= 430 and 10 <= mouse[1] <= 60:
                    warning_text = ''
                    # Push / Enqueue are the same function
                    stack.push(counter)
                    counter += 1

                # Dequeue button
                elif 440 <= mouse[0] <= 540 and 10 <= mouse[1] <= 60:
                    if stack.is_empty():
                        warning_text = 'Cannot dequeue from empty queue'
                    else:
                        warning_text = ''
                        stack.dequeue()

            elif event.type == pygame.KEYDOWN:
                # Return to menu
                if event.key == pygame.K_ESCAPE:
                    run(screen)

        screen.fill((200, 200, 250))

        # Draw numbered blocks
        for i, val in enumerate(stack._data):
            rect = pygame.Rect(START_X, BASE_Y - i * (BLOCK_HEIGHT + 5), BLOCK_WIDTH, BLOCK_HEIGHT)
            pygame.draw.rect(screen, (100, 150, 250), rect)
            text = font.render(str(val), True, (0, 0, 0))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

        # Title text
        title_text = font.render("Queue visualiser", True, 0)
        screen.blit(title_text, (20, 20))

        # Error message
        pygame.draw.rect(screen, (200, 200, 250), warning)
        warning_box = font.render(warning_text, True, "red")
        screen.blit(warning_box, warning)

        # Quit button
        buttonQuit = pygame.Rect(220, 10, 100, 50)
        quit_text = font.render("QUIT", True, (0))
        quit_location = quit_text.get_rect(center=buttonQuit.center)
        pygame.draw.rect(screen, (200, 200, 200), buttonQuit)
        screen.blit(quit_text, quit_location)

        #  Enqueue button
        buttonEnqueue = pygame.Rect(330, 10, 100, 50)
        enqueue_text = font.render("ENQUEUE", True, (0))
        enqueue_location = enqueue_text.get_rect(center=buttonEnqueue.center)
        pygame.draw.rect(screen, (200, 200, 200), buttonEnqueue)
        screen.blit(enqueue_text, enqueue_location)

        # Dequeue button
        buttonDequeue = pygame.Rect(440, 10, 100, 50)
        dequeue_text = font.render("DEQUEUE", True, (0))
        dequeue_location = dequeue_text.get_rect(center=buttonDequeue.center)
        pygame.draw.rect(screen, (200, 200, 200), buttonDequeue)
        screen.blit(dequeue_text, dequeue_location)

        pygame.display.flip()


# This function runs the Linked List visualiser
def linkedList(screen, font):
    # Snippets of code taken from https://stackoverflow.com/questions/46390231/how-can-i-create-a-text-input-box-with-pygame
    linked = DoublyLinkedList()

    # Box for user input
    input_box = pygame.Rect(340, 10, 200, 30)
    active = False

    # Error message setup
    warning = pygame.Rect(10, 100, 300, 30)
    warning_text = ""

    running = True

    # Output text variables
    text = 'Type here'
    visual_text = ""

    while running:
        # text and warning_text appear frequently to clear the message when not needed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Collider for user input box
                if input_box.collidepoint(event.pos):
                    text = ""
                    active = not active
                else:
                    active = False

                mouse = pygame.mouse.get_pos()

                # Quit button
                if 220 <= mouse[0] <= 320 and 10 <= mouse[1] <= 60:
                    running = False

                # Insert button
                elif 550 <= mouse[0] <= 650 and 10 <= mouse[1] <= 60:
                    # Error message
                    if text == '' or text == 'Type here':
                        warning_text = "Please enter data"

                    # Run as normal
                    else:
                        warning_text = ''
                        linked.insert_at_head(text)
                        visual_text = linked.traverse_forward()
                        text = ''

                # Delete button
                elif 550 <= mouse[0] <= 650 and 70 <= mouse[1] <= 120:
                    if linked.find(text):
                        warning_text = ''
                        linked.delete(text)
                        visual_text = linked.traverse_forward()
                        text = ''

                    # Error message
                    elif text == "":
                        warning_text = "Please enter data"
                    else:
                        warning_text = "Node does not exist"

                # Reverse button
                elif 660 <= mouse[0] <= 760 and 40 <= mouse[1] <= 90:
                    warning_text = ''
                    visual_text = linked.traverse_backward()[:-4]

            elif event.type == pygame.KEYDOWN:
                # Return to menu
                if event.key == pygame.K_ESCAPE:
                    run(screen)
                elif active:
                    # This section is for text input
                    if event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode


        screen.fill((200, 200, 250))

        # User input box
        pygame.draw.rect(screen, (200, 200, 200), input_box)
        txt_surface = font.render(text, True, 0)
        input_location = txt_surface.get_rect(center=input_box.center)
        screen.blit(txt_surface, input_location)

        # Error message
        pygame.draw.rect(screen, (200, 200, 250), warning)
        warning_box = font.render(warning_text, True, "red")
        screen.blit(warning_box, warning)

        # Title
        title_text = font.render("Linked list visualiser", True, 0)
        screen.blit(title_text, (20, 20))

        # Quit button
        buttonQuit = pygame.Rect(230, 10, 100, 50)
        quit_text = font.render("QUIT", True, (0))
        quit_location = quit_text.get_rect(center=buttonQuit.center)
        pygame.draw.rect(screen, (200, 200, 200), buttonQuit)
        screen.blit(quit_text, quit_location)

        # Insert button
        buttonInsert = pygame.Rect(550, 10, 100, 50)
        insert_text = font.render("INSERT", True, (0))
        insert_location = insert_text.get_rect(center=buttonInsert.center)
        pygame.draw.rect(screen, (200, 200, 200), buttonInsert)
        screen.blit(insert_text, insert_location)

        # Delete button
        buttonDelete = pygame.Rect(550, 70, 100, 50)
        delete_text = font.render("DELETE", True, (0))
        delete_location = delete_text.get_rect(center=buttonDelete.center)
        pygame.draw.rect(screen, (200, 200, 200), buttonDelete)
        screen.blit(delete_text, delete_location)

        # Reverse button
        buttonReverse = pygame.Rect(660, 40, 100, 50)
        reverse_text = font.render("REVERSE", True, (0))
        reverse_location = reverse_text.get_rect(center=buttonReverse.center)
        pygame.draw.rect(screen, (200, 200, 200), buttonReverse)
        screen.blit(reverse_text, reverse_location)

        # Output box
        linkedOutput = pygame.Rect(100, 150, 600, 350)
        pygame.draw.rect(screen, (200, 200, 250), linkedOutput)
        font = pygame.font.SysFont(None, 40)
        drawText(screen, visual_text, 0, linkedOutput, font)
        font = pygame.font.SysFont(None, 28)

        pygame.display.flip()


# This function runs the binary search tree visualiser
def binary_visualization(screen, font):
    # Snippets of code taken from https://stackoverflow.com/questions/46390231/how-can-i-create-a-text-input-box-with-pygame
    binary = BST()

    # User input box
    input_box = pygame.Rect(340, 10, 200, 30)
    active = False

    # Traversal setup
    traversal = pygame.Rect(25,520,750,30)
    traversal_text = 'Traversal order: '

    # Error message setup
    warning = pygame.Rect(10, 125, 200, 25)
    warning_text = ""

    running = True

    # Output text variables
    text = 'Type here'
    tree_text = ''

    while running:
        # text and warning_text appear frequently to clear the message when not needed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Collider for user input box
                if input_box.collidepoint(event.pos):
                    text = ""
                    active = not active
                else:
                    active = False

                mouse = pygame.mouse.get_pos()

                # Quit button
                if 220 <= mouse[0] <= 320 and 10 <= mouse[1] <= 60:
                    running = False

                # Insert Button
                elif 570 <= mouse[0] <= 670 and 10 <= mouse[1] <= 60:
                    traversal_text = 'Traversal order: '

                    # Error message
                    if text == '' or text == 'Type here':
                        warning_text = "Please enter data"
                        tree_text = binary.display_tree()
                    # Run as normal
                    else:
                        warning_text = ''
                        binary.insert(text)
                        tree_text = binary.display_tree()
                        text = ''

                # Delete button
                elif 570 <= mouse[0] <= 670 and 70 <= mouse[1] <= 120:
                    traversal_text = 'Traversal order: '

                    if binary.search(text):
                        warning_text = ''
                        binary.delete(text)
                        tree_text = binary.display_tree()
                        text = ''

                    # Error message
                    elif text == "":
                        warning_text = "Please enter data"
                        tree_text = binary.display_tree()
                    else:
                        warning_text = "Node does not exist"
                        tree_text = binary.display_tree()

                # Inorder button
                elif 230 <= mouse[0] <= 330 and 70 <= mouse[1] <= 120:
                    traversal_text = 'Traversal order: '

                    # Error message
                    if binary.inorder() == '':
                        warning_text = 'Cannot traverse an empty tree'

                    # Run as normal
                    else:
                        warning_text = ''
                        traversal_text = 'Inorder traversal: ' + binary.inorder()

                # Preorder button
                elif 340 <= mouse[0] <= 440 and 70 <= mouse[1] <= 120:
                    traversal_text = 'Traversal order: '

                    # Error message
                    if binary.preorder() == '':
                        warning_text = 'Cannot traverse an empty tree'

                    # Run as normal
                    else:
                        warning_text = ''
                        traversal_text = 'Preorder traversal: ' + binary.preorder()

                # Postorder button
                elif 450 <= mouse[0] <= 550 and 70 <= mouse[1] <= 120:
                    traversal_text = 'Traversal order: '

                    # Error message
                    if binary.postorder() == '':
                        warning_text = 'Cannot traverse an empty tree'

                    # Run as normal
                    else:
                        warning_text = ''
                        traversal_text = 'Postorder traversal: ' + binary.postorder()

            elif event.type == pygame.KEYDOWN:
                # Return to menu
                if event.key == pygame.K_ESCAPE:
                    run(screen)
                elif active:
                    # This section is for text input
                    if event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode


        screen.fill((200, 200, 250))

        # Section input into multiple lines for print
        tree_sections = tree_text.split("\n")
        textY = 150
        # Print output
        for i in tree_sections:
            treeText = font.render(i, True, (0))
            screen.blit(treeText, (245, textY))
            textY += 25

        # User input box
        pygame.draw.rect(screen, (200, 200, 200), input_box)
        txt_surface = font.render(text, True, 0)
        input_location = txt_surface.get_rect(center=input_box.center)
        screen.blit(txt_surface, input_location)

        # Error message
        pygame.draw.rect(screen, (200, 200, 250), warning)
        warning_box = font.render(warning_text, True, "red")
        screen.blit(warning_box, warning)

        # Traversal box
        pygame.draw.rect(screen, (200, 200, 250), traversal)
        traversal_box = font.render(traversal_text, True, 0)
        screen.blit(traversal_box, traversal)

        # Title
        title_text = font.render("Linked list visualiser", True, 0)
        screen.blit(title_text, (20, 20))

        # Quit button
        buttonQuit = pygame.Rect(230, 10, 100, 50)
        quit_text = font.render("QUIT", True, (0))
        quit_location = quit_text.get_rect(center=buttonQuit.center)
        pygame.draw.rect(screen, (200, 200, 200), buttonQuit)
        screen.blit(quit_text, quit_location)

        # Insert button
        buttonInsert = pygame.Rect(570, 10, 100, 50)
        insert_text = font.render("INSERT", True, (0))
        insert_location = insert_text.get_rect(center=buttonInsert.center)
        pygame.draw.rect(screen, (200, 200, 200), buttonInsert)
        screen.blit(insert_text, insert_location)

        # Delete button
        buttonDelete = pygame.Rect(570, 70, 100, 50)
        delete_text = font.render("DELETE", True, (0))
        delete_location = delete_text.get_rect(center=buttonDelete.center)
        pygame.draw.rect(screen, (200, 200, 200), buttonDelete)
        screen.blit(delete_text, delete_location)


        # Set a different font size for the next buttons
        font = pygame.font.SysFont(None, 22)

        # Inorder button
        buttonInorder = pygame.Rect(230, 70, 100, 50)
        inorder_text = font.render("INORDER", True, 0)
        inorder_location = inorder_text.get_rect(center=buttonInorder.center)
        pygame.draw.rect(screen, (200, 200, 200), buttonInorder)
        screen.blit(inorder_text, inorder_location)

        # Preorder button
        buttonPreorder = pygame.Rect(340, 70, 100, 50)
        preorder_text = font.render("PREORDER", True, 0)
        preorder_location = preorder_text.get_rect(center=buttonPreorder.center)
        pygame.draw.rect(screen, (200, 200, 200), buttonPreorder)
        screen.blit(preorder_text, preorder_location)

        # Postorder button
        buttonPostorder = pygame.Rect(450, 70, 100, 50)
        postorder_text = font.render("POSTORDER", True, 0)
        postorder_location = postorder_text.get_rect(center=buttonPostorder.center)
        pygame.draw.rect(screen, (200, 200, 200), buttonPostorder)
        screen.blit(postorder_text, postorder_location)

        # Return font to normal
        font = pygame.font.SysFont(None, 28)

        pygame.display.flip()


# Text wrap function
# Code taken from: https://www.pygame.org/wiki/TextWrap
def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = -2

    # Get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # Determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # Determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # If we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1

        # Render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + (lineSpacing + 10)

        # Remove the text we just blitted
        text = text[i:]

    return text


# Text elements from Main Menu
def draw_text(text, pos):
    txt = FONT.render(text, True, (0, 0, 0))
    screen.blit(txt, pos)


# Menu screen
def run(screen):
    font = pygame.font.SysFont(None, 28)
    running = True
    current_module = None

    while running:
        screen.fill((200, 200, 250))

        # Title
        draw_text("Data Structures Explorer", (WIDTH // 3, 50))

        # Available options
        buttons = {
            'Stack Visualisation': pygame.Rect(270, 150, 330, 50),
            'Queue Visualisation': pygame.Rect(270, 230, 330, 50),
            'Linked List Visualisation': pygame.Rect(270, 310, 330, 50),
            'BST Visualisation': pygame.Rect(270, 390, 330, 50),
            'Back': pygame.Rect(270, 470, 100, 50)
        }

        # Draw buttons
        for text, rect in buttons.items():
            pygame.draw.rect(screen, (150, 150, 200), rect)
            draw_text(text, (rect.x + 20, rect.y + 10))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    MainMenu.main()

            elif event.type == pygame.MOUSEBUTTONDOWN and current_module is None:
                # Collider for buttons
                for name, rect in buttons.items():
                    if rect.collidepoint(event.pos):
                        current_module = name
                        break

                # Run modules based on button pressed
                if current_module:
                    if current_module == 'Stack Visualisation':
                        stack_visualization(screen, font)

                    elif current_module == 'Queue Visualisation':
                        queue_visualization(screen, font)

                    elif current_module == 'Linked List Visualisation':
                        linkedList(screen, font)

                    elif current_module == 'BST Visualisation':
                        binary_visualization(screen, font)

                    elif current_module == 'Back':
                        MainMenu.main()

                    current_module = None

    pygame.quit()