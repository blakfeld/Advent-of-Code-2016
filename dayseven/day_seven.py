#!/usr/bin/env python
"""
--- Day 7: Internet Protocol Version 7 ---

While snooping around the local network of EBHQ, you compile a list of IP addresses (they're IPv7, of course; IPv6 is much too limited). You'd like to figure out which IPs support TLS (transport-layer snooping).

An IP supports TLS if it has an Autonomous Bridge Bypass Annotation, or ABBA. An ABBA is any four-character sequence which consists of a pair of two different characters followed by the reverse of that pair, such as xyyx or abba. However, the IP also must not have an ABBA within any hypernet sequences, which are contained by square brackets.

For example:

    * abba[mnop]qrst supports TLS (abba outside square brackets).
    * abcd[bddb]xyyx does not support TLS (bddb is within square brackets, even though xyyx is outside square brackets).
    * aaaa[qwer]tyui does not support TLS (aaaa is invalid; the interior characters must be different).
    * ioxxoj[asdfgh]zxcvbn supports TLS (oxxo is outside square brackets, even though it's within a larger string).

How many IPs in your puzzle input support TLS?

--- Part Two ---

You would also like to know which IPs support SSL (super-secret listening).

An IP supports SSL if it has an Area-Broadcast Accessor, or ABA, anywhere in the supernet sequences (outside any square bracketed sections), and a corresponding Byte Allocation Block, or BAB, anywhere in the hypernet sequences. An ABA is any three-character sequence which consists of the same character twice with a different character between them, such as xyx or aba. A corresponding BAB is the same characters but in reversed positions: yxy and bab, respectively.

For example:

    * aba[bab]xyz supports SSL (aba outside square brackets with corresponding bab within square brackets).
    * xyx[xyx]xyx does not support SSL (xyx, but no corresponding yxy).
    * aaa[kek]eke supports SSL (eke in supernet with corresponding kek in hypernet; the aaa sequence is not related, because the interior character must be different).
    * zazbz[bzb]cdb supports SSL (zaz has no corresponding aza, but zbz has a corresponding bzb, even though zaz and zbz overlap).

How many IPs in your puzzle input support SSL?

"""
from __future__ import print_function

import re
import sys
from itertools import chain

DEFAULT_INPUT = 'input.txt'
HYPERNET_RE = re.compile(r'\[(\w+)\]')
SUPERNET_RE = re.compile(r'\[\w+\]')


def read_input(fpath):
    """
    Read a specified file, and return a list of the file's contents
        separated by new lines.

    Args:
        fpath (str):    Path of the file to read.

    Returns:
        list
    """
    with open(fpath, 'r') as f:
        return f.read().splitlines()


def valid_ip(ip):
    """
    Check if an IP is valid.

    Args:
        ip (str):   The "IP" to validate.

    Returns:
        bool
    """
    abba_re = re.compile(r'(?=(\w)(\w)\2\1)')

    def valid_match(a, b):
        return a != b

    hypernets = HYPERNET_RE.findall(ip)
    hypernet_abbas = chain.from_iterable(
        abba_re.findall(h) for h in hypernets
    )

    supernets = SUPERNET_RE.split(ip)
    supernet_abbas = chain.from_iterable(
        abba_re.findall(s) for s in supernets
    )

    return (
        any(valid_match(*s) for s in supernet_abbas) and not
        any(valid_match(*h) for h in hypernet_abbas)
    )


def count_valid_ips(ips):
    """
    Count the number of valid IP addresses.

    Args:
        ips (list):     List of "IP" addresses to validate.

    Returns:
        int
    """
    count = 0
    for ip in ips:
        count += 1 if valid_ip(ip) else 0

    return count


def supports_ssl(ip):
    """
    Check if the IP supports "SSL" by checking if the supernet
        contains text like "aba" and the hypernet contains text
        like "bab".

    Args:
        ip (str):   The IP to test.

    Returns:
        bool
    """
    aba_re = re.compile(r'(?=(\w)(\w)(\1))')

    def bab(a, b, _):
        return (b, a, b)

    supernets = SUPERNET_RE.split(ip)
    supernet_abas = list(chain.from_iterable(
        aba_re.findall(s) for s in supernets)
    )

    hypernets = HYPERNET_RE.findall(ip)
    hypernet_abas = list(chain.from_iterable(
        aba_re.findall(h) for h in hypernets)
    )

    return any(bab(*s) in hypernet_abas for s in supernet_abas)


def count_valid_ssl_ips(ips):
    """
    Count the number of valid SSL IP addresses.

    Args:
        ips (list):     List of "IP" addresses to check for SSL.

    Returns:
        int
    """
    count = 0
    for ip in ips:
        count += 1 if supports_ssl(ip) else 0

    return count


def main():
    """
    Main.
    """
    global DEFAULT_INPUT
    try:
        input_file = sys.argv[1]
    except IndexError:
        input_file = DEFAULT_INPUT

    ips = read_input(input_file)

    print('Part One: {0}'.format(count_valid_ips(ips)))
    print('Part Two: {0}'.format(count_valid_ssl_ips(ips)))


if __name__ == '__main__':
    sys.exit(main())
