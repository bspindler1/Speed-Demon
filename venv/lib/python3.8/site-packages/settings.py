import pygame


class Settings():
    """存储游戏设置"""

    def __init__(self):
        # 初始化游戏的设置
        # 屏幕设置，根据自己显示器大小调控
        self.screen_width = 1200
        self.screen_height = 600
        # 加载设置原色
        # self.bg_color = (230, 230, 230)
        # 加载本地图片
        self.bg_image = pygame.image.load("images/bg.jpg")


        # 飞船设置
        self.ship_speed_factor = 5
        self.ship_limit = 3

        # 子弹设置
        self.bullet_speed_factor = 15
        self.bullet_width = 2
        self.bullet_height = 5
        self.bullet_color = 255, 245, 238
        # 设置子弹数量
        self.bullets_allowed = 3

        # 外星人设置
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 5
        # fleet_direction为1表示向右移动，-1 表示向左移动
        self.fleet_direction = 1