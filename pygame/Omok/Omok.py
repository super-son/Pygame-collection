import pygame, sys, random
from pygame.locals import *

board_color1 = (153, 102, 000)
board_color1 = (153, 102, 51)
board_color1 = (204, 153, 000)
board_color1 = (204, 153, 51)

window_width = 800
window_height = 500
board_size = 500
grid_size = 30

fps = 30
fps_clock = pygame.time.Clock()

def main():
    pygame.init()
    surface = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Omok game")

    white_img = pygame.image.load('image/white.png')
    black_img = pygame.image.load('image/black.png')
    white_img = pygame.transform.scale(white_img, (grid_size, grid_size))
    black_img = pygame.transform.scale(black_img, (grid_size, grid_size))
    
    surface.fill(board_color1)
    for i in range(15):
        for j in range(15):
            if j % 2 == 0:
                surface.blit(white_img, (j * grid_size + 25, i * grid_size + 25))
            else:
                surface.blit(black_img, (j * grid_size + 25, i * grid_size + 25))
    run_game(surface)

def run_game(surface):
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        fps_clock.tick(fps)
    

if __name__ == '__main__':
    main()
