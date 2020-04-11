import sys
import numpy as np
import matplotlib.pyplot as plot
from maze import *
from dice import Dice
from node import Node
from heuristic import Heuristic
from priorityQueue import PriorityQueue

class Problem:
    __slots__ = 'maze'

    def __init__(self, maze):
        self.maze = maze

    def get_start_state(self):
        x, y = self.maze.get_start_pos()
        if (x, y, 1, 3, 2) not in self.maze.nodeMap.keys():
            aDice = Dice()
            aNode = Node(self.maze, aDice, 'S', 0, None, x, y, None)
            self.maze.nodeMap[(x, y, 1, 3, 2)] = aNode
        return self.maze.nodeMap[(x, y, 1, 3, 2)]

    def get_successors(self, state):
        return state.get_successor_state()

    def is_goal_state(self, state):
        return state.get_name() == 'G' and state.dice.top == 1

    def get_goal_state(self):
        x, y = self.maze.get_goal_pos()
        if (x, y, 1) not in self.maze.nodeMap.keys():
            aDice = Dice()
            aNode = Node(self.maze, aDice, 'G', None, None, x, y, None)
            self.maze.nodeMap[(x, y, 1)] = aNode
        return self.maze.nodeMap[(x, y, 1)]

    def get_start_position(self):
        return self.maze.get_start_pos()

    def get_goal_position(self):
        return self.maze.get_goal_pos()

    def get_cost_of_action(self, actions=None):
        return 1


def a_star_search(problem, heuristicName, fringe, visitedNodes):
    startState = problem.get_start_state()
    heuristic = getattr(Heuristic, heuristicName)
    startState.set_F_cost(0 + heuristic(startState, problem))
    fringe.insert(startState)

    while not fringe.is_empty():
        curState = fringe.pop()

        if problem.is_goal_state(curState):
            print('SUCCESS')
            visitedNodes.add(curState)
            return curState

        if curState not in visitedNodes:
            visitedNodes.add(curState)

            for childState in problem.get_successors(curState):
                if childState not in visitedNodes:

                    if childState in fringe.queue:

                        location = fringe.find(childState)
                        tempNode = fringe.queue[location]
                        childStateFCost = curState.get_G_cost() + problem.get_cost_of_action() + \
                                          heuristic(childState, problem)

                        if childStateFCost < tempNode.get_F_cost():
                            childState.set_G_cost(curState.get_G_cost() + problem.get_cost_of_action())
                            hDist = heuristic(childState, problem)
                            childState.set_F_cost(childState.get_G_cost() + hDist)
                            childState.set_parent(curState)
                            fringe.update(childState)
                    else:
                        childState.set_G_cost(curState.get_G_cost() + problem.get_cost_of_action())
                        hDist = heuristic(childState, problem)
                        childState.set_F_cost(childState.get_G_cost() + hDist)
                        fringe.insert(childState)

    print("FAILURE")
    return None


class Game:
    @staticmethod
    def run(layout, heuristic):
        layoutText = load_maze(layout)
        currentMaze = Maze(layoutText)
        aMaze = Maze(layoutText)
        aProblem = Problem(aMaze)
        numberOfMoves = 0

        fringe = PriorityQueue()
        visitedNodes = set()

        goal = a_star_search(aProblem, heuristic, fringe, visitedNodes)
        path = list()

        while goal is not None:
            path.insert(0, goal)
            numberOfMoves += 1
            goal = goal.get_parent()

        move = 0
        print("For Heuristics: ", heuristic)
        if len(path) > 0:
            print("|------------- STARTING MAZE--------------|\n")
            currentMaze.update_maze(path[0].get_x_coordinate(), path[0].get_y_coordinate(), "S")
            currentMaze.printMaze()
            print("\n|------------- STARTING DICE ORIENTATION--------------|\n")
            path[0].dice.display()

        for currentNode in path:
            print("\n|-------------------- MOVE: " + str(move) + " -------------------|\n")
            print("|------------- MAZE--------------|\n")
            currentMaze.update_maze(currentNode.get_x_coordinate(), currentNode.get_y_coordinate(), '#')
            currentMaze.printMaze()
            print("\n|------------- DICE--------------|\n")
            currentNode.dice.display()
            move += 1

        print("\n|---------------- PERFORMANCE METRICS -----------------|\n")
        print("No. of moves in the solution                    : ", numberOfMoves - 1)
        print("No. of nodes put on the queue                   : ", fringe.nodesPutOnQueue)
        print("No. of nodes visited / removed from the queue   : ", len(visitedNodes))
        print("\n|------------------------------------------------------|\n")

        result = [heuristic, numberOfMoves - 1, fringe.nodesPutOnQueue, len(visitedNodes)]
        return result


def plots(results):
    bars = len(results)
    heuristic = [results[counter][0] for counter in range(len(results))]
    nodesPutOnQueue = [results[counter][2] for counter in range(len(results))]
    visitedNodes = [results[counter][3] for counter in range(len(results))]

    plot.subplots()
    index = np.arange(bars)
    bars_width = 0.25
    opacity = 1
    plot.bar(index, nodesPutOnQueue, bars_width, alpha=opacity, color='g', label='Nodes Generated')
    plot.bar(index + bars_width, visitedNodes, bars_width, alpha=opacity, color='y', label='Nodes Visited')
    plot.xlabel('Heuristic')
    plot.ylabel('Number of Nodes')
    plot.title('Heuristic Performance')
    plot.xticks(index + bars_width, heuristic)
    plot.legend()
    plot.show()


def main():
    results = []

    if len(sys.argv) != 2:
        print("Run in the following syntax: python3 rdMaze.py <Maze's filename>")
        
    elif len(sys.argv) == 2:
        layout = sys.argv[1]
        results.append(Game.run(layout, 'manhattan'))
        plots(results)
    

if __name__ == '__main__':
    main()