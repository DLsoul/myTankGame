
import pygame,os,sys
from pygame.locals import *
from sys import exit

pygame.init()

# #获取坦克图片
# while i<=tankNum:
#     sprite=pygame.image.load("../resources/img/tank_%d.png"%(i)).convert_alpha()
#     tankSprite.append(sprite)
#     i+=1

#获取地面图片
# startX,startY,rectWidth,rectHeight=0,0,20,20
# groundRect=pygame.Rect(startX,startY,rectWidth,rectHeight)
# while i<groundNum:
#     groundRect.left=i*rectWidth
#     groundRect.top=i*rectHeight
#     sprite=groundMap.subsurface(groundRect).copy()
#     groundSprite.append(sprite)
#     i+=1

#游戏实体
class GameObject(object):
    def __init__(self):
        self.x=None
        self.y=None
        self.width=None
        self.height=None
        self.isAlive=True
        self.sprite=None

    def setImage(self):
        pass

    def update(self):
        pass

    def display(self):
        pass

    #用于检测在此方块上的碰撞
    def isCrash(self,other):
        pass

    def __str__(self):
        return "坐标(%d,%d),名称%s"%(self.x,self.y,self)

#地图类
class Map(GameObject):
    def __init__(self,x,y,type):
        self.x=x
        self.y=y
        self.sprite=wallSprite[type-1]
        self.type=type

    #用于检测在此方块上的碰撞
    def isCrash(self,other):
        pass

    def setImage(self,sprite):
        self.sprite=sprite

    #在screen上绘制
    def display(self,screen):
        if self.type == 0:
            return
        screen.blit(self.sprite,(self.x,self.y))

    def update(self):
        pass

    def __str__(self):
        return "坐标(%d,%d),地图%s"%(self.x,self.y,self)

# 坦克类
# class Tank(GameObject):
#     def __init__(self,x,y,type):
#         super().__init__(x,y,type)
#         self.sprite=tankSprite[type-1]
#
#     def __str__(self):
#         return "坐标(%d,%d),坦克类型%d"%(self.x,self.y,self.type)
#

#地图测试
clock=pygame.time.Clock()
#地块类型表


#获取地图表
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

getList(mapList,mapArrayIndex)
#绘制背景地图
screen.blit(background,(0,0))
for mps in mapList:
    mps.setImage(screen)
    print(mps)
SCREEN_WIDTH=600
SCREEN_HEIGHT=400
bgColor = (55,45,85)

screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),0,32)
background=pygame.image.load("../resources/img/grass.png").convert()
clock=pygame.time.Clock()
#初始化
def init():
    i = 1
    # 获取墙图片
    while i <= wallNum:
        sprite = pygame.image.load("../resources/img/walls_%d.png" % (i)).convert_alpha()
        wallSprite.append(sprite)
        i += 1
    i = 1
mapBlockLenth=40 #地图块大小
wallSprite=[]   #障碍物精灵组
tankSprite=[]   #坦克精灵组
wallNum=20      #障碍物总数
tankNum=2       #坦克总数
mapArrayIndex=[
    [0,1,0,0,0,9,0,9,0,0,0,3,2,0,0,0,8,0,0,0],
    [0,0,0,0,2,0,8,0,0,0,0,0,0,1,12,0,0,0,3,0],
    [0,0,0,1,12,0,0,0,3,0,0,0,3,1,0,0,2,7,0,11],
    [2,0,0,1,0,12,1,0,0,0,0,0,0,7,0,11],
    [0,0,3,1,0,0,0,7,0,11],
    [0,20,8,0,0,5,0,0,0,0,0,2,0,0,0,1,12],
    [0,3,0,1,0,1,0,6,0,0],
    [0,0,0,1,0,1,0,3,19,0],
    [0,0,3,0,0,0,10,0,0,0],
    [0,0,2,1,6,0,0,9,0,14],
    [0,0,0,1,12,0,0,0,3,0,0,0,3,1,0,0,0,7,0,11],
    ]
mapList=[]
while True:
    for event in pygame.event.get():
        if event.type==QUIT:
            exit()

        # if event.type == VIDEORESIZE:
        #     SCREEN_SIZE = event.size
        #     screen = pygame.display.set_mode(SCREEN_SIZE, RESIZABLE, 32)
        #     pygame.display.set_caption("Window resized to" + str(event.size))
    # screenWidth, screenHeight = SCREEN_SIZE
    #
    # # 重新填满窗口
    # for y in range(0, screenHeight, background.get_height()):
    #     for x in range(0, screenWidth, background.get_width()):
    #         screen.blit(background, (x, y))
    # clock.tick(60)
    #screen.blit(background,(0,0))
    # screen.blit(ikongSprite,(0,0))
    # 绘制地图
    # for mps in mapList:
    #     mps.drawWall(screen)
    #     print(mp)

    for mps in mapList:
        mps.drawWall(screen)
    pygame.display.update()