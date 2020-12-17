import collections
import sys


def parse_rules(rules):
    d = {}
    for r in rules:
        name, rest = r.split(':')
        rest = rest.strip()
        bound_strs = rest.split(' or ')
        bounds = []
        for b in bound_strs:
            min, max = b.split('-')
            bounds.append((int(min), int(max)))
        d[name] = bounds
    return d

def num_matches_rule(rule, num):
    for ieq in rule:
        if ieq[0] <= num and ieq[1] >= num:
           return True
    return False

def num_matches_any_rule(rules, num):
    for r in rules.values():
        worked = num_matches_rule(r, num)
        if worked:
            return True
    return False


def count_valid_ticks(rules, ticks):
    count = 0
    for t in ticks:
        for num in t:
            if not num_matches_any_rule(rules, num):
                count += num
    return count


def is_valid_tick(rules, tick):
    for num in tick:
        if not num_matches_any_rule(rules, num):
            return False
    return True


def prod(it):
    p = 1
    for x in it:
        p *= x
    return p

def identify_fields(rules, my_tick, ticks):
    ticks = [my_tick] + [t for t in ticks if is_valid_tick(rules, t)]

    # Filter out invalid ones first...
    possibilities = [list(rules.keys()) for _ in range(len(my_tick))]
    for i in range(len(possibilities)):
        for t in ticks:
            j = len(possibilities[i]) - 1
            while j >= 0:
                p = possibilities[i][j]
                if not num_matches_rule(rules[p], t[i]):
                    possibilities[i].pop(j)
                j -= 1

    # Then, some may be uniquely assigned, so filter those out from the rest...
    uniques = [p[0] for p in possibilities if len(p) == 1]
    while len(uniques) != len(possibilities):
        for p in possibilities:
            for u in uniques:
                if u in p and len(p) > 1:
                    p.remove(u)
        uniques = [p[0] for p in possibilities if len(p) == 1]

    # Now compute desired checksum
    departure_idxs = [i for i in range(len(possibilities)) if possibilities[i][0].find('departure') != -1]
    return prod(my_tick[i] for i in range(len(my_tick)) if i in departure_idxs)


def main(argv):
    with open(argv[1]) as f:
        lines = [x.rstrip() for x in f]

        rules = []
        rules_done = False
        your_tick = None
        nearby_ticks = []
        for i in range(len(lines)):
            l = lines[i]
            if not rules_done:
                if l:
                    rules.append(l)
                else:
                    rules_done = True
            elif l.find("ticket:") != -1:
                continue
            elif l.find("tickets:") != -1:
                continue
            elif your_tick is None:
                your_tick = [int(x) for x in l.split(',')]
            elif not l:
                continue
            else:
                nearby_ticks.append([int(x) for x in l.split(',')])
        parsed_rules = parse_rules(rules)

        print(count_valid_ticks(parsed_rules, nearby_ticks)),
        print(identify_fields(parsed_rules, your_tick, nearby_ticks))



if __name__ == "__main__":
    main(sys.argv)

