#!/usr/bin/env python
from __future__ import print_function
import time
import sys
import random
import os
import copy

class World(object):
    def __init__(self, rows, columns, init_map = None):
        self.world = []
        self.prev_world = None
        self.generation = 0
        self.init_maps = {

            "blinker":      [ [0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0],
                              [0, 1, 1, 1, 0] ],

            "glider":   [ [0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 1, 0, 0, 0, 0],
                          [0, 0, 0, 1, 0, 0, 0],
                          [0, 1, 1, 1, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0] ],

            "pentomino":   [ [0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0],
                             [0, 1, 0, 1, 0, 0, 0],
                             [0, 1, 1, 1, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0] ],

            "glider_blinker":   [ [0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 1, 0, 0, 0, 0],
                                  [0, 0, 0, 1, 0, 0, 0],
                                  [0, 1, 1, 1, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 1],
                                  [0, 0, 0, 0, 0, 0, 1],
                                  [0, 0, 0, 0, 0, 0, 1] ],

            "beacon":      [ [0, 0, 0, 0, 0, 0, 0],
                             [0, 1, 1, 0, 0, 0, 0],
                             [0, 1, 1, 0, 0, 0, 0],
                             [0, 0, 0, 1, 1, 0, 0],
                             [0, 0, 0, 1, 1, 0, 0] ],

            "diehard":      [ [0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 1, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 1, 0, 0, 0],
                              [0, 1, 1, 0, 0, 1, 1, 1],
                              [0, 0, 0, 0, 0, 0, 0, 0] ],

            "block":        [ [0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 1, 1, 0, 0, 0, 0],
                              [0, 0, 1, 1, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0] ],

            "pentadecathlon":      [ [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ],

            }


        if init_map is None:
            for i in xrange(rows):
                self.world.append([])
                for j in xrange(columns):
                    self.world[i].append(Cell())

        elif init_map is not None:
            for i in xrange(rows):
                self.world.append([])
                for j in xrange(columns):
                    self.world[i].append(Cell(state=0))
            for i in xrange(len(self.world)):
                for j in xrange(len(self.world[i])):
                    try:
                        self.world[i][j].state = self.init_maps[init_map][i][j]
                    except IndexError:
                        self.world[i][j].state = 0

    def same(self):
        if self.prev_world is None:
            return False
        try:
            for i in xrange(len(self.world)):
                for j in xrange(len(self.world[i])):
                    if self.world[i][j].state != self.prev_world[i][j].state:
                        return False
        except IndexError:
            return False
        return True

    def update(self):
        self.generation += 1
        self.prev_world= copy.deepcopy(self.world)
        for i in xrange(len(self.world)):
            for j in xrange(len(self.world[i])):
                if self.world[i][j].nextState is not None:
                    self.world[i][j].state = self.world[i][j].nextState
                    self.world[i][j].nextState = None

    def show(self):
        _ = os.system("cls")
        print("Generation: %s" % self.generation)
        for i in xrange(len(self.world)):
            for j in xrange(len(self.world[i])):
                if j == (len(self.world[i]) - 1):
                    if self.world[i][j].state == 1:
                        #print("x")
                        print(u"\u2588")
                    else:
                        print(" ")
                else:
                    if self.world[i][j].state == 1:
                        #print("x", end="")
                        print(u"\u2588", end="")
                    else:
                        print(" ", end="")

    def scan(self):
        """
        1. Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
        2. Any live cell with two or three live neighbours lives on to the next generation.
        3. Any live cell with more than three live neighbours dies, as if by overpopulation.
        4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
        """
        for i in xrange(len(self.world)):
            for j in xrange(len(self.world[i])):
                count_live_neighbours = 0

                #right neighbour
                if (j + 1) < len(self.world[i]):
                    if self.world[i][j+1].state == 1:
                        count_live_neighbours += 1
                #left neighbour
                if (j - 1) >= 0:
                    if self.world[i][j-1].state == 1:
                        count_live_neighbours += 1
                #below neighbour
                if (i + 1) < len(self.world):
                    if self.world[i+1][j].state == 1:
                        count_live_neighbours += 1
                #above neighbour
                if (i - 1) >= 0:
                    if self.world[i-1][j].state == 1:
                        count_live_neighbours += 1

                #upper left diagonal neighbour
                if (i - 1) >= 0 and (j - 1) >= 0:
                    if self.world[i-1][j-1].state == 1:
                        count_live_neighbours += 1
                #upper right diagonal neighbour
                if (i - 1) >= 0 and (j + 1) < len(self.world[i]):
                    if self.world[i-1][j+1].state == 1:
                        count_live_neighbours += 1
                #lower left diagonal neighbour
                if (i + 1) < len(self.world) and (j - 1) >= 0:
                    if self.world[i+1][j-1].state == 1:
                        count_live_neighbours += 1
                #lower right diagonal neighbour
                if (i + 1) < len(self.world) and (j + 1) < len(self.world[i]):
                    if self.world[i+1][j+1].state == 1:
                        count_live_neighbours += 1

                if self.world[i][j].state == 1:
                    # underpopulation
                    if count_live_neighbours < 2:
                        self.world[i][j].nextState = 0
                        #print("Killing: [%s, %s]" % (i, j))

                    # overpopulation
                    if count_live_neighbours > 3:
                        self.world[i][j].nextState = 0
                        #print("Killing: [%s, %s]" % (i, j))

                if self.world[i][j].state == 0:
                    # reproduction
                    if count_live_neighbours == 3:
                        self.world[i][j].nextState = 1
                        #print("Reproducing: [%s, %s]" % (i, j))


class Cell(object):
    def __init__(self, state=None):
        if state is None:
            #self.state = 1
            self.state = random.randint(0, 1)
        else:
            self.state = state
        self.nextState = None

def usage():
    print("Usage:")
    print("python conway.py [num rows] [num columns] [optional initial map]")
    print("")
    print("Example 1: initialize to an initial map")
    print("python conway.py 20 30 glider")
    print("")
    print("Example 2: initialize to randomness")
    print("python conway.py 20 30")

def main():
    if len(sys.argv) == 4:
        world = World(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])
    elif len(sys.argv) == 3:
        world = World(int(sys.argv[1]), int(sys.argv[2]))
    else:
        print("Not enough arguments")
        usage()
        return -1
    #world = World(10, 10, "glider")
    world.show()
    try:
        while not world.same():
            time.sleep(1.0/10.0)
            #time.sleep(1.0)
            world.scan()
            world.update()
            world.show()
        print("Only still life or emptiness in the world. Halting.")
        print("Thank you for playing Conway's Game of Life")
    except KeyboardInterrupt:
        print("Thank you for playing Conway's Game of Life")

if __name__ == "__main__":
    main()

