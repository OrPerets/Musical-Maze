from pygame import image, draw, Surface
import pygame

from random import randint, choice
from math import sqrt
import copy

from psonic import *

def distance(p1, p2):
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def convert_states_to_tuples(states):
    result = []

    for state in states:
        result.append(state.location)

    return result

class Constant(object):
    def __getattr__(self, attr):
        return const.__dict__[attr]
    
    def __setattr__(self, attr, value):
        if attr in self.__dict__.keys():
            raise Exception("Error! trying to set exist attribute")
        else:
            self.__dict__[attr] = value
            
    def __str__(self):
        return self.__dict__.__str__()

'''
Define Constant object with colors, directions, width, height.
'''
const = Constant()

# Colors
const.white = (255, 255, 255)
const.pink = (255, 0, 255)
const.black = (0, 0, 0)
const.yellow = (255, 255, 0)
const.red = (255, 0, 0)
const.green = (0, 255, 0)
const.gray = (211, 211, 211)
const.blue = (12, 12, 200)
const.light_green = (192, 234, 68)
const.light_orange = (255, 201, 14)
const.light_blue = (18, 204, 214)

# Directions
const.right = 0
const.left = 1
const.up = 2
const.down = 3

# Width & Height (in single units)
const.wc = 25
const.hc = 25

# Others
const.time_poll = 75
const.players_data = "DB/players_data.json"
const.users = "DB/users.json"
const.passwords = "DB/passwords.json"
const.melodies_map = {
    1: "little_jonathan",
    2: "abc"
}

game_data = {
    "mode": "user",
    "level": (5,5),
    "walls": True,
    "user": None,
    "melody": None
}

class Point(object):
    def __init__(self, xy):
        self.x = xy[0]
        self.y = xy[1]      


class State(object):
    def __init__(self):
        self.state = False
        self.gate = [True, True, True, True]


class PositionWithBackground(object):
    def __init__(self, pos, color):
        self.pos = pos
        self.surf = Surface((const.wc, const.hc))
        self.surf.fill(color)


