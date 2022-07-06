from mazelib import Maze
from mazelib.generate.BacktrackingGenerator import BacktrackingGenerator
from mazelib.solve.BacktrackingSolver import BacktrackingSolver
import matplotlib.pyplot as plt

def generate_maze_img(grid):
    """Generate a simple image of the maze."""
    plt.figure(figsize=(10, 5))
    plt.imshow(grid, cmap=plt.cm.binary, interpolation='nearest')
    plt.xticks([]), plt.yticks([])
    plt.axis('off')
    plt.savefig('mazeimages/maze.png', bbox_inches='tight', pad_inches=0)

def generate_random_maze(width, height):
    m = Maze()
    m.generator = BacktrackingGenerator(width,height)
    m.generate()
    m.generate_entrances()
    print("Start: {}, End: {}".format(m.start, m.end))
    m.grid[m.start[0]][m.start[1]] = 0  # make start location blank
    m.grid[m.end[0]][m.end[1]] = 0      # make end location blank
    generate_maze_img(m.grid)
    return m.start, m.end

def generate_hard_maze(width, height):
    m = Maze()
    m.generator = BacktrackingGenerator(width,height)
    m.solver = BacktrackingSolver()
    m.generate_monte_carlo(50,5,1.0)
    print("Start: {}, End: {}".format(m.start, m.end))
    m.grid[m.start[0]][m.start[1]] = 0  # make start location blank
    m.grid[m.end[0]][m.end[1]] = 0      # make end location blank
    generate_maze_img(m.grid)
    return m.start, m.end
