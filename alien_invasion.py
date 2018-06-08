import pygame
from alien_invasions.settings import Settings
from alien_invasions.ship import Ship
import alien_invasions.game_functions as gf
from pygame.sprite import Group
from alien_invasions.game_stats import GameStats
from alien_invasions.button import Button
from alien_invasions.scoreboard import Scoreboard

def run_game():
    # 初始化游戏设置和屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien invasion")
    #　创建游戏状态
    stats = GameStats(ai_settings)
    # 创建得分
    sb = Scoreboard(screen, stats, ai_settings)
    # 创建一艘飞船编组、一个子弹编组，一个外星人编组
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    # 创建外星人群
    gf.create_fleet(ai_settings, screen, ship, aliens)
    # 创建play按钮
    play_button = Button(ai_settings, screen, "play")
    # 开始游戏的主循环
    while True:
        gf.check_events(ai_settings, screen, ship, bullets, stats, play_button, aliens, sb)
        if stats.game_active:
            # 飞船位置更新
            ship.update()
            # 子弹更新
            gf.update_bullets(ai_settings, screen, ship, bullets, aliens, stats, sb)
            gf.update_aliens(ai_settings, screen, ship, stats, aliens, bullets, sb)
        # 更新屏幕
        gf.update_screen(ai_settings, stats, screen, ship, aliens, bullets, play_button, sb)


run_game()
