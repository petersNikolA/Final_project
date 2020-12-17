import pygame
from pygame.draw import *


class Speeder:

    def __init__(self, x=50, y=200, l_1=20, l_2=50):
        self.x = x
        self.y = y
        self.width = l_1
        self.high = l_2
        self.speed = 50

    def draw(self):
        rect(screen, (255, 255, 255), (int(self.x), self.y, self.width, self.high))

    def move(self, dt):
        self.x += self.speed * dt

    def control(self):
        if self.x >= -self.width + 650 or self.x <= 50:
            self.speed *= -1

    def check(self):
        if 330 <= self.x <= -self.width + 370:
            print(3)
        elif 270 <= self.x <= -self.width + 430:
            print(2)
        else:
            print(1)


pygame.init()

screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
finished = False
FPS = 60
t = 1 / FPS
s = Speeder()
while not finished:
    rect(screen, (255, 238, 0), (50, 200, 600, 50))
    rect(screen, (255, 162, 0), (270, 200, 160, 50))
    rect(screen, (255, 0, 0), (330, 200, 40, 50))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.KEYDOWN:
            s.check()
    s.move(t)
    s.control()
    s.draw()
    pygame.display.update()
    screen.fill((0, 0, 0))

pygame.quit()
