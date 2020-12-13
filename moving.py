import pygame
from pygame.draw import *
from random import randint
from shoot import *


class Skier:

    def __init__(self, x_0=50, y_0=160):
        self.a = 10
        self.x = x_0
        self.y = y_0 - self.a
        self.ax = -0.5
        self.g = 75
        self.speed_x = 0
        self.speed_y = 0
        self.u = False
        self.f = False

    def speed(self, k, upfactor):
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
        self.speed_y = -7
        self.y += self.speed_y * dt
        self.speed_y = 0
        rect(screen, (255, 255, 255), (int(self.x), int(self.y), self.a, self.a))

    def control(self, x, l, k, b):
        for i in range(l + 3):
            if x[i] < self.x <= x[i + 1]:
                if k[i] >= 0:
                    self.ax = -0.1
                else:
                    self.ax = -0.3 * abs(k[i])
                if (self.y + self.a) - k[i] * self.x - b[i] < 0:
                    self.u = False
                    self.f = True
                elif (self.y + self.a) - k[i] * self.x - b[i] > 1:
                    self.speed_y = 0
                    self.u = True
                    self.f = False
                else:
                    self.speed_y = 0
                    self.u = False
                    self.f = False

    def checker(self):
        return self.u, self.f

    def end(self):
        if self.x + self.a >= 775:
            self.x = 50
            self.y = 150
            return True
        else:
            return False

    def speedchecker(self):
        if self.speed_x <= 0:
            self.speed_x = 0

    def text(self):
        return self.speed_x


class Track:

    def __init__(self, x_0=50, y_0=160):
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
        for i in range(l + 3):
            polygon(screen, (0, 255, 255), ((self.x[i], self.y[i]), (self.x[i + 1], self.y[i + 1]),
                                          (self.x[i + 1], 400), (self.x[i], 400)))

    def coefficient(self, l):
        coef1 = []
        coef2 = []
        for i in range(l + 3):
            k = (self.y[i + 1] - self.y[i]) / (self.x[i + 1] - self.x[i])
            coef1.append(k)
            b = self.y[i] - k * self.x[i]
            coef2.append(b)
        return coef1, coef2

    def coord_x(self):
        return self.x

    def coord_y(self):
        return self.y


class Speeder:

    def __init__(self, x=50, y=430, l_1=20, l_2=50):
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
            return 1.3
        elif 270 <= self.x <= -self.width + 430:
            return 1.2
        else:
            return 0.9


pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
finished = False
FPS = 60
t = 1 / FPS
T = 2

fall = False
up = False
checker = False
x = [False, False]
p = 0

tx = []  # набор координат x трассы
ty = []  # набор координат y трассы

finish = False
count = 0
ammo = 15
time = 0
scatter = 2000

level = int(input("Введите уровень сложности от 1 до 3"))
level *= 4


skier1 = Skier()
track = Track()
n = Speeder()
c_x = track.coord_x()
c_y = track.coord_y()
k, b = track.coefficient(level)
text1 = pygame.font.Font(None, 50)

while not finished:
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
                skier1.jump(T)
            if event.key == pygame.K_SPACE:
                p = n.check()
                skier1.speedchecker()
                skier1.speed(p, up)
    track.draw(level)
    skier1.control(c_x, level, k, b)
    x = skier1.checker()
    skier1.speedchecker()
    up = x[0]
    fall = x[1]
    skier1.forward(t, fall, up)
    checker = skier1.end()
    if checker:
        shooting(finish, time, scatter, ammo, count)
        finish = False
        track.__init__()
        k, b = track.coefficient(level)
        c_x = track.coord_x()
        c_y = track.coord_y()
    pygame.display.update()
    screen.fill((0, 0, 0))
    u = skier1.text()
    text = 'Скорость: ' + str("%.2f" % u)
    text2 = text1.render(text, True, WHITE, BLACK)
    screen.blit(text2, (50, 550))

pygame.quit()
