# import _pyinstaller_hooks_contrib
# import pyinstall
import random
import pygame as game
import pygame.transform
from pygame.locals import *


class player_bullet(object):
    def __init__(self, screen, x, y):
        self.x = x + 20
        self.y = y
        self.screen = screen
        self.image = game.image.load('wallhaven-wqd2wr.jpg')

    def move(self):
        self.y -= 0.5

    def check_s_out(self):
        if self.y < 0:
            return True
        else:
            return False

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))


class enemy_bullet(object):
    def __init__(self, screen, x, y):
        self.x = x
        self.y = y + 5
        self.screen = screen
        self.image = game.image.load('wallhaven-wqd2wr.jpg')

    def move(self):
        self.y += 0.3

    def check_s_out(self):
        if self.y >= 1000:
            return True
        else:
            return False

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))


class player_plane(object):
    def __init__(self, screen,str_player):
        self.x = 755
        self.y = 455
        self.screen = screen
        self.image = game.image.load(
            str_player)
        self.image=pygame.transform.scale(self.image,(40,40))

        self.bulletlist = []

    def move_to_left(self):
        if self.x>=15 :
            self.x -= 8

    def move_to_right(self):
        if self.x<=960-65:
            self.x += 8

    def move_to_back(self):
        if self.y<=800-65:
            self.y += 8

    def move_to_straight(self):
        if self.y>=12 :
            self.y -= 8

    def fire(self):
        bullet = player_bullet(self.screen, self.x, self.y)
        self.bulletlist.append(bullet)

    def display(self, ):
        self.screen.blit(self.image, (self.x, self.y))
        dellist = []

        for i in self.bulletlist:
            if i.check_s_out():
                dellist.append(i)
        for i in dellist:
            self.bulletlist.remove(i)
        for i in dellist:
            dellist.remove(i)
        for i in self.bulletlist:
            i.display()
            i.move()


class enemy_plane(object):
    def __init__(self, screen,speed,path_str):
        self.x = 0
        self.y = 0
        self.speed=speed
        self.screen = screen
        self.path_str=path_str
        self.bulletlist = []
        self.direction = 'right'
        self.image = game.image.load(
            self.path_str)
        self.image=pygame.transform.scale(self.image,(40,40))

    def move_randomly(self):
        if self.x >= 1000-40:
            self.direction = 'left'
        if self.x <= 0:
            self.direction = 'right'
        if self.direction == 'right':
            self.x += self.speed
        if self.direction == 'left':
            self.x -= self.speed
        # if self.y >= 380: self.y -= 0.4 * 20
        # if self.y <= 0: self.y += 0.4 * 20
        # if self.y >= 0 and self.y <= 380: self.y += random.randint(-1, 1) * 3

    def fire(self):
        num = random.randint(1, 400)
        if num == 300:
            bullet = enemy_bullet(self.screen, self.x, self.y)
            self.bulletlist.append(bullet)

    def display(self):
        self.move_randomly()
        self.screen.blit(self.image, (self.x, self.y))
        self.fire()
        dellist = []
        for i in self.bulletlist:
            if i.check_s_out():
                dellist.append(i)
        for i in dellist:
            self.bulletlist.remove(i)
        for i in self.bulletlist:
            i.display()
            i.move()


def key_check(player):
    pygame.key.set_repeat(20, 21)
    List_event = pygame.event.get()
    for i in List_event:
        if i.type == QUIT:
            print('退出')
            exit()
        if i.type == KEYDOWN:
            if i.key == K_LEFT or i.key == K_a:
                # print('left')
                player.move_to_left()
            if i.key == K_RIGHT or i.key == K_d:
                # print('right')
                player.move_to_right()
            if i.key == K_s:
                player.move_to_back()
            if i.key == K_w:
                player.move_to_straight()
            if i.key == K_SPACE:
                player.fire()
                # print('发射')

            if i.key == K_ESCAPE:
                exit()
            # if i.key == K_SPACE:
            #     player.move_space()


