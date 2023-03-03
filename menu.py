from tkinter import*
from tkinter import messagebox as mb
from time import sleep
from game import all

# цвета которые используются у интерфейса
theme = '#171717'
obj_color = '#212121'


class mv:
    # переменные, отвечающие за максимальный размер окна
    max_width = 1200
    max_height = 700

    # переменные, отвечающие за минимальный размер окна
    min_width = 400
    min_height = 700
    
    # переменные, отвечающие за текущий размер окна
    current_width = min_width
    current_height = min_height

    # переменная, отвечающая за проверку того, можно ли нажимать на кнопки, когда проигрывается анимация их движения
    can_click = False

# класс, отвечающий за передачу данных в файл с игрой
class cfg:
    min_ball_speed = 5
    max_ball_speed = 12
    player_speed = 8
    max_rounds = 10

    pl1_color = 'white'
    pl2_color = 'white'
    ball_color = 'white'
    bg_color = 'black'

# параметры окна
w = Tk()
w.geometry(f'{mv.min_width}x{mv.min_height}')
w.resizable(width= 0, height=0)
w.title('Pong Menu')
w['bg'] = theme

# создание окна предпросмотра
c = Canvas(w, width=320, height=220, bg='black')
c.place(x=450, y=430) 

# функция, отвечающая за начало игры на кнопку ИГРАТЬ
def play():
    if mv.can_click:
        w.destroy() 
        all(cfg.player_speed, cfg.min_ball_speed, cfg.max_ball_speed, cfg.max_rounds, cfg.bg_color, cfg.pl1_color, cfg.pl2_color, cfg.ball_color)

# функция, отвечающая за выход из программы на кнопку ВЫХОД
def exit():
    if mv.can_click:
        w.quit()

# функция, отвечающая за анимацию открытия настроек на кнопку НАСТРОЙКИЙ
def options_open():
    if mv.can_click:
        options_button.hide()
        while mv.current_width <= mv.max_width:
            mv.current_width += 10
            w.geometry(f'{mv.current_width}x{mv.min_height}')
            w.update()
            sleep(0.01)
        back_options_button.move(15, 565)

# функция, отвечающая за анимацию закрытия настроек на кнопку НАЗАД
def options_close():
    back_options_button.hide()
    while mv.current_width > mv.min_width:
        mv.current_width -= 10
        w.geometry(f'{mv.current_width}x{mv.min_height}')
        w.update()
        sleep(0.01)
    options_button.move(15, 565)

# функция, отвечающая за показ окна возможных параметров в настройках на кнопку INFO
def show_options_info():
    mb.showinfo(title='Информация о настройках', message='Минимальная Скорость Шара(1-8), Максимальная Скорость Шара(8-20), Скорость игрока(3-20), Раунды до победы(1-99), Смена цвета - цифры(0-9), буквы(A-F), сперва пишется "#", а затем 6 символов после неё, указанных ранее. Внимание: "Окно предпросмотра" показывает только цвета объектов, и не более!')

# функция, отвечающая за показ окна возможных информации о проекте на кнопку ИНФОРМАЦИЯ
def show_info():
    if mv.can_click:
        mb.showinfo(title='Информация о проекте', message='Управление без CAPS LOCK на англ. раскладке для игрока слева - "w" и  "s". Управление для игрока справа - "Стрелочка вверх" и "Стрелочка вниз". Создан только при помощи стандартных библиотек в Python!')

# функция, отвечающая за присвоение виджету ввода стандартных, прописанных в др. функциях значений
def default(obj, value):
    obj.clear()
    obj.write(value)

# функция, отвечающая за проверку значений в виджете ввода(исключая цвета) и выдачу ошибки, если оно не будет соответсвовать заданным
def value_error(ent, dft, txt, min, max):
    try:
        var = int(ent.return_get())
    except:
        mb.showerror(title='Ошибка', message=f'"{txt}" содержит не число, будет установлено значение по умолчанию!')
        default(ent, dft)
        var = dft

    if var < min or var > max:
        mb.showerror(title='Ошибка', message=f'"{txt}" выходит за заданные пределы, будет установлено значение по умолчанию! Пожалуйста, посмотрите возможные значения во вкладке INFO.')
        default(ent, dft)
        value = dft
        return value
    else:
        return var

