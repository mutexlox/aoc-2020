import sys
import re

REQUIRED_FIELDS=['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']

def has_all_fields(p):
    for f in REQUIRED_FIELDS:
        if not f in p:
            return False
    return True

def is_valid_passport(p):
    if not has_all_fields(p):
        return False

    # Validate each field
    fields = p.split()
    for f in fields:
        label, val = f.split(':')
        if label.endswith('yr'):
            if len(val) != 4:
                return False

            try:
                val = int(val)
            except ValueError:
                return False

            if label == 'byr':
                if not(val >= 1920 and val <= 2002):
                    return False
            elif label == 'iyr':
                if not(val >= 2010 and val <= 2020):
                    return False
            elif label == 'eyr':
                if not(val >= 2020 and val <= 2030):
                    return False
        elif label == 'hgt':
            try:
                int_part = int(val[:-2])
            except ValueError:
                return False
            if val[-2:] == 'cm':
                if not(int_part >= 150 and int_part <= 193):
                    return False
            elif val[-2:] == 'in':
                if not(int_part >= 59 and int_part <= 76):
                    return False
            else:
                return False
        elif label == 'hcl':
            if not(re.match('^#[0-9a-f]{6}$', val)):
                return False
        elif label == 'ecl':
            if val not in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'):
                return False
        elif label == 'pid':
            if not(re.match('^[0-9]{9}$', val)):
                return False

    return True

def count_valid_passports(lines):
    curr_pass = []
    lines.append("")
    loose, strict = 0, 0
    for l in lines:
        if not l:
            p = " ".join(curr_pass)
            if has_all_fields(p):
                loose += 1
            if is_valid_passport(p):
                strict += 1
            curr_pass = []
        else:
            curr_pass.append(l)
    return loose, strict

def main(argv):
    with open(argv[1]) as f:
        lines = [x.rstrip() for x in f]
        print(count_valid_passports(lines))


if __name__ == "__main__":
    main(sys.argv)