class Activity(object):
    def __init__(self, maze, sound):
        self.x = 0
        self.y = 0

        self.wrong_moves = 0
        self.path = None
        self.solved_path = []
        self.reverse = 0
        self.sound = sound
        self.backtrace = []
        self.maze = maze
        # user moves
        self.moves = [(0,0)]
        self.img = image.load("images/player.png")
        self.img = pygame.transform.scale(self.img, (30, 30))
        self.img.set_colorkey(const.pink)
        self.rect_img = self.img.get_rect()
        self.rect_img[0], self.rect_img[1] = (self.x * const.wc), (self.y * const.hc)

        self.start_pos = PositionWithBackground((0, 0), const.green)
        self.end_pos = PositionWithBackground(((self.maze.w * const.wc - const.wc), (self.maze.h * const.hc - const.hc)), const.light_orange)

        self.c_path = None

    def get_copy(self):
        maze = copy.deepcopy(self.maze)
        return Activity(maze, self.sound)

    def show(self, screen, walls=True):
        moves = []
        if self.solved_path:
            if self.reverse == 0:
                self.solved_path.reverse()
                self.reverse = 1

        moves.reverse()
        for c in moves:
            screen.blit(c.surf, c.pos)
            
        screen.blit(self.start_pos.surf, self.start_pos.pos)
        screen.blit(self.end_pos.surf, self.end_pos.pos)
        screen.blit(self.img, self.rect_img)
        if walls:
            self.maze.show(screen)

    def move(self, dir):
        if self.c_path is None:
            self.c_path = self.get_solution()
            self.c_path = self.c_path[::-1]
        current = self.maze.get_cell(self.x, self.y)
        position = current.location
        if not current.gate[dir]:
            if dir == const.right and self.x + 1 < self.maze.w:
                next_position = ((self.x+1)*const.wc, position[1])
                if next_position == self.c_path[0].location:
                    self.play_note_and_update_variables()

                elif next_position in self.backtrace:
                    self.play_return_to_path_sound()

                else:
                    self.sound.play_error_note()
                    self.wrong_moves += 1
                self.x += 1
            if dir == const.left and self.x - 1 >= 0:
                next_position = ((self.x-1) * const.wc, position[1])
                if next_position == self.c_path[0].location:
                    self.play_note_and_update_variables()

                elif next_position in self.backtrace:
                    self.play_return_to_path_sound()

                else:
                    self.sound.play_error_note()
                    self.wrong_moves += 1
                self.x -= 1
            if dir == const.up and self.y - 1 >= 0:
                next_position = (position[0], (self.y-1) * const.hc)
                if next_position == self.c_path[0].location:
                    self.play_note_and_update_variables()

                elif next_position in self.backtrace:
                    self.play_return_to_path_sound()

                else:
                    self.sound.play_error_note()
                    self.wrong_moves += 1
                self.y -= 1
            if dir == const.down and self.y + 1 < self.maze.h:
                next_position = (position[0], (self.y+1) * const.hc)
                if next_position == self.c_path[0].location:
                    self.play_note_and_update_variables()

                elif next_position in self.backtrace:
                    self.play_return_to_path_sound()

                else:
                    self.sound.play_error_note()
                    self.wrong_moves += 1
                self.y += 1
                
            self.rect_img[0], self.rect_img[1] = (self.x * const.wc), (self.y * const.hc)
            self.moves.append((self.x * const.wc,self.y * const.hc))

        else: # get a wall
            self.sound.play_wall_note()

    def play_note_and_update_variables(self):
        note, dur = self.sound.get_next_note()
        if note is not None:
            self.sound.play_single_note(note, dur)
            self.backtrace.append(self.c_path.pop(0).location)
            self.sound.index += 1

    def play_return_to_path_sound(self):
        self.sound.back_to_path()

    def astar(self, destination):
        dest = Point(destination)
        open = []
        close = []
        
        start = self.maze.get_cell(self.x, self.y)
        open.append(start)

        start.distance = distance((self.x, self.y), (dest.x, dest.y))
        start.parent_distance = 0
        start.dest_dist = distance((self.x, self.y), (dest.x, dest.y))
        start.parent = None
        
        while 1:
            if len(open) <= 0:
                break
            
            min, min_id = open[0].distance, 0
            for id, cell in enumerate(open[1:]):
                if cell.distance < min:
                    min = cell.distance
                    min_id = id + 1
                    
            close.append(open[min_id])
            if open[min_id].x == dest.x and open[min_id].y == dest.y:
                break
            
            self.handle_hueristic(close, open, open[min_id].x + 1, open[min_id].y, const.right, open[min_id], dest)
            self.handle_hueristic(close, open, open[min_id].x - 1, open[min_id].y, const.left, open[min_id], dest)
            self.handle_hueristic(close, open, open[min_id].x, open[min_id].y - 1, const.up, open[min_id], dest)
            self.handle_hueristic(close, open, open[min_id].x, open[min_id].y + 1, const.down, open[min_id], dest)
            
            open.remove(open[min_id])

    def handle_hueristic(self, close, open, x, y, dir, parent, dest):
        if parent.gate[dir]:
            return

        c = self.maze.get_cell(x, y)

        if c in close:
            return
        
        if c in open:
            child_distance = distance((x, y), (parent.x, parent.y))
            c.dir = self.maze.notdir(dir)
            
            if child_distance < c.parent_distance:
                c.parent_distance = child_distance
                c.distance = c.dest_dist + c.parent_distance
                c.parent = parent
                
        else:
            c.parent = parent
            c.dir = self.maze.not_dir(dir)
            c.parent_distance = distance((x, y), (parent.x, parent.y))
            c.dest_dist = distance((x, y), (dest.x, dest.y))
            c.distance = c.dest_dist + c.parent_distance
            open.append(c)

    def get_astar(self, c_source, c_dest):
        source = self.maze.get_cell(c_source[0], c_source[1])
        dest = self.maze.get_cell(c_dest[0], c_dest[1])
        
        current = dest
        path = []
        
        while current and (current.x != source.x or current.y != source.y):
            if current.x == current.parent.x - 1:
                self.solved_path.append(current)
                path.append(const.right)
            if current.x == current.parent.x + 1:
                self.solved_path.append(current)
                path.append(const.left)
            if current.y == current.parent.y - 1:
                self.solved_path.append(current)
                path.append(const.down)
            if current.y == current.parent.y + 1:
                self.solved_path.append(current)
                path.append(const.up)
                
            current = current.parent
            
        return_path = []
        id = len(path) - 1
        
        while id >= 0:
            return_path.append(self.maze.not_dir(path[id]))
            id -= 1

        return return_path
        
    def poll(self):
        if self.path:
            self.move(self.path.pop(0))
            self.solved_path.pop(0)
            
    def go_to(self, x):
        self.path = x

    def get_solution(self):
        copied = self.get_copy()
        copied.astar(((copied.maze.w - 1), (copied.maze.h - 1)))
        copied.get_astar((copied.x, copied.y), ((copied.maze.w - 1), (copied.maze.h - 1)))
        return copied.solved_path

    def serialize(self):
        return {
            "wrong_moves":self.wrong_moves,
            "moves":self.moves
        }
        
