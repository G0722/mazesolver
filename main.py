from pywebio.input import *
from pywebio.output import *
from pywebio import start_server, config
from pywebio.session import run_js
import mazegenerate, mazesolution
import cv2

@config(theme='dark')
def app():
    while True:
        clear()
        method = select(label='Select method:', options=['Upload','Generate'], value='Generate')
        maze_info = 0
        put_grid([
            [span(put_markdown('# CS4480 AI Maze Solver Project'), col=3)],
            [put_scope('maze'), put_scope('blank'), put_scope('solution')],
        ], cell_widths='45% 10% 45%')
        if method == 'Upload':
            maze_info = upload_maze_page()
        else:
            maze_info = maze_info_page()
        display_maze_page(maze_info)
        act = actions(buttons=[
            {'label': 'Solve', 'value': 'Solve', 'color': 'success'},
            {'label': 'Restart', 'value': 'Restart', 'color': 'warning'},
            {'label': 'Exit', 'value': 'Exit', 'color': 'danger'}
        ])
        if act == 'Solve':
            solve_maze()
        elif act == 'Restart':
            continue
        elif act == 'Exit':
            break
        act = actions(buttons=[
            {'label': 'Restart', 'value': 'Restart', 'color': 'warning'},
            {'label': 'Exit', 'value': 'Exit', 'color': 'danger'}
        ])
        if act == 'Exit':
            break

def upload_maze_page():
    maze_img = file_upload("Upload a file:", accept='.png')
    image = maze_img['content']
    open('mazeimages/maze.png', 'wb').write(image)
    return 'upload'

@use_scope('solution')
def solve_maze():
    put_markdown("### Maze solution:")
    with put_loading(shape='grow', color='light'):
        time_elapsed = mazesolution.solve_maze('mazeimages/maze.png')
        put_image(open('mazeimages/maze_solved.png', 'rb').read())
        put_text(f"Maze solved in {int(time_elapsed//60)} min {time_elapsed%60} sec(s).")

def check_dims(n):
    return "Exceeded max parameters" if n > 50 else None

def maze_info_page():
    maze_info = input_group('Maze Parameters', [
                    select(label='Select Difficulty', options=['Random','Hard'], value='Random', name='difficulty'),
                    input(label='width (max 50):', value='10', type=NUMBER, name='width', validate=check_dims),
                    input(label='height (max 50):', value='10', type=NUMBER, name='height', validate=check_dims),
                    ])
    with put_loading(shape='grow', color='light'):
        if maze_info['difficulty'] == 'Hard':
            mazegenerate.generate_hard_maze(maze_info['width'], maze_info['height'])
        elif maze_info['difficulty'] == 'Random':
            mazegenerate.generate_random_maze(maze_info['width'], maze_info['height'])
        return maze_info

@use_scope('maze')
def display_maze_page(maze_info):
    if maze_info == 'upload':
        put_markdown(f"### Your uploaded custom maze")
    else:
        put_markdown(f"### A {maze_info['difficulty']} maze of size ({maze_info['width']},{maze_info['height']}):")
    put_image(open('mazeimages/maze.png', 'rb').read())

if __name__ == '__main__':
    start_server(app, port=8080, debug=True)
