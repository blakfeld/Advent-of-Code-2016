#!/usr/bin/env python
"""
--- Day 4: Security Through Obscurity ---

Finally, you come across an information kiosk with a list of rooms. Of course, the list is encrypted and full of decoy data, but the instructions to decode the list are barely hidden nearby. Better remove the decoy data first.

Each room consists of an encrypted name (lowercase letters separated by dashes) followed by a dash, a sector ID, and a checksum in square brackets.

A room is real (not a decoy) if the checksum is the five most common letters in the encrypted name, in order, with ties broken by alphabetization. For example:

aaaaa-bbb-z-y-x-123[abxyz] is a real room because the most common letters are a (5), b (3), and then a tie between x, y, and z, which are listed alphabetically.
a-b-c-d-e-f-g-h-987[abcde] is a real room because although the letters are all tied (1 of each), the first five are listed alphabetically.
not-a-real-room-404[oarel] is a real room.
totally-real-room-200[decoy] is not.
Of the real rooms from the list above, the sum of their sector IDs is 1514.

What is the sum of the sector IDs of the real rooms?
"""
from __future__ import print_function

import re
import sys
from collections import Counter


INPUT = 'input.txt'


def read_input(fpath):
    """
    Read a specified input file and return the contents as a list
        separated by new lines.

    Args:
        fpath (str):    Path of file to read.

    Returns:
        list
    """
    with open(fpath, 'r') as f:
        return [format_sector_id(line.strip()) for line in f.readlines()]


def format_sector_id(encrypted_room):
    """
    Take a "sector_id" and break it into the ID and it's checksum.

    Args:
        encrypted_room (str):    The sector ID to format.

    Returns:
        tuple.
    """
    checksum = re.search(r'\[[a-z]+\]', encrypted_room).group(0)
    room_name = filter(lambda s: s.isalpha(),
                       encrypted_room.replace(checksum, ''))
    sector_id = int(filter(lambda d: d.isdigit(), encrypted_room))
    checksum = re.sub(r'(\[|\])', '', checksum)

    return room_name, sector_id, checksum


def generate_checksum(room_name):
    """
    Generate a checksum consisting of the most common characters
        in the string.

    Args:
        room_name (str):    The Room Name to generated a checksum for.

    Returns:
        str
    """
    counter = Counter(room_name)

    checksum = ''.join(k for (k, v) in sorted(counter.most_common(),
                                              key=lambda (x, y): (-y, x))[:5])
    checksum = ''.join(sorted(checksum))

    return checksum


def sum_valid_sectors(encrypted_ids):
    """
    Determine if a sector is valid, then sum it's id.

    Args:
        encrypted_ids (list):   The list of IDs to check.

    Returns:
        int
    """
    count = 0
    for encrypted_id in encrypted_ids:
        room_name, sector_id, checksum = encrypted_id
        checksum = ''.join(sorted(checksum))
        if checksum == generate_checksum(room_name):
            count += sector_id

    return count


def main():
    """
    Main.
    """
    encrypted_ids = read_input(INPUT)

    print('Part One: {}'.format(sum_valid_sectors(encrypted_ids)))


if __name__ == '__main__':
    sys.exit(main())
