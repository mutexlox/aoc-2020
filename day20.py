import math
import copy
import collections
import sys
import re

class Tile:
    def __init__(self, lines):
        self.lines = lines
        left = []
        right = []
        for l in lines:
            left += l[0]
            right += l[-1]
        # Top, right, bottom, left
        self.edges = [lines[0], right, lines[-1], left]
        # Maps original index of edge to new index, along
        # with whether it's reversed
        self.edge_order = [(False, 0), (False, 1), (False, 2), (False, 3)]

    def vert_flip(self):
        self.lines = list(reversed(self.lines))
        self.edges = [self.edges[2], list(reversed(self.edges[1])),
                      self.edges[0], list(reversed(self.edges[3]))]
        for i in range(len(self.edge_order)):
            if self.edge_order[i][1] % 2 == 0:
                # Doesn't reverse, but does move.
                self.edge_order[i] = (self.edge_order[i][0],
                                      (self.edge_order[i][1] + 2) % 4)
            else:
                # Reverses but doesn't move.
                self.edge_order[i] = (not self.edge_order[i][0],
                                      self.edge_order[i][1])

    def rotate(self, count=1):
        for c in range(count):
            new = [['.' for _ in l] for l in self.lines]
            for i in range(len(self.lines)):
                for j in range(len(self.lines[i])):
                    new[j][len(self.lines) - i - 1] = self.lines[i][j]
            self.lines = new
            for i in range(len(self.edge_order)):
                rev = self.edge_order[i][1] % 2 != 0
                self.edge_order[i] = (rev ^ self.edge_order[i][0],
                                      (self.edge_order[i][1] + 1) % 4)
            self.edges = [list(reversed(self.edges[3])), self.edges[0],
                          list(reversed(self.edges[1])), self.edges[2]]

    def get_edges_to(self, edge_goals):
        """Given a set of edge constraints, get the edges to match.

        edge_goals: a length-four list, possibly containing Nones, of what
        we want edge_order to match. Nones are ignored.

        Returns: True iff we could match the constraints.
        """
        for other in self.all_rotations():
            works = True
            for i in range(len(other.edge_order)):
                if edge_goals[i] is not None:
                    if edge_goals[i][1] != other.edge_order[i][1]:
                        works = False
                        break
                    if (edge_goals[i][0] != None and
                        edge_goals[i][0] != other.edge_order[i][0]):
                        works = False
                        break
            if works:
                self.lines = other.lines
                self.edges = other.edges
                self.edge_order = other.edge_order
                return True
        return False

    def all_rotations(self):
        clone = copy.deepcopy(self)
        for i in range(0, 4):
            clone.rotate(i)
            yield clone
            clone.vert_flip()
            yield clone
            # Put it back
            clone.vert_flip()
            clone.rotate((4-i) % 4)


    def count_water_roughness(self):
        num_hashes = 0
        for l in self.lines:
            for c in l:
                if c == '#':
                    num_hashes += 1

        top_re =    re.compile('..................#.')
        middle_re = re.compile('#....##....##....###')
        bottom_re = re.compile('.#..#..#..#..#..#...')
        sea_monster_hashes = 15

        count = 0
        for i in range(1, len(self.lines) - 1):
            for match in middle_re.finditer(''.join(self.lines[i])):
                s = match.start()
                if (top_re.match(''.join(self.lines[i - 1]), s) and
                    bottom_re.match(''.join(self.lines[i + 1]), s)):
                    count += 1
        if count == 0:
            return None
        return num_hashes - sea_monster_hashes * count


def prod(l):
    o = 1
    for x in l:
        o *= x
    return o

