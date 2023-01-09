import pygame

pygame.init() # 반드시해야하는 초기화

# 화면 크기 설정
screen_width = 480 # 가로크기
screen_height = 640 # 세로크기
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("Nado Game") # 게임이름

# 이벤트 루프. 이게 없다면 바로꺼진다.
running = True # 게임이 진행중인가?
while running:
    for event in pygame.event.get():
# 필수코드인데 게임을 계속유지하면서 사용자로부터
# 입력이 들어오는지 확인하는것, 어떤 이벤트가 발생하였는지
        if event.type == pygame.QUIT: #창이 닫히는 이벤트 발생
            running = False

# pygame 종료
pygame.quit()

