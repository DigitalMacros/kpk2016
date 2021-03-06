from tkinter import *
from random import choice, randint
from math import *

screen_width = 400
screen_height = 300
timer_delay = 100

class Ball:
    initial_number = 10
    minimal_radius = 10
    maximal_radius = 30
    available_colors = ['green', 'blue', 'red', 'orange', 'magenta']

    def __init__(self):
        """
        Cоздаёт шарик в случайном месте игрового холста canvas,
        при этом шарик не выходит за границы холста!
        """
        R = randint(Ball.minimal_radius, Ball.maximal_radius)
        x = randint(0, screen_width-1-2*R)
        y = randint(0, screen_height-1-2*R)
        self._R = R
        self._x = x
        self._y = y
        fillcolor = choice(Ball.available_colors)
        self._avatar = canvas.create_oval(x, y, x+2*R, y+2*R, width=1, fill=fillcolor, outline=fillcolor)
        if self._avatar > Ball.initial_number:
            canvas.itemconfig(self._avatar, fill='black', outline='black')
        self._Vx = randint(-3, +3)
        self._Vy = randint(-3, +3)

    def fly(self):
        self._x += self._Vx
        self._y += self._Vy
         # отбивается от горизонтальных стенок
        if self._x <= 1 and self._avatar <= Ball.initial_number:
            self._x = 1
            self._Vx = -self._Vx
        elif self._x + 2*self._R >= screen_width - 1:
            self._x = screen_width - 2*self._R -1
            self._Vx = -self._Vx
        # отбивается от вертикальных стенок
        if self._y <= 2 and self._avatar <= Ball.initial_number:
            self._y = 2
            self._Vy = -self._Vy
        elif self._y + 2*self._R >= screen_height - 1:
            self._y = screen_height - 2*self._R  - 1
            self._Vy = -self._Vy
        if self._avatar > Ball.initial_number and (self._x < -1 or self._x > screen_width+1 or self._y < -1 or self._y > screen_height+1):
            shells_on_fly.pop(0)
            canvas.delete(self._avatar)

        canvas.coords(self._avatar, self._x, self._y, self._x + 2*self._R, self._y + 2*self._R)


class Gun:
    def __init__(self):
        self._x = 0
        self._y = screen_height+3
        self._lx = +30
        self._ly = -30
        self._avatar = canvas.create_line\
            (self._x, self._y, self._x+self._lx, self._y+self._ly, width=5)

    def shoot(self):
        """
        :return возвращает объект снаряда (класса Ball)
        """
        shell = Ball()
        shell._R = 5
        shell._x = gun._lx
        shell._y = gun._ly
        shell._Vx = self._lx/10
        shell._Vy = self._ly/10
        shell.fly()
        return shell

def gun_turn(event):
    dx = gun._x - event.x
    dy = abs(gun._y - event.y)
    if dx == 0:
        ang = pi / 2
    else:
        ang = atan(dy / dx)
    dx = 30 * cos(ang)
    dy = screen_height + 30 * sin(ang)
    gun._lx = dx
    gun._ly = dy
    canvas.coords(gun._avatar, gun._x, gun._y, dx, dy)

def init_game():
    """
    Создаём необходимое для игры количество объектов-шариков,
    а также объект - пушку.
    """
    global balls, gun, shells_on_fly
    balls = [Ball() for i in range(Ball.initial_number)]
    gun = Gun()
    shells_on_fly = []

def init_main_window():
    global root, canvas, scores_text, scores_value
    root = Tk()
    root.title("Пушка")
    scores_value = IntVar()
    canvas = Canvas(root, width=screen_width, height=screen_height, bg="white")
    scores_text = Entry(root, textvariable=scores_value)
    canvas.grid(row=1, column=0, columnspan=3)
    scores_text.grid(row=0, column=2)
    canvas.bind('<ButtonRelease-3>', click_event_handler)
    canvas.bind('<Motion>', gun_turn)

def timer_event():
    # все периодические рассчёты, которые я хочу, делаю здесь
    for ball in balls:
        ball.fly()
    for shell in shells_on_fly:
        shell.fly()
    canvas.after(timer_delay, timer_event)


def click_event_handler(event):
    global shells_on_fly
    shell = gun.shoot()
    shells_on_fly.append(shell)

if __name__ == "__main__":
    init_main_window()
    init_game()
    timer_event()
    root.mainloop()