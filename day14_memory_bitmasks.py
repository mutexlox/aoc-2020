import sys

def evaluate(lines):
    mask_line = lines[0]
    mask_str = mask_line.split('=')[1].strip()
    or_mask = int(mask_str.replace('X', '0'), 2)
    and_mask = int(mask_str.replace('X', '1'), 2)
    mem = {}
    for l in lines:
        if l.startswith('mask = '):
            mask_line = l
            mask_str = mask_line.split('=')[1].strip()
            or_mask = int(mask_str.replace('X', '0'), 2)
            and_mask = int(mask_str.replace('X', '1'), 2)
        else:
            idx, val = [s.strip() for s in l.split('=')]
            val = int(val)
            idx = int(idx[4:idx.index(']')])
            mem[idx] = (val | or_mask) & and_mask
    return sum(mem.values())


def get_floating_idxs(idx, mask_str):
    idxs = []
    i = mask_str.find('X')
    if i== -1:
        return [idx]
    else:
        new_mask = mask_str[:i] + '0' + mask_str[i + 1:]
        new_idx = idx & (~ (1 << (36 - i - 1)))
        idxs.extend(get_floating_idxs(new_idx, new_mask))
        new_idx = idx | (1 << (36 - i - 1))
        idxs.extend(get_floating_idxs(new_idx, new_mask))
    return idxs


def evaluate_pt2(lines):
    mask_line = lines[0]
    mask_str = mask_line.split('=')[1].strip()
    or_mask = int(mask_str.replace('X', '0'), 2)
    mem = {}
    for l in lines:
        if l.startswith('mask = '):
            mask_line = l
            mask_str = mask_line.split('=')[1].strip()
            or_mask = int(mask_str.replace('X', '0'), 2)
        else:
            idx, val = [s.strip() for s in l.split('=')]
            val = int(val)
            idx = int(idx[4:idx.index(']')]) | or_mask
            for new_idx in get_floating_idxs(idx, mask_str):
                mem[new_idx] = val
    return sum(mem.values())


def main(argv):
    with open(argv[1]) as f:
        lines = [x.rstrip() for x in f]
        print(evaluate(lines))
        print(evaluate_pt2(lines))


if __name__ == "__main__":
    main(sys.argv)
