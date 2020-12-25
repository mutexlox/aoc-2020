import re
import sys

def build_rules(rules_lines):
    d = {}
    for r in rules_lines:
        num, rest = r.split(':')
        num = int(num)
        rest = rest.strip().split()
        opts = [[]]
        for r in rest:
            if r == '|':
                opts.append([])
            else:
                try:
                    val = int(r)
                except ValueError:
                    val = r[1:-1]
                opts[-1].append(val)
        d[num] = opts
    return d

def regexify(rules, rule=0):
    out = ""
    for opt in rules[rule]:
        for r in opt:
            if isinstance(r, int):
                inner = regexify(rules, r)
                if inner.find("|") != -1:
                    out += "(" + inner  + ")"
                else:
                    out += inner
            else:
                out += r
        out += "|"
    return out[:-1]

def regexify_pt2(rules, rule=0):
    out = ""
    if rule == 0:
        # Rule 0 is roughly equivalent to (42)^n (31)^m where n > m > 0
        return ("(?:" + regexify_pt2(rules, 42) + "){n}" +
               "(?:" + regexify_pt2(rules, 31) + "){m}")
    for opt in rules[rule]:
        for r in opt:
            if isinstance(r, int):
                inner = regexify_pt2(rules, r)
                if inner.find("|") != -1:
                    out += "(?:" + inner  + ")"
                else:
                    out += inner
            else:
                out += r
        out += "|"
    return out[:-1]

def get_summary(matches):
    chunks = []
    current_start = -1
    current_end = -1
    count = 0
    for m in matches:
        if current_start == -1:
            current_start = m.start()
            current_end = m.end()
            count = 1
        elif m.start() == current_end:
            current_end = m.end()
            count += 1
        else:
            chunks.append((current_start, current_end, count))
            current_start = m.start()
            current_end = m.end()
            count = 1
    return chunks


def matches_pt2(regex, l):
    for m in range(1, 10):
        for n in range(m + 1, 10):
            # Rule 0 is roughly equivalent to (42)^n (31)^m where n > m > 0
            re_to_use = regex.replace('n', str(n)).replace('m', str(m))
            if re.fullmatch(re_to_use, l):
                return True
    return False

def count_matches(rules, lines):
    count = 0
    regex = re.compile(regexify(rules, 0))
    for l in lines:
        if re.fullmatch(regex, l):
            count += 1
    return count

def count_matches_pt2(rules, lines):
    regex = regexify_pt2(rules, 0)
    count = 0
    for l in lines:
        if matches_pt2(regex, l):
            count += 1
    return count

def get_lines(f):
    rules = []
    lines = []
    seen_newline = False
    for line in f:
        line = line.strip()
        if not line:
            seen_newline = True
            continue
        if not seen_newline:
            rules.append(line)
        else:
            lines.append(line)
    return build_rules(rules), lines

def main(argv):
    with open(argv[1]) as f:
        rules, lines = get_lines(f)
        print(count_matches(rules, lines))
        print(count_matches_pt2(rules, lines))


if __name__ == "__main__":
    main(sys.argv)

