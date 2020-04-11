from dice import Dice

class Node:
    __slots__ = ('maze', 'dice', '__name', '__gCost', '__fCost', '__x', '__y', 'parent')
    def __init__(self, maze, dice, name, gCost, fCost, x, y, parent):
        
        self.__name = name
        self.__gCost = gCost
        self.__fCost = fCost
        self.__x = x
        self.__y = y
        self.parent = parent
        self.maze = maze
        self.dice = dice

    def get_name(self):
        return self.__name

    def get_parent(self):
        return self.parent

    def get_x_coordinate(self):
        return self.__x

    def get_y_coordinate(self):
        return self.__y

    def get_position(self):
        return self.__x, self.__y

    def get_F_cost(self):
        return self.__fCost

    def get_G_cost(self):
        return self.__gCost

    def get_Dice(self):
        return self.dice

    def __str__(self):
        return "(Symbol: '" + str(self.get_name()) + \
               "' Position: (" + str(self.__x) + "," + str(self.__y) + \
               ") Cost: " + str(self.__fCost) + \
               " DiceTop: " + str(self.dice.top) + ")"

    def set_name(self, name):
        self.__name = name

    def set_parent(self, node):
        self.parent = node

    def set_F_cost(self, cost):
        self.__fCost = cost

    def set_G_cost(self, cost):
        self.__gCost = cost

    def get_successor_state(self):
        successors = list()
        neighbors = self.maze.get_valid_neighbors(self.__x, self.__y, self.dice)

        for neighbor in neighbors:
            if neighbor in self.maze.nodeMap.keys():
                if self.maze.nodeMap[neighbor].get_name() == 'G':
                    goal_parent = self.maze.nodeMap[neighbor].get_parent()
                    if goal_parent is None:
                        self.maze.nodeMap[neighbor].set_parent(self)
                successors.append(self.maze.nodeMap[neighbor])
            else:
                x, y = neighbor[0], neighbor[1]
                neighborDice = Dice(neighbor[2], neighbor[3], neighbor[4])
                if self.maze.isGoal(x, y, neighborDice.top):
                    name = 'G'
                elif self.maze.get_start_pos == (x, y):
                    name = 'S'
                else: name = '.'
                if neighborDice.top != 6:
                    # Avoiding the goal location with wrong configuration
                    if self.maze.isGoalLocation(x, y) and \
                            not self.maze.isGoal(x, y, neighborDice.top):
                        continue
                    aNode = Node(self.maze, neighborDice, name, None, None, x, y, self)
                    self.maze.nodeMap[neighbor] = aNode
                    successors.append(aNode)

        return successors