from tkinter import *

canvas_width = 800                      # ширина игрового поля
canvas_height = 600                     # высота игрового поля
default_cell_size = 10                  # размер клетки по умолчанию (можно изменять в программе)
default_color_life = 'green'            # цвет живой клетки
default_color_not_life = 'white'        # цвет отсутствия жизни в клетке
grid_color = 'lightgray'                # цвет бордюра клетки
begin = False                           # флаг игры (изначально игра не запущена)
time_sleep = 50                         # задержка таймера
default_filename = 'map'                # имя сохраняемого (или считываемого) файла по умолчанию (можно изменять в программе)
steps = False                           # флаг пошагового выполения


class Field:
    def __init__(self):
        """
        инициализация основных переменных класса
        """
        self.cell_size = default_cell_size
        self.color_life = default_color_life
        self.color_no_life = default_color_not_life


    def calc_cell_count(self):
        """
        вычисление размеров поля и создание двумерных списков (массивов) для расчета соседей и вывода на холст
        """
        self.cells_x_count = canvas_width // self.cell_size
        self.cells_y_count = canvas_height // self.cell_size
        self.matrix = [[0] * self.cells_x_count for i in range(self.cells_y_count)]
        self.avatars = [[0] * self.cells_x_count for i in range(self.cells_y_count)]


    def cell_color(self,key):
        """
        вычисление цвета клетки для создания аватара
        :param key: содержимое клетки
        :return: цвет
        """
        colors = {0:self.color_no_life, 1:self.color_life}
        return colors[key]


    def cell_set(self,y,x):
        """
        прорисовка клетки (создание аватара)
        :param y, x: координаты клетки
        """
        self.avatars[y][x] = canvas.create_rectangle(x*self.cell_size, y*self.cell_size,
                                        (x+1)*self.cell_size, (y+1)*self.cell_size,
                                        fill = self.cell_color(self.matrix[y][x]), outline = grid_color)

    def all_paint(self):
        """
        прорисовка (вывод на экран) всего поля
        """
        for y in range(self.cells_y_count):
            for x in range(self.cells_x_count):
                self.cell_set(y,x)


    def change_cell(self,y,x):
        """
        изменение статуса клетки на обратное (жизнь на не_жизнь и наоборот)
        с одновременным изменением аватара на игровом поле
        :param y, x: координаты изменяемой клетки
        """
        if self.matrix[y][x] == 0:
            self.matrix[y][x] = 1
        else:
            self.matrix[y][x] = 0
        canvas.delete(self.avatars[y][x])
        self.cell_set(y,x)


    def next_population(self):
        """
        расчет поля следующего поколения и перерисовка измененных клеток
        :return: количество произведенных изменений на игровом поле
        """
        global count_changes
        count_changes = 0
        new_matrix = [[0] * self.cells_x_count for i in range(self.cells_y_count)]
        for y in range(1,self.cells_y_count-1):
            for x in range(1,self.cells_x_count-1):
                count_of_neighbours = 0
                for i in range(-1,2):
                    for j in range(-1,2):
                        count_of_neighbours += self.matrix[y+i][x+j]
                count_of_neighbours -= self.matrix[y][x]
                if self.matrix[y][x] == 1 and count_of_neighbours == 2 or count_of_neighbours == 3:
                    new_matrix[y][x] = 1
                else:
                    new_matrix[y][x] = 0
        for y in range(1,self.cells_y_count-1):
            for x in range(1,self.cells_x_count-1):
                if new_matrix[y][x] != self.matrix[y][x]:
                    self.change_cell(y,x)
                    count_changes += 1
        return count_changes


def new_field():
    """
    создание нового поля (логично было бы сделать в классе, но тут много всяких виджетов...)
    """
    print('Создание нового поля')
    label['text']='Ждите...'
    if begin:
        start_or_stop()
    label.update()
    field.cell_size = scale.get()
    canvas.delete("all")
    field.calc_cell_count()
    field.all_paint()
    label['text']=''
    label.update()


