import sys

def find_joltage_dist(nums):
    ones = 0
    threes = 0
    for i in range(len(nums) - 1):
        if nums[i] + 1 == nums[i + 1]:
            ones += 1
        elif nums[i] + 3 == nums[i + 1]:
            threes += 1
    return ones * threes

CACHE = {}

def num_possible_chains(nums):
    if tuple(nums) in CACHE:
        return CACHE[tuple(nums)]

    if len(nums) <= 2:
        return 1
    count = 0
    for i in range(1, min(4, len(nums) - 1)):
        if nums[i] - nums[0] <= 3:
            count += num_possible_chains(nums[i:])
    CACHE[tuple(nums)] = count
    return count


def main(argv):
    with open(argv[1]) as f:
        nums = sorted([int(x.rstrip()) for x in f])
        nums = [0] + nums + [nums[-1] + 3]

        print(find_joltage_dist(nums))
        print(num_possible_chains(nums))


if __name__ == "__main__":
    main(sys.argv)
