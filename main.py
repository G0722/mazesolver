from pywebio.input import *
from pywebio.output import *
from pywebio import start_server, config
from pywebio.session import run_js
import mazegenerate, mazesolution

@config(theme='dark')
def app():
    while True:
        clear()
        maze_info = maze_info_page()
        put_grid([
            [span(put_markdown('# CS4480 AI Maze Solver Project'), col=3)],
            [put_scope('maze'), put_scope('blank'), put_scope('solution')],
        ], cell_widths='45% 10% 45%')
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


def solve_maze():
    time_elapsed = mazesolution.solve_maze('mazeimages/maze.png')
    with use_scope('solution'):
        put_markdown("### Maze solution:")
        put_image(open('mazeimages/maze_solved.png', 'rb').read())
        put_text(f"Maze solved in {int(time_elapsed//60)} min {time_elapsed%60} sec(s).")

def check_dims(n):
    return "Exceeded max parameters" if n > 40 else None

def maze_info_page():
    maze_info = input_group('Maze Parameters', [
                    select(label='Select Difficulty', options=['Random','Hard'], value='Random', name='difficulty'),
                    input(label='width (max 40):', value='10', type=NUMBER, name='width', validate=check_dims),
                    input(label='height (max 40):', value='10', type=NUMBER, name='height', validate=check_dims),
                    ])
    if maze_info['difficulty'] == 'Hard':
        mazegenerate.generate_hard_maze(maze_info['width'], maze_info['height'])
    elif maze_info['difficulty'] == 'Random':
        mazegenerate.generate_random_maze(maze_info['width'], maze_info['height'])
    return maze_info

def display_maze_page(maze_info):
    with use_scope('maze'):
        put_markdown(f"### A {maze_info['difficulty']} maze of size ({maze_info['width']},{maze_info['height']}):")
        put_image(open('mazeimages/maze.png', 'rb').read())

if __name__ == '__main__':
    start_server(app, port=8080, debug=True)
