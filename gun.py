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
BlACGREY =(165, 165, 165)
TCOLOR = (150, 150, 150)
LCOLOR = (150, 150, 150)
POLCOLOR = (201, 201, 201)
WHEELS = 0x7D7D7D

# RED = 0xFF0000
# BLUE = 0x0000FF
# YELLOW = 0xFFC91F
# LIGHTYELLOW = 0x9e0606
# GREEN = 0x00FF00
# MAGENTA = 0xFF03B8
# CYAN = 0x00FFCC
# BLACK = 0xFFFFFF
# WHITE = (0, 0, 0)
# BlACGREY = 0x7D7D7D
# ORANGE = 0xFF8C00
# GREY = (165, 165, 165)
# TCOLOR = 0x7a7a7a


# GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
GAME_COLORS = [ORANGE, YELLOW, (255, 93, 0), (255, 200, 0), (255, 153, 0), (255, 229, 0)]

WIDTH = 800
HEIGHT = 600
GRAVITY = 120
LINEY = HEIGHT - 100
TATTACKTLONG = 500
TATTACKTSHORT = 50
MEGABOOM = 30

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

    def killing(self, which):
        # global boom
        # if self.r > 50:
        #     print(boom)
        #     boom -= 1
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
        self.r = 90
        self.birth = pygame.time.get_ticks()
        self.balllivind = MEGABOOM
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
        self.x = 40
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
        self.an = np.arctan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
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
            self.an = np.arctan2((event.pos[1]-self.y), (event.pos[0]-self.x))
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
        pygame.draw.ellipse(screen, BlACGREY, (self.x - 20, self.y - 5, 30, 20))
        pygame.draw.circle(screen, WHEELS, (self.x + 10, self.y + 10), 8)
        pygame.draw.circle(screen, WHEELS, (self.x - 20, self.y + 10), 8)
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
        self.r_min = 7
        self.r_max = 15
        self.color = TCOLOR
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
        x = self.x = rd.uniform(500, WIDTH)
        y = self.y = rd.uniform(300, LINEY)
        r = self.r = rd.uniform(self.r_min, self.r_max) 
        color = self.color

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        pygame.draw.circle(
            self.screen, BLACK,
            (self.x, self.y),
            self.r
        )
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r - 3
        )
        # FIXME

    
    def move(self):
        if self.x >= WIDTH - 10 or self.x <= 10:
            self.vx = -self.vx 
        if self.y <= 10 or self.y >= LINEY:
            self.vy = -self.vy
        self.x += self.vx*(1/FPS)
        self.y += self.vy*(1/FPS)
        if pygame.time.get_ticks() - self.time > 500:
            self.time = pygame.time.get_ticks()
            self.vy = self.vy*(1 + rd.uniform(-0.2, 0.23))
            self.vx = self.vx*(1 + rd.uniform(-0.2, 0.23))
            if self.vy > 410:
                self.vy = 400
            if self.vy < -410:
                self.vy = -400
            if self.vx > 410:
                self.vx = 400
            if self.vx < -410:
                self.vx = -400

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
        self.r_max = 10
        super().__init__(screen)
        self.b = 1
        self.color = BLACK
        self.b = 1
        self.v = 400
        self.new_megatarget()
        self.r = rd.uniform(self.r_min, self.r_max)
    
    def new_megatarget(self):
        self.live = 1
        # x = self.x = rd.uniform(600, 780)
        # y = self.y = rd.uniform(300, 550)
        # r = self.r = rd.uniform(self.r_min, self.r_max) 
        x = self.x = WIDTH
        y = self.y = rd.uniform(0, HEIGHT - 300)
        r = self.r = 30
        self.goingx = rd.uniform( 50, WIDTH - 50)
        self.goingy = self.y + rd.uniform( 50 - self.y, HEIGHT - 50 - self.y)*self.b
        v = self.v * rd.uniform(1, 2)
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
            self.goingy = self.y + rd.uniform( 50 - self.y, LINEY - self.y)*self.b
            self.vx = 1 * (self.goingx - self.x)
            self.vy = 1 * (self.goingy - self.y)
            v = self.v * rd.uniform(1, 2)
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

