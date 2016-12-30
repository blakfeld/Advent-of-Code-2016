#!/usr/bin/env python
"""
http://adventofcode.com/2016/day/1

--- Day 1: No Time for a Taxicab ---

Santa's sleigh uses a very high-precision clock to guide its movements, and the
clock's oscillator is regulated by stars. Unfortunately, the stars have been
stolen... by the Easter Bunny. To save Christmas, Santa needs you to retrieve
all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each
day in the advent calendar; the second puzzle is unlocked when you complete the
first. Each puzzle grants one star. Good luck!

You're airdropped near Easter Bunny Headquarters in a city somewhere. "Near",
unfortunately, is as close as you can get - the instructions on the Easter
Bunny Recruiting Document the Elves intercepted start here, and nobody had time
to work them out further.

The Document indicates that you should start at the given coordinates (where
you just landed) and face North. Then, follow the provided sequence: either
turn left (L) or right (R) 90 degrees, then walk forward the given number of
blocks, ending at a new intersection.

There's no time to follow such ridiculous instructions on foot, though, so you
take a moment and work out the destination. Given that you can only walk on the
street grid of the city, how far is the shortest path to the destination?

For example:

    Following R2, L3 leaves you 2 blocks East and 3 blocks North, or 5 blocks
    away.
    R2, R2, R2 leaves you 2 blocks due South of your starting position, which
    is 2 blocks away.
    R5, L5, R5, R3 leaves you 12 blocks away.
    How many blocks away is Easter Bunny HQ?
"""
from __future__ import print_function

import os
import sys


class FindEasterBunny(object):

    def __init__(self, shortcut=False):
        """
        Constructor.

        Args:
            shortcut (bool):    Boolean to indicate whether or not we can
                                    use the shortcut.
        """
        self.direction = 0  # 0123 = NESW
        self.history = set()
        self.x = 0
        self.y = 0
        self.shortcut = shortcut

    @property
    def distance(self):
        return abs(self.x) + abs(self.y)

    @property
    def coordinates(self):
        return (self.x, self.y)

    def _turn(self, turn_direction):
        """
        Change the DIRECTION variable to reflect which direction
            we're currently facing.

        Args:
            turn_direction (str):   Either an 'R' for a right turn
                                        or an 'L' for a left turn.
        """
        if turn_direction == 'R':
            self.direction += 1
        else:
            self.direction -= 1

        # Cap our direction.
        if self.direction < 0:
            self.direction = 3
        elif self.direction > 3:
            self.direction = 0

    def _move(self, steps):
        """
        Move some number of steps in the correct direction.

        Args:
            steps (int):    The number of steps to walk.
        """
        if self.direction == 0:
            self.y += steps
        elif self.direction == 1:
            self.x += steps
        elif self.direction == 2:
            self.y -= steps
        elif self.direction == 3:
            self.x -= steps

    def find_route(self, instructions):
        """
        Count the number of blocks traveled using a list of instructions.

        Args:
            instructions (str):     String containing a comma separated
                                        list of instructions.
        Returns:
            int - Number of blocks traveled.
        """
        for instruction in instructions:
            direction = instruction[0]
            steps = int(instruction[1:])

            self._turn(direction)
            self._move(steps)

        return self.distance


def main():
    """
    Main.
    """
    if len(sys.argv) < 2:
        print('Please provide an input')

    user_arg = sys.argv[1]
    if os.path.isfile(user_arg):
        with open(user_arg, 'r') as f:
            data = f.read()
    else:
        data = user_arg

    data = [i.strip() for i in data.split(',')]
    part_one = FindEasterBunny()
    print(part_one.find_route(data))


if __name__ == '__main__':
    sys.exit(main())
