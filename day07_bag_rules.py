import collections
import sys

MIDDLE = ' bags contain '

def parse(lines):
    g = {}  # maps a bag color to colors, counts it can contain
    rev_graph = collections.defaultdict(list)  # maps a bag color to colors that can contain it
    for l in lines:
        i = l.find(MIDDLE)
        outer = l[:i]
        inner = []
        rest = l[i + len(MIDDLE):].split(',')
        if rest[0] != 'no other bags.':
            for r in rest:
                r = r.strip()
                cnt = int(r[0])
                end = r.find(' bag')
                colo = r[2:end]
                inner.append((cnt, colo))
                rev_graph[colo].append(outer)
        g[outer] = inner
    return g, rev_graph

def count_possible_outers(rev_graph, inner, seen=None):
    count = 0
    if seen is None:
        seen = set([inner])
    for colo in rev_graph[inner]:
        if colo not in seen:
            seen.add(colo)
            count += 1 + count_possible_outers(rev_graph, colo, seen)
    return count

def count_minimum_inner(graph, outer):
    count = 0
    for cnt, colo in graph[outer]:
        count += cnt * (1 + count_minimum_inner(graph, colo))
    return count

def main(argv):
    with open(argv[1]) as f:
        lines = [x.rstrip() for x in f]
        graph, reverse = parse(lines)
        print(count_possible_outers(reverse, 'shiny gold'))
        print(count_minimum_inner(graph, 'shiny gold'))


if __name__ == "__main__":
    main(sys.argv)