class BoomTarget(MegaTarget):
    def __init__(self, screen: pygame.Surface):
        self.r_max = 20
        self.r_min = 20
        super().__init__(screen)
        self.b = 0
        self.v = 50
        self.color = BlACGREY
        self.new_megatarget()

    def draw(self):
        pygame.draw.polygon(screen, RED, 
                [[self.x - self.r, self.y], [self.x, self.y + self.r/2], 
                [self.x + self.r, self.y]])
        pygame.draw.polygon(screen, BLACK, 
                [[self.x - self.r*0.75, self.y], [self.x, self.y + self.r*0.75/2], 
                [self.x + self.r*0.75, self.y]])

    def startattact(self):
        global attacks
        new_attackt = Attackt(self.screen)
        new_attackt.vx = self.vx
        new_attackt.vy = 0
        attacks.append(new_attackt)

class Attackt(BoomTarget):
    def __init__(self, screen):
        self.screen = screen
        super().__init__(screen)
        self.r = 3
        self.coror = RED
        self.vx = 0
        self.vy = 0

    def move(self):
        if self.x >= WIDTH - 10 or self.x <= 10:
            self.vx = -self.vx 
        if self.y >= HEIGHT - 10:
            self.vy = -self.vy
        self.x += self.multi*self.vx*(1/FPS)
        self.y += self.multi*self.vy*(1/FPS) - self.gravity*(1/FPS)**2
        self.vy += self.gravity*(1/FPS)

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        global game
        if (self.x - obj.x)**2 + (self.y - obj.y)**2  < (self.r  + 25)**2:
            game = 0


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
fine = 0
balls = []
attacks = []
megaballs =[]
texttime = 0
pr = 0
st = 0
game = 2
boom = 0

clock = pygame.time.Clock()
gun = Gun(screen)
target1 = Target(screen)
target2 = Target(screen)
target3 = MegaTarget(screen)
target4 = BoomTarget(screen)
target5 = BoomTarget(screen)
finished = False

attacktlong = pygame.time.get_ticks()
attacktshort = pygame.time.get_ticks()

while not finished:
    screen.fill(WHITE)
    if game:
        if target1.live:
            target1.draw()
            target1.move()
        if target2.live:
            target2.draw()
            target2.move()
        if target3.live:
            target3.draw()
            target3.move()
        if target4.live:
            target4.draw()
            target4.move()
        if target5.live:
            target5.draw()
            target5.move()

        font = pygame.font.SysFont(None, 24)
        img = font.render('Балл: ' + str(target1.points + target2.points +  target3.points - fine), True, BLACK)
        screen.blit(img, (20, 20))

        for i in range(0, WIDTH + 100, 15):
            pygame.draw.line(screen, LCOLOR, [i-6.5, LINEY-5], [i, LINEY-5], 2)

        pygame.draw.polygon(screen, POLCOLOR, 
                        [[0, HEIGHT], [WIDTH, HEIGHT], [WIDTH, HEIGHT-37], [0, HEIGHT-37]])
        gun.draw()

        for b in balls + megaballs:
            b.draw()

        for a in attacks:
            a.draw()

        if pygame.time.get_ticks() - texttime < 500 and pr:
            font1 = pygame.font.SysFont(None, 40)
            m = int((pygame.time.get_ticks() - texttime) / 500 * 250)
            clr = (m, m, m)
            img1 = font1.render('Нет баллов для взрыва', True, clr)
            screen.blit(img1, (WIDTH/2 - 160, HEIGHT/2 - 50))  

        if pygame.time.get_ticks() - attacktlong > TATTACKTLONG:
            ph = 1
            target4.startattact()
            attacktlong = pygame.time.get_ticks()

        pygame.display.update()

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
                megaballs[boom].boom()
                if boom < len(megaballs) - 1:
                    boom += 1
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

            if b.hittest(target4) and target4.live:
                target4.live = 0
                target4.new_megatarget()

            if b.hittest(target5) and target5.live:
                target5.live = 0
                target5.new_megatarget()

        for a in attacks:
            if a.hittest(gun):
                game = 0

        gun.power_up()

        kill = []
        for i in range(len(balls)):
            if balls[i].killing(COMMON):
                kill.append(i)
        for i in kill:
            del balls[i]
            
        kill = []
        for i in range(len(megaballs)):
            if megaballs[i].killing(MEGA):
                kill.append(i)
        for i in kill:
            if megaballs[i].r > 50:
                boom -= 1
            del megaballs[i]

    else:  
        font4 = pygame.font.SysFont(None, 24)
        img4 = font4.render('GAME OVER', True, BLACK)
        screen.blit(img4, (20, 20))

        for event in pygame.event.get():                               
            if event.type == pygame.QUIT:
                finished = True
            if event.type == pygame.KEYDOWN:
                finished = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                finished = True

pygame.quit()
