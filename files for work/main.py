import math
import pygame
from pygame.draw import *
import random

pygame.init()

FPS = 30
sc = pygame.display.set_mode((700, 500))
width = 700
height = 500

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

count = 0
ammo = 15
time = 0
scatter = 2000
gun = pygame.image.load('gun.png')
target = pygame.image.load('target.png')
explosion = pygame.image.load('explosion.png')
explosion = pygame.transform.scale(explosion, (200, 200))
target = pygame.transform.scale(target, (80, 80))

pygame.mouse.set_visible(False)

wind = random.randint(0, 0)


class Ball:
    def __init__(self, x, y):

        self.r = random.randint(80, 80)
        self.x = x
        self.y = y
        self.color = RED
        self.rect = rect
        self.surf = pygame.Surface((2 * self.r, 2 * self.r), pygame.SRCALPHA)
        self.ballrect = pygame.Surface((2 * self.r, 2 * self.r), pygame.SRCALPHA).get_rect(center=(x, y))

    def ball(self):
        circle(self.surf, self.color, (self.r, self.r), self.r, 5)
        circle(self.surf, self.color, (self.r, self.r), int(self.r / 1.5), 5)
        circle(self.surf, self.color, (self.r, self.r), int(self.r / 3), 5)

    def show_ball(self):
        sc.blit(self.surf, self.ballrect)

    def shot(self):
        mouse_pos = [event.pos[0] + (wind * (500 - event.pos[1]) / 30 + random.randint(-1 * scatter, scatter) / 100),
                     event.pos[1] + random.randint(-1 * scatter, scatter) / 100]
        distance = math.sqrt((self.x - mouse_pos[0]) ** 2 + (self.y - mouse_pos[1]) ** 2)
        if (distance < self.r) and (distance > self.r * 2 / 3):
            points = 1
            shot = True
        elif (distance < self.r * 2 / 3) and (distance > self.r * 1 / 3):
            points = 2
            shot = True
        elif distance < self.r * 1 / 3:
            points = 3
            shot = True
        else:
            points = 0
            shot = False

        sc.blit(explosion, (int(mouse_pos[0]) - 100, mouse_pos[1] - 100))
        return shot, points


balls = []
for _ in range(1):
    new_ball = Ball(350, 150)
    balls.append(new_ball)

pygame.display.update()
clock = pygame.time.Clock()
finish = False

while not finish:
    sc.fill(BLACK)
# BACKGROUND
    rect(sc, BLUE, (0, 0, 700, 500))
    rect(sc, CYAN, (0, 200, 700, 500))
    rect(sc, WHITE, (250, 50, 200, 200))
    polygon(sc, RED, ((200, 50), (200, 60), ((200 + wind * 15), 55)))
    polygon(sc, YELLOW, ((200, 70), (200, 80), ((200 + scatter / 10), 75)))

    for i in balls:
        i.show_ball()
        i.ball()

    gunsurf = pygame.Surface((500, 500), pygame.SRCALPHA)
    aim = pygame.mouse.get_pos()
    sc.blit(gunsurf, aim)
    sc.blit(gun, (aim[0] - 310, aim[1]))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if ammo == 0:
                finish = True
            else:
                for i in balls:
                    if i.shot()[0]:
                        balls.remove(i)
                        i = Ball(350, 150)
                        balls.append(i)
                        count += i.shot()[1]
                ammo -= 1
                if scatter < 4000:
                    scatter += 1000
    time += 1
    # wind += math.cos(time / 30)
    if scatter > 0:
        scatter -= 20
    font_1 = pygame.font.SysFont('arial', 32, True)

    counttext = font_1.render("Счет: " + str(int(count * 10)), True, WHITE)
    place1 = counttext.get_rect(center=(100, 50))

    ammotext = font_1.render("Патроны: " + str(ammo), True, WHITE)
    place2 = ammotext.get_rect(center=(100, 80))

    timetext = font_1.render("Время: " + str(int(time / 30)), True, WHITE)
    place3 = timetext.get_rect(center=(100, 110))

    sc.blit(counttext, place1)
    sc.blit(ammotext, place2)
    sc.blit(timetext, place3)

    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
print(int(count))
print(time / 30)

if __name__ == "__main__":
    print("This module is not for direct call!")