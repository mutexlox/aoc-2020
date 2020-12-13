import sys

DIRS = ['N', 'E', 'S', 'W']

def update_pos(move_dir, vert_pos, horiz_pos, i, face):
    if move_dir == 'N':
        vert_pos += i
    elif move_dir == 'S':
        vert_pos -= i
    elif move_dir == 'E':
        horiz_pos += i
    elif move_dir == 'W':
        horiz_pos -= i
    elif move_dir == 'F':
        return update_pos(face, vert_pos, horiz_pos, i, face)
    elif move_dir == 'B':
        return update_pos(face, vert_pos, horiz_pos, -i, face)
    elif move_dir == 'L':
        idx = DIRS.index(face)
        face = DIRS[(idx - i // 90) % len(DIRS)]
    elif move_dir == 'R':
        idx = DIRS.index(face)
        face = DIRS[(idx + i // 90) % len(DIRS)]
    return (vert_pos, horiz_pos, face)

def move(directions):
    vert_pos = 0
    horiz_pos = 0
    face = 'E'
    for d in directions:
        c = d[0]
        i = int(d[1:])
        (vert_pos, horiz_pos, face) = update_pos(c, vert_pos, horiz_pos, i, face)
    return abs(horiz_pos) + abs(vert_pos)


def move_pt2(directions):
    ship_vert = 0
    ship_horiz = 0
    waypoint_vert = 1
    waypoint_horiz = 10
    for d in directions:
        c = d[0]
        i = int(d[1:])
        if c == 'N':
            waypoint_vert += i
        elif c == 'S':
            waypoint_vert -= i
        elif c == 'E':
            waypoint_horiz += i
        elif c == 'W':
            waypoint_horiz -= i
        elif c == 'L':
            while i >= 90:
                waypoint_vert, waypoint_horiz = waypoint_horiz, -waypoint_vert
                i -= 90
        elif c == 'R':
            while i >= 90:
                waypoint_vert, waypoint_horiz = -waypoint_horiz, waypoint_vert
                i -= 90
        elif c == 'F':
            ship_vert += i * waypoint_vert
            ship_horiz += i * waypoint_horiz
    return abs(ship_vert) + abs(ship_horiz)

def main(argv):
    with open(argv[1]) as f:
        lines = [x.rstrip() for x in f]
        print(move(lines))
        print(move_pt2(lines))


if __name__ == "__main__":
    main(sys.argv)
