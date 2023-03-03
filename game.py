from tkinter import*
from tkinter import messagebox as mb
from random import choice
from time import sleep
import winsound as ws
from os import system

def all(pl_s, b_min_s, b_max_s, m_r, bg_c, pl1_c, pl2_c, ball_c):   
    class mv:
        game_started = False    # перевенная отвечающая за проверку того, началась игра или нет
        max_score = m_r     # перевенная отвечающая за макимально возможный счёт игроков
        player1_score = 0   # перевенная отвечающая за счёт игрока слева
        player2_score = 0   # перевенная отвечающая за счёт игрока справа
        minutes = 0     # перевенная отвечающая за счёт минут в секундомере
        seconds = 0     # перевенная отвечающая за счёт секунд в секундомере

    # создание окна
    w = Tk()
    w.geometry('1100x675')
    w.resizable(width=0, height=0)
    w['bg'] = 'black'
    w.title('Pong')

    # создание холста с игрой
    c = Canvas(w, width=1075, height=575, bg=bg_c)
    c.place(x=10, y=85)
    c.focus_set()    

    # функция, отвечающая за секундомер
    def Stopwatch():
        if mv.minutes < 60:
            w.after(1000, Stopwatch)

        if mv.minutes > 9:    
            timer = f'{mv.minutes}:0{mv.seconds}'    
            if mv.seconds > 9:
                timer = f'{mv.minutes}:{mv.seconds}'            
        else:
            timer = f'0{mv.minutes}:0{mv.seconds}'
            if mv.seconds > 9:
                timer = f'0{mv.minutes}:{mv.seconds}'            

        if mv.minutes == 60:
            timer = 'xx:xx' 

        mv.seconds += 1

        if mv.seconds == 60:
            mv.seconds = 0
            mv.minutes += 1 

        time['text'] = (timer)
    
    # функция, отвечающая за объявление начала игры по кнопке ПРОБЕЛ
    def starting(event):
        if not mv.game_started:
            press_space.pack_forget()
            mv.game_started = True
            ws.PlaySound('space.wav', 1)

    # функция, отвечающая за объявление паузы
    def pause_game():
        press_space['text'] = 'Press SPACE to Continue!'
        press_space.pack(pady=10)
        mv.game_started = False  

    # класс, отвечающий за содание игроков на холсте и функций, присваиваемых игрокам
    class player:
        def __init__(self, pl, keyup, keydown):
            self.blk = pl    # присвоение переменной одного из игроков
            self.speed = 0    # текущая скорость игрока
            self.max_speed = pl_s    # максимальная скорость игрока
            self.pos = ()    # текущая позиция игрока
            
            c.bind(keyup, self.up)
            c.bind(keydown, self.down)

        # функция, отвечающая за смену направления движения игрока вверх
        def up(self, event):
            self.speed = 0
            if self.pos[1] > 0 and mv.game_started:
                mv.dir = -1
                self.speed = self.max_speed * -1            

        # функция, отвечающая за смену направления движения игрока вниз
        def down(self, event):
            self.speed = 0
            if self.pos[3] < 575 and mv.game_started:
                mv.dir = 1
                self.speed = self.max_speed * 1    

        # функция, отвечающая за движение игрока
        def pl_move(self):               
            c.move(self.blk, 0, self.speed) 
            self.pos = c.coords(self.blk)      
            if self.pos[1] <= 0:
                self.speed = 0
            if self.pos[3] >= 575:
                self.speed = 0

    # класс, отвечающий за содание шарика на холсте и функций, присваиваемых ему
    class Ball:
        def __init__(self):
            self.speed_x = 0    # текущая скорость шарика по оси x
            self.speed_y = 0    # текущая скорость шарика по оси y
            self.min_speed_x = b_min_s      # минимальная скорость шарика по оси x
            self.min_speed_y = self.min_speed_x / 1.25      # минимальная скорость шарика по оси y
            self.max_speed_x = b_max_s      # максимальная скорость шарика по оси x
            self.max_speed_y = self.max_speed_x / 1.2      # максимальная скорость шарика по оси y
            self.random_dir = True     #проверка, можно ли шарику менять направление в случайную сторону

        # функция, которая вызывается при столкновении горизонтальной стеной
        def horiz_wall(self):
            pause_game()
            c.moveto(ball, 535, 285)
            self.random_dir = True
                
            ws.PlaySound('score_plus.wav', 1)

        # функция, которая вызывается при столкновении с вертикальной стеной
        def vert_wall(self, value):
            self.speed_y = -self.speed_y
            if self.speed_y <= self.max_speed_y:
                self.speed_y += value
                ws.PlaySound('ball_hit.wav', 1)

        # функция, которая вызывается при столкновении с игроками
        def player_collision(self, dir, value):
            self.speed_x = -self.speed_x
            c.move(ball, 10*dir, 0)
            if self.speed_x <= self.max_speed_x:
                self.speed_x += value
                ws.PlaySound('ball_hit.wav', 1)

        # функция, отвечающая за проверку столкновения с объектами
        def collision(self):
            ball_pos = c.coords(ball)
            
            if ball_pos[0] <= crds.pl1_pos[2] and ball_pos[3] >= crds.pl1_pos[1] and ball_pos[1] <= crds.pl1_pos[3]:
                self.player_collision(1, choice((0.1, 0.15, 0.2, 0.25, 0,3)))

            elif ball_pos[2] >= crds.pl2_pos[0] and ball_pos[3] >= crds.pl2_pos[1] and ball_pos[1] <= crds.pl2_pos[3]:
                self.player_collision(-1, -choice((0.1, 0.15, 0.2, 0.25, 0,3)))

            if ball_pos[1] <= 0:
                self.vert_wall(choice((0.05, 0.1, 0.15, 0.2)))

            elif ball_pos[3] >= 575:
                self.vert_wall(-choice((0.05, 0.1, 0.15, 0.2)))

            if ball_pos[0] <= 0:
                self.horiz_wall()

                mv.player2_score += 1        
                pl2_score['text'] = mv.player2_score  

            elif ball_pos[2] >= 1075:
                self.horiz_wall() 

                mv.player1_score += 1        
                pl1_score['text'] = mv.player1_score  
                    
            self.move()

        # функция, отвечающая за движение шарика
        def move(self):
            if self.random_dir:
                self.speed_x = 0
                self.speed_y = 0
                if mv.game_started:
                    self.speed_x = choice((self.min_speed_x, -self.min_speed_x))
                    self.speed_y = choice((self.min_speed_y, -self.min_speed_y))
                    self.random_dir = False

            c.move(ball, self.speed_x, self.speed_y)

    # cоздание таймера
    time = Label(fg='white', bg='black', font=('Comic Sans MS', 40, 'bold'))
    time.pack()

    Stopwatch()
    
    #создание объектов в холсте
    blk1 = c.create_rectangle(1, 250, 21, 370, fill=pl1_c)
    blk2 = c.create_rectangle(1057, 250, 1077, 370, fill=pl2_c)  

    ball = c.create_oval(520, 290, 555, 325, fill=ball_c)

    # создание текста, выводимого при начале игры, паузе и окончание
    press_space = Label(fg='#cfcfcf', bg=bg_c, font=('Showcard Gothic', 50, 'bold'), text='Press SPACE to Begin!')
    press_space.pack(pady=10)

    # присвоение переменным классов, и задавание кнопок управления
    pl1 = player(blk1, '<w>', '<s>')
    pl2 = player(blk2, '<Up>', '<Down>')

    bl = Ball()

    # бинд кнопки ПРОБЕЛ
    c.bind('<space>', starting)

    # создание и вывод счёта игроков
    pl1_score = Label(fg='white', bg='black', font=('Comic Sans MS', 45, 'bold'), text='0')
    pl2_score = Label(fg='white', bg='black', font=('Comic Sans MS', 45, 'bold'), text='0')
    pl1_score.place(x=200, y=40, anchor=CENTER)
    pl2_score.place(x=900, y=40, anchor=CENTER)

    # класс, содержащий в себе координаты игроков
    class crds:
        pl1_pos = c.coords(blk1)
        pl2_pos = c.coords(blk2)

    # функция с присвоением значения переменным, при обновлении окна
    def coords_update():
        crds.pl1_pos = c.coords(blk1)
        crds.pl2_pos = c.coords(blk2)

    # функция проверки победы
    def check_win(pl_s, txt):
        if pl_s >= mv.max_score:
            press_space['text'] = 'Game Over!'
            winner = mb.showinfo(title='Game Over!', message=f'The {txt} Player Wins!')
            if winner:
                w.destroy()
                system('python menu.py')

    # цикл обновления окна 
    while True:
        pl1.pl_move()
        pl2.pl_move()
        coords_update()
        bl.collision()
        check_win(mv.player1_score, 'Left')
        check_win(mv.player2_score, 'Right')
        w.update()    
        sleep(0.01)