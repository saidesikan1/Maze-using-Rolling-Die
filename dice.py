class Dice:
    __slots__ = ("top", "right", "north", "sum")

    def __init__(self, top =1, right=3, north=2):
        self.top = top
        self.right = right
        self.north = north
        self.sum = 7

    def move_right(self):
        self.top, self.right = self.sum - self.right, self.top

    def move_left(self):
        self.top, self.right = self.right, self.sum - self.top

    def move_north(self):
        self.top, self.north = self.sum - self.north, self.top

    def move_south(self):
        self.top, self.north = self.north, self.sum - self.top

    def move(self, moveName):
        if moveName == 'move_left':
            self.move_left()
        elif moveName == 'move_right':
            self.move_right()
        elif moveName == 'move_south':
            self.move_south()
        elif moveName == 'move_north':
            self.move_north()

    def display(self):
        print("\t ", self.north, end="")
        print("\t" * 7, "NORTH")
        print("\t ", "|", end="")
        print("\t " * 7, "|")
        print(self.sum - self.right, "-", self.top, "/", self.sum - self.top, "-", self.right, end="")
        print("\t" * 2, "LEFT", "-", "TOP", "/", "BOTTOM", "-", "RIGHT")
        print("\t ", "|", end="")
        print("\t " * 7, "|")
        print("\t ", self.sum - self.north, end="")
        print("\t" * 7, "SOUTH", end="\n")