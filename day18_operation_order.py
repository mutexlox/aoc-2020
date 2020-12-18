import sys

def get_matching_paren(tokens, i):
    assert(tokens[i] == "(")
    num_paren = 1
    i += 1
    while i < len(tokens) and num_paren > 0:
        if tokens[i] == "(":
            num_paren += 1
        elif tokens[i] == ")":
            num_paren -= 1
        i += 1
    assert(num_paren == 0)
    return i - 1


def tokenize(line):
    tokens = []
    cur_tok = ""
    for c in line:
        if c == " ":
            if cur_tok != "":
                tokens.append(cur_tok)
                cur_tok = ""
        elif c in ("(", ")"):
            if cur_tok:
                tokens.append(cur_tok)
                cur_tok = ""
            tokens.append(c)
        else:
            cur_tok += c
    if cur_tok:
        tokens.append(cur_tok)
    return tokens


def eval_ltr(tokens):
    i = 0
    if tokens[i] == "(":
        match = get_matching_paren(tokens, i)
        accum = eval_ltr(tokens[i+1:match])
        i = match + 1
    else:
        accum = int(tokens[i])
        i += 1
    while i < len(tokens):
        op = tokens[i]
        i += 1

        if tokens[i] == "(":
            match = get_matching_paren(tokens, i)
            cur = eval_ltr(tokens[i + 1:match])
            i = match + 1
        else:
            cur = int(tokens[i])
            i += 1

        if op == "+":
            accum += cur
        else:
            assert(op == "*")
            accum *= cur

    return accum


def prod(it):
    acc = 1
    for x in it:
        acc *= x
    return acc


def eval_adds_first(tokens):
    i = 0
    if tokens[i] == "(":
        match = get_matching_paren(tokens, i)
        tokens[i] = eval_adds_first(tokens[i+1:match])
        tokens = tokens[:i + 1] + tokens[match + 1:]
        i += 1
    else:
        tokens[i] = int(tokens[i])
        i += 1

    # first do +
    while i < len(tokens):
        op = tokens[i]
        i += 1

        if tokens[i] == "(":
            match = get_matching_paren(tokens, i)
            tokens[i] = eval_adds_first(tokens[i+1:match])
            tokens = tokens[:i + 1] + tokens[match + 1:]
        else:
            tokens[i] = int(tokens[i])


        if op == "*":
            # Leave it for now...
            i += 1
            continue

        if op == "+":
            tokens[i - 2] = tokens[i - 2] + tokens[i]
            tokens = tokens[:i - 1] + tokens[i + 1:]
            i -= 1
        else:
            assert(op == "*")
            pass

    # Then do *
    return prod(x for x in tokens if isinstance(x, int))


def eval_all_ltr(lines):
    return sum(eval_ltr(tokenize(l)) for l in lines)


def eval_all_add_first(lines):
    return sum(eval_adds_first(tokenize(l)) for l in lines)


def main(argv):
    with open(argv[1]) as f:
        lines = [x.rstrip() for x in f]
        print(eval_all_ltr(lines))
        print(eval_all_add_first(lines))

if __name__ == "__main__":
    main(sys.argv)


