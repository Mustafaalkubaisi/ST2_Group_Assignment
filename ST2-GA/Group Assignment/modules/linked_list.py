class Node:
    """One datum in a Doubly Linked List"""
    def __init__(self, data, next=None, previous=None):
        self.__data = data
        self.__next = next
        self.__previous = previous

    # Represent Node as string
    def __repr__(self):
        return str(self.getData())

    # Get data assigned to Node
    def getData(self):
        return self.__data

    # Assign data to Node
    def setData(self, data):
        self.__data = data

    # Get next Node
    def getNext(self):
        return self.__next

    # Set next Node
    def setNext(self, node):
        if node is None or isinstance(node, Node):
            self.__next = node # Enforce type
        else:
            raise Exception("Next link must be a Node or None")

    # Get previous Node
    def getPrevious(self):
        return self.__previous

    # Set previous Node
    def setPrevious(self, node):
        if node is None or isinstance(node, Node):
            self.__previous = node # Enforce type
        else:
            raise Exception("Previous link must be a Node or None")

class DoublyLinkedList:
    """Implements a doubly linked list."""
    def __init__(self):
        self.head = None
        self.tail = None

    def insert_at_head(self, data):
        """Inserts a new node at the beginning of the DLL."""
        new_node = Node(data)
        if self.head is None: # If list is empty
            self.head = self.tail = new_node
        else:
            new_node.setNext(self.head)
            self.head.setPrevious(new_node)
            self.head = new_node

    def insert_at_tail(self, data):
        """Inserts a new node at the end of the DLL."""
        new_node = Node(data)
        if self.tail is None: # If list is empty
            self.head = self.tail = new_node
        else:
            new_node.setPrevious(self.tail)
            self.tail.setNext(new_node)
            self.tail = new_node

    def find(self, key):
        """Finds and returns a node with the given key."""
        current = self.head
        while current:
            if current.getData() == key:
                return current
            current = current.getNext()
        return None # If not found

    def delete(self, key):
        """Deletes a node with the given key."""
        target_node = self.find(key)
        if not target_node:
            return False # Key not found

        if target_node.getPrevious() is not None:
            target_node.getPrevious().setNext(target_node.getNext())
        else:
            target_node.getNext().setPrevious(None)
        if target_node.getNext() is not None:
            target_node.getNext().setPrevious(target_node.getPrevious())

        del target_node

    def traverse_forward(self):
        """List nodes from start to end."""
        result = ""
        node = self.head
        while node is not None:
            result += str(node)
            if node.getNext() is not None:
                result += " -> "
            node = node.getNext()
        return result

    def traverse_backward(self):
        """List nodes from end to start."""
        result = ""
        node = self.tail
        while node is not None:
            result += str(node)
            if node.getNext() is not None:
                result += " -> "
            if node.getPrevious() is not None:
                # This part removes the extra ' -> ' that might appear when reversing
                if result[len(result)-4:] == " -> ":
                    pass
                else:
                    result += " -> "
            node = node.getPrevious()
        return result