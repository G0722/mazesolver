from pywebio.input import *
from pywebio.output import *
from pywebio import start_server, config
from pywebio.session import run_js
import mazegenerate, mazesolution
import cv2

# Main function that displays onto webpage
@config(theme='dark')
def app():
    while True:
        clear()     # clear previous display
        # user determines file upload or input values to generate maze
        method = select(label='Select method:', options=['Upload','Generate'], value='Generate')
        maze_info = 0
        # Prints title and creates grid system for webpage
        put_grid([
            [span(put_markdown('# CS4480 AI Maze Solver Project'), col=3)],
            [put_scope('maze'), put_scope('blank'), put_scope('solution')],
        ], cell_widths='45% 10% 45%')
        # Handle the decision from method above
        if method == 'Upload':
            maze_info = upload_maze_page()
        else:
            maze_info = maze_info_page()

        display_maze_page(maze_info)
        # allow user to solve the maze or restart the app
        act = actions(buttons=[
            {'label': 'Solve', 'value': 'Solve', 'color': 'success'},
            {'label': 'Restart', 'value': 'Restart', 'color': 'warning'},
            {'label': 'Exit', 'value': 'Exit', 'color': 'danger'}
        ])
        # Handles the above actions
        if act == 'Solve':
            solve_maze()
        elif act == 'Restart':
            continue
        elif act == 'Exit':
            break

        # Allow user to restart or exit the app
        act = actions(buttons=[
            {'label': 'Restart', 'value': 'Restart', 'color': 'warning'},
            {'label': 'Exit', 'value': 'Exit', 'color': 'danger'}
        ])
        if act == 'Exit':
            break

# Handles image file upload form
def upload_maze_page():
    maze_img = file_upload("Upload a file:", accept='.png')
    image = maze_img['content']
    open('mazeimages/maze.png', 'wb').write(image)
    return 'upload'

# Handles the call to solve the maze by image
@use_scope('solution')
def solve_maze():
    put_markdown("### Maze solution:")
    # Loading animation until maze is solved and solution image is output
    with put_loading(shape='grow', color='light'):
        time_elapsed = mazesolution.solve_maze('mazeimages/maze.png')
        put_image(open('mazeimages/maze_solved.png', 'rb').read())
        put_text(f"Maze solved in {int(time_elapsed//60)} min {time_elapsed%60} sec(s).")

# Handles the form that takes in user inputs as maze parameters
def maze_info_page():
    limit = 50
    check_dims = lambda n: "Exceeded max parameters" if n > limit else None     # Checks whether input is above/below limit
    # Form to get dimensions and maze difficulty
    maze_info = input_group('Maze Parameters', [
                    select(label='Select Difficulty', options=['Random','Hard'], value='Random', name='difficulty'),
                    input(label=f'width (max {limit}):', value='10', type=NUMBER, name='width', validate=check_dims),
                    input(label=f'height (max {limit}):', value='10', type=NUMBER, name='height', validate=check_dims),
                    ])
    # Loading animation until maze is generated.
    # Hard maze takes longer
    with put_loading(shape='grow', color='light'):
        if maze_info['difficulty'] == 'Hard':
            mazegenerate.generate_hard_maze(maze_info['width'], maze_info['height'])
        elif maze_info['difficulty'] == 'Random':
            mazegenerate.generate_random_maze(maze_info['width'], maze_info['height'])
        return maze_info

# Handles display of user generated/uploaded maze image to webpage
@use_scope('maze')
def display_maze_page(maze_info):
    if maze_info == 'upload':
        put_markdown(f"### Your uploaded custom maze")
    else:
        put_markdown(f"### A {maze_info['difficulty']} maze of size ({maze_info['width']},{maze_info['height']}):")
    put_image(open('mazeimages/maze.png', 'rb').read())

if __name__ == '__main__':
    start_server(app, port=8080, debug=True)
