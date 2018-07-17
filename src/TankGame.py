import pygame,os,sys,math,random
from pygame.locals import *
from sys import exit
from gameobjects.vector2 import Vector2

pygame.init()
#==================游戏实体======================
class GameObject(object):
    def __init__(self):
        self.x=None
        self.y=None
        self.width=40
        self.height=40
        self.isAlive=True
        self.sprite=None

    def setImage(self,imgPath):
        self.sprite=pygame.image.load(imgPath)
        # self.width,self.height=self.sprite.get_size()

    def update(self):
        pass

    def display(self):
        surface.blit(self.sprite, (self.x, self.y))

    #用于检测在此方块上的碰撞
    def isCrash(self,other):
        if self.x < other.x + other.width-10 \
                and self.x + self.width > other.x +10 \
                and self.y < other.y + other.height-10  \
                and self.y + self.height > other.y+10 :
            return True
        return False

    def __str__(self):
        return "坐标(%d,%d),名称%s"%(self.x,self.y,self)

#========================地图类========================
class Map(GameObject):
    def __init__(self,x,y,type):
        super().__init__()
        self.x=x
        self.y=y
        self.sprite=wallSprite[type-1]
        self.type=type
        self.width,self.height=self.sprite.get_size()

    #用于检测在此方块上的碰撞
    def isCrash(self,other):
        pass

    def setImage(self,sprite):
        self.sprite=sprite
        self.width=sprite

    #在surface上绘制
    def display(self):
        if self.type == 0:
            return
        surface.blit(self.sprite,(self.x,self.y))

    def update(self):
        pass

    def __str__(self):
        return "坐标(%d,%d),地图%d"%(self.x,self.y,self.type)

# =====================玩家类=============================
class Player(GameObject):
    def __init__(self,x,y):
        super().__init__()
        super().setImage("../resources/img/tank_1.png")
        self.x=x
        self.y=y
        #self.direction=Vector2(0,-1)
        self.direction = 1      #坦克朝向 1上2右3下4左
        self.needMove=False
        self.speed=100
        self.life=100
        #self.lifeFrame=        #血条

    def fire(self):
        bullet = Bullet(self.x,self.y,self.width,self.height,self.direction)
        player_bullets.append(bullet)

    def hurt(self):
        pass

    def move(self):
        pass

    def isCrash(self,other):
        if super().isCrash(other):
            return self.direction
        return 0

    def update(self):
        #pressedKey = pygame.key.get_pressed()   #获取按键
        moveDir=Vector2(0,0)    #移动方向
        if pressedKey[K_a]:
            moveDir.x = -1
            if self.direction == 1 :
                self.sprite = pygame.transform.rotate(self.sprite, 90.)
            elif self.direction == 2:
                self.sprite = pygame.transform.rotate(self.sprite, 180.)
            elif self.direction == 3:
                self.sprite = pygame.transform.rotate(self.sprite, -90.)

            self.direction = 4
            self.needMove=True
        elif pressedKey[K_d]:
            moveDir.x = 1
            if self.direction == 1 :
                self.sprite = pygame.transform.rotate(self.sprite, -90.)
            elif self.direction == 3:
                self.sprite = pygame.transform.rotate(self.sprite, 90.)
            elif self.direction == 4:
                self.sprite = pygame.transform.rotate(self.sprite, 180.)

            self.direction=2
            self.needMove = True
        elif pressedKey[K_w]:
            moveDir.y = -1
            if self.direction == 4 :
                self.sprite = pygame.transform.rotate(self.sprite, -90.)
            elif self.direction == 2:
                self.sprite = pygame.transform.rotate(self.sprite, 90.)
            elif self.direction == 3:
                self.sprite = pygame.transform.rotate(self.sprite, 180.)

            self.direction=1
            self.needMove = True
        elif pressedKey[K_s]:
            moveDir.y = 1
            if self.direction == 1 :
                self.sprite = pygame.transform.rotate(self.sprite, 180.)
            elif self.direction == 2:
                self.sprite = pygame.transform.rotate(self.sprite, -90.)
            elif self.direction == 4:
                self.sprite = pygame.transform.rotate(self.sprite, 90.)

            self.direction=3
            self.needMove = True
        # else:
        #     self.x=0
        #     self.y=0
        #     self.needMove=False
        moveDir.normalise()     #向量规格化
        self.x += moveDir.x * self.speed * timePassedSecond
        self.y += moveDir.y * self.speed * timePassedSecond
        borderLimit(self)
    def changWeapon(self):
        pass

    def display(self):
        surface.blit(self.sprite,(self.x,self.y))