def crate_enemy(screen,speed,path_str):
    a = enemy_plane(screen,speed,path_str)
    a.x = random.randint(100, 1000)
    a.y = random.randint(100, 400)
    return a


def check_attack_player(player, enemys):
    hit_times = 0
    be_hit_times = 0

    # player = player_plane(player)
    for j in enemys:
        for i in j.bulletlist:
            if player.x >= i.x - 20 and player.x <= i.x + 20 and player.y<=i.y+20 and player.y>=i.y-20:
                hit_times+=1
                try:
                    j.bulletlist.remove(i)
                except:
                    print('too quicka')
    return hit_times
Score=0
def check_attack_enemy(player,enemys):
    hit_list=[]
    global Score
    for i in player.bulletlist:
        for j in range(len(enemys)):
            if enemys[j].x>=i.x-10 and enemys[j].x<=i.x+10 and enemys[j].y<=i.y+10 and enemys[j].y  >=i.y-10:
                hit_list.append(j)

                try:
                    player.bulletlist.remove(i)
                    Score += 1
                    print(Score)
                except:
                    print(("too quick"))
    return hit_list
def begin(HP,level,screen,background,args,list_player):
    pygame.init()
    path=args###敌人路径列表，包括飞机照片和子弹照片
    i=int(2-HP//34)
    player = player_plane(screen,list_player[i])
    enemys = []
    score_font=pygame.font.Font('baddf.ttf',20)
    global Score
    for i in range(random.randint(5*level,10*level)): enemys.append(crate_enemy(screen,(random.randint(2,5)/10),path))
    while True:
        screen.blit(background, (0, 0))
        player.display()
        for i in enemys: i.display()
        HP -= check_attack_player(player, enemys)*(level*0.5)
        key_check(player)
        score_next=score_font.render('血量'+str(HP),True,(128,128,128)    )
        score_text = score_font.render('得分'+str(Score), True, (128, 128, 128))
        text_rect =score_text.get_rect()
        text_rect_2=score_next.get_rect()
        text_rect.topleft=[10,20]
        text_rect_2.topleft=[30,40]
        screen.blit(score_text,text_rect)
        screen.blit(score_next,text_rect_2)
        game.display.update()
        if len(enemys) != 0:
            for i in check_attack_enemy(player,enemys):
                try:
                    enemys.pop(i)
                except :
                    print("too quick")
        else:break
        # print(HP)
        if HP<=0:break
    return HP
def Ng(screen):
    HP=100
    clock=pygame.time.Clock()
    clock.tick(60)
    # pygame.font.Font()
    pygame.display.set_caption('Game')

    background = game.image.load('BACK.jpg')
    pygame.mixer.init()
    pygame.mixer.music.load('White Knight Instrumental - She Is My Sin (纯音乐).mp3')
    pygame.mixer.music.play(-1,0,0)
    str0='enemy'
    list_enemy_image=[str0+'1.png',str0+'2.png',str0+'3.png',str0+'4.png']
    list_player=['player1.png','player2.png','player3.png']
    for i in range(100):
        print(i)
        HP=begin(HP,i,screen,background,list_enemy_image[int(i%4)],list_player)
        if HP <=0:break
    bakc_end=game.image.load(".idea/green image.jpg")

screen = game.display.set_mode((1000, 800))
Ng(screen)
while True:
    List_event = pygame.event.get()
    for i in List_event:
        if i.type == QUIT:
            print('退出')
            exit()
    image_1=pygame.image.load('gameover.png')
    image_1=pygame.transform.scale(image_1,(1000,800))
    screen.blit(image_1,(0,0))
    game.display.update()
# screen_new=game.display.set_mode((1000,800))
# image_1=pygame.image.load('gameover.png')
# image_1=pygame.transform.scale(image_1,(1000,800))
# while True:
#     screen.blit(image_1,(0,0))
