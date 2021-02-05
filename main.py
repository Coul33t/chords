import random as rn

import pygame
from pygame.locals import *

import pygame_menu

COLOURS = ((255, 100, 100), (100, 255, 100), (100, 100, 255), (255, 255, 100), (255, 100, 255), (255, 255, 100))

class Size:
    def __init__(self, w, h):
        self.w = w
        self.h = h

WHITE_KEY_SIZE = Size(25, 110)
BLACK_KEY_SIZE = Size(12, 60)
MAIN_WINDOW_SIZE = Size(1500, 800)

class Key:
    def __init__(self, type, note, octave, x):
        self.type = type

        if type == 'white':
            self.rect = Rect(x, 20, WHITE_KEY_SIZE.w, WHITE_KEY_SIZE.h)
            self.fill_colour = (255, 255, 255)
        else:
            self.rect = Rect(x, 20, BLACK_KEY_SIZE.w, BLACK_KEY_SIZE.h)
            self.fill_colour = (0, 0, 0)

        self.current_colour = self.fill_colour

        self.note = note
        self.octave = octave

    def return_colour(self):
        if self.type == 'white':
            return 1
        return 0

    def get_inside_rect(self, border_size = 1):
        return Rect(self.rect.left + border_size,
        self.rect.top + border_size,
        self.rect.width - border_size * 2,
        self.rect.height - border_size * 2)

    def size_to_str(self):
        return '(' + str(self.rect.left) + ', ' +\
                str(self.rect.top) + ') / (' +\
                str(self.rect.right) + ', ' +\
                str(self.rect.bottom) + ')'

    def __str__(self):
        if self.type == 'white':
            return self.note + str(self.octave) #+ ' ' + self.size_to_str()

        elif self.note[0] == 'G':
            return self.note[:1] + str(self.octave) + self.note[1:-1] + str(self.octave + 1) + self.note[-1:]

        else:
            return self.note[:1] + str(self.octave) + self.note[1:]

class Piano:
    def __init__(self):
        self.keys = []
        self.selected_octave = 4
        self.selected_key = 'A'
        self.selected_mod = 'None'

    def create(self):
        octave_offset = WHITE_KEY_SIZE.w*7
        white_key_offset = WHITE_KEY_SIZE.w
        black_key_offset = WHITE_KEY_SIZE.w - (BLACK_KEY_SIZE.w / 2)

        begin_offset = 4 * white_key_offset

        white_offset = lambda o, k: begin_offset + o*octave_offset + k*white_key_offset
        black_offset = lambda o, k: begin_offset + o*octave_offset + k*white_key_offset + black_key_offset

        self.keys.append(Key('white', 'A',  str(1), begin_offset - white_key_offset))
        self.keys.append(Key('black', 'A#/Bb', str(1), begin_offset - white_key_offset + black_key_offset))
        self.keys.append(Key('white', 'B',  str(1), begin_offset))

        for i in range(7):
            self.keys.append(Key('white', 'C', i+1, white_offset(i, 1)))
            self.keys.append(Key('black', 'C#/Db', i+1, black_offset(i, 1)))
            self.keys.append(Key('white', 'D', i+1, white_offset(i, 2)))
            self.keys.append(Key('black', 'D#/Eb', i+1, black_offset(i, 2)))
            self.keys.append(Key('white', 'E', i+1, white_offset(i, 3)))
            self.keys.append(Key('white', 'F', i+1, white_offset(i, 4)))
            self.keys.append(Key('black', 'F#/Gb', i+1, black_offset(i, 4)))
            self.keys.append(Key('white', 'G', i+1, white_offset(i, 5)))
            self.keys.append(Key('black', 'G#/Ab', i+1, black_offset(i, 5)))
            self.keys.append(Key('white', 'A', i+2, white_offset(i, 6)))
            self.keys.append(Key('black', 'A#/Bb', i+2, black_offset(i, 6)))
            self.keys.append(Key('white', 'B',  i+2, white_offset(i, 7)))

        self.keys.append(Key('white', 'C', 8, white_offset(6, 8)))

        # for i in self.keys:
        #     print(i)

    def find_key(self):
        if self.selected_mod == 'None':
            key_range = (12 * (self.selected_octave - 1), 12 * self.selected_octave)
            for key in self.keys[key_range[0]:key_range[1]]:
                key.current_colour = (255, 255, 100)
            #return self.keys[]

    def light_random_key(self):
        key_idx = rn.randint(0, len(self.keys) - 1)
        colour_idx = rn.randint(0, len(COLOURS) - 1)
        self.keys[key_idx].current_colour = COLOURS[colour_idx]

    def light_key(self):
        self.reset_key_colours()
        self.find_key()

    def light_specific_key(self, selected):
        key = selected[0]
        mod = 'None'
        octave = 0

        # Field doesn't take # as a valid character???
        if selected[1] == 'd' or selected[1] == 'b':
            if selected[1] == 'd':
                mod = '#'
            else:
                mod = 'b'

            octave = int(selected[2])

        else:
            octave = selected[1]

        print(f"{key}{mod if mod != 'None' else ''}{octave}")



    def set_octave(self, selected, value):
        self.selected_octave = int(selected[0][0])
        print(f'SELECTED={selected}, VALUE={value}')

    def set_key(self, selected, value):
        self.selected_key = selected[0][0]
        print(f'SELECTED={selected}, VALUE={value}')

    def set_mod(self, selected, value):
        self.selected_mod = selected[0][0]
        print(f'SELECTED={selected}, VALUE={value}')

    def reset_key_colours(self):
        for key in self.keys:
            key.current_colour = key.fill_colour

    def draw(self, display):
        for key in self.keys:
            if key.type == 'white':
                display.fill((0, 0, 0), key.rect)
                display.fill(key.current_colour, key.get_inside_rect(1))

        for key in self.keys:
            if key.type == 'black':
                display.fill((0, 0, 0), key.rect)
                display.fill(key.current_colour, key.get_inside_rect(1))
            # pygame.draw.rect(display, (0, 0, 0), key.rect, 1)