class Bullet(GameObject):
    def __init__(self,x,y,width,height,direction):
        super().__init__()
        self.direction = direction
        self.damage = random.randint(5,10)
        self.setImage("../resources/img/bullet_2.png")
        if(direction == 1):
            self.sprite = pygame.transform.rotate(self.sprite, 90.)
            self.xSpeed = 0
            self.ySpeed = -5
            self.x = x + width/2 - self.width/2
            self.y = y - self.height
        elif(direction == 2):
            # self.sprite = pygame.transform.rotate(self.sprite, 90.)
            self.xSpeed = 5
            self.ySpeed = 0
            self.x = x + width
            self.y = y + height/2 - self.height/2
        elif(direction == 3):
            self.sprite = pygame.transform.rotate(self.sprite, -90.)
            self.xSpeed = 0
            self.ySpeed = 5
            self.x = x + width/2 - self.width/2
            self.y = y + height
        elif(direction == 4):
            self.sprite = pygame.transform.rotate(self.sprite, 180.)
            self.xSpeed = -5
            self.ySpeed = 0
            self.x = x - self.width
            self.y = y + height/2 -self.height/2

    def update(self):
        self.x += self.xSpeed
        self.y += self.ySpeed
        if self.x > surface_WIDTH or self.x + self.width < 0 or \
            self.y > surface_HEIGHT or self.y + surface_HEIGHT < 0:
            self.isAlive = False
    def display(self):
        surface.blit(self.sprite,(self.x, self.y))

#========================敌人类=====================
class Enemy():
    def __init__(self,x,y):
        super().__init__()
        super().setImage("../resources/img/tank_2.png")
        self.x = x
        self.y = y
        # self.direction=Vector2(0,-1)
        self.direction = 1  # 坦克朝向 1上2右3下4左
        self.needMove = False
        self.speed = 100
        self.life = 100
        self.patrolPath=[]

    def hurt(self):
        pass

    def move(self):
        pass

    def update(self):
        moveDir = Vector2(0, 0) #移动方向

        if self.direction==1:
            moveDir=Vector2(0,-1)
        elif self.direction == 2:
            moveDir=Vector2(1,0)
        elif self.direction == 3:
            moveDir=Vector2(0,1)
        elif self.direction == 4:
            moveDir=Vector2(-1,0)

        moveDir.normalise()  # 向量规格化

        # self.x += moveDir.x * self.speed * timePassedSecond
        # self.y += moveDir.y * self.speed * timePassedSecond

    def patrol(self):
        pathPoint=self.patrolPath.pop()


    def setPatrolPath(self):
        pass

#============操控行为方法================
def arrive(source,destination):
    lenX=destination.x-source.x
    lenY=destination.y-source.y
    # dirTo=destination-source
    if lenY==0:
        if lenX > 10:
            source.x+=source.speed * timePassedSecond
        elif lenX <-10:
            source.x -= source.speed * timePassedSecond
        else :
            source.x+=source.speed*timePassedSecond*lenX/10.
    elif lenX==0:
        if lenY > 10:
            source.y+=source.speed * timePassedSecond
        elif lenY<-10:
            source.y -= source.speed * timePassedSecond
        else :
            source.y+=source.speed*timePassedSecond*lenY/10.

def seek(source,destination):
    lenX = destination.x - source.x
    lenY = destination.y - source.y
    # dirTo=destination-source
    if lenY == 0:
        source.x += source.speed * timePassedSecond
    elif lenX == 0:
        source.y += source.speed * timePassedSecond


#==================边界限制方法====================
def borderLimit(eneity):
    if eneity.x > surface_WIDTH - eneity.width:
        eneity.x = surface_WIDTH - eneity.width
    if eneity.x < 0:
        eneity.x = 0
    if eneity.y > surface_HEIGHT- eneity.height:
        eneity.y = surface_HEIGHT- eneity.height
    if eneity.y < 0:
        eneity.y = 0

#=======================事件监听方法=====================
def eventListener():
    global pressedKey   #按键信息
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                player.fire()
        # if event.type == MOUSEBUTTONDOWN:  # 按下鼠标触发
        #     left, wheel, right = pygame.mouse.get_pressed()
        #     if left == 1:
        #         player.move()
        # if event.type == MOUSEBUTTONUP:  # 抬起鼠标触发
        #     left, wheel, right = pygame.mouse.get_pressed()
        #     if left == 0:
        #         player.stop()
        # if event.type == KEYDOWN:  #键盘按下
        #     if event.key == locals.K_b:
        #         super_boom()
        # if event.type == VIDEORESIZE: #屏幕拉伸
        #     surface_SIZE = event.size
        #     surface = pygame.display.set_mode(surface_SIZE, RESIZABLE, 32)
        #     pygame.display.set_caption("Window resized to" + str(event.size))
    pressedKey = pygame.key.get_pressed()

#======================获取地图表方法===========================
def getList(Tlist,Tarray):
    blockLen=len(Tarray) #地图表长度
    i,j=0,0
    #获取地图表
    while i<blockLen:
        while j<len(Tarray[i]):
            mp=Map(j*mapBlockLenth,i*mapBlockLenth,Tarray[i][j])
            Tlist.append(mp)
            j+=1
        j=0
        i+=1

