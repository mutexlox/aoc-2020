import collections
import sys

def get_ingredients(line):
    idx = line.index("(")
    return set(line[:idx].strip().split())

def get_allergens(line):
    idx = line.index("contains") + len("contains ")
    end = line.index(")", idx)
    l = line[idx:end].replace(",", "")
    return set(l.strip().split())

def find_non_allergens(lines):
    # Map allergens to possible encoded names
    d = {}
    all_ingredients = []
    for l in lines:
        ingredients = get_ingredients(l)
        all_ingredients.extend(ingredients)
        for allergen in get_allergens(l):
            if not allergen in d:
                d[allergen] = ingredients.copy()
            else:
                d[allergen] &= ingredients
    possible_allergens = set()
    for s in d.values():
        possible_allergens |= s
    count = 0
    for i in set(all_ingredients):
        if i not in possible_allergens:
            count += all_ingredients.count(i)
    return count, d
    
def find_canonical_list(d):
    canonical = {}
    while any(len(v) != 0 for v in d.values()):
        for k, v in d.items():
            if len(v) == 1:  # identified it
                item = list(v)[0]
                canonical[k] = item
                for v2 in d.values():
                    try:
                        v2.remove(item)
                    except KeyError:
                        pass
    l = sorted(canonical)
    s = canonical[l[0]]
    for i in range(1, len(l)):
        s += ",%s" % canonical[l[i]]

    return s


def main(argv):
    with open(argv[1]) as f:
        lines = [x.rstrip() for x in f]
        count, d = find_non_allergens(lines)
        print(count)
        print(find_canonical_list(d))

if __name__ == "__main__":
    main(sys.argv)