# функция, отвечающая за проверку значений в виджете ввода цвета и выдачу ошибки, если оно не будет соответсвовать возможным
def color_error(ent, txt, obj):
    try:
        c.itemconfig(obj, fill=ent.return_get())
    except:
        mb.showerror(title='Ошибка', message=f'"{txt}" содержит неправильное значение, будет установлено значение по умолчанию!')
        default(ent, '#ffffff')
        value = '#ffffff'
        c.itemconfig(obj, fill='#ffffff')
        return value

# функция, отвечающая за присвоение значений в файл с игрой
def apply():
    # функции проверки
    cfg.ball_color = color_error(ball_color_ent, 'Цвет шарика', oval)

    cfg.pl1_color = color_error(pl1_color_ent, 'Цвет игрока слева', blk1)

    cfg.pl2_color = color_error(pl2_color_ent, 'Цвет игрока справа', blk2)

    ball_min_value = value_error(ball_min_speed_ent, 5, 'Минимальная Скорость Шара', 1, 8)

    ball_max_value = value_error(ball_max_speed_ent, 12, 'Максимальная Скорость Шара', 8, 20)

    player_value = value_error(player_speed_ent, 8, 'Скорость игрока', 3, 20)

    max_rounds = value_error(max_rounds_ent, 10, 'Раунды до победы', 1, 99)

    try:
        c['bg'] = bg_color_ent.return_get()
    except:
        mb.showerror(title='Ошибка', message='"Цвет фона" содержит неправильное значение, будет установлено значение по умолчанию!')
        default(bg_color_ent, '#000000')
        cfg.bg_color = '#000000'
        c['bg'] = '#000000'

    # присвоение значений
    cfg.min_ball_speed = ball_min_value
    cfg.max_ball_speed = ball_max_value
    cfg.player_speed = player_value
    cfg.max_rounds = max_rounds

    cfg.ball_color = ball_color_ent.return_get()
    cfg.pl1_color = pl1_color_ent.return_get()
    cfg.pl2_color = pl2_color_ent.return_get()
    cfg.bg_color = bg_color_ent.return_get()

# функция, отвечающая за анимацию движения текста, выводимого в окне
def label_animation(obj, y_cur, x_pos, y_pos, speed):
    while y_cur <= y_pos:
        obj.place(x_pos, y_cur)
        y_cur+=speed
        w.update()
        sleep(0.01)

# функция, отвечающая за анимацию движения кнопок, в главном меню
def button_animation(obj, x_cur, x_pos, y_pos, speed):
    while x_cur <= x_pos:
        obj.move(x_cur, y_pos)
        x_cur+=speed
        w.update()
        sleep(0.005)

# класс отвечающий за создаие кнопок, дополнительно задающий им функции
class Buttons:
    def __init__(self, txt, cmd, xpos, ypos, wth):
        self.button = Button(w, fg='white', bg=obj_color, font=('Comic Sans MS', 30, 'bold'), text=txt, relief='flat', width=wth, command=cmd)  #присвоение параметров кнопке
        self.xpos = xpos    #переменная, принимающая в себя значение оси x
        self.ypos = ypos    #переменная, принимающая в себя значение оси y
        self.move(xpos, ypos)

    def hide(self):
        self.button.place_forget()

    # функция, отвечающая за установку кнопок в окне
    def move(self, x_pos, y_pos):
        self.button.place(x=x_pos, y=y_pos)

# класс отвечающий за создаие текста, дополнительно задающий им функции
class Labels:
    def __init__(self, txt, xpos, ypos, ft, color='white'):
        self.text = Label(fg=color, bg=theme, font=('Comic Sans MS', ft, 'bold'), text=txt)      #присвоение параметров тексту, выводимого в окне
        self.text.place(x=xpos, y=ypos)

    # функция, отвечающая за установку текста в окне
    def place(self, x_pos, y_pos):
        self.text.place(x=x_pos, y=y_pos)

# класс отвечающий за создаие виджетов ввода, дополнительно задающий им функции
class Entries:
    def __init__(self, xpos, ypos, ft, wth, write_txt):
        self.ent = Entry(fg='#e1e1e1', bg=obj_color, font=('Comic Sans MS', ft, 'bold'), width=wth, relief='flat', bd=wth)   #присвоение параметров полю ввода
        self.ent.place(x=xpos, y=ypos)     # установка поля ввода по координатам
        self.write(write_txt)

    # функция, отвечающая за запись значения в виджет ввода
    def write(self, value):
        self.ent.insert(0, value)

    # функция, отвечающая за очистку значения в виджет ввода
    def clear(self):
        self.ent.delete(0, 'end')

    # функция, отвечающая за получение значения из виджета ввода
    def return_get(self):
        return self.ent.get()

