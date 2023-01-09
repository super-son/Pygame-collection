import pygame

pygame.init() # 반드시해야하는 초기화

# 화면 크기 설정
screen_width = 480 # 가로크기
screen_height = 640 # 세로크기
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("Nado Game") # 게임이름

# FPS
clock = pygame.time.Clock()

#배경 이미지 불러오기
background = pygame.image.load(r"C:\Users\hj144\Desktop\Python\pygame\pygame_basic\images\background.png")
#그림판에서 크기조정:픽셀로 가로, 세로 똑같이 맞추고 직접그린거
#탈출문자 때문에 \를 모두 /로 바꿔주자

# 캐릭터(스프라이트) 불러오기 얘 사이즈는 70*70
character = pygame.image.load(r"C:\Users\hj144\Desktop\Python\pygame\pygame_basic\images\character.png")
character_size = character.get_rect().size #이미지의 크기를 구해옴(rect : 사각)
character_width = character_size[0] # 캐릭터의 가로크기
character_height = character_size[1] # 캐릭터의 세로크기
character_x_pos = (screen_width/2) - (character_width/2) #화면 가로의 절반 크기에 해당하는 곳에 위치
character_y_pos = screen_height - character_height #화면 세로 크기 가장 아래에 위치
#이 캐릭터의 좌표는 배경이미지 (0,0)설정된거 감안해야지

# 이동할 좌표
to_x = 0
to_y = 0

# 이동 속도
character_speed = 0.6

# 적 enemy 캐릭터
enemy = pygame.image.load(r"C:\Users\hj144\Desktop\Python\pygame\pygame_basic\images\enemy.png")
enemy_size = enemy.get_rect().size #이미지의 크기를 구해옴(rect : 사각)
enemy_width = enemy_size[0] # 캐릭터의 가로크기
enemy_height = enemy_size[1] # 캐릭터의 세로크기
enemy_x_pos = (screen_width/2) - (enemy_width/2) #화면 가로의 절반 크기에 해당하는 곳에 위치
enemy_y_pos = (screen_height/2) - (enemy_height/2) #화면 세로 크기 가장 아래에 위치

#폰트 정의
game_font = pygame.font.Font(None, 40) #폰트 객체 생성(폰트,크기)
#총 시간
total_time = 10
#시작 시간정보
start_ticks = pygame.time.get_ticks() #시작 tick을 받아옴



# 이벤트 루프. 이게 없다면 바로꺼진다.
running = True # 게임이 진행중인가?
while running:
    dt = clock.tick(80) #게임화면의 초당 프레임 수 설정. dt는 델타라는 뜻
    # print(dt)
# 캐릭터가 100만큼 이동을 해야함
# 10fps : 1초 동안에 10번 동작 -> 1번에 10만큼 이동해야 10 * 10 = 100
# 20fps : 1초 동안에 20번 동작 -> 1번에 5만큼 이동해야 20 * 5 = 100
    # print("fps: "+str(clock.get_fps())) #fps 실시간 확인가능
    for event in pygame.event.get():
# 필수코드인데 게임을 계속유지하면서 사용자로부터
# 입력이 들어오는지 확인하는것, 어떤 이벤트가 발생하였는지
        if event.type == pygame.QUIT: #창이 닫히는 이벤트 발생
            running = False
        if event.type == pygame.KEYDOWN: #키가 눌러졌는지 확인
            if event.key == pygame.K_LEFT:
                to_x -=character_speed
            elif event.key ==pygame.K_RIGHT:
                to_x +=character_speed
            elif event.key ==pygame.K_UP:
                to_y -=character_speed
            elif event.key ==pygame.K_DOWN:
                to_y +=character_speed

        if event.type == pygame.KEYUP: #방향키를 떼면 멈춤
            if event.key == pygame.K_LEFT or event.key ==pygame.K_RIGHT:
                to_x = 0
            elif event.key == pygame.K_UP or event.key ==pygame.K_DOWN:
                to_y = 0
        
    character_x_pos += to_x * dt # 일괄성을 주기위해 dt값 곱해준다
    character_y_pos += to_y * dt

    #가로 경계값 처리         
    if character_x_pos < 0:
        character_x_pos=0
    elif character_x_pos >= screen_width-character_width : #410
        character_x_pos= screen_width-character_width
    #세로 경계값 처리
    if character_y_pos < 0:
        character_y_pos=0
    elif character_y_pos >= screen_height-character_height : 
        character_y_pos= screen_height-character_height

    # 캐릭터 충돌처리
    character_rect = character.get_rect()
    # 포지션이 변경되서 사실 캐릭터의 rect 정보는 항상 똑같은 위치를 가르킨다 
    character_rect.left = character_x_pos # 그래서 바꿔준다
    character_rect.top = character_y_pos

    enemy_rect = enemy.get_rect()
    enemy_rect.left = enemy_x_pos 
    enemy_rect.top = enemy_y_pos
    #충돌 체크
    if character_rect.colliderect(enemy_rect):
        print("충돌했어요")
        running=False

    screen.blit(background, (0, 0)) #배경이미지 좌표설정
                                    #이미지의 왼쪽위 꼭짓점을 (0,0) 잡게된다
    screen.blit(character, (character_x_pos, character_y_pos)) # 캐릭터 그리기
    screen.blit(enemy, (enemy_x_pos, enemy_y_pos)) # 적 그리기!

    #타이머 집어 넣기
    # 경과 시간 계산
    elapsed_time = (pygame.time.get_ticks()-start_ticks) /1000
    # 경과 시간(ms)을 1000으로 나누어서 초(s) 단위로 표시
    
    timer = game_font.render(str(int(total_time - elapsed_time)), True, (255,255,255))
    # render(시간, True, 글자 색상) 순
    screen.blit(timer, (10,10))
    pygame.display.update() #게임화면을 다시 그리기!
    # print(start_ticks)
    # print(pygame.time.get_ticks()) #이해쫌 한다고 적었다.
    if total_time-elapsed_time <= 0:
        print("time Out")
        running=False

#종료시 잠시만 대기
pygame.time.delay(2000) #2초 정도 대기
# pygame 종료
pygame.quit()
