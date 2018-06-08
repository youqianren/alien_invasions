import sys
import pygame
from alien_invasions.bullet import Bullet
from alien_invasions.alien import Alien
from time import sleep

def check_keydown_events(stats, aliens, event, ai_settings, screen, ship, bullets, sb):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(bullets, ai_settings, screen, ship)
    elif event.key == pygame.K_ESCAPE:
        sys.exit()
    elif event.key == pygame.K_p:
        if not stats.game_active:
            start_game(stats, aliens, bullets, ai_settings, screen, ship, sb)

def fire_bullet(bullets, ai_settings, screen, ship):
    """限制发射的子弹数"""
    # 创建新子弹并将其加入编组Bullet
    if len(bullets) < ai_settings.bullets_allowed:
        new_buttle = Bullet(ai_settings, screen, ship)
        bullets.add(new_buttle)

def check_keyup_events(event, ship):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_play_button(ai_settings, screen, stats, play_button, mouse_x, mouse_y, aliens, bullets, ship, sb):
    """点下play键游戏开始工作"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # 重置游戏速度
        ai_settings.initialize_dynamic_settings()
        start_game(stats, aliens, bullets, ai_settings, screen, ship, sb)

def start_game(stats, aliens, bullets, ai_settings, screen, ship, sb):
    """开始游戏前的准备"""
    # 隐藏光标
    pygame.mouse.set_visible(False)
    # 让飞船数、分数，游戏等级 重置
    stats.reset_stats()
    stats.game_active = True
    # 重置记分牌分数
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()
    # 删除外星人和子弹
    aliens.empty()
    bullets.empty()
    # 重新创造一群新的外星人并将其居中
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

def check_events(ai_settings, screen, ship, bullets, stats, play_button, aliens, sb):
    """响应按键和鼠标事件"""
    for  event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(stats, aliens, event, ai_settings, screen, ship, bullets, sb)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, mouse_x, mouse_y, aliens, bullets, ship, sb)

def get_number_aliens_x(ai_settings, alien_width):
    """计算出一行的外星人数"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """逐一添加外星人"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien_height = alien.rect.height
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.y = alien_height + 2 * alien_height * row_number
    alien.rect.x = alien.x
    alien.rect.y = alien.y
    aliens.add(alien)

def get_number_rows(ai_settings, alien_height, ship_height):
    """计算可容纳几行的外星人"""
    available_space_y = ai_settings.screen_height - 3 * alien_height - ship_height
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    alien = Alien(ai_settings, screen)
    #计算出一行的外星人数
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    #计算出可容纳几行外星人
    number_rows = get_number_rows(ai_settings, alien.rect.height, ship.rect.height)
    #逐一添加外星人
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_fleet_edges(ai_settings, aliens):
    """有外星人到达边缘时采取措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """将整群外星人向下移，并改变他们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def update_screen(ai_settings, stats,screen, ship, aliens, bullets, play_button, sb):
    screen.fill(ai_settings.bg_color)
    # 绘制得分和最高分
    sb.show_score()
    #在飞船和外星人后面重绘所有的子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    if not stats.game_active:
        play_button.draw_buttom()
    #让最近绘制的图片可见
    pygame.display.flip()

def update_aliens(ai_settings, screen, ship, stats, aliens, bullets, sb):
    """对每个外星人调用update()"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    # 检测外星人是否被撞毁
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, ship, stats, aliens, bullets, sb)
    # 检查外星人是否到达屏幕底部
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb)

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb):
    """ 检查外星人是否到达屏幕底部"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #像飞船被撞掉一样处理
            ship_hit(ai_settings, screen, ship, stats, aliens, bullets, sb)
            break

def ship_hit(ai_settings, screen, ship, stats, aliens, bullets, sb):
    """响应外星人撞到飞船"""
    if stats.ships_left > 0:
        stats.ships_left -= 1
        #
        sb.prep_ships()
        #清空外星人和子弹
        aliens.empty()
        bullets.empty()
        # 重新创建新的外星人组，并将飞船放在屏幕底端中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        # 暂停
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
def update_bullets(ai_settings, screen, ship, bullets, aliens, stats, sb):
    """更新子弹位置，并删除已消失的子弹"""
    #更新子弹位置
    bullets.update()
    # 删除消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # 检查子弹是否击中外星人
    # 如果击中就删除相应的子弹与外星人
    check_bullet_alien_collisions(ai_settings, screen, ship, aliens,bullets, stats, sb)

def check_high_score(stats, sb):
    """更新最高分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets, stats, sb):
    """  响应子弹和外星人的碰撞"""
    # 当子弹击中外星人，删除子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    # 外星人群被消灭后，重新创建外星人群
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)


