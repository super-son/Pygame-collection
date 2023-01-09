import pygame

pygame.init() # 반드시해야하는 초기화

# 화면 크기 설정
screen_width = 480 # 가로크기
screen_height = 640 # 세로크기
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("Nado Game") # 게임이름

#배경 이미지 불러오기
background = pygame.image.load("C:/Users/hj144/Desktop/Coding/python/pygame/pygame_basic/background.png")
#그림판에서 크기조정:픽셀로 가로, 세로 똑같이 맞추고 직접그린거
#탈출문자 때문에 \를 모두 /로 바꿔주자

# 캐릭터(스프라이트) 불러오기
character = pygame.image.load("C:/Users/hj144/Desktop/Coding/python/pygame/pygame_basic/character.png")
character_size = character.get_rect().size #이미지의 크기를 구해옴(rect : 사각)
character_width = character_size[0] # 캐릭터의 가로크기
character_height = character_size[1] # 캐릭터의 세로크기
character_x_pos = (screen_width/2) - (character_width/2) #화면 가로의 절반 크기에 해당하는 곳에 위치
character_y_pos = screen_height - character_height #화면 세로 크기 가장 아래에 위치
#이 캐릭터의 좌표는 배경이미지 (0,0)설정된거 감안해야지

# 이벤트 루프. 이게 없다면 바로꺼진다.
running = True # 게임이 진행중인가?
while running:
    for event in pygame.event.get():
# 필수코드인데 게임을 계속유지하면서 사용자로부터
# 입력이 들어오는지 확인하는것, 어떤 이벤트가 발생하였는지
        if event.type == pygame.QUIT: #창이 닫히는 이벤트 발생
            running = False

    screen.blit(background, (0, 0)) #배경이미지 좌표설정
                                    #이미지의 왼쪽위 꼭짓점을 (0,0) 잡게된다
    screen.blit(character, (character_x_pos, character_y_pos)) # 캐릭터 그리기

    pygame.display.update() #게임화면을 다시 그리기!


# pygame 종료
pygame.quit()
