

import numpy as np
from NetworkManager import NetworkManager
from EnvironmentState import State
import math

LEFT = bytes.fromhex('00')
UP = bytes.fromhex('01')
RIGHT = bytes.fromhex('02')
DOWN = bytes.fromhex('03')
NOOP = bytes.fromhex('04')


def distance(a, b):
    return sum(abs(e1-e2) for e1, e2 in zip(a, b))


def getStates(currentState: State, opMap):
    head = np.array([currentState.body[0].x1, currentState.body[0].y1])
    return [head+opMap[op] for op in opMap.keys()]


def collisionDetection(p1, body):
    for line in body:
        if distance(p1, [line.x1, line.y1]) + distance(p1, [line.x2, line.y2]) == distance([line.x2, line.y2], [line.x1, line.y1]):
            return math.inf
    return 0


class Controller:

    def __init__(self, ip='localhost', port=4668):
        # Do not Modify
        self.networkMgr = NetworkManager()
        State.col_dim, State.row_dim = self.networkMgr.initiateConnection(
            ip, port)  # Initialize network manager and set environment dimensions
        self.state = State()  # Initialize empty state
        self.myInit()  # Initialize custom variables
        pass

    # define your variables here
    def myInit(self):
        self.opMap = {LEFT: [-1, 0], RIGHT: [1, 0], UP: [0, -1], DOWN: [0, 1]}
        self.ops = list(self.opMap.keys())
        pass

    def add_to_open(self, open, object):
        for objs in open:
            if object.x == objs.x and object.y == objs.y and object.f < objs.f:
                return True
        return False
    # Returns next command selected by the agent.

    def getNextCommand(self):
        food = list(self.state.food)
        states = getStates(self.state, self.opMap)
        cost = [distance(food, head)+collisionDetection(head,
                                                        self.state.body) for head in states]

        open = []
        # open.append(states)
        closed = []
        if len(open) > 0:
            # implementing A* search
            initialState = (self.state.body[0], self.state.body[1])
            goalState = food

            openedStates = []

            while len(open) > 0:
                # calculating g(x)
                costIncured = distance(
                    initialState, (self.state.body[0], self.state.body[1]))

            # calculating h(x)
            x = self.state.body[0]
            y = self.state.body[1]
            m = [((x-1, y), RIGHT), ((x+1, y), LEFT),
                 ((x, y-1), DOWN), ((x, y+1), UP)]
            moves = []
            for a, b in m:
                if a[0] == self.state.body[0][0] and a[1] == self.state.body[0][1]:
                    continue
                else:
                    moves.append((a, b))
            minCost = 0
            for move in moves:
                cost = [distance(food, move) +
                        collisionDetection(move, self.state.body)]
                index = move
                # backtracking
                openedStates.append(move)
            if cost < minCost:
                minCost = cost
                return self.ops[moves[index]]

            # if path becomes less promising
            for openState in openedStates:
                if openState.object.x == open.object.x and openState.object.y == open.object.y:
                    path = (openState.object.x, openState.object.y)
                    openedStates.append(path)

                return self.ops[path]

        return self.ops[np.argmin(cost)]
        # return NOOP

    def agent(self):
        class Node:
            def __init__(self, x, y, parent=None, direction=None):
                self.f = 0
                self.g = 0
                self.h = 0
                self.x = x
                self.y = y
                self.parent = parent
                self.direction = direction

            def __eq__(self, other):
                return self.position == other.position

            def __lt__(self, other):
                return self.f < other.f
        open = []
        closed = []
        start_node = Node(self.body[0], self.body[1], None)
        goal_node = Node(self.state.food[0], self.state.food[1], None)
        open.append(start_node)
        while len(open) > 0:
            # Sort the open list to get the node with the lowest cost first
            open.sort()
            # Get the node with the lowest cost
            current_node = open.pop(0)
            # Add the current node to the closed list
            closed.append(current_node)

            # Check if we have reached the goal, return the path
            if current_node.x == goal_node.x and current_node.y == goal_node.y:
                path = []
                while current_node != start_node:
                    path.append(current_node.direction)
                    current_node = current_node.parent
                return path[::-1]
            # Unzip the current node position
            (x, y) = current_node.position
            # Get neighbors
            neighbors = []
            n = [((x-1, y), RIGHT), ((x+1, y), LEFT),
                 ((x, y-1), DOWN), ((x, y+1), UP)]
            for neighbour, direction in n:
                if neighbour.x != self.body[0] or neighbour.y != self.body[1]:
                    neighbors.append((neighbour, direction))
            # Loop neighbors
            for next in neighbors:
                # Create a neighbor node
                neighbor = Node(next[0][0], next[0][1],
                                parent=current_node, direction=next[1])

                # Check if the neighbor is in the closed list
                if(neighbor in closed):
                    continue
                # Calculate heuristics (Manhattan distance)
                neighbor.g = abs(neighbor.position[0] - start_node.position[0]) + abs(
                    neighbor.position[1] - start_node.position[1])
                neighbor.h = abs(neighbor.position[0] - goal_node.position[0]) + abs(
                    neighbor.position[1] - goal_node.position[1])
                neighbor.f = neighbor.g + neighbor.h
                # Check if neighbor is in open list and if it has a lower f(x) value
                fopen = []
                for objs in open:
                    if object.x == objs.x and object.y == objs.y and object.f < objs.f:
                        fopen.append(neighbor)
                    else:
                        fopen.append(objs)
                open = fopen

                # if(add_to_open(open, neighbor) == True):
                #     # Everything is green, add neighbor to open list
                #     open.append(neighbor)
    def control(self):
        # Do not modify the order of operations.
        # Get current state, check exit condition and send next command.
        while(True):
            # 1. Get current state information from the server
            self.state.setState(self.networkMgr.getStateInfo())
            # 2. Check Exit condition
            if self.state.food == None:
                break
            # 3. Send next command
            self.networkMgr.sendCommand(self.getNextCommand())


cntrl = Controller()
cntrl.control()
