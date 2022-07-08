import cv2
import numpy as np
import heapq
import time

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

def thin_maze_image(image):
    # convert maze image into 1px-wide skeleton using the Zhang-Suen thinning algorithm
    thn = cv2.ximgproc.thinning(image, None, thinningType=cv2.ximgproc.THINNING_ZHANGSUEN)

    # algorithm to find holes in skeleton and fill them with white
    # holes typically happen at junctions/turns
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

    # save thinned and filled image
    # cv2.imwrite(f'{folder}/thinned_{name}', thn)
    return thn

def astar(maze, start, end):
    """
    Returns a list of tuples as a path from the given start to the given end in the given maze
    :param maze:
    :param start:
    :param end:
    :return:
    """

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Heapify the open_list and Add the start node
    heapq.heapify(open_list)
    heapq.heappush(open_list, start_node)

    # what squares do we search
    adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0),)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = heapq.heappop(open_list)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_position in adjacent_squares: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] == 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:
            # Child is on the closed list
            if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            if len([open_node for open_node in open_list if child.position == open_node.position and child.g > open_node.g]) > 0:
                continue

            # Add the child to the open list
            heapq.heappush(open_list, child)


def draw_path(maze, path, thickness):
    path_image = np.zeros((maze.shape[0],maze.shape[1],3), dtype=maze.dtype)
    for p in path:
        if p[0] < thickness or p[0] > len(maze)-1 - thickness or p[1] < thickness or p[1] > len(maze[0])-1 - thickness:
            continue
        for i in range(p[0]-thickness, p[0]+thickness+1):
            for j in range(p[1]-thickness, p[1]+thickness+1):
                path_image[i][j] = [0,0,255]
    return path_image

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
    thickness = []
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
            thickness.append(lengths[key])
    return points, max(thickness)

# whole solution process.
def solve_maze(image_path):
    begin = time.time()
    image = cv2.imread(image_path, 0)                       # obtain the image from the file path
    thn = thin_maze_image(image)                            # thin the maze image
    start_end, thickness = find_start_end(thn)              # find start and end points of maze
    path = astar(thn, start_end[0], start_end[1])           # find solution path using A-star algorithm
    path_image = draw_path(image, path, thickness//2)       # draw the path in red on the original maze
    solved_path = ''
    for c in image_path:
        if c == '.':
            break
        solved_path += c
    solved_path += '_solved.png'
    #cv2.imwrite(solved_path, image)
    end = time.time()
    elapsed = round(end-begin,2)
    print(f"Maze solved in {elapsed // 60}min {elapsed % 60}sec.")
    maze_overlay = np.zeros((image.shape[0],image.shape[1],3), dtype=image.dtype)
    for i in range(len(image)):
        for j in range(len(image[i])):
            value = image[i][j]
            maze_overlay[i][j] = [value, value, value]
    for i in range(len(maze_overlay)):
        for j in range(len(maze_overlay[i])):
            if(path_image[i][j][2] == 255 and maze_overlay[i][j][1] == 255):
                maze_overlay[i][j] = path_image[i][j]
    cv2.imwrite(solved_path,maze_overlay)
    return elapsed
