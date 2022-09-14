from itertools import product 
from random import random, randint 
import pygame
import sys

from node import Node
from automaton import Automaton
from simulator import Simulator


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



    starwars = Automaton(200, 200, [3,4,5], [2], 4)

    loc = (0, 0)

    sim = Simulator([starwars], [loc], 800, 800)
    sim.simulate()










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
    # ----> Write filter functions, add ability to pass filters into simlulate.
    # Split into multiple files [DONE 9/12]
    # Add location coordinates to Automatons

    # ---- Controls ----
    # Number keys to change index

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

