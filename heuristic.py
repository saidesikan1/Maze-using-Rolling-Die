import copy
import math

class Heuristic:
    @staticmethod
    def manhattan(curState, problem):
        pos1 = curState.get_position()
        pos2 = problem.get_goal_position()
        dx, dy = Heuristic.finddXdY(pos1, pos2)
        return dx + dy

    @staticmethod
    def finddXdY(pos1, pos2):
        dx = abs(pos1[0] - pos2[0])
        dy = abs(pos1[1] - pos2[1])
        return dx, dy

        rewardA = rewardB = 0

        if abs(dx) < 2 or abs(dy) < 2:

            temp_dice = copy.deepcopy(curState.getDice())
            if dx > 0:
                for moves in range(abs(dx) % 4):
                    temp_dice.move_left()
            else:
                for moves in range(abs(dx) % 4):
                    temp_dice.move_right()
            if dy > 0:
                for moves in range(abs(dy) % 4):
                    temp_dice.move_north()
            else:
                for moves in range(abs(dy) % 4):
                    temp_dice.move_south()

            if temp_dice.top == 1:
                rewardA = -.50

            temp_dice = copy.deepcopy(curState.getDice())
            if dy > 0:
                for moves in range(abs(dy) % 4):
                    temp_dice.move_north()
            else:
                for moves in range(abs(dy) % 4):
                    temp_dice.move_south()
            if dx > 0:
                for moves in range(abs(dx) % 4):
                        temp_dice.move_left()
            else:
                for moves in range(abs(dx) % 4):
                    temp_dice.move_right()

            if temp_dice.top == 1:
                rewardB = -.50

        return manhattanDist + min(rewardA, rewardB)

    @staticmethod
    def forecast_manhattan(curState, problem):
        manhattanDist = Heuristic.manhattan(curState, problem)
        neighbours = problem.maze.get_valid_neighbors(curState.get_x_coordinate(),
                                                    curState.get_y_coordinate(),
                                                    curState.getDice())
        validNeighbours = [neighbour for neighbour in neighbours
                           if neighbour[2] != 6]

        totalPenalty = 0
        if len(validNeighbours) == 1:
            return manhattanDist + 1

        return manhattanDist + totalPenalty
