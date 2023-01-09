import os
import pygame
#################################################################
#기본 초기화 (반드시 해야 하는 것들)
pygame.init()

# 화면 크기 설정
screen_width = 640 # 가로크기
screen_height = 480 # 세로크기
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("Nado Pang") # 게임이름

# FPS
clock = pygame.time.Clock()
#################################################################

# 1. 사용자 게임 초기화(배경 화면, 게임 이미지, 좌표, 속도, 폰트 등)
current_path = os.path.dirname(__file__) #현재 파일의 위치 반환
image_path = os.path.join(current_path, "images") # 이미지 폴더 위치 변환

#배경만들기
background = pygame.image.load(os.path.join(image_path, "background.png"))

#스테이지 만들기
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1]

#캐릭터 만들기
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width/2)-(character_width/2)
character_y_pos = screen_height - stage_height - character_height

character_to_x_LEFT=0 #부드러운 무빙 코드
character_to_x_RIGHT=0
character_speed=5

# 무기 만들기
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# 무기는 한 번에 여러 발 발사 가능
weapons = []

# 무기 이동 속도
weapon_speed = 10

# 공 만들기
ball_images = [
    pygame.image.load(os.path.join(image_path, "ball1.png")),
    pygame.image.load(os.path.join(image_path, "ball2.png")),
    pygame.image.load(os.path.join(image_path, "ball3.png")),
    pygame.image.load(os.path.join(image_path, "ball4.png"))]

# 공 크기에 따른 최초 스피드 (y축으로만 속도변화)
ball1_speed_y = [-18, -15, -12, -9] #index 0,1,2,3에 해당

#공들 #딕셔너리로 다룰 예정
balls = []

#최초 발생하는 큰공 추가
balls.append({
    "pos_x" : 50, #공의 x좌표
    "pos_y" : 50, #공의 y좌표
    "img_idx" : 0, #공의 이미지 인덱스
    "to_x":3, #x축 이동방향, -3이면 왼쪽 3이면 오른쪽
    "to_y":-6, #y축 이동방향
    "init_spd_y" : ball1_speed_y[0]}) #y 최초속도



running = True # 게임이 진행중인가?
while running:
    dt = clock.tick(30) 
    # 2.이벤트 처리(키보드, 마우스 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_x_LEFT -= character_speed
            elif event.key == pygame.K_RIGHT:
                character_to_x_RIGHT += character_speed
            elif event.key == pygame.K_SPACE:
                weapon_x_pos = character_x_pos + (character_width/2) - (weapon_width/2)
                weapon_y_pos = character_y_pos #위치먼저 정의해주고   
                weapons.append([weapon_x_pos,weapon_y_pos])
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT :
                character_to_x_LEFT = 0
            if event.key == pygame.K_RIGHT:
                character_to_x_RIGHT = 0

    # 3. 게임 캐릭터 위치 정의
    character_x_pos += character_to_x_LEFT + character_to_x_RIGHT

    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width
    # 무기 위치 조정 # 또다시 위치가 조정된 리스트로 재탄생
    # 100, 200 -> 180, 160, 140, ...
    # 500, 200 -> 180, 160, 140, ...
    weapons = [ [w[0], w[1] - weapon_speed] for w in weapons] #무기를 올리는작업

    # 천장에 닿은 무기 없애기
    weapons = [ [w[0], w[1] ] for w in weapons if w[1] > 0] 
        #조건에 부합하지않는 건 빼겠다는 거네

    #공 위치 정의(enumerate : 해당 인덱스와 값을 보여준다)
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        #가로벽에 닿았을때 공 이동위치 변경(바운스)
        if ball_pos_x <0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"] * -1 

        #세로 위치
        #스테이지에 튕겨서 올라가는 처리
        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_spd_y"] 
        else: # 그 외의 모든 경우에는 속도를 줄여나감
            ball_val["to_y"] += 0.5

        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]
    # 4. 충돌 처리
    
    # 5. 화면에 그리기
    screen.blit(background, (0,0))

    for weapon_x_pos, weapon_y_pos in weapons: 
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for idx,val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x,ball_pos_y))


    screen.blit(stage, (0,screen_height-stage_height))
    screen.blit(character,(character_x_pos,character_y_pos))

    
    
    pygame.display.update() 
        
#종료시 잠시만 대기
pygame.time.delay(1000) #2초 정도 대기(ms)

# pygame 종료
pygame.quit()
