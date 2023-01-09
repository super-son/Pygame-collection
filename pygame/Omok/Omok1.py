import pygame, sys, random
from pygame.locals import *

board_color1 = (153, 102, 000)
board_color2 = (153, 102, 51)
board_color3 = (204, 153, 000)
board_color4 = (204, 153, 51)
bg_color = (128, 128, 128)
black = (0, 0, 0)
blue = (0, 50, 255)
white = (255, 255, 255)

window_width = 800
window_height = 500
board_width = 500
grid_size = 30
board_size = 15
stone_size = 30
left_margin = 40
top_margin = 30

empty = 0
black_stone = 1
white_stone = 2

fps = 60
fps_clock = pygame.time.Clock()

def main():
    global white_img, black_img
    pygame.init()
    surface = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Omok game")

    white_img = pygame.image.load('image/white.png')
    white_img = pygame.transform.scale(white_img, (stone_size, stone_size))
    black_img = pygame.image.load('image/black.png')
    black_img = pygame.transform.scale(black_img, (stone_size, stone_size))

    surface.fill(bg_color)
    omok = Omok(surface)
    menu = Menu(surface)
    run_game(surface, omok, menu)

def run_game(surface, omok, menu):
    omok.init_game()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                menu.terminate()
            elif event.type == MOUSEBUTTONUP:
                if not omok.check_board(event.pos):
                    if menu.check_rect(event.pos, omok):
                        omok.init_game()

        pygame.display.update()
        fps_clock.tick(fps)