#=========================初始化方法==========================
def init():
    global surface,clock,player,background,tank1,tank2,tank3
    surface = pygame.display.set_mode((surface_WIDTH, surface_HEIGHT), 0, 32)
    background = pygame.image.load("../resources/img/background.png").convert()
    tank1 = pygame.image.load("../resources/img/tank_1.png").convert_alpha()
    tank2 = pygame.image.load("../resources/img/tank_2.png").convert_alpha()
    tank3 = pygame.image.load("../resources/img/tank_3.png").convert_alpha()
    clock = pygame.time.Clock()
    player = Player(320, 240)

    i = 1
    # 获取墙图片
    while i <= wallNum:
        sprite = pygame.image.load("../resources/img/wall_%d.png" % (i)).convert_alpha()
        wallSprite.append(sprite)
        i += 1

#=========================随机地图======================
def random_map():
    i=1
    generated_map=[]
    while i<=10:
        map_row =[]
        j = 1
        while j<=15:
            if random.random()<=0.6:
                map_row.append(0)
            else:
                map_row.append(random.randint(1,6))
            j+=1
        generated_map.append(map_row)
        i+=1
    return generated_map
#=========================总更新方法======================
def update():
    crash()
    player.update()
    bullets_update()

#========================显示 绘制 方法========================
def display():
    surface.blit(background, (0, 0))
    for mps in mapList:
        mps.display()
    player.display()
    for bullet in player_bullets:
        bullet.display()

def bullets_update():
    need_remove = []
    for bullet in player_bullets:
        if not bullet.isAlive:
            need_remove.append(bullet)
        bullet.update()
    for bullet in need_remove:
        player_bullets.remove(bullet)

def crash():
    player_crash_block()



def player_crash_block():
    for blk in mapList:
        if blk.type:
            if player.isCrash(blk) == 1:
                player.y = blk.y + 40
            elif player.isCrash(blk) == 2:
                player.x = blk.x - 40
            elif player.isCrash(blk) == 3:
                player.y = blk.y - 40
            elif player.isCrash(blk) == 4:
                player.x = blk.x + 40

surface = None
clock = None
background=None
tank1=None
tank2=None
tank3=None
timePassed=0        #记录游戏时间，ms
timePassedSecond=0  #记录游戏时间，s
gameTime = 0        #游戏总时间
surface_WIDTH=600   #屏幕宽度
surface_HEIGHT=400  #屏幕高度
# bgColor = (55,45,85)

player_bullets = [] #玩家子弹

FPS=60          #最大帧数
mapBlockLenth=40 #地图块大小
wallSprite=[]   #障碍物精灵组
tankSprite=[]   #坦克精灵组
wallNum=6      #障碍物总数
tankNum=2       #坦克总数

player=None     #玩家

#障碍物位置信息  15*10
mapArrayIndex=[
    [0,1,0,0,0,4,0,2,0,0,0,3,2,0,0,0],
    [0,0,0,0,2,0,4,0,0,0,0,0,0,1,2,0],
    [0,0,0,1,5,0,0,0,3,0,0,0,3,1,0,0],
    [2,0,0,1,0,6,1,0,0,0,0,0,0,5,0,1],
    [0,0,3,1,0,0,0,3,0,1,2,0,0,0,2,1],
    [0,2,6,0,0,5,0,0,0,0,0,2,0,0,0,1],
    [0,3,0,1,0,1,0,6,0,0,0,0,3,0,3,6],
    [0,0,0,1,0,1,0,3,1,0,0,1,0,1,5,2],
    [0,0,3,0,0,0,0,0,0,0,2,6,0,1,4,6],
    [0,0,2,1,6,0,0,5,0,4,0,6,1,0,2,1],
    #[0,0,0,1,2,0,0,0,3,0,0,0,3,1,0,0],
    ]
mapArrayIndex=random_map()
mapList=[]      #地图表，存储障碍物精灵图片
init()          #初始化
getList(mapList,mapArrayIndex)  #根据障碍物位置信息填写地图表
#绘制背景地图
surface.blit(background,(0,0))
#绘制障碍物
# for mps in mapList:
#     mps.display(surface)
#     print(mps)

while True:
    eventListener() #事件监听
    timePassed = clock.tick(FPS)  # 获取时间ms
    timePassedSecond = timePassed / 1000.0  # 时间转换为s
    gameTime += timePassed
    # for event in pygame.event.get():
    #     if event.type == QUIT:
    #         exit()
    # surfaceWidth, surfaceHeight = surface_SIZE
    #
    # # 重新填满窗口
    # for y in range(0, surfaceHeight, background.get_height()):
    #     for x in range(0, surfaceWidth, background.get_width()):
    #         surface.blit(background, (x, y))
    # clock.tick(60)
    #surface.blit(background,(0,0))
    # surface.blit(ikongSprite,(0,0))
    # 绘制地图
    # for mps in mapList:
    #     mps.drawWall(surface)
    #     print(mp)
    update()
    display()

    pygame.display.update()