class Engine:
    def __init__(self):
        self.piano = Piano()
        self.piano.create()
        self.display = self.init_pygame()

        self.menu = pygame_menu.Menu(
            height=MAIN_WINDOW_SIZE.h - 400,
            width=MAIN_WINDOW_SIZE.w - 200,
            title='Test',
            enabled=True,
            mouse_enabled=True,
            theme=pygame_menu.themes.THEME_ORANGE
        )

        self.menu.add_button(title='Test button', id='Test', action=self.piano.light_key)
        self.menu.add_selector('Octave: ', [(str(x+1), x) for x in range(7)], default=4, onchange=self.piano.set_octave)
        self.menu.add_selector('Key: ', [(chr(65+x), x) for x in range(7)], default=0, onchange=self.piano.set_key)
        self.menu.add_selector('Mod: ', [('None', 0), ('#', 1), ('b', 2)], default=0, onchange=self.piano.set_mod)
        self.menu.add_text_input('Desired note:', default='A3', onreturn=self.piano.light_specific_key)
    def init_pygame(self):
        pygame.init()
        return pygame.display.set_mode((MAIN_WINDOW_SIZE.w, MAIN_WINDOW_SIZE.h), 0, 32)

    def display_menu(self):
        pass

    def display(self):
        self.piano.draw()

    def run(self):

        while(True):
            self.display.fill((255, 255, 255))

            while True:
                events = pygame.event.get()
                for event in events:
                    if event.type==QUIT:
                        pygame.quit()
                        return

                if self.menu.is_enabled():
                    self.menu.update(events)
                    self.menu.draw(self.display)

                self.piano.draw(self.display)
                pygame.display.flip()
                pygame.display.update()


def main():
    engine = Engine()
    engine.run()

if __name__ == '__main__':
    main()

# def draw_piano(display, offset=0):
#     for i in range(7):
#         draw_octave(display, offset + i*140)

# def draw_octave(display, offset):
#     for i in range(7):
#         pygame.draw.rect(display, BLACK, (offset + i*20, 20, 20, 75), 1)
#     pygame.draw.rect(display, BLACK, (offset + 15, 20, 10, 40))
#     pygame.draw.rect(display, BLACK, (offset + 35, 20, 10, 40))
#     pygame.draw.rect(display, BLACK, (offset + 75, 20, 10, 40))
#     pygame.draw.rect(display, BLACK, (offset + 95, 20, 10, 40))
#     pygame.draw.rect(display, BLACK, (offset + 115, 20, 10, 40))



    # def white_offset(self, idx):
    #     return idx*octave_offset + key_offset

    # def black_offset(self, idx):
    #     return idx*octave_offset + key_offset + black_offset