import pygame
from settings import Settings
from game_stats import GameStats
from button import Button
from ship import Ship
import game_functions
from pygame.sprite import Group


def run_game():
    # 初始化pygame,设置屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("外星人入侵")
    # 创建一个用于存储游戏统计信息的实例
    stats = GameStats(ai_settings)

    # 创建开始游戏按钮
    play_button = Button(ai_settings, screen, "Start")

    # 创建一艘飞船
    ship = Ship(ai_settings, screen)

    # 创建一个外星人编组
    aliens = Group()
    # 创建外星人群
    game_functions.create_fleet(ai_settings, screen, ship, aliens)

    # 创建一个用于存储子弹的编组
    bullets = Group()

    # 开始游戏的主循环
    while True:
        game_functions.check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets)
        if stats.game_active:
            ship.update()
            game_functions.update_bullets(ai_settings, screen, ship, aliens, bullets)
            game_functions.update_aliens( ai_settings, stats, screen, ship, aliens, bullets)
        game_functions.update_screen(ai_settings,stats, screen, ship, aliens, bullets, play_button)


run_game()