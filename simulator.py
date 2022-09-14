import pygame
import sys

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
            ca.evolve()
            # ca.evolve_active()
    
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

                    if event.key == pygame.K_0:
                        if paused:
                            self.index = 0
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
