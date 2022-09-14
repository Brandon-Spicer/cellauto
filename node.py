class Node:
    def __init__(self, val, x, y):
        self.x = x
        self.y = y
        self.val = val
        self.next_val = val
        self.adj = set()