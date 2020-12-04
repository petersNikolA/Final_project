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

rect(sc, BLUE, (0, 0, 700, 500))
rect(sc, GREEN, (0, 200, 700, 500))

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
########################################
wind = random.randint(0, 0)


class Ball:
    def __init__(self, x, y):

        self.r = random.randint(80, 80)
        self.x = x
        self.y = y
        self.v_x = random.choice([0])
        self.v_y = random.choice([0])
        self.color = random.choice([RED, YELLOW])
        self.rect = rect
        self.surf = pygame.Surface((2 * self.r, 2 * self.r), pygame.SRCALPHA)
        self.ballrect = pygame.Surface((2 * self.r, 2 * self.r), pygame.SRCALPHA).get_rect(center=(x, y))

    def ball(self):
        #sc.blit(self.surf, (self.x, self.y))
        #sc.blit(target, (self.x + 40, self.y))
        circle(self.surf, self.color, (self.r, self.r), self.r, 5)
        circle(self.surf, self.color, (self.r, self.r), int(self.r / 1.5), 5)
        circle(self.surf, self.color, (self.r, self.r), int(self.r / 3), 5)
        #sc.blit()

    def move_ball(self):
        sc.blit(self.surf, self.ballrect)
        self.ballrect = self.ballrect.move(self.v_x, self.v_y)
        if self.ballrect.left < 0 or self.ballrect.right > width:
            self.v_x = -self.v_x
        if self.ballrect.top < 0 or self.ballrect.bottom > height:
            self.v_y = -self.v_y
        self.x += self.v_x
        self.y += self.v_y

    def shot(self):
        mouse_pos = [event.pos[0] + (wind * (500 - event.pos[1]) / 30 + random.randint(-1 * scatter, scatter)/100), event.pos[1]+ random.randint(-1 * scatter, scatter)/100]
        distance = math.sqrt((self.x - mouse_pos[0]) ** 2 + (self.y - mouse_pos[1]) ** 2)
        if distance < self.r:
            points = 1 - distance / self.r
            shot = True
        else:
            shot = False
            points = 0

        # circle(sc, WHITE, (int(mouse_pos[0]), mouse_pos[1]), 20)
        sc.blit(explosion, (int(mouse_pos[0]) - 100, mouse_pos[1] - 100))
        return shot, points


balls = []
for _ in range(1):
    new_ball = Ball(random.randint(350, 350), random.randint(149, 150))
    balls.append(new_ball)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    sc.fill(BLACK)

    rect(sc, BLUE, (0, 0, 700, 500))
    rect(sc, GREEN, (0, 200, 700, 500))
    polygon(sc, RED, ((200, 50), (200, 60), ((200 + wind * 15), 55)))
    polygon(sc, YELLOW, ((200, 70), (200, 80), ((200 + scatter / 10), 75)))

    for i in balls:
        i.move_ball()
        i.ball()

    gunsurf = pygame.Surface((500, 500), pygame.SRCALPHA)
    aim = pygame.mouse.get_pos()
    sc.blit(gunsurf, aim)
    sc.blit(gun, (aim[0] - 310, aim[1]))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if ammo == 0:
                print("reloading")
            else:
                for i in balls:
                    if i.shot()[0]:
                        balls.remove(i)
                        i = Ball(random.randint(350, 350), random.randint(150, 150))
                        balls.append(i)
                        count += i.shot()[1]
                        # print(i.shot()[1])
                ammo -= 1
                scatter += 1000
    time += 1
    #wind += math.cos(time / 30)
    if scatter > 0:
        scatter -= 20
    font_1 = pygame.font.SysFont('arial', 32, True)
    counttext = font_1.render("Счет: " + str(int(count * 10)), True, WHITE)
    place1 = counttext.get_rect(center=(100, 50))

    ammotext = font_1.render("Патроны: " + str(ammo), True, WHITE)
    place2 = ammotext.get_rect(center=(100, 80))
    sc.blit(counttext, place1)
    sc.blit(ammotext, place2)

    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
print(int(count * 10))
