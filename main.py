from pywebio.input import *
from pywebio.output import *
from pywebio import start_server
import mazegenerate

def app():
    while True:
        maze_info = maze_info_page()
        display_maze_page(maze_info)
        act = actions(buttons=['Restart', 'Exit'])
        if act == 'Exit':
            break

def maze_info_page():
    maze_info = input_group('Maze Parameters', [
                    select(label='Select Difficulty', options=['Random','Hard'], value='Random', name='difficulty'),
                    input(label='width (max 30):', value='10', type=NUMBER, name='width'),
                    input(label='height (max 30):', value='10', type=NUMBER, name='height')
                    ])
    if maze_info['difficulty'] == 'Hard':
        mazegenerate.generate_hard_maze(maze_info['width'], maze_info['height'])
    elif maze_info['difficulty'] == 'Random':
        mazegenerate.generate_random_maze(maze_info['width'], maze_info['height'])
    return maze_info

def display_maze_page(maze_info):
    put_text(f"A {maze_info['difficulty']} maze of size ({maze_info['width']},{maze_info['height']}):")
    put_image(open('mazeimages/maze.png', 'rb').read())

if __name__ == '__main__':
    start_server(app, port=36535, debug=True)
