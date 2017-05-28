#!/usr/bin/env python
from __future__ import print_function
import time
import sys
import random
import os

world = []

class Cell:
    def __init__(self, state=None):
        if state is None:
            #self.state = 1
            self.state = random.randint(0, 1)
        else:
            self.state = state
        self.nextState = None

blinker =     [ [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 1, 1, 1, 0] ]

glider =  [ [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0] ]

pentomino =  [ [0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0],
               [0, 1, 0, 1, 0, 0, 0],
               [0, 1, 1, 1, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0] ]

glider_blinker =  [ [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0, 0, 0],
                    [0, 0, 0, 1, 0, 0, 0],
                    [0, 1, 1, 1, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 1],
                    [0, 0, 0, 0, 0, 0, 1],
                    [0, 0, 0, 0, 0, 0, 1] ]

def initWorld(rows, columns, init_map = None):
    global world
    world = []
    if init_map is None:
        for i in xrange(rows):
            world.append([])
            for j in xrange(columns):
                world[i].append(Cell())

    elif init_map is not None:
        for i in xrange(rows):
            world.append([])
            for j in xrange(columns):
                world[i].append(Cell(state=0))
        for i in xrange(len(world)):
            for j in xrange(len(world[i])):
                try:
                    world[i][j].state = init_map[i][j]
                except IndexError:
                    world[i][j].state = 0

def showWorld():
    _ = os.system("cls")
    global world
    for i in xrange(len(world)):
        for j in xrange(len(world[i])):
            if j == (len(world[i]) - 1):
                if world[i][j].state == 1:
                    #print("x")
                    print(u"\u2588")
                else:
                    print(" ")
            else:
                if world[i][j].state == 1:
                    #print("x", end="")
                    print(u"\u2588", end="")
                else:
                    print(" ", end="")

def scanWorld():
    """
    1. Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
    2. Any live cell with two or three live neighbours lives on to the next generation.
    3. Any live cell with more than three live neighbours dies, as if by overpopulation.
    4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
    """
    global world
    for i in xrange(len(world)):
        for j in xrange(len(world[i])):
            count_live_neighbours = 0

            #right neighbour
            if (j + 1) < len(world[i]):
                if world[i][j+1].state == 1:
                    count_live_neighbours += 1
            #left neighbour
            if (j - 1) >= 0:
                if world[i][j-1].state == 1:
                    count_live_neighbours += 1
            #below neighbour
            if (i + 1) < len(world):
                if world[i+1][j].state == 1:
                    count_live_neighbours += 1
            #above neighbour
            if (i - 1) >= 0:
                if world[i-1][j].state == 1:
                    count_live_neighbours += 1

            #upper left diagonal neighbour
            if (i - 1) >= 0 and (j - 1) >= 0:
                if world[i-1][j-1].state == 1:
                    count_live_neighbours += 1
            #upper right diagonal neighbour
            if (i - 1) >= 0 and (j + 1) < len(world[i]):
                if world[i-1][j+1].state == 1:
                    count_live_neighbours += 1
            #lower left diagonal neighbour
            if (i + 1) < len(world) and (j - 1) >= 0:
                if world[i+1][j-1].state == 1:
                    count_live_neighbours += 1
            #lower right diagonal neighbour
            if (i + 1) < len(world) and (j + 1) < len(world[i]):
                if world[i+1][j+1].state == 1:
                    count_live_neighbours += 1

            if world[i][j].state == 1:
                # underpopulation
                if count_live_neighbours < 2:
                    world[i][j].nextState = 0
                    #print("Killing: [%s, %s]" % (i, j))

                # overpopulation
                if count_live_neighbours > 3:
                    world[i][j].nextState = 0
                    #print("Killing: [%s, %s]" % (i, j))

            if world[i][j].state == 0:
                # reproduction
                if count_live_neighbours == 3:
                    world[i][j].nextState = 1
                    #print("Reproducing: [%s, %s]" % (i, j))


def updateWorld():
    global world
    for i in xrange(len(world)):
        for j in xrange(len(world[i])):
            if world[i][j].nextState is not None:
                world[i][j].state = world[i][j].nextState
                world[i][j].nextState = None


def main():
    #initWorld(50, 50, init_map = pentomino)
    initWorld(columns=80, rows=50)
    showWorld()
    try:
        while 1:
            #time.sleep(1.0/10.0)
            #time.sleep(1.0)
            scanWorld()
            updateWorld()
            showWorld()
    except KeyboardInterrupt:
        print("Thank you for playing Conway's Game of Life")

if __name__ == "__main__":
    main()

