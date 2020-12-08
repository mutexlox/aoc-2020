import sys

def fix(prog):
    """Run and fix the program"""
    for i in range(len(prog)):
        op, arg = prog[i].split()
        # Attempt each replacement...
        if op == 'jmp':
            prog[i] = 'nop ' + arg
        elif op == 'nop':
            prog[i] = 'jmp ' + arg
        # ... and see if it worked
        acc, worked = interpret(prog)
        if worked:
            return acc
        prog[i] = op + ' ' + arg
    return None


def interpret(prog):
    acc = 0
    visited = set()
    pc = 0
    while pc not in visited and pc < len(prog):
        visited.add(pc)
        ins, arg = prog[pc].split()
        if ins == 'nop':
            pass
        elif ins == 'acc':
            acc += int(arg)
        elif ins == 'jmp':
            pc += int(arg)
            continue
        pc += 1
    return acc, pc >= len(prog)


def main(argv):
    with open(argv[1]) as f:
        lines = [x.rstrip() for x in f]
        print(interpret(lines)[0])
        print(fix(lines))

if __name__ == "__main__":
    main(sys.argv)