# создание кнопок в гл. меню
play_button = Buttons('Играть', play, -450, 135, 15)

info_button = Buttons('Информация', show_info, -450, 250, 15)

exit_button = Buttons('Выход', exit, -450, 365, 15)

options_button = Buttons('Настройки', options_open, -450, 565, 15)

back_options_button = Buttons('Назад', options_close, 15, 565, 15)
back_options_button.hide()

# создание кнопок в настройках
info_options_button = Buttons('INFO', show_options_info, 800, 580, 5)

apply_button = Buttons('Применить', apply, 945, 580, 10)

options_text = Labels('Настройки', 635, 5, 45)

# создание заголовка игры
title = Labels('PONG', 85, -100, 60)

# создание текста в настройках
ball_min_speed_txt = Labels('Мин. Скорость Шара:', 425, 110, 20, '#bababa')

ball_max_speed_txt = Labels('Макс. Скорость Шара:', 420, 180, 20, '#bababa')

player_speed_txt = Labels('Скорость Игроков:', 450, 245, 20, '#bababa')

max_rounds_txt = Labels('Раунды до победы:', 440, 310, 20, '#bababa')

ball_color_txt = Labels('Цвет шарика:', 900, 110, 20, '#bababa')

pl1_color_txt = Labels('Цвет игрока слева:', 860, 220, 20, '#bababa')

pl2_color_txt = Labels('Цвет игрока справа:', 852, 330, 20, '#bababa')

pl2_color_txt = Labels('Цвет фона:', 910, 440, 20, '#bababa')

preshow_win_txt = Labels('Окно предпросмотра', 470, 380, 20, '#bababa')

# создание полей ввода в настройках
ball_min_speed_ent = Entries(725, 110, 22, 2, 5)

ball_max_speed_ent = Entries(730, 180, 22, 2, 12)

player_speed_ent = Entries(710, 245, 22, 2, 8)

max_rounds_ent = Entries(725, 305, 22, 2, 10)

ball_color_ent = Entries(925, 160, 22, 7, '#ffffff')

pl1_color_ent = Entries(923, 275, 22, 7, '#ffffff')

pl2_color_ent = Entries(921, 380, 22, 7, '#ffffff')

bg_color_ent = Entries(921, 490, 22, 7, '#000000')

# создание объектов в окне предпросмотра
blk1 = c.create_rectangle(1, 85, 10, 135, fill='white')
blk2 = c.create_rectangle(323, 85, 313, 135, fill='#ffffff')
oval = c.create_oval(157, 107, 172, 122, fill='white')

# проигрывание анимаций объектов в гл. меню
label_animation(title, -250, 85, 5, 3)

button_animation(play_button, -400, 15, 135, 5)

button_animation(info_button, -400, 15, 250, 5)

button_animation(exit_button, -400, 15, 365, 5)

button_animation(options_button, -400, 15, 565, 5)

mv.can_click = True

# класс, отвечающий за движение игроков в окне предпросмотра
class pl_pre_show:
    def __init__(self, pl, dir):
        self.pl = pl
        self.dir = dir

    def pl_move(self, speed):
        c.move(self.pl, 0, speed*self.dir)   
        pos = c.coords(self.pl)    
        if pos[3] >= 220 or pos[1] <= 0:
            self.dir = -self.dir

# класс, отвечающий за движение шарика в окне предпросмотра
class ball_preshow:
    def __init__(self):
        self.ball_speed = 4

    def ball_move(self):
        pos = c.coords(oval)
        
        if pos[1] <= 0 or pos[3] >= 220:
            self.ball_speed = -self.ball_speed
        c.move(oval, 0, self.ball_speed)

# присвоение переменным классов, находящихся выше
pl1 = pl_pre_show(blk1, 1)
pl2 = pl_pre_show(blk2, -1)
ball = ball_preshow()

# цикл, отвечающий за обновление окна предпросмотра 100 раз в сек.
while True:
    pl1.pl_move(2)
    pl2.pl_move(2)
    ball.ball_move()
    w.update()
    sleep(0.01)