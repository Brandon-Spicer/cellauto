from itertools import product 
from random import random, randint 
import pygame
import sys

# TODO: 
    # Write randomization function [DONE]
    # Write function to print out nodes [DONE]
    # Write function to connect adjacent nodes [DONE]
    # Write evolution function (matrix version) [DONE]
        # Write get_neighbors [DONE]
        # Write calc_next_state [DONE]
        # Write evolution loop [DONE]
    # Write draw function [DONE]
    # Write Simulate function [DONE]
    # Write Simulator class [DONE]
    # Make big Star Wars! [DONE]
    # Add history to Automaton [DONE 8/2]
    # Add key controls to simulate with history [DONE 9/10]
    # Add option to animate to simulate function
    # Input neighborhoods as lists of tuples
    # Write filter functions, add ability to pass filters into simlulate
    # Split into multiple files

    # ---- Fun set stuff ----
    # Write set version of evolution function [DONE 7/31]
    # Write function to switch algorithms and preserve state
    # Press button to switch algorithms
    # Write function to change edge connections
        # Different cases: toroid, live/dead
        # Figure out how to handle other automatons as edges
    # Make big star wars with multiple automatons!
    # ----

    # Write GUI to input Automatons
    # Output videos
    # Post on youtube

    # ---- LOW PRIORITY ----
    # Write opposites for initialization functions
    # Input rule as string

# ~~~~ GOALS ~~~~

# Make minimum usable product
    # Library to quickly simulate and visualize 2d CAs
    # Output videos, put on youtube
# Ability to create and link multiple Automatons in a Simulator



SIZE = 1

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

class Node:
    def __init__(self, val, x, y):
        self.x = x
        self.y = y
        self.val = val
        self.next_val = val
        self.adj = set()

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



    # Connect boundaries

    # connect(a1, 'right', 'a2', 'left')

        

class Simulator:
    def __init__(self, automatons, coordinates, X, Y):
        self.automatons = automatons
        self.coordinates = coordinates 
        self.X = X
        self.Y = Y
        self.index = 0
        self.generation = 0

    def update(self):
        for ca in self.automatons:
            # ca.evolve()
            ca.evolve_active()
    
    def draw(self, screen):
        for i, ca in enumerate(self.automatons):
            x, y = self.coordinates[i]
            ca.draw(screen, x, y)

    def draw_history(self, screen):
        for i, ca in enumerate(self.automatons):
            x, y = self.coordinates[i]
            ca.draw_history(screen, x, y, self.index)

    def simulate(self):
        # Use an iterator
        # Use generations
        # j increments iterator
        # k decrements iterator
        # if iterator < generations:
            # draw history
        # else
            # draw (create new history)
        pygame.init()
        fps = 60
        fpsClock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.X, self.Y))
        paused = True

        screen.fill((0, 0, 0))
        while True:
            assert(self.index <= self.generation, "Index is greater than generation number!")
            if self.index < self.generation:
                self.draw_history(screen)
            else:
                self.draw(screen)

            for event in pygame.event.get():
                print(event)
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paused = not paused

                    if event.key == pygame.K_j:
                        if paused:
                            if self.index < self.generation:
                                self.index += 1
                            else:
                                self.index += 1
                                self.generation += 1
                                self.update()
                    if event.key == pygame.K_k:
                        if paused:
                            self.index -= 1
            if not paused:
                if self.index < self.generation:
                    self.index += 1
                else:
                    self.index += 1
                    self.generation += 1
                    self.update()




                # self.update()
            # self.draw(screen)
            # If len(history) <= iterator 
                # draw
            # if len(history) > iterator
                # draw_history
            pygame.display.flip()
            fpsClock.tick(fps)










if __name__ == '__main__':

    '''
    automatons = []
    for _ in range(5):
        automatons.append(Automaton(10, 10, [2,3],[3],2))

    for ca in automatons:
        ca.randomize()

    coordinates = []
    for i in range(5):
        coordinates.append((i*50, i*50))

    sim = Simulator(automatons, coordinates, 500, 500)
    sim.simulate()
    '''



    starwars = Automaton(400, 400, [3,4,5], [2], 4)

    loc = (0, 0)

    sim = Simulator([starwars], [loc], 900, 900)
    sim.simulate()



    


