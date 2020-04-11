class Maze:
    def __init__(self, layoutText):
        self.width = len(layoutText[0])
        self.height = len(layoutText)
        self.obstacles = [[False for y in range(self.height)] for x in range(self.width)]
        self.maze_orientation = [[None for y in range(self.height)] for x in range(self.width)]
        self.starting_pos = (None, None)
        self.goal_pos = (None, None)
        self.process_layout(layoutText)
        self.nodeMap = {}

    def process_layout(self, layoutText):
        maxY = self.height - 1
        for y in range(self.height):
            for x in range(self.width):
                layoutChar = layoutText[maxY - y][x]
                self.maze_orientation[x][y] = layoutChar
                self.process_layout_char(x, y, layoutChar)

    def process_layout_char(self, x, y, layoutChar):
        if layoutChar == '*':
            self.obstacles[x][y] = True
        elif layoutChar == 'S':
            self.starting_pos = (x, y)
        elif layoutChar== 'G':
            self.goalPos = (x, y)

    def isObstacle(self, pos):
        if self.is_pos_in_maze(pos):
            x, y = pos
            return self.obstacles[x][y]

    def is_pos_in_maze(self, pos):
        x, y = pos
        return 0 <= x <= self.width - 1 and 0 <= y <= self.height - 1

    def get_valid_neighbors(self, x, y, dice):
        neighbors = list()
        if self.is_pos_in_maze((x - 1, y)) and not self.obstacles[x - 1][y]:
            dice.move_left()
            top = dice.top
            right = dice.right
            north = dice.north
            dice.move_right()
            neighbors.append((x - 1, y, top, right, north))

        if self.is_pos_in_maze((x + 1, y)) and not self.obstacles[x + 1][y]:
            dice.move_right()
            top = dice.top
            right = dice.right
            north = dice.north
            dice.move_left()
            neighbors.append((x + 1, y, top, right, north))

        if self.is_pos_in_maze((x, y - 1)) and not self.obstacles[x][y - 1]:
            dice.move_south()
            top = dice.top
            right = dice.right
            north = dice.north
            dice.move_north()
            neighbors.append((x, y - 1, top, right, north))

        if self.is_pos_in_maze((x, y + 1)) and not self.obstacles[x][y + 1]:
            dice.move_north()
            top = dice.top
            right = dice.right
            north = dice.north
            dice.move_south()
            neighbors.append((x, y + 1, top, right, north))

        return neighbors

    def isGoal(self, x, y, diceTop):
        return self.goalPos == (x, y) and diceTop == 1

    def isGoalLocation(self, x, y):
        return self.goalPos == (x, y)

    def get_start_pos(self):
        return self.starting_pos

    def get_goal_pos(self):
        return self.goalPos

    def update_maze(self, x, y, symbol):
        self.maze_orientation[x][y] = symbol

    def printMaze(self):
        for i in range(self.height - 1, -1, -1):
            for j in range(self.width):
                print(self.maze_orientation[j][i], end=" ")
            print()

def load_maze(fileName):
    layout = open(fileName)
    try:
        return [line.strip() for line in layout]
    finally:
        layout.close()