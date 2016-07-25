from tkinter import *
from random import choice, randint
from math import *

screen_width = 600
screen_height = 400
timer_delay = 100
area_vx_vy = 20 # Диапазон скоростей
ang = pi/2

class Ball:
    """
    Родительскиц класс создания круглых объектов (целей и снарядов)
    """
    def __init__(self, x=0, y=0, r=10, vx=1, vy=-1, color='purple', ay=0):
        """
        Создание шарика
        :param x: начальное полопжение по оси OX
        :param y: начальное полопжение по оси OY
        :param r: радиус
        :param vx: скорость по оси OX
        :param vy: скорость по оси Oy
        :param color: цвет шарика
        :param ay: ускорение по оси OY
        """
        self._number = canvas.create_oval(x, y, x+2*r, y+2*r, width=0, fill=color)

class Target(Ball):
    """
    Подкласс целей (шариков)
    """
    initial_number = 10
    minimal_radius = 10
    maximal_radius = 30
    available_colors = ['green', 'blue', 'red', 'orange', 'magenta']

    def __init__(self):
        r = randint(Target.minimal_radius, Target.maximal_radius)
        x = randint(0, screen_width-2*r)
        y = randint(0, screen_height-2*r)
        color = choice(Target.available_colors)
        self._x = x
        self._y = y
        self._r = r
        self._vx = randint(-area_vx_vy, area_vx_vy)
        self._vy = randint(-area_vx_vy, area_vx_vy)
        super().__init__(self._x, self._y, self._r, self._vx, self._vy, color)

    def target_fly(self):
        self._x += self._vx
        self._y += self._vy
         # отбивается от горизонтальных стенок
        if self._x <= 1:
            self._x = 1
            self._vx = -self._vx
        elif self._x + 2*self._r >= screen_width:
            self._x = screen_width - 2*self._r -1
            self._vx = -self._vx
        # отбивается от вертикальных стенок
        if self._y <= 2 :
            self._y = 2
            self._vy = -self._vy
        elif self._y + 2*self._r >= screen_height:
            self._y = screen_height - 2*self._r  - 1
            self._vy = -self._vy
        canvas.coords(self._number, self._x, self._y, self._x + 2*self._r, self._y + 2*self._r)

class Gun:
    gun_len = 30
    def __init__(self):
        self._x = 0
        self._y = screen_height + 3
        self._lx = Gun.gun_len
        self._ly = -Gun.gun_len
        self._avatar = canvas.create_line(self._x, self._y, self._x+self._lx, self._y+self._ly, width=5)

class Shoot(Ball):
    """
    Класс снарядов на основе класса Ball
    """
    def __init__(self, x=20, y=screen_height-20, r=5, color='black', vx=1, vy=1, ay=.1):
        """
        Создание снаряда
        :param x: полопжение снаряда по оси OX
        :param y: положение снаряда по оси OY 
        :param r: радиус снаряда
        :param color: цвет снаряда
        :param vx: скорость снаряда по оси OX
        :param vy: скорость снаряда по оси OY
        :param ay: ускорение снаряда по оси OY
        """
        self._r = 2.5
        self._x = gun._lx
        self._y = gun._ly - 2 * self._r
        self._vx = vx
        self._vy = -vy
        self._ay = ay
        super().__init__(self._x, self._y, self._r, self._vx, self._vy, 'black', self._ay)

    def shell_fly(self):
        self._x += self._vx
        self._y += self._vy
        self._vy += self._ay
        canvas.coords(self._number, self._x, self._y, self._x + 2*self._r, self._y + 2*self._r)

def gun_turn(event):
    global ang
    if abs(gun._x - event.x) == 0:
        ang = pi / 2
    else:
        ang = atan(abs(gun._y - event.y) / abs(gun._x - event.x))
    gun._lx = Gun.gun_len * cos(ang)
    gun._ly = screen_height - Gun.gun_len * sin(ang)
    canvas.coords(gun._avatar, gun._x, gun._y, gun._lx, gun._ly)

def click_event_handler(event):
    global shells
    shell = Shoot(vx=5, vy=5, ay=.05)
    shells.append(shell)
    shell.shell_fly()

def timer_event():
    # все периодические рассчёты, которые я хочу, делаю здесь
    for ball in balls:
        ball.target_fly()
    for shell in shells:
        shell.shell_fly()
    canvas.after(timer_delay, timer_event)

def init_game():
    """
    Создаём необходимое для игры количество объектов-шариков,
    а также объект - пушку.
    """
    global balls, gun, shells
    balls = [Target() for i in range(Target.initial_number)]
    gun = Gun()
    shells = []

def init_main_window():
    global root, canvas, scores_text, scores_value
    root = Tk()
    root.title("Пушка")
    scores_value = IntVar()
    canvas = Canvas(root, width=screen_width, height=screen_height, bg="white")
    scores_text = Entry(root, textvariable=scores_value)
    canvas.grid(row=1, column=0, columnspan=3)
    scores_text.grid(row=0, column=2)
    canvas.bind('<ButtonRelease-1>', click_event_handler)
    canvas.bind('<Motion>', gun_turn)

if __name__ == "__main__":
    init_main_window()
    init_game()
    timer_event()
    root.mainloop()