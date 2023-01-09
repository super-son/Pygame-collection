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
        self.set_image_font()
        self.board = [[0 for i in range(board_size)] for j in range(board_size)]

    def init_game(self):
        self.turn  = black_stone
        self.draw_board()
        self.menu.show_msg(empty)
        self.init_board()
        self.coords = []
        self.redos = []
        self.id = 1
        self.is_show = True

    def set_image_font(self):
        white_img = pygame.image.load('image/white.png')
        self.white_img = pygame.transform.scale(white_img, (grid_size, grid_size))
        black_img = pygame.image.load('image/black.png')
        self.black_img = pygame.transform.scale(black_img, (grid_size, grid_size))
        self.board_img = pygame.image.load('image/board.png')
        self.font = pygame.font.Font("freesansbold.ttf", 14)

    def init_board(self):
        for y in range(board_size):
            for x in range(board_size):
                self.board[y][x] = 0

    def draw_board(self):
        self.surface.blit(self.board_img, (0, 0))

    def draw_image(self, img_index, x, y):
        img = [self.black_img, self.white_img]
        self.surface.blit(img[img_index], (x, y))

    def show_number(self, x, y, stone, number):
        color = black
        if stone == black_stone:
            color = white
        self.make_text(self.font, str(number), color, x + 15, y + 15, 'center')

    def hide_numbers(self):
        for i in range(len(self.coords)):
            x, y = self.coords[i]
            self.draw_image(i % 2, x, y)

    def show_numbers(self):
        stone = 1
        for i in range(len(self.coords)):
            x, y = self.coords[i]
            self.show_number(x, y, stone, i + 1)
            stone = 3 - stone
        
    def undo(self):
        if not self.coords:
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

    def undo_all(self):
        if not self.coords:
            return
        self.id = 1
        while self.coords:
            coord = self.coords.pop()
            self.redos.append(coord)
            self.init_board()
        self.draw_board()
        self.turn  = black_stone

    def redo(self):
        if not self.redos:
            return
        self.id += 1
        coord = self.redos.pop()
        self.coords.append(coord)
        x, y = self.get_point(coord)
        self.board[y][x] = self.turn
        self.draw_image(self.turn - 1, coord[0], coord[1])
        if self.is_show:
            self.show_numbers()
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
                self.pixel_coords.append((x * grid_size + 25, y * grid_size + 25))

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
        self.board[y][x] = self.turn
        self.coords.append(coord)

        x, y = coord
        self.draw_image(self.turn - 1, x, y)
        if self.is_show:
            self.show_number(x, y, self.turn, self.id)
        self.id += 1
        self.turn = 3 - self.turn
        if len(self.redos):
            self.redos = []
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
        self.undo_rect = self.make_text(self.font, 'Undo', blue, None, top - 150, left)
        self.uall_rect = self.make_text(self.font, 'Undo All', blue, None, top - 120, left)
        self.redo_rect = self.make_text(self.font, 'Redo', blue, None, top - 90, left)

    def show_msg(self, msg_id):
        msg = {
            empty : '                                    ',
            black_stone: 'Black win!!!  ',
            white_stone: 'White win!!!',
            'tie': 'Tie',
        }
        center_x = window_width - (window_width - board_width) // 2
        self.make_text(self.font, msg[msg_id], blue, bg_color, 30, center_x, 1)

    def make_text(self, font, text, color, bgcolor, top, left, position = 0):
        surf = font.render(text, False, color, bgcolor)
        rect = surf.get_rect()
        if position:
            rect.center = (left, top)
        else:    
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
        elif self.uall_rect.collidepoint(pos):
            omok.undo_all()
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
