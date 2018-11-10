import pygame
from plane_sprites import *

#初始化
pygame.mixer.init()

pygame.mixer.music.load('./music/HandClap.mp3')

#播放
pygame.mixer.music.play(loops = -1)

HERO_FIRE_EVENT = pygame.USEREVENT + 1
class PlaneGame(object):
    def __init__(self):
        #游戏初始化
        # 创建游戏窗口 pygame.display.se_mode
        self.screen = pygame.display.set_mode(SCREEN_REACT.size)
        #创建游戏时钟
        self.clock = pygame.time.Clock()
        #创建精灵和精灵组内容较多 故封装成一个方法
        self.__create_sprites()

        #设置定时器 每间隔多少秒创造一个敌机
        pygame.time.set_timer(CREATE_ENEMY_EVENT,800)
        #设置定时器 发射子弹
        pygame.time.set_timer(HERO_FIRE_EVENT,400)
        #上面这一步定义了系统每隔0.5秒 调用一次pygame 事件

    def star_game(self):
        while True:
            #设置帧率
            self.clock.tick(200)
            #事件监听 主要监听鼠标键盘事件
            self.__event_handler()

            #碰撞检测
            self.__check_collide()
            #更新精灵和精灵组
            self.__update_sprites()
            #更新显示
            pygame.display.update()
            #以上都是要实时检测的 所以写在循环里

    #创建精灵和精灵组
    def __create_sprites(self):
        bg1 = Background()
        #True 表示是第二张图片
        bg2 = Background(True)

        #英雄
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)

        self.back_group = pygame.sprite.Group(bg1, bg2)
        #敌机组
        self.enemy_group = pygame.sprite.Group()

    #事件监听
    def __event_handler(self):
        for event in pygame.event.get():
            #如果某个键按下 对应的值应该是
            keys_pressed = pygame.key.get_pressed()
           
            #控制飞机移动
            if keys_pressed[276]:
                # print('left')
                self.hero.move = False
                self.hero.speed = -5
            elif keys_pressed[275]:
                # print('right')
                self.hero.move = False
                self.hero.speed = 5
            elif keys_pressed[273]:
                # print('up')
                self.hero.move = True
                if self.hero.rect.bottom < 139:
                    self.hero.speed = 0
                else:
                    self.hero.speed = -5
            elif keys_pressed[274]:
                # print('down')
                self.hero.move = True
                if self.hero.rect.bottom > 520:
                     self.hero.speed = 0
                else:     
                    self.hero.speed = 5
            else:
                self.hero.speed = 0

            if event.type == pygame.QUIT:
                self.__game_over()

            elif event.type == CREATE_ENEMY_EVENT:
                #产生新的敌机
                self.enemy_group.add(Enemy())
            #发射子弹
            elif event.type == HERO_FIRE_EVENT:
                self.hero.fire()

    # 更新精灵和精灵组
    def __update_sprites(self):

        for x in [self.back_group, self.enemy_group, self.hero_group, self.hero.bullet]:
            x.update()
            x.draw(self.screen)

    def __check_collide(self):
        #碰撞检测
        #子弹摧毁飞机
        #第一个参数和第二个参数是要参加碰撞检测的精灵
        #第三个参数为True的时候 就是当碰撞的时候被碰撞的精灵从精灵组移除
        pygame.sprite.groupcollide(self.enemy_group,self.hero.bullet, True, True)
        #敌机摧毁飞机
        enemies = pygame.sprite.spritecollide(self.hero,self.enemy_group, True)

        #判断列表时候有内容
        if len(enemies) > 0:
            #让英雄牺牲
            self.hero.kill()

            #结束游戏
            PlaneGame.__game_over()
    @staticmethod
    def __game_over():
        print('游戏结束')
        #这是pygame提供的卸载模块功能
        pygame.quit()
        exit()
        #需要先卸载pygame模块 然后退出脚本

if __name__ == '__main__':
    game = PlaneGame()
    game.star_game()