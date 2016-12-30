#!/usr/bin/env python
"""
--- Day 3: Squares With Three Sides ---

Now that you can think clearly, you move deeper into the labyrinth of hallways and office furniture that makes up this part of Easter Bunny HQ. This must be a graphic design department; the walls are covered in specifications for triangles.

Or are they?

The design document gives the side lengths of each triangle it describes, but... 5 10 25? Some of these aren't triangles. You can't help but mark the impossible ones.

In a valid triangle, the sum of any two sides must be larger than the remaining side. For example, the "triangle" given above is impossible, because 5 + 10 is not larger than 25.

In your puzzle input, how many of the listed triangles are possible?

--- Part Two ---

Now that you've helpfully marked up their design documents, it occurs to you that triangles are specified in groups of three vertically. Each set of three numbers in a column specifies a triangle. Rows are unrelated.

For example, given the following specification, numbers with the same hundreds digit would be part of the same triangle:

101 301 501
102 302 502
103 303 503
201 401 601
202 402 602
203 403 603
In your puzzle input, and instead reading by columns, how many of the listed triangles are possible?
"""
from __future__ import print_function

import sys
from itertools import permutations

INPUT = 'input.txt'


def valid_triangle(sides):
    """
    Check if a sides makes a valid triangle.

    Args:
        sides (tuple):  Tuple containing the sides of a triangle.

    Returns:
        bool
    """
    for permutation in permutations(sides):
        if (permutation[0] + permutation[1]) <= permutation[2]:
            return False
    return True


def format_into_columns(lines):
    """
    Break the columns of our data into one big row we can parse
        into sectons.

    Args:
        lines (list):   The lines to parse.

    Returns:
        list
    """
    one = []
    two = []
    three = []
    for line in lines:
        line = line.split()
        one.append(line[0])
        two.append(line[1])
        three.append(line[2])

    combined = one + two + three
    columns = [tuple(map(int, combined[i:i + 3]))
               for i in xrange(0, len(combined) - 1, 3)]

    return columns


def read_input(fpath):
    """
    Read an input file, and return a list of tuples, each item
        containing a single line.

    Args:
        fpath (str):    File path of the file to read.

    Returns:
        list of tuples:
            [ (xxx, xxx, xxx) ]
    """
    with open(fpath, 'r') as f:
        data = [line.strip() for line in f.readlines()]

    rows = [tuple(map(int, d.split())) for d in data]
    columns = format_into_columns(data)

    return rows, columns


def count_valid_triangles(triangles):
    """
    Given a list of possible triangles, return a count of the number of
        valid triangles.

    Args:
        triangles (list):   List of tuples containing the measurements of
                                a triangle.

    Returns:
        int
    """
    count = 0
    for triangle in triangles:
        if valid_triangle(triangle):
            count += 1
    return count


def main():
    """
    Main
    """
    rows, columns = read_input(INPUT)

    print('Rows: {0}'.format(count_valid_triangles(rows)))
    print('Columns: {0}'.format(count_valid_triangles(columns)))


if __name__ == '__main__':
    sys.exit(main())