def rotate_and_align_tiles(tiles):
    matches = collections.defaultdict(list)
    # First, determine which edges can be next to each other...
    keys = list(tiles)
    for i in range(len(keys)):
        id_i = keys[i]
        ti = tiles[id_i]
        for j in range(i + 1, len(keys)):
            id_j = keys[j]
            tj = tiles[id_j]
            for ei in range(len(ti.edges)):
                for ej in range(len(tj.edges)):
                    if ti.edges[ei] == tj.edges[ej]:
                        matches[id_i].append((id_j, ei, ej, False))
                        matches[id_j].append((id_i, ej, ei, False))
                    elif ti.edges[ei] == list(reversed(tj.edges[ej])):
                        matches[id_i].append((id_j, ei, ej, True))
                        matches[id_j].append((id_i, ej, ei, True))

    # Now find the corners
    corners = [m for m in matches if len(matches[m]) == 2]
    print("part 1: %d" % prod(corners))

    line_size = int(math.sqrt(len(tiles)))
    compiled = [[[] for _i in range(line_size)] for _j in range(line_size)]

    # arbitrarily say corners[0] is top left at first.
    top_left_id = corners[0]
    top_left_match = matches[top_left_id]
    top_left = tiles[top_left_id]

    # Arbitrarily orient how we want; it'll just be off by rotations and flips
    # at worst.
    want = [None, None, None, None]
    want[top_left_match[0][1]] = (None, 1)
    want[top_left_match[1][1]] = (None, 2)
    assert(top_left.get_edges_to(want))

    compiled[0][0] = top_left_id

    done = {}
    done[top_left_id] = (0,0)
    next_tiles = [top_left_match[0][0], top_left_match[1][0]]

    # OK, now we have one of them. get the rest.
    while next_tiles:
        next_id = next_tiles.pop(0)
        neighbors = matches[next_id]
        tile = tiles[next_id]
        want = [None, None, None, None]

        placed_match = None

        # Find the proper alignment
        for i in range(len(neighbors)):
            n = neighbors[i]
            if n[0] not in done:
                if n[0] not in next_tiles:
                    next_tiles.append(n[0])
                continue
            match_tile = tiles[n[0]]
            new_orient, new_neigh_idx = match_tile.edge_order[n[2]]
            neighbors[i] = (n[0], n[1], new_neigh_idx, new_orient ^ n[3])
            n = neighbors[i]
            want[n[1]] = (n[3], (n[2] + 2) % 4)
            if placed_match is None:
                placed_match = n

        assert(tile.get_edges_to(want))

        # Find where it should go in relation to placed_match.
        _, matching_edge = tile.edge_order[placed_match[1]]

        coords = done[placed_match[0]]
        if matching_edge == 0:
            # Below neighbor
            coords = (coords[0] + 1, coords[1])
        elif matching_edge == 1:
            # To the left of neighbor
            coords = (coords[0], coords[1] - 1)
        elif matching_edge == 2:
            # Below neighbor
            coords = (coords[0] - 1, coords[1])
        elif matching_edge == 3:
            # To the right of neighbor
            coords = (coords[0], coords[1] + 1)
        compiled[coords[0]][coords[1]] = next_id
        done[next_id] = coords

    # Now we've oriented and assembled all tiles. Combine them into an image.
    line_size = (len(tiles[compiled[0][0]].lines) - 2) * line_size
    image = [['.' for _i in range(line_size)] for _j in range(line_size)]
    for tile_x in range(len(compiled)):
        for tile_y in range(len(compiled[0])):
            tile = tiles[compiled[tile_x][tile_y]]
            multiplier = len(tile.lines) - 2
            for internal_x in range(1, len(tile.lines) - 1):
                for internal_y in range(1, len(tile.lines[0]) - 1):
                    x = multiplier * tile_x + internal_x - 1
                    y = multiplier * tile_y + internal_y - 1
                    image[x][y] = tile.lines[internal_x][internal_y]

    image = Tile(image)
    for r in image.all_rotations():
        c = r.count_water_roughness()
        if c is not None:
            print(c)

def main(argv):
    with open(argv[1]) as f:
        lines = [x.rstrip() for x in f]
        tiles = {}
        i = 0
        while i < len(lines):
            tile_id = int(lines[i].split(' ')[1][:-1])
            i += 1
            tile_spec = []
            while i < len(lines) and lines[i].strip():
                tile_spec.append([c for c in lines[i].strip()])
                i += 1
            tiles[tile_id] = Tile(tile_spec)
            i += 1
        rotate_and_align_tiles(tiles)

if __name__ == "__main__":
    main(sys.argv)

