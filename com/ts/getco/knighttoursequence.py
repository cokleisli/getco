__author__ = 'me'
'''
Created on Jun 5, 2012
@author: Iftikhar Khan
'''
REQD_SEQUENCE_LENGTH = 10
VOWEL_LIMIT = 2
VOWELS = [(0, 0), (4, 0), (3, -1), (4, -2)]


def build_keypad():
    """Generates 2-D mesh representation of keypad."""
    keypad = [(x, y) for x in range(5) for y in range(-3, 1)]
    # adjust topology
    keypad.remove((0, -3))
    keypad.remove((4, -3))
    return keypad


def check_position(position):
    """Determines if the transform is valid. That is, not off-keypad."""
    if position == (0, -3) or position == (4, -3):
        return False

    if (-1 < position[0] < 5) and (-4 < position[1] < 1):
        return True
    else:
        return False


def build_map(keypad):
    """Generates a map of all possible Knight moves for all keys."""
    moves = [(1, -2), (1, 2), (2, -1), (2, 1), (-1, -2), (-1, 2), (-2, -1), (-2, 1)]
    keymap = {}
    for key_pos in keypad:
        for move in moves:
            x = key_pos[0] + move[0]
            y = key_pos[1] + move[1]
            if check_position((x, y)):
                keymap.setdefault(key_pos, []).append((x, y))
    return keymap


def build_sequence(k, p, m, v, ks):
    """Generates n-key sequence permutations under m-vowel constraints using
        memoization optimisation technique. A valid permutation is a function
        of a key press, position of a key in a sequence and the current
        vowel count. This memoization data is stored as a 3-tuple, (k,p,v), in
        dictionary m.
    """
    if k in VOWELS:
        v += 1
        if v > VOWEL_LIMIT:
            v -= 1
            return 0

    if p == REQD_SEQUENCE_LENGTH:
        m[(k, p, v)] = 0
        return 1
    else:
        if (k, p, v) in m:
            return m[(k, p, v)]
        else:
            m[(k, p, v)] = 0
            for e in ks[k]:
                m[(k, p, v)] += build_sequence(e, p + 1, m, v, ks)

    return m[(k, p, v)]


def count(keys):
    """Counts all n-key permutations under m-vowel constraints."""
    # initialise counters
    sequence_position = 1
    vowel_count = 0
    memo = {}

    return sum(build_sequence(key, sequence_position, memo, vowel_count, keys)
               for key in keys)


if __name__ == '__main__':
    print(count(build_map(build_keypad())))