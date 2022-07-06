import cv2
import numpy as np
from warnings import warn
import heapq
from math import sqrt

class Node:
    """
    A node class for A* Pathfinding
    """

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __repr__(self):
      return f"{self.position} - g: {self.g} h: {self.h} f: {self.f}"

    # defining less than for purposes of heap queue
    def __lt__(self, other):
      return self.f < other.f

    # defining greater than for purposes of heap queue
    def __gt__(self, other):
      return self.f > other.f

# algorithm to find holes in skeleton and fill them with white
def fill_thinned_holes(thn):
    holes = []
    for i in range(1,len(thn)-1):
        for j in range(1,len(thn[i])-1):
            if (thn[i][j] == 0):
                # checks conditions of holes. if it's a hole, record index to fill later.
                if (    (thn[i+1][j] and thn[i][j+1] and not thn[i+1][j+1])
                    or  (thn[i][j-1] and thn[i+1][j] and not thn[i+1][j-1])
                    or  (thn[i-1][j] and thn[i][j+1] and not thn[i-1][j+1])
                    or  (thn[i][j-1] and thn[i-1][j] and not thn[i-1][j-1]) ):
                    holes.append((i,j))
    # now fill all holes white
    for h in holes:
        i, j = h[0], h[1]
        thn[i][j] = 255

def thin_maze_image(folder,name):
    path = folder+'/'+name
    image = cv2.imread(path,0)

    # convert maze image into 1px-wide skeleton using the Zhang-Suen thinning algorithm
    thn = cv2.ximgproc.thinning(image, None, thinningType=cv2.ximgproc.THINNING_ZHANGSUEN)

    # algorithm to find holes in skeleton and fill them with white
    # holes typically happen at junctions
    fill_thinned_holes(thn)

    # save thinned and filled image
    cv2.imwrite(f'{folder}/thinned_{name}', thn)

def return_path(current_node):
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    return path[::-1]  # Return reversed path

def astar(maze, start, end):
    """
    Returns a list of tuples as a path from the given start to the given end in the given maze
    :param maze:
    :param start:
    :param end:
    :return:    """
    #create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # initialize both open and closed list
    open_list = []
    closed_list = []

    # Heapify open list and add the start_node
    heapq.heapify(open_list)
    heapq.heappush(open_list, start_node)

    # Add a stop condition
    outer_iterations = 0
    max_iterations = (len(maze[0])*len(maze)) // 2

    # We may only search up, down, left and right no diagonals
    adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0),)

    # Loop until reach the end node
    while len(open_list) > 0:
        outer_iterations += 1

        # if we hit this condition we stop and return path as is
        # will not contain destination
        if outer_iterations >= max_iterations:
            warn("Giving up on pathfinding. Too many iterations.")
            return(return_path(current_node))

        # Get the current node
        current_node = heapq.heappop(open_list)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            return return_path(current_node)

        # Generate children
        children = []

        # Loop through all adjacent squares
        for new_position in adjacent_squares:
            # Get adjacent node position
            node_position = (current_node.position[0]+new_position[0], current_node.position[1]+new_position[1])

            # Make sure within range
            if (node_position[0] > (len(maze) - 1) or node_position[0] < 0
                or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0):
                continue

            # Make sure path is white (walkable)
            if maze[node_position[0]][node_position[1]]:
                continue

            # Create new adjacent node object and append to children
            new_node = Node(current_node, node_position)
            children.append(new_node)

        # Loop through all children
        for child in children:
            # Child is on the closed list?
            if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                continue

            # Create f, g, h values
            child.g = current_node.g + 1

            # Euclidean distance from child to end node
            child.h = int(sqrt((child.position[0]-end_node.position[0])**2 + (child.position[1]-end_node.position[1])**2))
            # Manhattan distance from child to end node
            #child.h = abs(child.position[0]-end_node.position[0]) + abs(child.position[1]-end_node.position[1])
            child.f = child.h + child.g     # heuristic for A* alg: f = h + g

            # Child is already in the open list
            if len([open_node for open_node in open_list if child.position == open_node.position and child.g > open_node.g]) > 0:
                continue

            # Add the child to the open list
            heapq.heappush(open_list, child)

    # Happens if we exceed maximum iterations allowed
    warn("Couldn't get a path to the destination")
    return None

def draw_path(maze, path):
    for p in path:
        maze[path[0]][path[1]] = (255,0,0)

def find_start_end(maze):
    # search the very edge (first/last row and first/last col) to locate start/end positions
    # start and end points are arbitrary.
    # yields exact same solution path no matter how we assign start/end positions

    # initialize dicts to keep track of important information
    locations = {'top': None, 'left': None, 'bottom': None, 'right': None}
    lengths = {'top': 0, 'left': 0, 'bottom': 0, 'right': 0}

    # search top row
    for i in range(len(maze[0])):
        if maze[0][i]:
            lengths['top'] += 1
            locations['top'] = (0, i)

    # search left col
    for i in range(len(maze)):
        if maze[i][0]:
            lengths['left'] += 1
            locations['left'] = (i, 0)

    # search bottom row
    for i in range(len(maze[0])):
        if maze[len(maze)-1][i]:
            lengths['bottom'] += 1
            locations['bottom'] = (len(maze)-1, i)

    # search right col
    for i in range(len(maze)):
        if maze[i][len(maze[0])-1]:
            lengths['right'] += 1
            locations['right'] = (i, len(maze[0])-1)

    # pick correct start/end and fix their positions
    points = []
    for key in locations:
        if locations[key]:
            if key == 'top':
                points.append((locations[key][0], locations[key][1]-lengths[key]//2))
            elif key == 'left':
                points.append((locations[key][0]-lengths[key]//2, locations[key][1]))
            elif key == 'bottom':
                points.append((locations[key][0], locations[key][1]-lengths[key]//2))
            elif key == 'right':
                points.append((locations[key][0]-lengths[key]//2, locations[key][1]))
    return points
