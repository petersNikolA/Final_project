import pygame
from pygame.draw import *
from random import randint
from shoot import *


class Skier:

    def __init__(self, x=50, y=50):
        self.x = x
        self.y = y
        self.a = 10
        self.ax = -0.5
        self.g = 50
        self.speed_x = 500
        self.speed_y = 0

    def speed(self, k, upfactor):
        if self.speed_x >= 35 and k > 1:
            if upfactor and self.speed_y <= 35:
                self.speed_y *= k
        else:
            self.speed_x *= k
            if upfactor and self.speed_y <= 35:
                self.speed_y *= k

    def forward(self, dt, fallfactor, upfactor):
        self.speed_x += self.ax * dt
        self.x += self.speed_x * dt
        if fallfactor:
            self.speed_y += self.g * dt
            self.y += self.speed_y * dt
        elif upfactor:
            self.x -= self.speed_x * dt
            self.speed_y = -30
            self.y += self.speed_y * dt
        rect(screen, (255, 255, 255), (int(self.x), int(self.y), self.a, self.a))

    def jump(self, dt):
        self.speed_y = -5
        self.y += self.speed_y * dt
        self.speed_y = 0
        rect(screen, (255, 255, 255), (int(self.x), int(self.y), self.a, self.a))

    def control(self, x, y):
        if x[0] < self.x <= x[1]:
            k = (y[1] - y[0]) / (x[1] - x[0])
            b = y[0] - k * x[0]
            if k > 0:
                self.ax = -0.01
            else:
                self.ax = -1
            if (self.y + self.a) - k * self.x - b < 0:
                u = False
                f = True
                return f, u
            elif (self.y + self.a) - k * self.x - b > 2:
                self.speed_y = 0
                u = True
                f = False
                return f, u
            else:
                self.speed_y = 0
                u = False
                f = False
                return f, u
        elif x[1] < self.x <= x[2]:
            k = (y[1] - y[2]) / (x[1] - x[2])
            b = y[1] - k * x[1]
            if k > 0:
                self.ax = -0.01
            else:
                self.ax = -1
            if (self.y + self.a) - k * self.x - b < 0:
                u = False
                f = True
                return f, u
            elif (self.y + self.a) - k * self.x - b > 2:
                self.speed_y = 0
                u = True
                f = False
                return f, u
            else:
                self.speed_y = 0
                u = False
                f = False
                return f, u
        elif x[2] < self.x <= x[3]:
            k = (y[3] - y[2]) / (x[3] - x[2])
            b = y[2] - k * x[2]
            if k > 0:
                self.ax = -0.01
            else:
                self.ax = -1
            if (self.y + self.a) - k * self.x - b < 0:
                u = False
                f = True
                return f, u
            elif (self.y + self.a) - k * self.x - b > 2:
                self.speed_y = 0
                u = True
                f = False
                return f, u
            else:
                self.speed_y = 0
                u = False
                f = False
                return f, u
        else:
            self.speed_y = 0
            u = False
            f = False
            return f, u

    def end(self):
        if self.x + self.a >= 700:
            self.x = 50
            self.y = 50
            self.speed_x = 20
            self.speed_y = 0
            return True
        else:
            return False

    def speedchecker(self):
        print(self.speed_x, self.speed_y, self.ax)


class Track:

    # тут можно сделать генерацию x и y циклом с количеством иттераций в зависимости от уровня сложности при помощи
    # массива но сначала хочется разобраться на простом и потом усложнить
    def __init__(self, x=50, y=60):
        self.x = x
        self.y = y
        self.x1 = self.x
        self.x2 = randint(150, 250)
        self.x3 = randint(350, 500)
        self.x4 = 700
        self.y1 = self.y
        self.y2 = randint(60, 70)
        self.y3 = randint(self.y2 + 30, 250)
        self.y4 = randint(50, self.y3 + 40)
        """
        for i in range(level):

        """

    def draw(self):
        polygon(screen, (255, 0, 0), ((self.x1, 300), (self.x1, self.y1), (self.x2, self.y2),
                                      (self.x3, self.y3), (self.x4, self.y4), (self.x4, 300)))

    def coord_x(self):
        return self.x1, self.x2, self.x3, self.x4

    def coord_y(self):
        return self.y1, self.y2, self.y3, self.y4


class Speeder:

    def __init__(self, x=50, y=330, l_1=20, l_2=50):
        self.x = x
        self.y = y
        self.width = l_1
        self.high = l_2
        self.speed = 1000

    def draw(self):
        rect(screen, (255, 255, 255), (int(self.x), self.y, self.width, self.high))

    def move(self, dt):
        self.x += self.speed * dt

    def control(self):
        if self.x >= -self.width + 650 or self.x <= 50:
            self.speed *= -1

    def check(self):
        if 330 <= self.x <= -self.width + 370:
            return 1.15
        elif 270 <= self.x <= -self.width + 430:
            return 1.1
        else:
            return 0.9


pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
finished = False
FPS = 60
t = 1 / FPS
T = 2
skier1 = Skier()
track = Track()
n = Speeder()
fall = False
up = False
checker = False
x = []
coord_x = []
coord_y = []
p = 0
coord_x = track.coord_x()
coord_y = track.coord_y()

finish = False
count = 0
ammo = 15
time = 0
scatter = 2000

while not finished:
    rect(screen, (255, 238, 0), (50, 330, 600, 50))
    rect(screen, (255, 162, 0), (270, 330, 160, 50))
    rect(screen, (255, 0, 0), (330, 330, 40, 50))
    n.move(t)
    n.draw()
    n.control()
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                skier1.jump(T)
            if event.key == pygame.K_SPACE:
                p = n.check()
                skier1.speed(p, up)
                skier1.speedchecker()
    track.draw()
    x = skier1.control(coord_x, coord_y)
    fall = x[0]
    up = x[1]
    skier1.forward(t, fall, up)
    checker = skier1.end()
    if checker:
        circle(finish, time, scatter, ammo, count)
        finish = False
        track.__init__()
        coord_x = track.coord_x()
        coord_y = track.coord_y()
    pygame.display.update()
    screen.fill((0, 0, 0))

pygame.quit()
