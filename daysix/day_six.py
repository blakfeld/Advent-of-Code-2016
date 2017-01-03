#!/usr/bin/env python
"""
--- Day 6: Signals and Noise ---

Something is jamming your communications with Santa. Fortunately, your signal is only partially jammed, and protocol in situations like this is to switch to a simple repetition code to get the message through.

In this model, the same message is sent repeatedly. You've recorded the repeating message signal (your puzzle input), but the data seems quite corrupted - almost too badly to recover. Almost.

All you need to do is figure out which character is most frequent for each position. For example, suppose you had recorded the following messages:

eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar
The most common character in the first column is e; in the second, a; in the third, s, and so on. Combining these characters returns the error-corrected message, easter.

Given the recording in your puzzle input, what is the error-corrected version of the message being sent?
--- Part Two ---

Of course, that would be the message - if you hadn't agreed to use a modified repetition code instead.

In this modified code, the sender instead transmits what looks like random data, but for each character, the character they actually want to send is slightly less likely than the others. Even after signal-jamming noise, you can look at the letter distributions in each column and choose the least common letter to reconstruct the original message.

In the above example, the least common character in the first column is a; in the second, d, and so on. Repeating this process for the remaining characters produces the original message, advent.

Given the recording in your puzzle input and this new decoding methodology, what is the original message that Santa is trying to send?
"""
from __future__ import print_function

import sys
from collections import Counter

DEFAULT_INPUT = 'input.txt'


def read_input(fpath):
    """
    Read the global input file.

    Args:
        fpath (str):    Path to the input file to read.

    Returns:
        list
    """
    with open(fpath, 'r') as f:
        return [line.strip() for line in f.readlines()]


def decode_message_most_common(signals):
    """
    Decode the message using the most common character
        in each column.

    Args:
        signals (list):     List of signals to "decode".

    Returns:
        str

    """
    result = []
    for i in xrange(0, len(signals[0])):
        result.append(
            Counter([s[i] for s in signals])
            .most_common()[0][0]
        )

    return ''.join(result)


def decode_message_least_common(signals):
    """
    Decode the message using the least common character
        in each column.

    Args:
        signals (list):     List of signals to "decode".

    Returns:
        str
    """
    result = []
    for i in xrange(0, len(signals[0])):
        result.append(
            Counter([s[i] for s in signals])
            .most_common()[-1][0]
        )

    return ''.join(result)


def main():
    """
    Main.
    """
    global DEFAULT_INPUT
    try:
        input_file = sys.argv[1]
    except IndexError:
        input_file = DEFAULT_INPUT

    signals = read_input(input_file)

    print('Part One: {}'.format(decode_message_most_common(signals)))
    print('Part Two: {}'.format(decode_message_least_common(signals)))


if __name__ == '__main__':
    sys.exit(main())
