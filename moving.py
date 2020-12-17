import pygame
from pygame.draw import *
from random import randint
from shoot import *


class Skier:
    """
    class for main object - skier
    """
    def __init__(self, x_0=50, y_0=160):
        """
        :param x_0: horizontal starting position
        :param y_0: vertical starting position
        a - size
        ax - horizontal acceleration
        g - vertical acceleration
        speed_x - horizontal speed
        speed_y - vertical speed
        u - upfactor
        f - fallfactor
        w - jump_factor
        """
        self.a = 10
        self.x = x_0
        self.y = y_0 - self.a
        self.ax = -0.5
        self.g = 300
        self.speed_x = 2
        self.speed_y = 0
        self.u = False
        self.f = False
        self.w = True

    def speed(self, k, upfactor):
        """
        determines speed of skier
        :param k: coefficient obtained from speeder
        :param upfactor: factor whether skier needs to climb the hill
        :return: speed
        """
        if self.speed_x <= 2:
            if k > 0:
                self.speed_x += 1
            else:
                self.speed_x = 2
        elif self.speed_x >= 20 and k > 1:
            self.speed_x = 20
            if upfactor and self.speed_y <= 35:
                self.speed_y *= k
        elif self.speed_x >= 10 and k > 1:
            if k == 1.3:
                self.speed_x += 1
            else:
                self.speed_x += 0.5
        else:
            self.speed_x *= k
            if upfactor and self.speed_y <= 35:
                self.speed_y *= k

    def forward(self, dt, fallfactor, upfactor):
        """
        movement of skier
        :param dt: time of movement
        :param fallfactor: factor whether skier needs to go down
        :param upfactor: factor whether skier needs to climb the hill
        """
        self.speed_x += self.ax * dt
        self.x += self.speed_x * dt
        if fallfactor:
            self.speed_y += self.g * dt
            self.y += self.speed_y * dt
        elif upfactor:
            self.x -= self.speed_x * dt
            self.speed_y = -10
            self.y += self.speed_y * dt
        rect(screen, (255, 0, 0), (int(self.x), int(self.y), self.a, self.a))

    def jump(self, dt, factor):
        """
        skier jumping
        :param dt: time of jumping
        :param factor: checking if skier has not jumped yet
        """
        if factor:
            self.speed_y = -10
            self.y += self.speed_y * dt
            self.x += 2
            self.speed_y = 0
            rect(screen, (255, 255, 255), (int(self.x), int(self.y), self.a, self.a))

    def control(self, x, l, k, b):
        """
        makes skier moves along the track
        :param x: track's horizontal coordinates
        :param l: number of track parts
        :param k: coefficient of track's tilt
        :param b: another track coefficient
        """
        for i in range(l + 3):
            if x[i] < self.x <= x[i + 1]:
                if k[i] >= 0:
                    self.ax = -0.1
                    if (self.y + self.a) - k[i] * self.x - b[i] < 10:
                        self.g = 120
                    else:
                        self.g = 2000
                else:
                    self.ax = -0.25 * abs(k[i]) * (l // 4)
                    if not self.f:
                        self.g = 25
                    else:
                        self.g = 100
                if (self.y + self.a) - k[i] * self.x - b[i] < 1:
                    self.u = False
                    self.f = True
                    if (self.y + self.a) - k[i] * self.x - b[i] < -5:
                        self.w = False
                    else:
                        self.w = True
                elif k[i] >= 0 and (self.y + self.a / 1.2) - k[i] * self.x - b[i] > 0:
                    self.speed_y = 0
                    self.u = True
                    self.f = False
                    self.w = True
                elif k[i] < 0 and (self.y + self.a * 2 ** (1 / 2) - k[i] * self.x - b[i] > 0):
                    self.speed_y = 0
                    self.u = True
                    self.f = False
                    self.w = True
                else:
                    self.speed_y = 0
                    self.u = False
                    self.f = False
                    self.w = True

    def checker(self):
        """
        checks whether skier needs to climb up or go down, or can jump
        :return: upfactor, fallfactor, jump_factor
        """
        return self.u, self.f, self.w

    def end(self):
        """
        check if skier has finished part of the track
        :return: True if skier has finished otherwise False
        """
        if self.x + self.a >= 775:
            self.x = 50
            self.y = 150
            return True
        else:
            return False

    def speedchecker(self):
        """
        limits speed so that skier won't go back
        :return: new speed value
        """
        if self.speed_x <= 0:
            self.speed_x = 2

    def text(self):
        """
        :return: skier's speed
        """
        return self.speed_x

    def boost_checker(self, m):
        """
        checks if skier has riched booster
        :param m: True if skier had riched otherwise False
        :return: new speed value
        """
        if m - 0.1 <= self.x + 2 <= m + 0.1:
            self.speed_x += 2.1

    def coords_obstacle(self):
        """
        :return: skier's coordinates
        """
        return self.x, self.y

    def ob_checker(self, ob_factor):
        """
        checks if skier has collided obstacle
        :param ob_factor: True if skier had collided obstacle otherwise False
        :return: new speed value
        """
        if ob_factor:
            self.speed_x -= 1


class Track:
    """
    class that describes the track on which skier moves
    """
    def __init__(self, x_0=50, y_0=160):
        """
        randomly generates coordinates of track
        :param x_0: zero horizontal position
        :param y_0: zero vertical position
        x - array of horizontal coordinates
        y - array of vertical coordinates
        """
        l = level
        self.x = [x_0, x_0 + 50]
        self.y = [y_0, y_0]
        for i in range(l):
            self.x.append(self.x[i + 1] + 600 // l)
            self.y.append(randint(60, 300))
        self.x.append(self.x[l + 1] + 50)
        self.x.append(self.x[l + 2] + 25)
        self.y.append(y_0)
        self.y.append(y_0)

    def draw(self, l):
        """
        draws track on screen
        :param l: number of track parts
        """
        for i in range(l + 3):
            polygon(screen, CYAN, ((self.x[i], self.y[i]), (self.x[i + 1], self.y[i + 1]),
                                   (self.x[i + 1], 400), (self.x[i], 400)))

    def obstacle(self, l):
        """
        makes massive for obstacles
        :param l: number of track parts
        """
        for i in range(l + 3):
            coord_mas.append([self.x[i], self.y[i]])

    def coefficient(self, l):
        """
        count coefficients of track lines
        :param l: number of track parts
        :return: coefficients of track lines
        """
        coef1 = []
        coef2 = []
        for i in range(l + 3):
            k = (self.y[i + 1] - self.y[i]) / (self.x[i + 1] - self.x[i])
            coef1.append(k)
            b = self.y[i] - k * self.x[i]
            coef2.append(b)
        return coef1, coef2

    def coord_x(self):
        """
        :return: horizontal coordinates of track
        """
        return self.x

    def coord_y(self):
        """
        :return: vertical coordinates of track
        """
        return self.y


class Speeder:
    """
    describes special object under the track, that determines skier's speed
    """
    def __init__(self, x=50, y=430, l_1=20, l_2=50):
        """
        :param x: first position (horizontal)
        :param y: first position (vertical)
        :param l_1: length
        :param l_2: height
        """
        self.x = x
        self.y = y
        self.width = l_1
        self.high = l_2
        self.speed = 1000

    def draw(self):
        """
        drawing speeder (object)
        """
        rect(screen, (255, 255, 255), (int(self.x), self.y, self.width, self.high))

    def move(self, dt):
        """
        moving of speeder
        :param dt: time of movement
        """
        self.x += self.speed * dt

    def control(self):
        """
        checks position of speeder
        """
        if self.x >= -self.width + 650 or self.x <= 50:
            self.speed *= -1

    def check(self):
        """
        determines value of k
        :return: value of k - speed coefficient
        """
        if 330 <= self.x <= -self.width + 370:
            return 1.3
        elif 270 <= self.x <= -self.width + 430:
            return 1.2
        else:
            return 0.9


class Clouds:
    """
    class that describes clouds - part of background
    """
    def __init__(self):
        """
        x - first horizontal position
        y - first vertical position
        l - length
        w - height
        """
        self.x = randint(50, 100)
        self.y = randint(1, 100)
        self.l = randint(100, 200)
        self.w = randint(30, 50)
        self.speed = randint(-50, 50)

    def checker(self):
        """
        makes speed non zero
        :return: new value of speed
        """
        if self.speed == 0:
            self.speed = randint(10, 50)
        elif 0 < self.speed < 10:
            self.speed = randint(10, 50)
        elif -10 < self.speed < 0:
            self.speed = randint(-50, -10)

    def draw(self):
        """
        draws cloud on screen
        """
        ellipse(screen, WHITE, (int(self.x), self.y, self.l, self.w))

    def move(self, dt):
        """
        movement of cloud
        :param dt: time of moving (dt = 1 / FPS)
        :return: new horizontal coordinate
        """
        self.x += self.speed * dt

    def control(self):
        """
        check collision with the frames
        :return: new position of cloud
        """
        if self.x >= 800:
            self.x = 0
        elif self.x <= 0:
            self.x = 800


class Boost:
    """
    class for small helper - booster, that increases speed
    """
    def __init__(self):
        """
        x - horizontal position on screen
        y - vertical position on the screen
        r - size
        """
        self.x = randint(100, 750)
        self.y = 60
        self.r = 5

    def checker(self, x):
        """
        checks if track coordinates don't matches with coordinate of booster
        in order to avoid some mistakes
        :param x: coordinates of track
        :return: new coordinate of booster
        """
        for i in range(level + 3):
            if x[i] - 5 <= self.x <= x[i] + 5:
                self.x += 20

    def draw(self):
        """
        draws booster on screen
        """
        circle(screen, (139, 0, 0), (self.x, self.y), self.r)

    def coord(self):
        """
        :return: coordinate of booster
        """
        return self.x

    def change_y(self, l, x, k, b):
        '''
        places booster on track
        :param l: level (number of track parts)
        :param x: track coordinates
        :param k: k coefficient of track lines (track line: y=kx+b)
        :param b: b coefficient of track lines
        :return: new vertical booster coordinate
        '''
        for i in range(l + 3):
            if x[i] <= self.x <= x[i + 1]:
                self.y = int(k[i] * self.x + b[i] - 5)


class Obstacle:
    """
    class for object called obstacle, that interferes skier
    """
    def __init__(self):
        """
        height - size
        x - horizontal coordinate
        y - vertical coordinate
        """
        self.height = 8
        self.x = 0
        self.y = 0

    def apply_coords(self, mass, i):
        """
        determines coordinates of obstacles
        :param mass: array of track coordinates
        :param i: number of coordinates in mass
        :return:
        """
        self.x = mass[i][0]
        self.y = mass[i][1]

    def draw(self):
        '''
        draws obstacles on screen
        '''
        line(screen, (255, 255, 0), (self.x, self.y - self.height), (self.x, self.y), 4)

    def bang(self, skier_coords_x, skier_coords_y):
        '''
        checks collision of skier and obstacle
        :param skier_coords_x: x coordinates of skier
        :param skier_coords_y: y coordinates of skier
        :return: True if skier and obstacle collided otherwise False
        '''
        if abs(self.x - skier_coords_x) <= 1 and abs(skier_coords_y - self.y + self.height) <= 2:
            return True
        else:
            return False


def possible_spots(mas):
    """
    determines possible places of obstacles
    :param mas: track coordinates
    :return: coordinates of obstacles
    """
    coords = []
    for i in range(len(mas) - 1):
        A = mas[i][1] - mas[i + 1][1]
        B = -mas[i][0] + mas[i + 1][0]
        C = (mas[i][0] * mas[i + 1][1]) - (mas[i + 1][0] * mas[i][1])
        for X in range(min(mas[i][0], mas[i + 1][0]), max(mas[i][0], mas[i + 1][0]), 33):
            for Y in range(min(mas[i][1], mas[i + 1][1]), max(mas[i][1], mas[i + 1][1])):
                Const = A * X + B * Y + C
                if (abs(Const) / (math.sqrt(A ** 2 + B ** 2))) < 2:
                    coords.append([X, Y])
    return coords


pygame.init()

screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
ski_surface = pygame.Surface((50, 60), pygame.SRCALPHA)  # попытка сделать так, чтобы лыжник поворачивался по склону
finished = False
FPS = 60
t = 1 / FPS
T = 2

fall = False
up = False
checker = False
x = [False, False, True]
j_factor = x[2]
p = 0
track_counter = 0
r = []
final = 0
coord_mas = []
s_coord = []
s_x = 0
s_y = 0
ob = False

finish = False
count = 0
ammo = 15
time = 0
scatter = 2000
wind = 0

timing = 100
factor = False

first = pygame.font.Font(None, 50)
second = pygame.font.Font(None, 50)
f_text = "Обратите внимание на консоль"
s_text = "Ознакомьтесь с правилами"
ffirst = first.render(f_text, True, WHITE, BLACK)
ssecond = second.render(s_text, True, WHITE, BLACK)
screen.blit(ffirst, (100, 100))
screen.blit(ssecond, (100, 150))
pygame.display.update()
print('перед началом игры ознакомтесь с правилами ....')
level = int(input("Введите уровень сложности от 1 до 3 "))
level *= 4
name = str(input("Введите ваше имя. Только латинcкие буквы "))

skier1 = Skier()
track = Track()
track.obstacle(level)
n = Speeder()
c_x = track.coord_x()  # набор координат x трассы
c_y = track.coord_y()  # набор координат y трассы
k, b = track.coefficient(level)
cloud1 = Clouds()
cloud1.checker()
cloud2 = Clouds()
cloud2.checker()
booster = Boost()
obstacles = []

for i in range(10):
    obstacles.append(Obstacle())

coords = random.sample(possible_spots(coord_mas), 10)

for i in obstacles:
    i.apply_coords(coords, obstacles.index(i))

text1 = pygame.font.Font(None, 50)
text3 = pygame.font.Font(None, 50)
text5 = pygame.font.Font(None, 50)
rules1 = pygame.font.Font(None, 50)
rules2 = pygame.font.Font(None, 50)
rules3 = pygame.font.Font(None, 50)
rules4 = pygame.font.Font(None, 50)
rule1 = 'Space - ускорение лыжника'
rule2 = 'При нажатии стрелки вверх - прыжок'
rule3 = 'Для начала игры нажмите Tab'
rule4 = 'Для выхода нажмите Esc'

while not finished:
    pygame.display.update()
    rules11 = rules1.render(rule1, True, WHITE, BLACK)
    rules22 = rules2.render(rule2, True, WHITE, BLACK)
    rules33 = rules3.render(rule3, True, WHITE, BLACK)
    rules44 = rules4.render(rule4, True, WHITE, BLACK)
    screen.blit(rules11, (50, 100))
    screen.blit(rules22, (50, 150))
    screen.blit(rules33, (50, 200))
    screen.blit(rules44, (50, 250))
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                factor = True
            elif event.key == pygame.K_ESCAPE:
                finished = True
        elif event.type == pygame.QUIT:
            finished = True
    if factor:
        while not finished:
            rect(screen, (0, 0, 255), (0, 0, 800, 400))
            rect(screen, (255, 238, 0), (50, 430, 600, 50))
            rect(screen, (255, 162, 0), (270, 430, 160, 50))
            rect(screen, (255, 0, 0), (330, 430, 40, 50))
            n.move(t)
            n.draw()
            n.control()
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        skier1.jump(T, j_factor)
                    elif event.key == pygame.K_SPACE:
                        p = n.check()
                        skier1.speedchecker()
                        skier1.speed(p, up)
                    elif event.key == pygame.K_ESCAPE:
                        finished = True
            cloud1.draw()
            cloud2.draw()
            cloud1.move(t)
            cloud2.move(t)
            cloud1.control()
            cloud2.control()
            booster.checker(c_x)
            booster.change_y(level, c_x, k, b)
            track.draw(level)
            booster.draw()
            b_coord = booster.coord()
            skier1.control(c_x, level, k, b)
            x = skier1.checker()
            skier1.speedchecker()
            up = x[0]
            fall = x[1]
            j_factor = x[2]
            skier1.forward(t, fall, up)
            skier1.boost_checker(b_coord)
            checker = skier1.end()
            for i in obstacles:
                s_x, s_y = skier1.coords_obstacle()
                i.draw()
                ob = i.bang(s_x, s_y)
                skier1.ob_checker(ob)
                ob = False
                skier1.speedchecker()
            if checker:
                r = shooting(finish, time, scatter, ammo, count, wind)
                timing -= r[1]
                final += r[0]
                finish = False
                cloud1.__init__()
                cloud1.checker()
                cloud2.__init__()
                cloud2.checker()
                track.__init__()
                track_counter += 1
                k, b = track.coefficient(level)
                c_x = track.coord_x()
                c_y = track.coord_y()
                coord_mas = []
                track.obstacle(level)
                obstacles = []
                for i in range(10):
                    obstacles.append(Obstacle())
                coords = random.sample(possible_spots(coord_mas), 10)
                for i in obstacles:
                    i.apply_coords(coords, obstacles.index(i))
            pygame.display.update()
            screen.fill((0, 0, 0))
            u = skier1.text()
            timing -= 1 / FPS
            text = 'Скорость: ' + str("%.2f" % u)
            text_n = 'Количество пройденных участков: ' + str(track_counter)
            text_t = 'Осталось времени: ' + str(int(timing))
            text2 = text1.render(text, True, WHITE, BLACK)
            text4 = text3.render(text_n, True, WHITE, BLACK)
            text6 = text5.render(text_t, True, WHITE, BLACK)
            screen.blit(text2, (50, 550))
            screen.blit(text4, (50, 600))
            screen.blit(text6, (50, 650))
            if timing <= 0:
                final += (track_counter * level * 50)
                records = open("records.txt", "a")
                records.write(name + " : " + str(final) + "\n")
                records.close()
                finished = True

pygame.quit()
