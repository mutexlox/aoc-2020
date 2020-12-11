import sys

def find_summing_triple(l):
    s = set(l)
    for x in s:
        for y in s:
            if 2020 - x - y in s:
                return x * y * (2020 - x - y)

def find_summing_pair(l):
    s = set(l)
    for x in s:
            if 2020 - x in s:
                return x * (2020 - x)

def main(argv):
    with open(argv[1]) as f:
        l = [int(x.strip()) for x in f]
        print(find_summing_pair(l))
        print(find_summing_triple(l))

if __name__ == "__main__":
    main(sys.argv)