class Maze(object):
    def __init__(self, w=25, h=30, sx=0, sy=0):
        self.w = w
        self.h = h
        
        self.cases = []
        self.wc = const.wc
        self.hc = const.hc
        
        self.sx = sx
        self.sy = sy

        self.solution_size = 0

        for v in range(self.w * self.h):
            a = State()
            a.x = v % self.w
            a.y = int(v / self.w)
            a.location = (a.x * const.wc,a.y * const.hc)
            self.cases.append(a)
        
    def get_cell(self, x, y):
        return self.cases[(y*self.w) + x]
    
    def not_dir(self, dir):
        if dir == const.right:
            return const.left
        if dir == const.left:
            return const.right
        if dir == const.up:
            return const.down
        if dir == const.down:
            return const.up
        
    def generate_maze(self, x=-1, y=-1):
        if x == -1:
            x = randint(0, self.w - 1)
            y = randint(0, self.h - 1)

        cell_act = self.get_cell(x, y)

        if not cell_act.state:
            cell_act.state = True
            tab = []

            if x + 1 < self.w and not self.get_cell(x + 1, y).state:
                tab.append((x + 1, y, const.right))
            if x - 1 >= 0 and not self.get_cell(x - 1, y).state:
                tab.append((x - 1, y, const.left))
            if y + 1 < self.h and not self.get_cell(x, y + 1).state:
                tab.append((x, y + 1, const.down))
            if y - 1 >= 0 and not self.get_cell(x, y - 1).state:
                tab.append((x, y - 1, const.up))


            if tab:
                while tab:
                    C = choice(tab)
                    if not self.get_cell(C[0], C[1]).state:
                        cell = self.get_cell(C[0], C[1])
                        cell_act.gate[C[2]] = False
                        cell.gate[self.not_dir(C[2])] = False
                        self.generate_maze(C[0], C[1])
                    else:
                        tab.remove(C)

                    
    def show(self, screen):
        w, h = self.wc, self.hc
        sx, sy = self.sx, self.sy
        
        for y in range(self.h - 1):
            for x in range(self.w - 1):
                c = self.get_cell(x, y)
                
                if c.gate[const.right]:
                    draw.line(screen, const.black, (sx + ((x + 1) * w), (sy + (y * h))), (sx + ((x + 1) * w), sy + ((y+1) * h)), 2)
                if c.gate[const.down]:
                    draw.line(screen, const.black, ((sx + (x * w)), (sy + ((y+1) * h))), (sx + ((x + 1) * w), sy + ((y+1) * h)), 2)
                                     
        x = self.w - 1
        
        for y in range(self.h - 1):
            c = self.get_cell(x, y)
            
            if c.gate[const.down]:
                draw.line(screen, const.black, ((sx + (x * w)), (sy + ((y+1) * h))), (sx + ((x + 1) * w), sy + ((y+1) * h)), 2)
                
        y = self.h - 1
        
        for x in range(self.w - 1):
            c = self.get_cell(x, y)
            
            if c.gate[const.right]:
                draw.line(screen, const.black, (sx + ((x + 1) * w), (sy + (y * h))), (sx + ((x + 1) * w), sy + ((y+1) * h)), 2)

        draw.rect(screen, const.black, (sx, sy, w * self.w, h * self.h), 2)


class Sound(object):
    def __init__(self, notes, dur):
        self.notes = notes
        self.left_notes = notes.copy()
        self.dur = dur
        self.left_dur = dur.copy()
        self.index = 0
        self.backtrace_note = 80

    def get_notes_by_index(self):
        return self.notes[:self.index], self.dur[:self.index]

    def get_notes(self):
        return self.notes, self.dur

    def play_all(self):
        for i in range(len(self.notes)):
            play(self.notes[i])
            sleep(self.dur[i])

    def play_single_note(self, note, dur, pan=0):
        play(note, pan=pan)
        sleep(dur)

    def get_next_note(self):
        if not len(self.left_notes):
            return None, None
        return self.left_notes.pop(0), self.left_dur.pop(0)

    def play_error_note(self):
        use_synth(SAW)
        for i in range(60, 47, -1):
            play(i, amp=0.3)
            sleep(0.08)

    def play_hint(self, pan=0):
        if self.index < len(self.notes) - 1:
            play(self.left_notes[0], pan=pan)
            sleep(self.left_dur[0])

    def play_wall_note(self):
        play(chord(E3, MAJOR))
        sleep(1)

    def back_to_path(self):
        play(self.notes[self.index-1])

    def play_win(self):
        for i in range(1, 12):
            sample(DRUM_SNARE_SOFT, rate=i, amp=i / 10)
            sleep(0.125)