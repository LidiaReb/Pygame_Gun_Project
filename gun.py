import math
import random as rd
import choice
import numpy as np

import pygame


FPS = 100

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
LIGHTYELLOW = 0xfffa69
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
ORANGE = 0xFF8C00
BlACGREY = (165, 165, 165)
# GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
GAME_COLORS = [RED, ORANGE, YELLOW]

WIDTH = 800
HEIGHT = 600
GRAVITY = 120

COMMON = 1
MEGA = 0

class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y 
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.multi = 8
        self.color = GAME_COLORS[rd.randint(0, len(GAME_COLORS) - 1)]
        self.live = 30
        self.birth = pygame.time.get_ticks()  
        self.balllivind = 2000
        self.gravity = GRAVITY


    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        if self.x >= WIDTH - 10 or self.x <= 10:
            self.vx = -self.vx 
        if self.y >= HEIGHT - 10:
            self.vy = -self.vy
        self.x += self.multi*self.vx*(1/FPS)
        self.y += self.multi*self.vy*(1/FPS) - self.gravity*(1/FPS)**2
        self.vy += self.gravity*(1/FPS)
        # FIXME

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def killing(self):
        if pygame.time.get_ticks() - self.birth > self.balllivind:
            return True
        return False

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (self.x - obj.x)**2 + (self.y - obj.y)**2  < (obj.r + self.r)**2:
            return True
        else:
            return False
        # FIXME

class MegaBall(Ball):

    def __init__(self, screen: pygame.Surface, x=40, y=450):
        super().__init__(screen, x, y)
        self.r = 3
        self.multi = 10

    def boom(self):
        self.r = 70
        self.balllivind = 500
        self.vx = 0
        self.vy = 0
        self.gravity = 0
        self.color = LIGHTYELLOW


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.x = 50
        self.y = HEIGHT - 50
        self.len = 20
        self.wight = 10

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event, whichball = COMMON):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        if whichball:
            new_ball = Ball(self.screen)
        else:
            new_ball = MegaBall(self.screen)
        new_ball.r += 5
        self.an = np.arctan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = 2 * self.f2_power * math.cos(self.an)
        new_ball.vy = 2 * self.f2_power * math.sin(self.an)
        new_ball.x = 20 + self.x + (self.f2_power + self.len) * math.cos(self.an)
        new_ball.y = 20 + self.y + (self.f2_power + self.len) * math.sin(self.an)
        if whichball:
            balls.append(new_ball)
        else:
            megaballs.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = np.arctan2((event.pos[1]-(self.y)), (event.pos[0]-self.x))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        pygame.draw.line(
            self.screen,
            self.color,
            [self.x, self.y], 
            [self.x + (self.f2_power + self.len) * math.cos(self.an), self.y + (self.f2_power + self.len) * math.sin(self.an)], 
            self.wight)
        pygame.draw.ellipse(screen, BlACGREY, (self.x - 20, self.y - 5, 30,20))
        # FIXME don't know how to do it

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY

    def move(self, m):
        if self.x < WIDTH - 10 and self.x > 10:
            self.x += m
        if self.x >= WIDTH - 30 and m < 0:
            self.x += m
        if self.x <= 30 and m > 0:
            self.x += m

class Target:

    def __init__(self, screen):
        self.screen = screen
        self.points = 0
        self.live = 1
        self.time = pygame.time.get_ticks()
        self.vx = 100
        self.vy = 100
        self.r_min = 10
        self.r_max = 30
        self.color = (150, 150, 150)
        self.new_target()

    # self.points = 0
    # self.live = 1
    # FIXME: don't work!!! How to call this functions when object is created?
    # self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        # x = self.x = rnd(600, 780)
        # y = self.y = rnd(300, 550)
        # r = self.r = rnd(2, 50) 
        self.live = 1
        x = self.x = rd.uniform(600, 780)
        y = self.y = rd.uniform(300, 550)
        r = self.r = rd.uniform(self.r_min, self.r_max) 
        color = self.color

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        pygame.draw.circle(
            self.screen,
            BLACK,
            (self.x, self.y),
            self.r
        )
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r - 5
        )
        # FIXME

    
    def move(self):
        if self.x >= WIDTH - 10 or self.x <= 10:
            self.vx = -self.vx 
        if self.y <= 10 or self.y >= HEIGHT - 10:
            self.vy = -self.vy
        self.x += self.vx*(1/FPS)
        self.y += self.vy*(1/FPS)
        if pygame.time.get_ticks() - self.time > 500:
            self.time = pygame.time.get_ticks()
            self.vy = self.vy*(1 + rd.uniform(-0.2, 0.23))
            self.vx = self.vx*(1 + rd.uniform(-0.2, 0.23))
        # if pygame.time.get_ticks() - self.time > 500:
        #     self.time = pygame.time.get_ticks()
        #     self.vx = self.vx*(1 + rd.uniform(-0.2, 0.2))
        # if pygame.time.get_ticks() - self.time > rd.uniform(1000, 5000):
        #     self.time = pygame.time.get_ticks()
        #     self.vx = -self.vx 
        # FIXME   