class Omok(object):
    def __init__(self, surface):
        self.menu = Menu(surface)
        self.surface = surface
        self.pixel_coords = []
        self.set_coords()
        self.board = [[0 for i in range(board_size)] for j in range(board_size)]

    def init_game(self):
        self.turn  = black_stone
        self.draw_board()
        self.inti_board()
        self.coords = []
        self.redos = []
        self.id = 1
        self.is_show = True

    def inti_board(self):
        for y in range(board_size):
            for x in range(board_size):
                self.board[y][x] = 0

    def draw_board(self):
        pygame.draw.rect(self.surface, board_color3, (0, 0, board_width, board_width))
        for y in range(board_size):
            for x in range(board_size):
                x1, y1 = x * grid_size + 40, y * grid_size + 40
                x2, y2 = board_width - 40, board_width - 40
                pygame.draw.line(self.surface, black, (x1, y1), (x2, y1))
                pygame.draw.line(self.surface, black, (x1, y1), (x1, y2))
                self.draw_line_number()
                self.draw_point()

    def draw_line_number(self):
        alpha = 'ABCDEFGHIJKLMNO'
        # font = pygame.font.SysFont("ARLRDBD", 22)
        font = pygame.font.Font("freesansbold.ttf", 15)
        j = board_size
        for i in range(board_size):
            x, x1 = i * grid_size + 40, 23
            y, y1 = x, board_width - 13
            self.make_text(font, str(j), black, x1, y, 'midright')
            self.make_text(font, alpha[i], black, x, y1, 'center')
            j -= 1

    def draw_point(self):
        x = grid_size * 3 + 40
        y = board_width - x
        points = [(x, x), (x, y), (y, x), (y, y), (board_width // 2, board_width // 2)]
        for point in points:
            pygame.draw.circle(self.surface, black, point, 3, 0)
    
    def show_number(self, x, y, stone, number):
        font = pygame.font.Font("freesansbold.ttf", 14)
        color = black
        if stone == black_stone:
            color = white
        self.make_text(font, str(number), color, x + 16, y + 16, 'center')

    def hide_numbers(self):
        global white_img, black_img
        img = [black_img, white_img]
        for i in range(self.id - 1):
            x, y = self.coords[i]
            self.surface.blit(img[i % 2], (x + 1, y + 1))

    def show_numbers(self):
        font = pygame.font.Font("freesansbold.ttf", 15)
        for i in range(self.id - 1):
            x, y = self.coords[i]
            color = black
            if i % 2 == 0:
                color = white
            self.make_text(font, str(i + 1), color, x + 16, y + 16, 'center')
        
    def undo(self):
        if self.id == 1:
            return            
        self.id -= 1
        self.draw_board()
        coord = self.coords.pop()
        self.redos.append(coord)
        x, y = self.get_point(coord)
        self.board[y][x] = 0
        if self.is_show:
            self.hide_numbers()
            self.show_numbers()
        else:
            self.hide_numbers()
        self.turn = 3 - self.turn

    def redo(self):
        if not len(self.redos):
            return
        self.id += 1
        coord = self.redos.pop()
        self.coords.append(coord)
        x, y = self.get_point(coord)
        self.board[y][x] = self.turn
        if self.is_show:
            self.hide_numbers()
            self.show_numbers()
        else:
            self.hide_numbers()
        self.turn = 3 - self.turn

    def make_text(self, font, text, color, x, y, position):
        surf = font.render(text, False, color)
        rect = surf.get_rect()
        if position == 'center':
            rect.center = (x, y)
        else:
            rect.midright = (x, y)
        self.surface.blit(surf, rect)

    def set_coords(self):
        for y in range(board_size):
            for x in range(board_size):
                self.pixel_coords.append((x * grid_size + 24, y * grid_size + 24))

    def get_coord(self, pos):
        for coord in self.pixel_coords:
            x, y = coord
            rect = pygame.Rect(x, y, grid_size, grid_size)
            if rect.collidepoint(pos):
                return coord
        return None

    def get_point(self, coord):
        x, y = coord
        x = (x - 25) // grid_size
        y = (y - 25) // grid_size
        return x, y
                                 
    def check_board(self, pos):
        coord = self.get_coord(pos)
        if not coord:
            return False

        x, y = self.get_point(coord)
        if self.board[y][x] != empty:
            return True
        else:
            return self.draw_stone(x, y, coord)
                                  
    def draw_stone(self, x, y, coord):
        global white_img, black_img
        img = [black_img, white_img]
        self.board[y][x] = self.turn
        self.coords.append(coord)

        x, y = coord
        self.surface.blit(img[self.turn - 1], (x + 1, y + 1))
        if self.is_show:
            self.show_number(x, y, self.turn, self.id)
        self.id += 1
        self.turn = 3 - self.turn
        return True
        
class Menu(object):
    def __init__(self, surface):
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.surface = surface
        self.draw_menu()

    def draw_menu(self):
        top, left = window_height - 30, window_width - 200
        self.new_rect = self.make_text(self.font, 'New Game', blue, None, top - 30, left)
        self.quit_rect = self.make_text(self.font, 'Quit Game', blue, None, top, left)
        self.show_rect = self.make_text(self.font, 'Hide Number  ', blue, None, top - 60, left)
        self.undo_rect = self.make_text(self.font, 'Undo', blue, None, top - 120, left)
        self.redo_rect = self.make_text(self.font, 'Redo', blue, None, top - 90, left)

    def show_msg(self, msg_id):
        msg = {
            'X': 'You lost!',
            'O': 'You win!!',
            'tie': 'Tie',
        }
        self.make_text(msg[msg_id], blue, white, center_x, 30)

    def make_text(self, font, text, color, bgcolor, top, left):
        surf = font.render(text, False, color, bgcolor)
        rect = surf.get_rect()
        rect.topleft = (left, top)
        self.surface.blit(surf, rect)
        return rect

    def show_hide(self, omok):
        top, left = window_height - 90, window_width - 200
        if omok.is_show:
            self.make_text(self.font, 'Show Number', blue, bg_color, top, left)
            omok.hide_numbers()
            omok.is_show = False
        else:
            self.make_text(self.font, 'Hide Number  ', blue, bg_color, top, left)
            omok.show_numbers()
            omok.is_show = True

    def check_rect(self, pos, omok):
        if self.new_rect.collidepoint(pos):
            return True
        elif self.show_rect.collidepoint(pos):
            self.show_hide(omok)
        elif self.undo_rect.collidepoint(pos):
            omok.undo()
        elif self.redo_rect.collidepoint(pos):
            omok.redo()
        elif self.quit_rect.collidepoint(pos):
            self.terminate()
        return False
    
    def terminate(self):
        pygame.quit()
        sys.exit()

    def is_continue(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.terminate()
                elif event.type == MOUSEBUTTONUP:
                    if (self.check_rect(event.pos)):
                        return
            pygame.display.update()
            fps_clock.tick(fps)    

if __name__ == '__main__':
    main()