def mouse_click(event):
    """
    клик мышкой на игровом поле меняет статус клетки на противоположный.
    *кликать можно и во время игры (сделано специально)
    """
    global field
    field.change_cell(event.y // field.cell_size,event.x // field.cell_size)


def start_or_stop():
    """
    запуск или остановка игры (расчета поколений)
    """
    global begin
    if begin:
        button_start_or_stop['text']='Старт'
        print('Программа остановлена.')
    else:
        button_start_or_stop['text']='Стоп'
        print('Поехали!')
    begin = not begin


def save_to_file():
    """
    сохранение игрового поля в файл (текущий каталог)
    имя файла берется из текстового поля
    *возможно только при остановленной игре
    """
    if not begin:
        s = entry.get()
        if s != '':
            f = open(s,"w")
            f.write(str(field.cell_size)+'\n')
            for y in range(0,field.cells_y_count):
                for x in range(0,field.cells_x_count):
                    f.write(str(field.matrix[y][x])+'\n')
            f.close()
            print('Файл '+s+' успешно сохранён.')
    else:
        print('Операция недоступна!')


def load_of_file():
    """
    чтение игрового поля из файла (текущий каталог)
    имя файла берется из текстового поля
    *возможно только при остановленной игре
    """
    global scale
    if not begin:
        s = entry.get()
        try:
            f = open(s,"r")
            scale.set(int(f.readline().strip()))
            new_field()
            for y in range(0,field.cells_y_count):
                for x in range(0,field.cells_x_count):
                    field.matrix[y][x] = int(f.readline().strip())
            f.close()
            field.all_paint()
            print('Содержимое файла '+s+' прочитано.')
        except IOError:
            print('Ошибка: Не могу открыть файл с именем '+s)
    else:
        print('Операция недоступна!')


def step_back():
    pass # FIME Пока нет идей как реализовать шаг назад


def step_forward():
    """
    Выполняет один шаг.
    Вычисляет следующую картину популяции и ждёт дальнейших действий пользователя.
    """
    global begin, steps
    steps = True
    if begin:
        start_or_stop()
    field.next_population()
    field.all_paint()


def init_window():
    """
    инициализация окна программы
    создание и упаковка виджетов
    """
    global root, label, scale, field, canvas, button_start_or_stop, entry
    root = Tk()
    root.title("Игра \"Жизнь\"")
    ew = root.winfo_screenwidth()
    eh = root.winfo_screenheight()
    w = canvas_width+100
    h = canvas_height
    x = (ew - w) // 2
    y = (eh - h) // 2 - 50
    s = str(w)+'x'+str(h)+'+'+str(x)+'+'+str(y)
    root.geometry(s)
    root.resizable(False,False)
    canvas = Canvas(root, width = canvas_width, height = canvas_height)
    canvas.pack(side=LEFT)
    canvas.bind('<Button-1>', mouse_click)
    scale = Scale(root, from_=4, to=20, orient=HORIZONTAL, length=80)
    scale.place(x = canvas_width+10,y = 10)
    scale.set(default_cell_size)
    button_new_field = Button(root, text='Новые поле', command=new_field)
    button_new_field.place(x = canvas_width+10,y = 50)
    label = Label(root, text='')
    label.place(x = canvas_width+10,y = 80)
    button_start_or_stop = Button(root, text='Старт', width=7, command=start_or_stop, font='arial 14')
    button_start_or_stop.place(x = canvas_width+10,y = 240)

    button_step_back = Button(root, text='<--', width=4, command=step_back)
    button_step_back.place(x = canvas_width+10,y = 280)
    button_step_forward = Button(root, text='-->', width=4, command=step_forward)
    button_step_forward.place(x = canvas_width+58,y = 280)


    button_save = Button(root, text='Сохранить', width=10, command=save_to_file)
    button_save.place(x = canvas_width+10,y = 150)
    button_load = Button(root, text='Открыть', width=10, command=load_of_file)
    button_load.place(x = canvas_width+10,y = 120)
    filename = StringVar()
    filename.set(default_filename)
    entry = Entry(root, textvariable = filename, width = 12)
    entry.place(x = canvas_width+10,y = 180)
    field = Field()
    new_field()
    field.all_paint()


def time_event():
    """
    собственно таймер
    (если изменений на поле нет, то программа останавливается)
    учитывается автоматическое или пошаговое выполнение
    """
    global steps, begin
    if begin or steps:
        if field.next_population() == 0:
            if button_start_or_stop['text']=='Стоп':
                start_or_stop()
            if not(1 in field.matrix):
                steps = begin = False
                print('Все погибли...')
    canvas.after(time_sleep,time_event)
    steps = False


if __name__ == "__main__":
    """
    Основная программа
    """
    init_window()
    time_event()
    root.mainloop()