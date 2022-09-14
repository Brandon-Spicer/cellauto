import pygame
from node import Node
from random import randint

SIZE = 4

# --- colors ---- 
# TODO: Figure out where to put this
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
colors = [black, white, red, blue, green]
pink1 = (255, 128, 128)
pink2 = (255, 64, 64)
colors = [black, white, pink1, pink2]

class Automaton:
    def __init__(self, X, Y, S, B, G):
        self.X = X
        self.Y = Y
        self.S = S
        self.B = B
        self.G = G

        self.matrix = [[None] * X for _ in range(Y)]
        self.nodes = set()
        self.active = set()
        self.live = set()
        self.history = []       # 3D list of vals 
        self.remember = True

        self.create_nodes()
        self.connect_adjacent()
        self.randomize()
        self.populate_sets()
        self.record_history()

    def create_nodes(self):
        for y in range(self.Y):
            for x in range(self.X):
                node = Node(0, x, y) 
                self.nodes.add(node)
                self.matrix[y][x] = node

    def connect_adjacent(self):
        for y in range(self.Y):
            for x in range(self.X):
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if not i == j == 0:
                            neighbor = self.matrix[(y + i)%self.Y][(x + j)%self.X]
                            self.matrix[y][x].adj.add(neighbor)

    def randomize(self):
        for node in self.nodes:
            node.val = randint(0, self.G - 1)

    def print_vals(self):
        for y in range(self.Y):
            for x in range(self.X):
                val = self.matrix[y][x].val 
                print(val, end=' ')
            print()

    def print_history(self, i):
        for y in range(self.Y):
            for x in range(self.X):
                val = self.history[i][y][x]
                print(val, end=' ')
            print()

    def count_adjacent(self, node):
        count = 0
        for a in node.adj:
            if a.val == 1:
                count += 1
        return count

    def calc_next(self, node):
        num = self.count_adjacent(node)

        if node.val == 0:
            if num in self.B:
                return 1
            else:
                return 0 
        elif node.val == 1:
            if num in self.S:
                return 1
            else:
                return (node.val + 1) % self.G
        else:
            return (node.val + 1) % self.G

    def evolve(self):
        if self.remember:
            self.record_history()
        # Calculate next values
        for y in range(self.Y):
            for x in range(self.X):
                node = self.matrix[y][x]
                node.next_val = self.calc_next(node)
        # Update values
        for y in range(self.Y):
            for x in range(self.X):
                node = self.matrix[y][x]
                node.val = node.next_val

    def evolve_active(self):
        addset = set()
        remset = set()
        if self.remember:
            self.record_history()
        # Calculate next values
        for node in self.active:
            node.next_val = self.calc_next(node)
        # Update values
        for node in self.active:
            node.val = node.next_val
            if node.val > 0:
                self.live.add(node)
                for a in node.adj:
                    addset.add(a)
            elif node in self.live:
                self.live.remove(node)
                hasLiveNeighbor = False
                for a in node.adj:
                    if a.val > 0:
                        hasLiveNeighbor = True
                        break
                if not hasLiveNeighbor:
                    remset.add(a)
        # Update active set
        self.active = self.active | addset
        self.active = self.active - remset

    def update_active(self):
        
        # Nodes to add:
        #   Neighbors of newly alive nodes.
        
        # Nodes to remove:
        #   Active Nodes that are dead AND have no live neighbors in active

        addset = set()
        remset = set()
        # Nodes to add adj to active: alive but not active
        addset = self.live - self.active
        # Nodes to remove adj from active:
        remset = self.active - self.live
        # Get live cells not in active and put them in active
        for node in addset:
            self.active.add(node)
            for adj in node.adj:
                self.active.add(adj)

        # Get active cells not in live and remove them from active
        for node in remset:
            valsum = 0
            for adj in node.adj:
                valsum += adj.val
            if valsum == 0:
                self.active.remove(node)

        self.active = self.active | addset
        self.active = self.active - remset

        print(len(self.active))


    def populate_sets(self):
        # Add all live nodes and neighbors to active
        for node in self.nodes:
            if node.val > 0:
                self.active.add(node)
                self.live.add(node)
                for adj in node.adj:
                    self.active.add(adj)

    def draw(self, screen, start_x, start_y):
        # draw rects to given screen with offsets
        for y in range(self.Y):
            for x in range(self.X):
                val = self.matrix[y][x].val
                color = colors[val]
                rect = pygame.Rect(x*SIZE + start_x, y*SIZE + start_y, SIZE, SIZE)
                pygame.draw.rect(screen, color, rect)
            
    def draw_history(self, screen, start_x, start_y, index):
        for y in range(self.Y):
            for x in range(self.X):
                val = self.history[index][y][x]
                color = colors[val]
                rect = pygame.Rect(x*SIZE + start_x, y*SIZE + start_y, SIZE, SIZE)
                pygame.draw.rect(screen, color, rect)

    def record_history(self):
        current_grid = [[0]*self.X for _ in range(self.Y)]
        for y in range(self.Y):
            for x in range(self.X):
                current_grid[y][x] = self.matrix[y][x].val

        self.history.append(current_grid)