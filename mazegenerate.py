from mazelib import Maze
from mazelib.generate.BacktrackingGenerator import BacktrackingGenerator
from mazelib.solve.BacktrackingSolver import BacktrackingSolver
import matplotlib.pyplot as plt

# Converts mazelib maze grid into image and saves into memory
def generate_maze_img(grid):
    """Generate a simple image of the maze."""
    plt.figure(figsize=(10, 5))
    plt.imshow(grid, cmap=plt.cm.binary, interpolation='nearest')
    plt.xticks([]), plt.yticks([])
    plt.axis('off')
    plt.savefig('mazeimages/maze.png', bbox_inches='tight', pad_inches=0)

# Generates one random maze
def generate_random_maze(width, height):
    m = Maze()
    m.generator = BacktrackingGenerator(width,height)
    m.generate()
    m.generate_entrances()
    print("Start: {}, End: {}".format(m.start, m.end))
    m.grid[m.start[0]][m.start[1]] = 0  # make start location blank
    m.grid[m.end[0]][m.end[1]] = 0      # make end location blank
    generate_maze_img(m.grid)           # convert to png to save into memory
    return m.start, m.end

# returns a very hard maze that has a long solution path
def generate_hard_maze(width, height):
    m = Maze()
    m.generator = BacktrackingGenerator(width,height)
    m.solver = BacktrackingSolver()
    m.generate_monte_carlo(50,5,1.0)    # generates many mazes and selects the one with the longest solution path
    print("Start: {}, End: {}".format(m.start, m.end))
    m.grid[m.start[0]][m.start[1]] = 0  # make start location blank (white)
    m.grid[m.end[0]][m.end[1]] = 0      # make end location blank   (white)
    generate_maze_img(m.grid)           # convert to png to save into memory
    return m.start, m.end
