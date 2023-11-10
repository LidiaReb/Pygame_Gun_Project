import math
import random as rd
import choice

import pygame


FPS = 100

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
LIGHTYELLOW = 0xFFFFE0
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

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
        self.balllivind = 3000


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
        self.y += self.multi*self.vy*(1/FPS) - GRAVITY*(1/FPS)**2
        self.vy += GRAVITY*(1/FPS)
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
        self.r = 25
        self.balllivind = 100
        self.color = LIGHTYELLOW



class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.x = 50
        self.y = 50
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
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = 2 * self.f2_power * math.cos(self.an)
        new_ball.vy = 2 * self.f2_power * math.sin(self.an)
        new_ball.x = 20 + self.x + (self.f2_power + self.len) * math.cos(self.an)
        new_ball.y = 20 + HEIGHT - self.y + (self.f2_power + self.len) * math.sin(self.an)
        if whichball:
            balls.append(new_ball)
        else:
            megaballs.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.pos[1]-450) / (event.pos[0]-20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        pygame.draw.line(
            self.screen,
            self.color,
            [self.x, HEIGHT - self.y], 
            [self.x + (self.f2_power + self.len) * math.cos(self.an), HEIGHT - self.y + (self.f2_power + self.len) * math.sin(self.an)], 
            self.wight
            )
        # FIXME don't know how to do it

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:

    def __init__(self, screen):
        self.screen = screen
        self.points = 0
        self.live = 1
        self.time = pygame.time.get_ticks()
        self.vx = 100
        self.vy = 100
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
        r = self.r = rd.uniform(10, 30) 
        color = self.color = (150, 150, 150)

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
        self.y += self.vy*(1/FPS) - GRAVITY*(1/FPS)**2
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


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []
megaballs =[]

clock = pygame.time.Clock()
gun = Gun(screen)
target1 = Target(screen)
target2 = Target(screen)
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

    font = pygame.font.SysFont(None, 24)
    img = font.render('Балл: ' + str(target1.points + target2.points), True, 0)
    screen.blit(img, (20, 20))

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
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and len(megaballs) != 0:
            megaballs[0].boom()

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
    gun.power_up()

pygame.quit()
