#!/usr/bin/env python
"""
--- Day 2: Bathroom Security ---

You arrive at Easter Bunny Headquarters under cover of darkness. However, you left in such a rush that you forgot to use the bathroom! Fancy office buildings like this one usually have keypad locks on their bathrooms, so you search the front desk for the code.

"In order to improve security," the document you find says, "bathroom codes will no longer be written down. Instead, please memorize and follow the procedure below to access the bathrooms."

The document goes on to explain that each button to be pressed can be found by starting on the previous button and moving to adjacent buttons on the keypad: U moves up, D moves down, L moves left, and R moves right. Each line of instructions corresponds to one button, starting at the previous button (or, for the first line, the "5" button); press whatever button you're on at the end of each line. If a move doesn't lead to a button, ignore it.

You can't hold it much longer, so you decide to figure out the code as you walk to the bathroom. You picture a keypad like this:

1 2 3
4 5 6
7 8 9
Suppose your instructions are:

ULL
RRDDD
LURDL
UUUUD
You start at "5" and move up (to "2"), left (to "1"), and left (you can't, and stay on "1"), so the first button is 1.
Starting from the previous button ("1"), you move right twice (to "3") and then down three times (stopping at "9" after two moves and ignoring the third), ending up with 9.
Continuing from "9", you move left, up, right, down, and left, ending with 8.
Finally, you move up four times (stopping at "2"), then down once, ending with 5.
So, in this example, the bathroom code is 1985.

Your puzzle input is the instructions from the document you found at the front desk. What is the bathroom code?

--- Part Two ---

You finally arrive at the bathroom (it's a several minute walk from the lobby so visitors can behold the many fancy conference rooms and water coolers on this floor) and go to punch in the code. Much to your bladder's dismay, the keypad is not at all like you imagined it. Instead, you are confronted with the result of hundreds of man-hours of bathroom-keypad-design meetings:

    1
  2 3 4
5 6 7 8 9
  A B C
    D
You still start at "5" and stop when you're at an edge, but given the same instructions as above, the outcome is very different:

You start at "5" and don't move at all (up and left are both edges), ending at 5.
Continuing from "5", you move right twice and down three times (through "6", "7", "B", "D", "D"), ending at D.
Then, from "D", you move five more times (through "D", "B", "C", "C", "B"), ending at B.
Finally, after five more moves, you end at 3.
So, given the actual keypad layout, the code would be 5DB3.

Using the same instructions in your puzzle input, what is the correct bathroom code?
"""
from __future__ import print_function

import sys


INPUT = 'input.txt'
KEYPAD_ONE = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 9, 9],
]
KEYPAD_TWO = [
    ['X', 'X', 1, 'X', 'X'],
    ['X', 2, 3, 4, 'X'],
    [5, 6, 7, 8, 9],
    ['X', 'A', 'B', 'C', 'X'],
    ['X', 'X', 'D', 'X', 'X']
]


class KeyPadInput(object):

    MOVEMENT_MAP = {
        'U': (-1, 0),
        'D': (1, 0),
        'L': (0, -1),
        'R': (0, 1),
    }

    def __init__(self, keypad, starting_number, padding_char='X'):
        """
        Constructor.
        """
        self.keypad = keypad
        self.x, self.y = self._find_starting_coords(starting_number)
        self.padding_char = padding_char

    @property
    def x_bound(self):
        return len(self.keypad) - 1

    @property
    def y_bound(self):
        return len(self.keypad[self.x]) - 1

    def _find_starting_coords(self, starting_number):
        """
        Search the keypad for a number, then return that numbers
            coordinates within the matrix.

        Args:
            starting_number (int):  The number to find.

        Returns:
            Tuple - (X, Y)
        """
        for i, x in enumerate(self.keypad):
            for j, y in enumerate(self.keypad[i]):
                if self.keypad[i][j] == starting_number:
                    return i, j

    def find_passcode(self, instructions):
        """
        Generate a passcode based upon the supplied instructions.

        Args:
            instructions (list):    List of instructions. Each entrry
                                        to generate a single digit.

        Returns:
            str
        """
        result = []
        for instruction in instructions:
            result.append(str(self._find_passcode_digit(instruction)))
        return ''.join(result)

    def _find_passcode_digit(self, instructions):
        """
        Given the instructions, find the number on the keypad.

        Args:
            instruction (interable):    An interable of characters
                                            that indicate the location
                                            of the number on the keypad.

        Returns:
            int
        """
        for inst in instructions:
            delta_x, delta_y = self.MOVEMENT_MAP.get(inst)
            if self._valid_delta(delta_x, delta_y):
                self.x += delta_x
                self.y += delta_y
        return self.keypad[self.x][self.y]

    def _valid_delta(self, delta_x, delta_y):
        """
        Validate that the delta we want to apply to our coordinates
            doesn't put us out of bounds.

        Args:
            delta_x (int)       Integer representing the movement we want
                                    to apply to the X-axis.
            delta_y (int)       Integer representing the movement we want
                                    to apply to the Y-axis.

        Returns:
            bool
        """
        new_x = self.x + delta_x
        new_y = self.y + delta_y
        bound_tests = [
            new_x > self.x_bound,
            new_x < 0,
            new_y > self.y_bound,
            new_y < 0,
        ]
        if any(bound_tests) or self.keypad[new_x][new_y] == self.padding_char:
            return False

        return True


def read_input():
    """
    Read input file.

    Returns:
        list - The input, new line separated.
    """
    global INPUT
    with open(INPUT, 'r') as f:
        return [line.strip() for line in f.readlines()]


def main():
    """
    Main.
    """
    result = []
    instructions = read_input()

    passcode_one = KeyPadInput(KEYPAD_ONE, 5)
    passcode_two = KeyPadInput(KEYPAD_TWO, 5)

    print('Part One: {}'.format(passcode_one.find_passcode(instructions)))
    print('Part Two: {}'.format(passcode_two.find_passcode(instructions)))


if __name__ == '__main__':
    sys.exit(main())
