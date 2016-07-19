from tkinter import *
import time
from random import choice, randint

ball_initial_number = 20
ball_minimal_radius = 15
ball_maximal_radius = 40
ball_available_colors = '0123456789ABCD'# Набор символов для генерации случайного цвета
balls_coord = []#список координат шариков
balls_num = []#список номеров шариков
points = 0 # Набранные очки
time_game = int(time.time())+100 # Время игры 100 секунд

def click_ball(event):
    """ Обработчик событий мышки для игрового холста canvas
    :param event: событие с координатами клика
    По клику мышкой нужно удалять тот объект, на который мышка указывает.
    А также засчитываеть его в очки пользователя.
    """
    global points, label,  balls_coord, balls_num
    obj = canvas.find_closest(event.x, event.y)
    x1, y1, x2, y2 = canvas.coords(obj)
    num = obj[0]# вытаскиваем номер объекта из кортежа
    if x1 <= event.x <= x2 and y1 <= event.y <= y2:
        canvas.delete(obj)
        index = balls_num.index(num)# определяем индекс элемента списка, где храниться номер объекта
#  Определяем радиус удалённого шарика для начисления очков.
#  За большой шарик меньше очков, чем за маленький
        R = balls_coord[index][3]
        points+=1000//R
        balls_num.pop(index)# удаляем элемент списка с номером объекта
        balls_coord.pop(index)# удаляем элемент списка с координатами объекта
        label['text']=int(points)
        create_random_ball()
    else: # если щелчок мимо, то вычитается 5 очков
        points-=5
        label['text']=int(points)

def move_all_balls(event):
    """ передвигает все шарики на чуть-чуть
    for obj in canvas.find_all():
        dx = randint(-1, 1)
        dy = randint(-1, 1)
        canvas.move(obj, dx, dy)"""
    global balls_coord, points, time_game
    """каждый шарик движется по своей траектории"""
    for obj in balls_coord:
        x1, y1, x2, y2 =canvas.coords(obj[0])
        # проверяем, не выйдет ли шарик за границы холста
        if x1+obj[1]+obj[3]>=400 or x1+obj[1]<=0:
            obj[1]=-obj[1] #меняем направление движения
        if y1+obj[2]+obj[3]>=400 or y1+obj[2]<=0:
            obj[2]=-obj[2]
        canvas.move(obj[0],obj[1],obj[2])
        points-=.01
        label['text']=int(points)

def create_random_ball():
    """
    создаёт шарик в случайном месте игрового холста canvas,
     при этом шарик не выходит за границы холста!
    """
    global balls_coord, balls_num
    R = randint(ball_minimal_radius, ball_maximal_radius)
    x = randint(0, int(canvas['width'])-1-2*R)
    y = randint(0, int(canvas['height'])-1-2*R)
    #рисуем шарик и запоминаем его номер в num_oval
    num_oval = canvas.create_oval(x, y, x+R, y+R, width=0, fill=random_color())
    dx = randint(-2, 2)
    dy = randint(-2, 2)
    # запоминаем идентификатор, вектор и радиус движения нового шарика
    balls_coord.append([num_oval, dx, dy, R])
    balls_num.append(num_oval)# запоминаем номер нового шарика

def random_color():
    """
    :return: Случайный цвет из некоторого набора цветов
    """
    color = '#'
    for c in range(6):
        color = color + choice(ball_available_colors)
    return color

def timer():
    """
    Осушествляет обработку времени игры: обратный отсчёт до 0 секунд.
    По истечении времени перходит к завершению игры.
    """
    if time_game-int(time.time())==0:
        label_time_val.config(text=0)
        end_game()
    else:
        label_time_val.config(text=time_game-int(time.time()))
        label_time_val.after(200, timer)

def end_game():
    """
    Завершение игры. Удаляет все шарики. Выводит результат
    """
    canvas.delete('all')
    text_game_over = 'Игра окончена. Ваш результат: ' + str(int(points))
    label_game_over = Label(root, background='#ffffff', width=57, height=27, text=text_game_over)
    label_game_over.grid(row=3, column=1)
    label_game_over.bind("<Button>", exit_game)
# Не удалось отключить методы для корректного завершения работы
#    canvas.unbind("<Motion>", move_all_balls)
#    canvas.unbind("<Button>", click_ball)

def exit_game(event):
    exit()

def init_ball_catch_game():
    """
    Создаём необходимое для игры количество шариков, по которым нужно будет кликать.
    """
    for i in range(ball_initial_number):
        create_random_ball()

def init_main_window():
    global root, canvas, label, label_time_val

    root = Tk()
    label_text = Label(root, text = 'Набранные очки')
    label_text.grid(row=1,column=0)
    label = Label(root, text=points)#привязка к переменной
    label.grid(row=2,column=0)
    label_time = Label(root, text = 'Время игры')
    label_time.grid(row=1,column=1)
    label_time_val = Label(root, text=time_game)#привязка к переменной
    label_time_val['text']=100
    label_time_val.grid(row=2,column=1)
    canvas = Canvas(root, background='white', width=400, height=400)
    canvas.bind("<Button>", click_ball)
    canvas.bind("<Motion>", move_all_balls)
    canvas.grid(row=3, column=1)
    timer()


if __name__ == "__main__":
    init_main_window()
    init_ball_catch_game()
    root.mainloop()
