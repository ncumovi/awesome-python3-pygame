# 这个模块放一些常用的工具和基础类和精灵类
# 引入其他模块使用
import pygame
import random
# 设置游戏屏幕大小 这是一个常量
SCREEN_REACT = pygame.Rect(0,0,580,574)
# 敌机的定时器事件常量
CREATE_ENEMY_EVENT = pygame.USEREVENT

# 定制一个精灵类 需要继承pygame提供的精灵类
# 需要定义的属性有：
# image 图片
# rect 坐标
#speed 速度

#接下来开始写敌机方面的内容 生产敌机器
#先定义一个事件常量(发射子弹)
HERO_FIRE_EVENT = pygame.USEREVENT + 1

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, new_image, new_speed=1):
        super().__init__()
        #图片
        self.image = pygame.image.load(new_image)
        #速度
        self.speed = new_speed
        #位置 获取图片的宽和高 get_rect(0,0,宽，高)
        self.rect = self.image.get_rect()
        #精灵移动的速度 包括英雄精灵 背景精灵 低级精灵 子弹精灵
        self.speed = new_speed

    def update(self, *args):
        #默认垂直方向移动 y轴控制垂直方向
        self.rect.y += self.speed
        #self.rect.x += 1

#以上是游戏的基础类 接下来是设置背景类
#明确背景类继承游戏的精灵类
class Background(GameSprite):
    def __init__(self, is_alt = False):
        #is_alt判断是否是另一张图像
        #False表示第一张图
        #True表示另一张图
        #两张图像交替循环
        #传图片
        super().__init__('./images/beijing.jpg')
        if is_alt:
            #如果是第二张图片 初始位置为-slef.rect.height
            self.rect.y = -self.rect.height
    def update(self, *args):
        #调用父类方法
        super().update()
        if self.rect.y >= SCREEN_REACT.height:
            self.rect.y = - self.rect.height

#敌机出动
class Enemy(GameSprite):
    #敌机精灵
    def __init__(self):
        #调用父类方法 创建敌机精灵 并且指定低级图像
        super().__init__('./images/enemy1.jpg')
        #设置低级的随机初始速度1-3
        self.speed = random.randint(2,6)
        #设置敌机随机初始位置
        self.rect.bottom = 0
        max_x = int(SCREEN_REACT.width - self.rect.width)
        self.rect.x = random.randint(0,max_x)
    def update(self, *args):
        #调用父类方法 让敌机在垂直方向运动
        super().update()
        #判断是否飞出屏幕 如果是 需要将敌机从精灵组删除
        if self.rect.y >= SCREEN_REACT.height:
            self.kill()
# 英雄出场
class Hero(GameSprite):
    def __init__(self):
        super().__init__('./images/life.jpg',0)
        self.bullet = pygame.sprite.Group()
        #设置初始位置
        self.rect.center = SCREEN_REACT.center
        self.rect.bottom = SCREEN_REACT.bottom-120
        self.move = False
    def update(self, *args):
        if not self.move:
            self.rect.x += self.speed
        else:
            self.rect.y += self.speed

        #英雄飞出屏幕
        if self.rect.bottom <= 139:
            if self.speed < 0:
                self.rect.y = 0
        elif self.rect.bottom > 520:
            if self.speed > 0:
                self.rect.y = SCREEN_REACT.height - self.rect.height
        if self.rect.left <= 0:
            self.rect.x = 0
        elif self.rect.right >= SCREEN_REACT.width:
            self.rect.x = SCREEN_REACT.width-self.rect.width

    def fire(self):
        #发射子弹
        for i in (1,2,3):
            bullet = Bullet()
            bullet.rect.bottom = self.rect.y - i*20
            bullet.rect.center = self.rect.center
            self.bullet.add(bullet)

#子弹精灵
class Bullet(GameSprite):
    def __init__(self):
        super().__init__('./images/bullet1.png',-5)
    def update(self, *args):
        super().update()
        # 判断是否飞出屏幕 如果是从精灵组删除
        if self.rect.bottom < 0:
            self.kill()
