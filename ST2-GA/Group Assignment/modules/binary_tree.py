class Node:
    """Class representing a single node in the Binary Search Tree."""
    def __init__(self, key):
        self.val = key
        self.left = None
        self.right = None

class BST:
    """Binary Search Tree class implementing insert, search, delete, and traversal methods."""
    # Global result to return as string
    global result
    result = ''

    def __init__(self):
        self.root = None

    def insert(self, key):
        """Insert a new node into the BST."""
        if self.root is None:
            self.root = Node(key)
        else:
            self._insert_recursive(self.root, key)

    def _insert_recursive(self, root, key):
        """Helper method for inserting recursively."""
        if key < root.val:
            if root.left is None:
                root.left = Node(key)
            else:
                self._insert_recursive(root.left, key)
        else:
            if root.right is None:
                root.right = Node(key)
            else:
                self._insert_recursive(root.right, key)

    def inorder(self):
        """Perform an inorder traversal (Left Right) and print elements in sorted order."""
        global result
        result = ''
        self._inorder_recursive(self.root)
        # Remove ', ' at the end of the result
        return result[:-2]

    def _inorder_recursive(self, root):
        """Helper method for recursive inorder traversal."""
        global result
        if root:
            self._inorder_recursive(root.left)
            result += str(root.val) + ', '
            self._inorder_recursive(root.right)

    def preorder(self):
        """Perform a preorder traversal (Root Right) and print elements."""
        global result
        result = ''
        self._preorder_recursive(self.root)
        # Remove ', ' at the end of the result
        return result[:-2]

    def _preorder_recursive(self, root):
        """Helper method for recursive preorder traversal."""
        global result
        if root:
            result += str(root.val) + ", "
            self._preorder_recursive(root.left)
            self._preorder_recursive(root.right)

    def postorder(self):
        """Perform a postorder traversal (Left Root) and print elements."""
        global result
        result = ''
        self._postorder_recursive(self.root)
        # Remove ', ' at the end of the result
        return result[:-2]

    def _postorder_recursive(self, root):
        """Helper method for recursive postorder traversal."""
        global result
        if root:
            self._postorder_recursive(root.left)
            self._postorder_recursive(root.right)
            result += str(root.val) + ", "

    def search(self, key):
        """Search for a key in BST. Returns True if found, False otherwise."""
        return self._search_recursive(self.root, key)

    def _search_recursive(self, root, key):
        """Helper method for recursive search."""
        if root is None:
            return False
        if root.val == key:
            return True
        if key < root.val:
            return self._search_recursive(root.left, key)
        return self._search_recursive(root.right, key)

    def delete(self, key):
        """Delete a node from BST."""
        self.root = self._delete_recursive(self.root, key)

    def _delete_recursive(self, root, key):
        """Helper method for recursive deletion."""
        if root is None:
            return root
        if key < root.val:
            root.left = self._delete_recursive(root.left, key)
        elif key > root.val:
            root.right = self._delete_recursive(root.right, key)
        else:

            # Case 1: Node has no child
            if root.left is None and root.right is None:
                return None

            # Case 2: Node has one child
            elif root.left is None:
                return root.right
            elif root.right is None:
                return root.left

            # Case 3: Node has two children
            temp = self._minValueNode(root.right)
            root.val = temp.val
            root.right = self._delete_recursive(root.right,
            temp.val)
        return root

    def _minValueNode(self, node):
        """Helper function to find the minimum value node in the right subtree."""
        current = node
        while current.left:
            current = current.left
        return current

    def display_tree(self, root=None, level=0, prefix="Root: "):
        """Display tree structure visually in console without global variables."""
        if root is None and level == 0:
            root = self.root

        if root is None:
            return ""

        # Build the current line
        result = " " * (level * 4) + prefix + str(root.val) + "\n"

        # Go through the node's children
        if root.left or root.right:
            if root.left:
                result += self.display_tree(root.left, level + 1, "L--- ")
            else:
                result += " " * ((level + 1) * 4) + "L--- None\n"

            if root.right:
                result += self.display_tree(root.right, level + 1, "R--- ")
            else:
                result += " " * ((level + 1) * 4) + "R--- None\n"

        return result