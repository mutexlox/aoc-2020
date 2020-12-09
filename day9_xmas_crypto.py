import sys

PREAMBLE_LEN = 25

def find_first_nonmatching(nums):
    preamble_start = 0
    s = set(nums[:PREAMBLE_LEN])
    for i in xrange(PREAMBLE_LEN, len(nums)):
        want = nums[i]
        good = False
        for i in xrange(preamble_start, preamble_start + PREAMBLE_LEN):
            if want - nums[i] in s:
                good = True
                break
        s.remove(nums[preamble_start])
        s.add(nums[preamble_start + PREAMBLE_LEN])
        preamble_start += 1
        if not good:
            return want
    return None


def find_contiguous_set(nums, target):
    for i in xrange(len(nums)):
        for j in xrange(i + 1, len(nums)):
            s = sum(nums[i:j])
            if s == target:
                return min(nums[i:j]) + max(nums[i:j])
            elif s > target:
                break  # can't get there by adding more; all positive


def main(argv):
    with open(argv[1]) as f:
        nums = [int(x.rstrip()) for x in f]
        first = find_first_nonmatching(nums)
        print(first)
        print(find_contiguous_set(nums, first))



if __name__ == "__main__":
    main(sys.argv)
