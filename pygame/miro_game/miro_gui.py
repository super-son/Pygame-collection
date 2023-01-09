from tkinter import *
import tkinter.ttk as ttk
import os
import keyboard
import time
import tkinter.font
from random import *
import pygame

#pyinstaller을 위한 함수설정
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
    pygame_start

#기본설정
root = Tk()
root.title("Miro World")
root.geometry("640x480")

font=tkinter.font.Font(family="휴먼가는팸체", size=20, weight="normal", underline = "False", overstrike = "False")
# slant="italic"
font2=tkinter.font.Font(family="휴먼가는팸체", size=15, weight="normal", underline = "False", overstrike = "False")

# 큰 프레임 설정
frame = Frame(root, relief="solid", bd=2, bg="white")
frame.pack(expand=True)

label1 = Label(frame, text="환영합니다",font=font,bg="white")
label1.pack(padx=5, pady=5)

photo = PhotoImage(file=resource_path(r"images\spider_login.png"))
label2 = Label(frame, image=photo,bg="white")
label2.pack()

# 정보 입력창
frame2 = Frame(frame, bg="white")
frame2.pack()
id_W = Label(frame2, text="아이디",font=font2,bg="white").pack(side="left",padx=11, pady=3)
id_input = Entry(frame2) ## .pack 묶어쓰니 get()을 못하네
id_input.pack(side="right",padx=10)

frame3 = Frame(frame, bg="white")
frame3.pack()
pw_W = Label(frame3, text="비밀번호",font=font2,bg="white").pack(side="left", padx=5, pady=3)
pw_input = Entry(frame3, show="*")
pw_input.pack(side="right",padx=10)

# 비밀번호 암호화설정
# 엔트리의 show 옵션을 이용하라!
# passwd-entry = Entry(root, show ="*")

# 로그인 함수설정
def login_check():
    if id_input.get() == 'hj1447' and pw_input.get() == 'jun5281447' :
        login_change()
    else :
        label1.config(text="로그인 정보가 맞지않습니다",font=font) 
        
def login_change():
    label1.config(text="로그인 되었습니다",font=font) 
    global photo2
    photo2 = PhotoImage(file=resource_path(r"images\spider_login2.png"))
    label2.config(image=photo2)
    frame2.destroy()
    frame3.destroy()
    frame4.destroy() # frame4 초기화!!

    #초기화후 음악선택
    frame5 = Frame(frame, bg="white")
    frame5.pack()
    label3 = Label(frame5, text="BGM",font=font2,bg="white").pack(side="left",padx=10,pady=5)
    song_list = ["원슈타인 - 사랑은","아이유 - 시간의 바깥", "아웃사이더 - 늙은 개"] 
    combobox = ttk.Combobox(frame5, width =25, height=5, values=song_list)
    combobox.pack(side="right",padx=5,pady=12)

    #게임시작 버튼
    frame6 = Frame(frame, bg="white")
    frame6.pack(fill="x")
    exit_button = Button(frame6, text="로그아웃",font=font2,bg="white",command=root.destroy)
    exit_button.pack(side="left",padx=10,pady=8,ipady=3,)
    start_button = Button(frame6, text="게임시작",font=font2,bg="white",command=pygame_start)
    start_button.pack(side="right",padx=10,pady=8,ipady=3)

def sorry():
    label1.config(text="죄송합니다. 서비스 준비중입니다", font=font) 
    
# 버튼
frame4 = Frame(frame, bg="white")
frame4.pack()
btn1=Button(frame4, text="회원가입",font=font2, command=sorry,bg="white")
btn2=Button(frame4, text="아이디/비밀번호 찾기",font=font2, command=sorry,bg="white")
btn3=Button(frame4, text="로그인",font=font2, command=login_check, bg="yellow")
keyboard.add_hotkey("enter", login_check) # 사용자가 엔터를 누르면

btn1.pack(side="left", padx=5, pady=5, ipady=3)
btn2.pack(side="left", padx=5, pady=5, ipady=3)
btn3.pack(side="right", padx=5, pady=5, ipady=3)


