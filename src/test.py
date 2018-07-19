#========================敌人类=====================
class Enemy(GameObject):
    def __init__(self,x,y):
        super().__init__()
        super().setImage("../resources/img/tank_2.png")
        self.x = x
        self.y = y
        # self.direction=Vector2(0,-1)
        self.direction = 1  # 坦克朝向 1上2右3下4左
        self.needMove = False
        self.speed = 50
        self.life = 5
        self.patrolPath=[]
        self.lifeFrame = pygame.image.load("../resources/img/blood.png")
        self.randomDir = 1
        self.moveAble = True
        self.boom_index = 0
        self.boom_img = []
        for i in range(11,21):
            self.boom_img.append(pygame.image.load("../resources/img/bomb_"+str(i)+".png"))

    def hurt(self,bullet):
        self.life -= bullet.damage
        if self.life <= 0:
            #to do socre
            global score
            score+=10
            self.isAlive = False

    def fire(self):
        bullet = Bullet(self.x,self.y,self.width,self.height,self.direction)
        enemyBullets.append(bullet)

    def move(self):
        pass

    def update(self):
        global enemies
        if self.isAlive:
            moveDir = Vector2(0, 0) #移动方向
            # randomDir = random.randint(1, 4)
            # randomDir = 1
            if gameCount % 30 == 0:
                self.fire()
            if gameCount % 30 == 0:
                self.randomDir = random.randint(1,4)
            if self.randomDir == 4:
                moveDir.x = -1
                if self.direction == 1:
                    self.sprite = pygame.transform.rotate(self.sprite, 90.)
                elif self.direction == 2:
                    self.sprite = pygame.transform.rotate(self.sprite, 180.)
                elif self.direction == 3:
                    self.sprite = pygame.transform.rotate(self.sprite, -90.)

                self.direction = 4
                self.needMove=True
            elif self.randomDir == 2:
                moveDir.x = 1
                if self.direction == 1 :
                    self.sprite = pygame.transform.rotate(self.sprite, -90.)
                elif self.direction == 3:
                    self.sprite = pygame.transform.rotate(self.sprite, 90.)
                elif self.direction == 4:
                    self.sprite = pygame.transform.rotate(self.sprite, 180.)

                self.direction=2
                self.needMove = True
            elif self.randomDir == 1:
                moveDir.y = -1
                if self.direction == 4 :
                    self.sprite = pygame.transform.rotate(self.sprite, -90.)
                elif self.direction == 2:
                    self.sprite = pygame.transform.rotate(self.sprite, 90.)
                elif self.direction == 3:
                    self.sprite = pygame.transform.rotate(self.sprite, 180.)

                self.direction=1
                self.needMove = True
            elif self.randomDir == 3:
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
            # if self.moveAble:
            self.x += moveDir.x * self.speed * timePassedSecond
            self.y += moveDir.y * self.speed * timePassedSecond
            if self.moveAble==False:
                if gameCount%30 ==0:
                    self.moveAble=True
                    self.speed=50


            # else:
            #     moveDir.x = -moveDir.x
            #     moveDir.y = -moveDir.y
            #     self.x += moveDir.x * self.speed * timePassedSecond
            #     self.y += moveDir.y * self.speed * timePassedSecond
            #     # if gameCount%40==0:
            #     self.moveAble = True

            borderLimit(self)
        else:
            if self.boom_index >= len(self.boom_img):
                enemies.remove(self)
                self.isAlive = False
                self.boom_index = len(self.boom_img) - 1
            self.sprite = self.boom_img[self.boom_index]
            # print(game_count)
            if gameCount % 6 == 0:
                self.boom_index += 1

    def display(self):
        if self.life > 0:
            surface.blit(self.lifeFrame, (self.x, self.y - 5))
            pygame.draw.rect(surface, (255, 0, 0),
                             (self.x - self.width + 39.8, self.y - self.height + 35,
                              1140 * self.life / 140, 5))
        surface.blit(self.sprite,(self.x,self.y))

    def isCrash(self,other):
        if super().isCrash(other,True) and other.isAlive:
        # if super().isCrash(other, False) and other.isAlive:
            if other==player:
                self.speed=0
                self.moveAble = False
            # self.speed = -self.speed

            return self.direction
        return 0

   #============================================================================================
class FoolState(State):
    def __init__(self,tank):
        State.__init__(self,"Fool")
        self.tank=tank

    def update(self):
        # print(self.tank.standardPos)
        if distanceTo(self.tank, self.tank.standardPos) < self.tank.arriveDist:
            print("位置规格化")
            arrive(self.tank,self.tank.standardPos,self.tank.speedDownDist)
        else:
            if self.tryObstacle(self.tank.direction):
                arrive(self.tank,self.tank.target,self.tank.speedDownDist)
            else:
                i=random.randint(1,3)
                print("(randomint):%d"%i)
                x,y=self.tank.direction
                print("原來direction坐標(x,y):%d,%d"%(x,y))
                if i==1:        #[x*cos90-y*sin90,x*sin90+y*cos90]
                    self.tank.direction.x=-y
                    self.tank.direction.y=x
                elif i==2:
                    self.tank.direction.x = -x
                    self.tank.direction.y = -y
                elif i==3:
                    self.tank.direction.x = y
                    self.tank.direction.y = -x

    def checkConditions(self):
        pass
        # tank = self.tank.world.getCloseEnemy("tank2",self.tank.location)
        # if tank is not None:

    def entryActions(self):
        pass

    def tryObstacle(self,direction):
        x=self.tank.x//40 +1
        y=self.tank.y//40 +1
        print("对应地图数组下标:",(x,y))
        tar=Vector2(x,y)+direction

        print("方向：",direction)
        print("目标",tar)
        block = self.findMapBlock(tar)
        # print(block)
        if block.type == 0:
            self.tank.target=Vector2(block.x,block.y)
            return True
        return False

    def findMapBlock(self,point):
        return mapList[int(point.x+15*point.y)]
