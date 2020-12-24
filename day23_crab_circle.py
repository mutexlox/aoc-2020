import collections
import sys

class List:
    def __init__(self, items):
        self.mini = items[0]
        self.maxi = items[0]
        self.head = None
        self.tail = None
        self.nodes = {}
        for item in items:
            if item < self.mini:
                self.mini = item
            if item > self.maxi:
                self.maxi = item
            self.insert_after(self.tail, item)

    def insert_after(self, node, item):
        n = Node(item)
        self.nodes[item] = n
        if self.head is None:
            self.head = n
            self.tail = n
            n.next = n
        else:
            n.next = node.next
            node.next = n
            if node == self.tail:
                self.tail = n

    def remove_after(self, node):
        val = node.next.label
        del self.nodes[val]
        if node.next == self.head:
            self.head = self.head.next
        if node.next == self.tail:
            self.tail = node
        node.next = node.next.next
        return val

    def find_node(self, val):
        return self.nodes[val]

    def advance_head(self):
        self.head = self.head.next
        self.tail = self.tail.next

class Node:
    def __init__(self, label):
        self.label = label
        self.next = self


def step(state):
    picked = []
    cur_label = state.head.label
    for i in range(3):
        picked.append(state.remove_after(state.head))
    dest_label = cur_label - 1

    if dest_label < state.mini:
        dest_label = state.maxi
    while dest_label in picked:
        dest_label -= 1
        if dest_label < state.mini:
            dest_label = state.maxi

    dest = state.find_node(dest_label)
    for i in range(len(picked)):
        state.insert_after(dest, picked[i])
        dest = dest.next
    state.advance_head()


def do_game(start, steps):
    state = List(start)
    for i in range(steps):
        step(state)
    one_node = state.find_node(1)
    out = ""
    node = one_node.next
    while node != one_node:
        out += str(node.label)
        node = node.next
    return out


def do_big_game(start, steps):
    state = List(start)
    for i in range(steps):
        step(state)
    one_node = state.find_node(1)
    return one_node.next.label * one_node.next.next.label

def main(argv):
    inp_test = [3, 8, 9, 1, 2,5,4,6,7]
    inp = [9, 6, 2, 7, 1, 3, 8, 5, 4]
    print(do_game(inp, 100))
    print(do_big_game(inp + list(range(10, 1000001)), 10000000))

if __name__ == "__main__":
    main(sys.argv)



