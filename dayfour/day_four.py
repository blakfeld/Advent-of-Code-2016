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

--- Part Two ---

With all the decoy data out of the way, it's time to decrypt this list and get moving.

The room names are encrypted by a state-of-the-art shift cipher, which is nearly unbreakable without the right software. However, the information kiosk designers at Easter Bunny HQ were not expecting to deal with a master cryptographer like yourself.

To decrypt a room name, rotate each letter forward through the alphabet a number of times equal to the room's sector ID. A becomes B, B becomes C, Z becomes A, and so on. Dashes become spaces.

For example, the real name for qzmt-zixmtkozy-ivhz-343 is very encrypted name.

What is the sector ID of the room where North Pole objects are stored?
"""
from __future__ import print_function

import re
import sys
import string
from collections import Counter


INPUT = 'input.txt'
NORTH_POLE_NAME = 'northpole object storage'


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
    room_name = filter(lambda s: s.isalpha() or s == '-',
                       encrypted_room.replace(checksum, '')).rstrip('-')
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


def get_valid_rooms(encrypted_rooms):
    """
    Determine if a room is valid, then sum it's id.

    Args:
        encrypted_rooms (list):   The list of IDs to check.

    Returns:
        list
    """
    valid_rooms = []
    for encrypted_room in encrypted_rooms:
        room_name, sector_id, checksum = encrypted_room
        room_name = room_name.replace('-', '')
        checksum = ''.join(sorted(checksum))
        if checksum == generate_checksum(room_name):
            valid_rooms.append(encrypted_room)

    return valid_rooms


def decode_room_name(room_name, sector_id):
    """
    Using a shift cipher, decode the room name.

    Args:
        room_name (str):    The encoded room name.
        sector_id (int):    The sector ID to use with the shift
                                cipher.

    Returns:
        str
    """
    decoded_name = []
    alpha = string.ascii_lowercase
    for c in room_name:
        if c == '-':
            decoded_name.append(' ')
            continue

        i = alpha.index(c)
        decoded_name.append(alpha[(i + sector_id) % len(alpha)])

    return ''.join(decoded_name)


def find_north_pole(valid_rooms):
    """
    Decode the room names and find the north pole.

    Args:
        valid_rooms (list):     A list of valid rooms to decode/search.

    Returns:
        tuple
    """
    for room in valid_rooms:
        room_name, sector_id, checksum = room
        decoded_name = decode_room_name(room_name, sector_id)
        if decoded_name == NORTH_POLE_NAME:
            return decoded_name, sector_id


def sum_valid_rooms(valid_rooms):
    """
    Get the sum of all the sector IDs in valid rooms.

    Args:
        valid_rooms (list):     List containting tuples of valid rooms.

    Returns:
        int
    """
    # Valid Room:
    #   (room_name, sector_id, checksum)
    return sum([i[1] for i in valid_rooms])


def main():
    """
    Main.
    """
    encrypted_rooms = read_input(INPUT)
    valid_rooms = get_valid_rooms(encrypted_rooms)

    print('Part One: {}'.format(sum_valid_rooms(valid_rooms)))

    print('Part Two: {}'.format(find_north_pole(valid_rooms)))


if __name__ == '__main__':
    sys.exit(main())
