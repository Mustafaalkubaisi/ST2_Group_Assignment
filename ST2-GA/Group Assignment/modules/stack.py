"""Stack (and Queue) class"""
class Stack:
    # Make an empty list
    def __init__(self):
        self._data = []

    # This function works for push and enqueue
    def push(self, val):
        self._data.append(val)

    # Remove data from end of list
    def pop(self):
        if not self.is_empty():
            return self._data.pop()

    # Remove data from start of list
    def dequeue(self):
        if not self.is_empty():
            return self._data.pop(0)

    # Check if the list is empty
    def is_empty(self):
        return len(self._data) == 0

    # Return size of data list
    def size(self):
        return len(self._data)
