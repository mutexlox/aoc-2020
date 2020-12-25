import collections
import itertools
import sys

def transform(subject, size, val=1):
    for i in range(size):
        val = val * subject
        val = val % 20201227
    return val

def get_loop_size(pubkey, subject=7):
    val = 1
    for i in range(1000000000):
        val = transform(subject, 1, val)
        if val == pubkey:
            return i + 1
    return None

def break_key(door_pubkey, card_pubkey):
    door_loop_size = get_loop_size(door_pubkey)
    card_loop_size = get_loop_size(card_pubkey)
    print(door_loop_size, card_loop_size)
    key = transform(card_pubkey, door_loop_size)
    return key

def main(argv):
    with open(argv[1]) as f:
        lines = [int(x.rstrip()) for x in f]
        print(break_key(lines[0], lines[1]))

if __name__ == "__main__":
    main(sys.argv)