def pygame_start():
    root.destroy()
    ######################################################
    #초기화
    pygame.init()

    #스크린 설정
    screen_width = 640
    screen_height = 480
    screen = pygame.display.set_mode((screen_width, screen_height))

    # FPS
    clock = pygame.time.Clock()

    # 화면 타이틀 설정
    pygame.display.set_caption("Miro World") 
    pygame.mixer.init()     
    pygame.mixer.music.load(r'C:\Users\hj144\Desktop\손휘준의 개인폴더\Coding\Python\pygame\miro_game\사랑은.mp3')
    pygame.mixer.music.play() 

    # 폰트와 시간정의
    game_font1 = pygame.font.SysFont('haettenschweiler', 40)
    game_font2 = pygame.font.SysFont('haettenschweiler', 30)
    game_result = "Game Over"
    total_time = 100
    start_ticks = pygame.time.get_ticks()

    #배경 설정하기
    background = pygame.image.load(r"C:\Users\hj144\Desktop\손휘준의 개인폴더\Coding\Python\pygame\miro_game\images\ground.png")

    #캐릭터 설정하기
    character_list = [
    pygame.image.load(r"C:\Users\hj144\Desktop\손휘준의 개인폴더\Coding\Python\pygame\miro_game\images\spider_left.png"),
    pygame.image.load(r"C:\Users\hj144\Desktop\손휘준의 개인폴더\Coding\Python\pygame\miro_game\images\spider_right.png"),
    pygame.image.load(r"C:\Users\hj144\Desktop\손휘준의 개인폴더\Coding\Python\pygame\miro_game\images\spider_up.png"),
    pygame.image.load(r"C:\Users\hj144\Desktop\손휘준의 개인폴더\Coding\Python\pygame\miro_game\images\spider_down.png")
    ]
    character=character_list[2]
    character_size = character.get_rect().size
    character_width = character_size[0]
    character_height = character_size[1]
    character_x_pos = 0
    character_y_pos = screen_height - character_height

    #캐릭터 무빙세분화 설정
    character_to_x_LEFT=0 
    character_to_x_RIGHT=0
    character_to_y_DOWN=0
    character_to_y_UP=0
    character_speed=0.6

    #적 설정하기
    enemy = pygame.image.load(r'C:\Users\hj144\Desktop\손휘준의 개인폴더\Coding\Python\pygame\miro_game\images\enemy.png')
    enemy_size = enemy.get_rect().size
    enemy_width = enemy_size[0]
    enemy_height = enemy_size[1]
    enemy_x_pos=screen_width - enemy_width
    enemy_y_pos=0

    #적 움직임 설정
    enemy_to_x=0
    enemy_to_y=0
    enemy_speed=0.05

    #적 설정하기
    enemy2 = pygame.image.load(r'C:\Users\hj144\Desktop\손휘준의 개인폴더\Coding\Python\pygame\miro_game\images\enemy.png')
    enemy2_size = enemy2.get_rect().size
    enemy2_width = enemy2_size[0]
    enemy2_height = enemy2_size[1]
    enemy2_x_pos=0
    enemy2_y_pos=0

    #적 움직임 설정
    enemy2_to_x=0
    enemy2_to_y=0
    enemy2_speed=0.05

    # block 설정 #여기서 바로 for로 들어가도 좋을꺼 같은데 지원안된데
    block1 = pygame.image.load(r'C:\Users\hj144\Desktop\손휘준의 개인폴더\Coding\Python\pygame\miro_game\images\block1.png')
    block1_size = block1.get_rect().size
    block1_width = block1_size[0]
    block1_height = block1_size[1]
    block1_x_pos=100
    block1_y_pos=100

    block2 = pygame.image.load(r'C:\Users\hj144\Desktop\손휘준의 개인폴더\Coding\Python\pygame\miro_game\images\block1.png')
    block2_size = block2.get_rect().size
    block2_width = block2_size[0]
    block2_height = block2_size[1]
    block2_x_pos=300
    block2_y_pos=300

    # 이벤트 루프. 
    running = True 
    while running:
        dt = clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False
            ####### 방향키 설정 #########
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    character_to_x_LEFT -= character_speed
                    character=character_list[0]
                if event.key == pygame.K_RIGHT:
                    character_to_x_RIGHT += character_speed
                    character=character_list[1]
                if event.key == pygame.K_UP:
                    character_to_y_UP -= character_speed
                    character=character_list[2]
                if event.key == pygame.K_DOWN:
                    character_to_y_DOWN += character_speed
                    character=character_list[3]

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT :
                    character_to_x_LEFT = 0
                if event.key == pygame.K_RIGHT:
                    character_to_x_RIGHT = 0
                if event.key == pygame.K_UP :
                    character_to_y_UP = 0
                if event.key == pygame.K_DOWN:
                    character_to_y_DOWN = 0

        character_to_x = character_to_x_LEFT + character_to_x_RIGHT
        character_to_y = character_to_y_UP + character_to_y_DOWN
        character_x_pos += (character_to_x)*dt
        character_y_pos += (character_to_y)*dt
        
        # 적의 이동설정 (랜덤으로 방향설정)
        random_vote1=randint(0,2)
        random_vote2=randint(0,2)
        if random_vote1 == 0 :
            enemy_to_x -= enemy_speed
        if random_vote1 == 1 :
            enemy_to_x += enemy_speed
        if random_vote2 == 0 :
            enemy_to_y -= enemy_speed
        if random_vote2 == 1 :
            enemy_to_y += enemy_speed

        enemy_x_pos += enemy_to_x * dt
        enemy_y_pos += enemy_to_y * dt

        random_vote3=randint(0,2)
        random_vote4=randint(0,2)
        if random_vote3 == 0 :
            enemy2_to_x -= enemy2_speed
        if random_vote3 == 1 :
            enemy2_to_x += enemy2_speed
        if random_vote4 == 0 :
            enemy2_to_y -= enemy2_speed
        if random_vote4 == 1 :
            enemy2_to_y += enemy2_speed

        enemy2_x_pos += enemy2_to_x * dt
        enemy2_y_pos += enemy2_to_y * dt

        # 게임 캐릭터 위치 정의
        if character_x_pos < 0:
            character_x_pos = 0
        if character_x_pos > screen_width - character_width:
            character_x_pos = screen_width - character_width
        if character_y_pos < 0:
            character_y_pos = 0
        if character_y_pos > screen_height - character_height:
            character_y_pos = screen_height - character_height

        # 게임 적 위치 정의
        if enemy_x_pos < 0:
            enemy_x_pos = 0
            enemy_to_x =0
        if enemy_x_pos > screen_width - enemy_width:
            enemy_x_pos = screen_width - enemy_width
            enemy_to_x =0
        if enemy_y_pos < 0:
            enemy_y_pos = 0
            enemy_to_y =0
        if enemy_y_pos > screen_height - enemy_height:
            enemy_y_pos = screen_height - enemy_height
            enemy_to_y =0

        if enemy2_x_pos < 0:
            enemy2_x_pos = 0
            enemy2_to_x =0
        if enemy2_x_pos > screen_width - enemy2_width:
            enemy2_x_pos = screen_width - enemy2_width
            enemy2_to_x =0
        if enemy2_y_pos < 0:
            enemy2_y_pos = 0
            enemy2_to_y =0
        if enemy2_y_pos > screen_height - enemy2_height:
            enemy2_y_pos = screen_height - enemy2_height
            enemy2_to_y =0

        # 충돌처리를 위한 rect 정보 업데이트
        character_rect = character.get_rect()
        character_rect.left = character_x_pos
        character_rect.top = character_y_pos
        enemy_rect = enemy.get_rect()
        enemy_rect.left = enemy_x_pos
        enemy_rect.top = enemy_y_pos
        enemy2_rect = enemy2.get_rect()
        enemy2_rect.left = enemy2_x_pos
        enemy2_rect.top = enemy2_y_pos

        block1_rect = block1.get_rect()
        block2_rect = block2.get_rect()
        block1_rect.left = block1_x_pos
        block1_rect.top = block1_y_pos
        block2_rect.left = block2_x_pos
        block2_rect.top = block2_y_pos

        if character_rect.colliderect(enemy_rect):
            game_result="Game Over"
            running=False

        if character_rect.colliderect(enemy2_rect):
            game_result="Game Over"
            running=False

        # 완전히 안 부딫히고 팅기는 코드를 써야하는데 못하겠다.
        if character_rect.colliderect(block1_rect):
            character_to_x_LEFT *= -0.001
            character_to_x_RIGHT *= -0.001
            character_to_y_UP *= -0.001
            character_to_y_DOWN *= -0.001

        if character_rect.colliderect(block2_rect):
            character_to_x_LEFT *= -0.001
            character_to_x_RIGHT *= -0.001
            character_to_y_UP *= -0.001
            character_to_y_DOWN *= -0.001

        if enemy_rect.colliderect(enemy2_rect):
            enemy_to_x *= -1
            enemy_to_y *= -1
            enemy2_to_x *= -1
            enemy2_to_y *= -1
        
        # 그려주기
        screen.blit(background, (0, 0))
        screen.blit(block1, (block1_x_pos, block1_y_pos))
        screen.blit(block2, (block2_x_pos, block2_y_pos))
        screen.blit(character, (character_x_pos,character_y_pos))
        screen.blit(enemy, (enemy_x_pos,enemy_y_pos))
        screen.blit(enemy2, (enemy2_x_pos,enemy2_y_pos))
        pygame.display.update() 

        #경과 시간 계산
        elapsed_time = (pygame.time.get_ticks()-start_ticks)/1000
        timer= game_font2.render("{}".format(int(total_time - elapsed_time)),True,(0,0,255))
        screen.blit(timer,(600,10))

        #초과한 시간처리
        if total_time - elapsed_time <= 0 : 
            game_result = "Time over"
            running=False
        pygame.display.update()
        
    # 메세지도 그려주기
    msg = game_font1.render(game_result,True,(10,250,240))
    msg_rect = msg.get_rect(center=(int(screen_width/2), int(screen_height/2)))
    screen.blit(msg,msg_rect)
    pygame.display.update()
        
    # pygame 종료
    pygame.time.delay(500) 
    pygame.quit()

root.mainloop()
 