class MegaTarget(Target):

    def __init__(self, screen: pygame.Surface):
        self.r_min = 5
        self.r_max = 15
        super().__init__(screen)
        self.goingx = rd.uniform( 50, WIDTH - 50)
        self.goingy = rd.uniform( 50, HEIGHT - 50)
        self.color = BLACK
        self.vx = 1 * (self.goingx - self.x)
        self.vy = 1 * (self.goingy - self.y)
        v = 400 * rd.uniform(1, 2)
        self.vx = v * (self.goingx - self.x) / ((self.goingx-self.x)**2 + (self.goingy - self.y)**2)**0.5
        self.vy = v * (self.goingy - self.y) / ((self.goingx-self.x)**2 + (self.goingy - self.y)**2)**0.5
    
    def hit(self, points = 3):
        """Попадание шарика в цель."""
        self.points += points
   
    def move(self):
        self.x += self.vx*(1/FPS)
        self.y += self.vy*(1/FPS)
        if (self.x - self.goingx)**2 + (self.y - self.goingy)**2  < (self.r)**2:
            self.goingx = rd.uniform( 50, WIDTH - 50)
            self.goingy = rd.uniform( 50, HEIGHT - 50)
            self.vx = 1 * (self.goingx - self.x)
            self.vy = 1 * (self.goingy - self.y)
            v = 400 * rd.uniform(1, 2)
            self.vx = v * (self.goingx - self.x) / ((self.goingx-self.x)**2 + (self.goingy - self.y)**2)**0.5
            self.vy = v * (self.goingy - self.y) / ((self.goingx-self.x)**2 + (self.goingy - self.y)**2)**0.5

    def new_target(self):
        """ Инициализация новой цели. """
        # x = self.x = rnd(600, 780)
        # y = self.y = rnd(300, 550)
        # r = self.r = rnd(2, 50) 
        self.live = 1
        x = self.x = rd.uniform(600, 780)
        y = self.y = rd.uniform(300, 550)
        r = self.r = rd.uniform(self.r_min, self.r_max) 
        self.goingx = rd.uniform( 50, WIDTH - 50)
        self.goingy = rd.uniform( 50, HEIGHT - 50)
        self.color = BLACK
        v = 400 * rd.uniform(1, 2)
        self.vx = v * (self.goingx - self.x) / ((self.goingx-self.x)**2 + (self.goingy - self.y)**2)**0.5
        self.vy = v * (self.goingy - self.y) / ((self.goingx-self.x)**2 + (self.goingy - self.y)**2)**0.5

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
fine = 0
balls = []
megaballs =[]
texttime = 0
pr = 0

clock = pygame.time.Clock()
gun = Gun(screen)
target1 = Target(screen)
target2 = Target(screen)
target3 = MegaTarget(screen)
finished = False

while not finished:
    screen.fill(WHITE)
    gun.draw()
    if target1.live:
        target1.draw()
        target1.move()
    if target2.live:
        target2.draw()
        target2.move()
    if target3.live:
        target3.draw()
        target3.move()


    font = pygame.font.SysFont(None, 24)
    img = font.render('Балл: ' + str(target1.points + target2.points +  target3.points - fine), True, 0)
    screen.blit(img, (20, 20))

    if pygame.time.get_ticks() - texttime < 500 and pr:
        font1 = pygame.font.SysFont(None, 40)
        m = int((pygame.time.get_ticks() - texttime) / 500 * 250)
        clr = (m, m, m)
        img1 = font1.render('Нет баллов для взрыва', True, clr)
        screen.blit(img1, (WIDTH/2 - 160, HEIGHT/2 - 50))  

    for b in balls + megaballs:
        b.draw()
    pygame.display.update()

    kill = []
    for i in range(len(balls)):
        if balls[i].killing():
            kill.append(i)
    for i in kill:
        del balls[i]
    kill = []
    for i in range(len(megaballs)):
        if megaballs[i].killing():
            kill.append(i)
    for i in kill:
        del megaballs[i]

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            left, middle, right = pygame.mouse.get_pressed()
            gun.fire2_start(event)
            if left:
                whball = MEGA
            if right:
                whball = COMMON
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event, whball)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and len(megaballs) != 0 and target1.points + target2.points + target3.points - fine == 0:
            texttime = pygame.time.get_ticks()
            pr = 1

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and len(megaballs) != 0 and target1.points + target2.points + target3.points - fine > 0:
            megaballs[0].boom()
            fine += 1
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        gun.move(2)
    elif keys[pygame.K_a]:
        gun.move(-2)
    else:
        gun.move(0)


    for b in balls + megaballs:
        b.move()
        if b.hittest(target1) and target1.live:
            target1.live = 0
            target1.hit()
            target1.new_target()

        if b.hittest(target2) and target2.live:
            target2.live = 0
            target2.hit()
            target2.new_target()

        if b.hittest(target3) and target3.live:
            target3.live = 0
            target3.hit()
            target3.new_target()
    gun.power_up()

pygame.quit()
