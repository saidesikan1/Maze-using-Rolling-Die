class PriorityQueue:
    __slots__ = 'queue', 'nodesPutOnQueue', 'nodesTakenOff'

    def __init__(self):
        self.queue = list()
        self.nodesPutOnQueue = 0
        self.nodesTakenOff = 0

    def insert(self, node):
        self.queue.append(node)
        self.nodesPutOnQueue += 1
        self.__heapify(len(self.queue) - 1)

    def replace(self, node, location):
        self.queue.insert(node, location)
        self.__heapify(location - 1)

    def pop(self):
        if len(self.queue) > 0:
            node = self.queue.pop(0)
            self.nodesTakenOff += 1
            if len(self.queue) > 0:
                self.queue.insert(0, self.queue.pop(-1))
                self.__bubble_down(0)
            return node

    def __heapify(self, loc):
        while loc > 0:
            parent_loc = self.getParent(loc)
            if self.queue[loc].get_F_cost() < self.queue[parent_loc].get_F_cost():
                self.queue[loc], self.queue[parent_loc] = self.queue[parent_loc], self.queue[loc]
                loc = parent_loc
            else:
                break

    def __bubble_down(self, loc):
        while 2 * loc + 1 <= len(self.queue) - 1:
            swap_loc = self.__get_min_neighbour(loc)
            if swap_loc == loc:
                break
            else:
                self.queue[loc], self.queue[swap_loc] = self.queue[swap_loc], self.queue[loc]
                loc = swap_loc

    def __get_min_neighbour(self, loc):
        child1 = self.queue[2 * loc + 1]
        if len(self.queue) - 1 < 2 * loc + 2:
            min_val = min(self.queue[loc].get_F_cost(), child1.get_F_cost())
            if self.queue[loc].get_F_cost() == min_val:
                return loc
            elif child1.get_F_cost() == min_val:
                return 2 * loc + 1

        else:
            child2 = self.queue[2 * loc + 2]
            min_val = min(self.queue[loc].get_F_cost(), child1.get_F_cost(), child2.get_F_cost())
            if self.queue[loc].get_F_cost() == min_val:
                return loc
            elif child1.get_F_cost() == min_val:
                return 2 * loc + 1
            else:
                return 2 * loc + 2

    def find(self, node):
        for loc in range(len(self.queue)):
            if node is self.queue[loc]:
                return loc
        return None

    def update(self, node):
        loc = self.find(node)
        self.__heapify(loc)

    def is_empty(self):
        return len(self.queue) == 0

    def getParent(self, loc):
        return (loc - 1) // 2
