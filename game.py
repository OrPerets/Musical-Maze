from pygame import init, display, key, quit, joystick
from sys import exit
from pygame.locals import *
from pygame import time as py_time
from files_functions import save_to_json
from widgets.main import Button, render_widgets, handle_widgets
from classes import *
import time

# sounds
from sounds import little_jonathan as lj

def start():
    global maze
    global activity
    global current_user

    def solve():
        global activity
        activity.solved_path = []
        activity.reverse = 0
        activity.astar(((activity.maze.w - 1), (activity.maze.h - 1)))
        path = activity.get_astar((activity.x, activity.y), ((activity.maze.w - 1), (activity.maze.h - 1)))
        activity.go_to(path)

    def play_to_index():
        # play (60, attack=0.5, decay=1, sustain_level=0.4, sustain=2, release=0.5)
        notes, dur = sound.get_notes_by_index()
        for i in range(len(notes)):
            play(notes[i])
            sleep(dur[i])

    def play_all():
        sound.play_all()

    def play_hint():
        sound.play_hint()

    def save_user_data(activity, start_time):
        user_data = {
            "activity": activity.serialize(),
            "time": time.time() - start_time
        }
        save_to_json(user_data, "players")


    # Pygame initialize variable
    init()
    width, height = 640, 480
    window = display.set_mode((width, height))
    display.set_caption("Musical Maze")

    # Game
    size = game_data["level"]
    maze = Maze(size[0], size[1])
    maze.generate_maze()


    notes = lj.notes
    dur = lj.dur
    sound = Sound(notes, dur)
    activity = Activity(maze, sound)

    '''
    PROBLEM:
    Maze size is not match to notes size. 
    '''

    # Display "solve" button for user
    if game_data["mode"] == 'user':
        play_button = Button(window, text="Play", width=100,
                              height=60, bordercolor=const.black,
                              colour=const.light_blue, fontsize=20, target=play_to_index)
        play_button.place((515, 95))

        solve_button = Button(window, text="Solve", width=100,
                              height=60, bordercolor=const.black,
                              colour=const.light_blue, fontsize=20, target=solve)
        solve_button.place((515, 185))

        all_button = Button(window, text="Play All", width=100,
                              height=60, bordercolor=const.black,
                              colour=const.light_blue, fontsize=20, target=play_all)
        all_button.place((515, 275))

        hint_button = Button(window, text="Hint", width=100,
                            height=60, bordercolor=const.black,
                            colour=const.light_blue, fontsize=20, target=play_hint)
        hint_button.place((515, 365))

    act_time = 0

    display.flip()
    key.set_repeat(50, 55)

    if joystick.get_count() > 0:
        Joy = joystick.Joystick(0)
        Joy.init()

    if game_data["mode"] == "a-star":
        solve()

    start_time = time.time()
    # Main loop
    while True:
        py_time.Clock().tick(13)
        window.fill(const.gray)
        for event in handle_widgets():
            if event.type == QUIT:
                quit()
                exit()

            elif event.type == JOYAXISMOTION:
                if event.axis == 1:
                    if round(event.value) < 0:
                        if not activity.solved_path:
                            activity.move(const.up)
                    if round(event.value) > 0:
                        if not activity.solved_path:
                            activity.move(const.down)
                if event.axis == 0:
                    if round(event.value) < 0:
                        if not activity.solved_path:
                            activity.move(const.left)
                    if round(event.value) > 0:
                        if not activity.solved_path:
                            activity.move(const.right)

            elif event.type == JOYBUTTONDOWN:
                if event.button == 8:
                    activity.solved_path = []
                    activity.reverse = 0
                    activity.astar(((activity.maze.w - 1), (activity.maze.h - 1)))
                    path = activity.get_astar((activity.x, activity.y), ((activity.maze.w - 1), (activity.maze.h - 1)))
                    activity.go_to(path)

        keys = key.get_pressed()
        if keys:
            if keys[K_UP]:
                if not activity.solved_path:
                    activity.move(const.up)
            if keys[K_DOWN]:
                if not activity.solved_path:
                    activity.move(const.down)
            if keys[K_LEFT]:
                if not activity.solved_path:
                    activity.move(const.left)
            if keys[K_RIGHT]:
                if not activity.solved_path:
                    activity.move(const.right)

        if py_time.get_ticks() - act_time >= const.time_poll:
            act_time = py_time.get_ticks()
            activity.poll()

        activity.show(window, walls=game_data["walls"])
        render_widgets()
        display.flip()

        # game over
        if activity.x == activity.maze.w - 1 and activity.y == activity.maze.h - 1:
            save_user_data(activity, start_time)
            py_time.delay(300)
            size = game_data["level"]
            maze = Maze(size[0], size[1])
            maze.generate_maze()
            sound = Sound(lj.notes, lj.dur)
            activity = Activity(maze, sound)
            window.fill(const.gray)
            activity.show(window, walls=game_data["walls"])
            render_widgets()
            display.flip()

