import os
import pygame
from pygame.locals import *
import pygameMenu
from pygameMenu.locals import *
from game import start
from classes import game_data, const

def main_menu(current_user):
    FPS = 60
    W_SIZE = 800
    H_SIZE = 550

    melodies = [('Little Jonathan', 1), ('ABC', 2)]

    # init pygame
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    # Create window
    surface = pygame.display.set_mode((W_SIZE, H_SIZE))
    pygame.display.set_caption('Musical Maze')
    clock = pygame.time.Clock()

    game_data["user"] = current_user
    def main_menu_background():
        surface.fill(const.light_blue)

    def set_game_walls(c, **kargs):
        game_data["walls"] = c
        if kargs['write_on_console']:
            print("Mode:", c)

    def set_game_mode(c, **kargs):
        game_data["mode"] = c
        if kargs['write_on_console']:
            print("Mode:", c)

    def set_game_level(c, **kargs):
        game_data["level"] = c
        if kargs['write_on_console']:
            print("level:", c)

    def set_game_melody(c, **kargs):
        game_data["melody"] = c
        if kargs['write_on_console']:
            print("level:", c)

    game_options_menu = pygameMenu.Menu(surface,
                                        dopause=False,
                                        font=pygameMenu.fonts.FONT_NEVIS,
                                        menu_alpha=85,
                                        menu_color=(0, 0, 0),
                                        menu_color_title=(0, 0, 0),
                                        menu_height=int(H_SIZE / 2),
                                        menu_width=600,
                                        onclose=PYGAME_MENU_RESET,
                                        title='Game Options',
                                        title_offsety=5,
                                        window_height=H_SIZE,
                                        window_width=W_SIZE
                                        )

    game_options_menu.add_selector('Mode',
                                   [('User', "user"),
                                    ('Algorithm', "a-star")],
                                   onchange=set_game_mode,
                                   onreturn=None,
                                   default=0,
                                   write_on_console=False
                                   )

    # Adds a selector (element that can handle functions)
    game_options_menu.add_selector('Level',
                                   [('1', (5, 5)),
                                    ('2', (10, 5)),
                                    ('3', (10, 10)),
                                    ('4', (15, 15)),
                                    ('5', (20, 18))],
                                   onchange=set_game_level,
                                   onreturn=None,
                                   default=0,
                                   write_on_console=False
                                   )

    # option for walls to without walls
    game_options_menu.add_selector('Walls',
                                   [('Yes', True),
                                    ('No', False)],
                                   onchange=set_game_walls,
                                   onreturn=None,
                                   default=0,
                                   write_on_console=False
                                   )

    game_options_menu.add_selector('Melody',
                                   melodies,
                                   onchange=set_game_melody,
                                   onreturn=None,
                                   default=0,
                                   write_on_console=False
                                   )
    game_options_menu.add_option('Start Game', start)

    # About menu
    about_menu = pygameMenu.TextMenu(surface,
                                     dopause=False,
                                     font=pygameMenu.fonts.FONT_NEVIS,
                                     font_size_title=30,
                                     font_title=pygameMenu.fonts.FONT_8BIT,
                                     menu_color_title=const.blue,
                                     onclose=PYGAME_MENU_DISABLE_CLOSE,
                                     text_fontsize=20,
                                     title='About',
                                     window_height=H_SIZE,
                                     window_width=W_SIZE
                                     )
    about_menu.add_option('Return to Menu', PYGAME_MENU_BACK)
    for line in ["Musical maze", "Or Perets", "2018"]:
        about_menu.add_line(line)
    about_menu.add_line(PYGAMEMENU_TEXT_NEWLINE)

    # Main menu, pauses execution of the application
    menu = pygameMenu.Menu(surface,
                           bgfun=main_menu_background,
                           enabled=False,
                           font=pygameMenu.fonts.FONT_NEVIS,
                           menu_alpha=90,
                           onclose=PYGAME_MENU_CLOSE,
                           title='Main Menu',
                           title_offsety=5,
                           window_height=H_SIZE,
                           window_width=W_SIZE
                           )

    menu.add_option(game_options_menu.get_title(), game_options_menu)
    menu.add_option(about_menu.get_title(), about_menu)
    menu.add_option('Exit', PYGAME_MENU_EXIT)

    while True:
        events = pygame.event.get()
        menu.enable()
        menu.mainloop(events)
        pygame.display.flip()

        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pass



