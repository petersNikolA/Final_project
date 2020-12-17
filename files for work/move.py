import pygame
from pygame.draw import *
from random import randint


class Skier:

    def __init__(self, x=50, y=50):
        self.x = x
        self.y = y
        self.a = 10
        self.g = 50
        self.speed_x = 15
        self.speed_y = 0

    def speed(self):
        pass

    def forward(self, dt, fallfactor, upfactor):
        self.x += self.speed_x * dt
        if fallfactor:
            self.speed_y += self.g * dt
            self.y += self.speed_y * dt
        elif upfactor:
            self.x -= self.speed_x * dt
            self.speed_x = 0
        rect(screen, (255, 255, 255), (int(self.x), int(self.y), self.a, self.a))

    def jump(self, dt):
        k = self.speed_y
        self.speed_y = -5
        print(self.y)
        self.y += self.speed_y * dt
        print(self.y)
        self.speed_y = k
        rect(screen, (255, 255, 255), (int(self.x), int(self.y), self.a, self.a))

    def control(self, coord_x, coord_y):
        if coord_x[0] < self.x <= coord_x[1]:
            k = (coord_y[1] - coord_y[0]) / (coord_x[1] - coord_x[0])
            b = coord_y[0] - k * coord_x[0]
            if (self.y + self.a) - k * self.x - b < 0:
                up = False
                fall = True
                return fall, up
            elif (self.y + self.a) - k * self.x - b > 2:
                self.speed_y = 0
                up = True
                fall = False
                return fall, up
            else:
                self.speed_y = 0
                up = False
                fall = False
                return fall, up
        elif coord_x[1] < self.x <= coord_x[2]:
            k = (coord_y[1] - coord_y[2]) / (coord_x[1] - coord_x[2])
            b = coord_y[1] - k * coord_x[1]
            if (self.y + self.a) - k * self.x - b < 0:
                up = False
                fall = True
                return fall, up
            elif (self.y + self.a) - k * self.x - b > 2:
                self.speed_y = 0
                up = True
                fall = False
                return fall, up
            else:
                self.speed_y = 0
                up = False
                fall = False
                return fall, up
        elif coord_x[2] < self.x <= coord_x[3]:
            k = (coord_y[3] - coord_y[2]) / (coord_x[3] - coord_x[2])
            b = coord_y[2] - k * coord_x[2]
            if (self.y + self.a) - k * self.x - b < 0:
                up = False
                fall = True
                return fall, up
            elif (self.y + self.a) - k * self.x - b > 2:
                self.speed_y = 0
                up = True
                fall = False
                return fall, up
            else:
                self.speed_y = 0
                up = False
                fall = False
                return fall, up
        else:
            self.speed_y = 0
            up = False
            fall = False
            return fall, up

    def up(self, up):
        pass


class Track:

    # тут можно сделать генерацию x и y циклом с количеством иттераций в зависимости от уровня сложности при помощи
    # массива но сначала хочется разобраться на простом и потом усложнить
    def __init__(self, x=50, y=60):
        self.x = x
        self.y = y
        self.x1 = self.x
        self.x2 = randint(150, 250)
        self.x3 = randint(350, 500)
        self.x4 = randint(600, 750)
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


pygame.init()

screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
finished = False
FPS = 60
t = 1 / FPS
T = 1
skier1 = Skier()
track = Track()
fall = False
up = False
x = []
coord_x = []
coord_y = []
coord_x = track.coord_x()
coord_y = track.coord_y()
while not finished:
    rect(screen, (0, 0, 255), (50, 350, 100, 20))
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.KEYDOWN:
            skier1.jump(T)
    track.draw()
    x = skier1.control(coord_x, coord_y)
    skier1.forward(t, fall, up)
    fall = x[0]
    up = x[1]
    skier1.up(up)
    pygame.display.update()
    screen.fill((0, 0, 0))

pygame.quit()