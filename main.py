from pywebio.input import *
from pywebio.output import *
from pywebio import start_server, config
import mazegenerate, mazesolution

@config(theme='dark')
def app():
    while True:
        clear()
        maze_info = maze_info_page()
        put_grid([
            [span(put_markdown('# CS4480 Maze Solver Project'), col=3)],
            [put_scope('maze'), put_scope('actions') ,put_scope('solution')],
        ], cell_widths='40% 10% 50%')
        display_maze_page(maze_info)
        with use_scope('actions'):
            act = actions(buttons=['Solve', 'Restart', 'Exit'])
            if act == 'Solve':
                solve_maze()
            elif act == 'Restart':
                continue
            elif act == 'Exit':
                break
            clear()
            act = actions(buttons=['Restart', 'Exit'])
            if act == 'Restart':
                continue
            elif act == 'Exit':
                break

def solve_maze():
    time_elapsed = mazesolution.solve_maze('mazeimages/maze.png')
    with use_scope('solution'):
        put_markdown("### Maze solution:")
        put_image(open('mazeimages/maze_solved.png', 'rb').read())
        put_text(f"Maze solved in {time_elapsed//60} min {time_elapsed%60} sec(s).")

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
        put_markdown("### Maze:")
        put_text(f"A {maze_info['difficulty']} maze of size ({maze_info['width']},{maze_info['height']}):")
        put_image(open('mazeimages/maze.png', 'rb').read())

if __name__ == '__main__':
    start_server(app, port=8080, debug=True)
