import pygame
import os
from random import *
#################################################################
#기본 초기화 (반드시 해야 하는 것들)
pygame.init()

# 화면 크기 설정
screen_width = 480 # 가로크기
screen_height = 640 # 세로크기
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("Nado Game") # 게임이름

# FPS
clock = pygame.time.Clock()
#################################################################

# 1. 사용자 게임 초기화(배경 화면, 게임 이미지, 좌표, 속도, 폰트 등)
current_path = os.path.dirname(__file__) #현재 파일의 위치 반환
image_path = os.path.join(current_path, "images") # 이미지 폴더 위치 변환

background = pygame.image.load(os.path.join(image_path, "background.png"))
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size 
character_width = character_size[0] 
character_height = character_size[1] 
character_x_pos = (screen_width/2) - (character_width/2) 
character_y_pos = screen_height - character_height

enemy = pygame.image.load(os.path.join(image_path, "ddong.png"))
enemy_size = enemy.get_rect().size 
enemy_width = enemy_size[0] 
enemy_height = enemy_size[1] 
enemy_x_pos = randint(0,screen_width-enemy_width)
enemy_y_pos = 0 - enemy_height
enemy2 = pygame.image.load(os.path.join(image_path, "ddong.png"))
enemy2_size = enemy2.get_rect().size 
enemy2_width = enemy2_size[0] 
enemy2_height = enemy2_size[1] 
enemy2_x_pos = randint(0,screen_width-enemy2_width)
enemy2_y_pos = 0 - enemy2_height

while abs(enemy_x_pos-enemy2_x_pos) <= max(enemy_width, enemy2_width) :
    enemy_x_pos =randint(0,screen_width-enemy_width)
    enemy2_x_pos =randint(0,screen_width-enemy2_width)


to_x = 0
to_y = 0
character_speed = 0.6

enemy_to_x = 0
enemy_to_y = 0.6
enemy_speed = 0.6

enemy2_to_x = 0
enemy2_to_y = 0.6
enemy2_speed = 0.6

running = True # 게임이 진행중인가?
while running:
    dt = clock.tick(30) 
    # 2.이벤트 처리(키보드, 마우스 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_LEFT:
                to_x -=character_speed
            elif event.key ==pygame.K_RIGHT:
                to_x +=character_speed
            elif event.key ==pygame.K_UP:
                to_y -= 0
            elif event.key ==pygame.K_DOWN:
                enemy_to_y += enemy_speed

        if event.type == pygame.KEYUP: 
            if event.key == pygame.K_LEFT or event.key ==pygame.K_RIGHT:
                to_x = 0
            elif event.key == pygame.K_UP :
                to_y = 0
            elif event.key ==pygame.K_DOWN :
                enemy_to_y = 0.6

    character_x_pos += to_x * dt 
    character_y_pos += to_y * dt
    enemy_y_pos += enemy_to_y * dt
    enemy2_y_pos += enemy2_to_y * dt

    # 3. 게임 캐릭터 위치 정의
    if character_x_pos < 0:
        character_x_pos=0
    elif character_x_pos >= screen_width-character_width : 
        character_x_pos= screen_width-character_width
    if enemy_y_pos >= screen_height:
        enemy_x_pos = randint(0,screen_width-enemy_width)
        enemy_y_pos=0 - enemy_height
    if enemy2_y_pos >= screen_height:
        enemy2_x_pos = randint(0,screen_width-enemy2_width)
        enemy2_y_pos=0 - enemy2_height
    
    while abs(enemy_x_pos-enemy2_x_pos) <= max(enemy_width, enemy2_width) :
        enemy_x_pos =randint(0,screen_width-enemy_width)
        enemy2_x_pos =randint(0,screen_width-enemy2_width)
        
    # 4. 충돌 처리
    character_rect = character.get_rect()
    character_rect.left = character_x_pos 
    character_rect.top = character_y_pos

    enemy_rect = enemy.get_rect()
    enemy_rect.left = enemy_x_pos 
    enemy_rect.top = enemy_y_pos

    enemy2_rect = enemy2.get_rect()
    enemy2_rect.left = enemy2_x_pos 
    enemy2_rect.top = enemy2_y_pos
    
    if character_rect.colliderect(enemy_rect):
        print("똥에 맞았어요")
        running=False
    if character_rect.colliderect(enemy2_rect):
        print("똥에 맞았어요")
        running=False    

    # 5. 화면에 그리기
    screen.blit(background, (0, 0))  
    screen.blit(character, (character_x_pos, character_y_pos))
    screen.blit(enemy, (enemy_x_pos, enemy_y_pos))
    screen.blit(enemy2, (enemy2_x_pos, enemy2_y_pos))
    pygame.display.update() 
        
#종료시 잠시만 대기
pygame.time.delay(1000) #2초 정도 대기(ms)

# pygame 종료
pygame.quit()
