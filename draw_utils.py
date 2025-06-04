import pygame
from config import *

def draw_environment(surface):
    """绘制游戏环境"""
    # 绘制背景
    surface.fill(BACKGROUND)
    
    # 绘制网格
    for x in range(0, WIDTH, 50):
        pygame.draw.line(surface, GRID_COLOR, (x, 0), (x, HEIGHT), 1)
    for y in range(0, HEIGHT, 50):
        pygame.draw.line(surface, GRID_COLOR, (0, y), (WIDTH, y), 1)
    
    # 绘制中线
    pygame.draw.line(surface, (80, 100, 150), (WIDTH//2, 0), (WIDTH//2, HEIGHT), 2)
    
    # 绘制标题
    font = pygame.font.SysFont(None, 36)
    title = font.render("Advanced Missile Defense System", True, TEXT_COLOR)
    surface.blit(title, (WIDTH//2 - title.get_width()//2, 10))
    
    # 绘制区域标签
    font = pygame.font.SysFont(None, 28)
    attack_label = font.render("Attack Zone", True, (255, 100, 100))
    defense_label = font.render("Defense Zone", True, (100, 255, 150))
    surface.blit(attack_label, (WIDTH//4 - attack_label.get_width()//2, 20))
    surface.blit(defense_label, (3*WIDTH//4 - defense_label.get_width()//2, 20))

def draw_launcher(surface, pos):
    """绘制发射器"""
    pygame.draw.rect(surface, LAUNCHER_COLOR, (pos[0]-20, pos[1]-10, 40, 20))
    pygame.draw.rect(surface, (0, 100, 200), (pos[0]-15, pos[1]-30, 30, 20))
    pygame.draw.circle(surface, (200, 200, 100), (pos[0], pos[1]-40), 8)

def draw_target(surface, pos):
    """绘制目标"""
    pygame.draw.circle(surface, TARGET_COLOR, pos, 25)
    pygame.draw.circle(surface, (150, 30, 30), pos, 18)
    pygame.draw.circle(surface, (100, 20, 20), pos, 10)
    
    # 绘制目标符号
    pygame.draw.line(surface, (255, 255, 200), (pos[0]-15, pos[1]), (pos[0]+15, pos[1]), 2)
    pygame.draw.line(surface, (255, 255, 200), (pos[0], pos[1]-15), (pos[0], pos[1]+15), 2)

def draw_physics_info(surface, environment, defense_enabled):
    """绘制物理信息和防御状态 - 放在左上角"""
    font = pygame.font.SysFont(None, 24)
    
    # 获取实际和测量的风力值
    actual_wind_x, actual_wind_y = environment.get_wind_actual()
    measured_wind_x, measured_wind_y = environment.get_wind_with_error()
    
    # 绘制标题
    physics_title = font.render("Physics Parameters", True, TEXT_COLOR)
    surface.blit(physics_title, (20, 60))
    
    # 绘制实际风力信息
    actual_wind_text = font.render(f"Actual Wind: X:{actual_wind_x:.4f}, Y:{actual_wind_y:.4f}", True, TEXT_COLOR)
    surface.blit(actual_wind_text, (30, 90))
    
    # 绘制测量风力信息（带误差）
    measured_wind_text = font.render(f"Measured Wind: X:{measured_wind_x:.4f}, Y:{measured_wind_y:.4f}", True, (200, 200, 100))
    surface.blit(measured_wind_text, (30, 120))
    
    # 绘制地转偏向力信息
    coriolis_text = font.render(f"Coriolis Factor: {CORIOLIS_FACTOR:.6f}", True, TEXT_COLOR)
    surface.blit(coriolis_text, (30, 150))
    
    # 绘制重力信息
    gravity_text = font.render(f"Gravity: {GRAVITY:.2f} px/frame", True, TEXT_COLOR)
    surface.blit(gravity_text, (30, 180))
    
    # 绘制防御系统状态
    # defense_status = "ENABLED" if defense_enabled else "DISABLED"
    # defense_color = (100, 255, 100) if defense_enabled else (255, 100, 100)
    # defense_text = font.render(f"Defense System: {defense_status}", True, defense_color)
    # surface.blit(defense_text, (30, 210))

def draw_stats(surface, missiles_launched, missiles_intercepted, missiles_hit, defense_enabled, auto_intercept):
    """绘制统计数据 - 放在右上角"""
    font = pygame.font.SysFont(None, 24)
    
    # 绘制统计标题
    stats_title = font.render("System Stats", True, TEXT_COLOR)
    surface.blit(stats_title, (WIDTH - 220, 60))
    
    # 绘制发射导弹数
    launched_text = font.render(f"Missiles: {missiles_launched}", True, TEXT_COLOR)
    surface.blit(launched_text, (WIDTH - 210, 90))
    
    # 绘制拦截导弹数
    intercepted_text = font.render(f"Intercepted: {missiles_intercepted}", True, TEXT_COLOR)
    surface.blit(intercepted_text, (WIDTH - 210, 120))
    
    # 绘制命中目标数
    hit_text = font.render(f"Target Hits: {missiles_hit}", True, TEXT_COLOR)
    surface.blit(hit_text, (WIDTH - 210, 150))
    
    # 绘制防御系统状态
    defense_status = "ON" if defense_enabled else "OFF"
    defense_color = (0, 255, 0) if defense_enabled else (255, 0, 0)
    defense_text = font.render(f"Press F:Defense: {defense_status}", True, defense_color)
    surface.blit(defense_text, (30, 210))
    
    # 绘制自动发射状态
    auto_status = "ON" if auto_intercept else "OFF"
    auto_color = (0, 255, 0) if auto_intercept else (255, 0, 0)
    auto_text = font.render(f"Press X:Auto-intercept: {auto_status}", True, auto_color)
    surface.blit(auto_text, (30, 240))
    
    # 绘制命中率（防御关闭时显示）
    if missiles_launched > 0:
        hit_rate = missiles_hit / missiles_launched * 100
        rate_text = font.render(f"Hit Rate: {hit_rate:.1f}%", True, TARGET_COLOR)
        surface.blit(rate_text, (WIDTH - 210, 180))
    
    # 绘制拦截率（防御开启时显示）
    if defense_enabled and missiles_launched > 0:
        intercept_rate = missiles_intercepted / missiles_launched * 100
        rate_text = font.render(f"Intercept Rate: {intercept_rate:.1f}%", True, INTERCEPTOR_COLOR)
        surface.blit(rate_text, (WIDTH - 210, 210))
    
    # 绘制导弹说明
    real_text = font.render("Red: Real missile", True, REAL_MISSILE_COLOR)
    decoy_text = font.render("Orange: Decoy missile", True, DECOY_MISSILE_COLOR)
    surface.blit(real_text, (WIDTH - 700, 210))
    surface.blit(decoy_text, (WIDTH - 700, 240))

def draw_instructions(surface, defense_enabled, auto_intercept):
    """绘制操作说明"""
    font = pygame.font.SysFont(None, 24)
    text1 = font.render("Press S to launch missile", True, TEXT_COLOR)
    text2 = font.render("Press D to launch decoy missile", True, TEXT_COLOR)
    # text3 = font.render("Press F to toggle defense system", True, TEXT_COLOR)
    text4 = font.render("Press R to reset game", True, TEXT_COLOR)
    text5 = font.render("Press A to launch guided missile", True, TEXT_COLOR)
    # text6 = font.render("Press X to toggle auto-intercept", True, TEXT_COLOR)  # 新增自动发射提示
    text7 = font.render("Press SPACE to launch combo missiles", True, TEXT_COLOR)  # 新增组合发射提示
    text8 = font.render("Left-click: select intercept point", True, TEXT_COLOR)
    text9 = font.render("Right-click: launch interceptor", True, TEXT_COLOR)

    surface.blit(text1, (WIDTH//2 - text1.get_width()//2-450, HEIGHT - 300))
    surface.blit(text2, (WIDTH//2 - text2.get_width()//2-450, HEIGHT - 270))
    # surface.blit(text3, (WIDTH//2 - text3.get_width()//2-450, HEIGHT - 240))
    surface.blit(text4, (WIDTH//2 - text4.get_width()//2-450, HEIGHT - 210))
    surface.blit(text5, (WIDTH//2 - text5.get_width()//2-450, HEIGHT - 330))
    # surface.blit(text6, (WIDTH//2 - text6.get_width()//2-450, HEIGHT - 180))  # 新增自动发射提示
    surface.blit(text7, (WIDTH//2 - text7.get_width()//2-450, HEIGHT - 150))  # 新增组合发射提示
    surface.blit(text8, (WIDTH//2 - text8.get_width()//2-450, HEIGHT - 120))
    surface.blit(text9, (WIDTH//2 - text9.get_width()//2-450, HEIGHT - 90))
    # 显示防御状态提示
    if not defense_enabled:
        warning = font.render("DEFENSE SYSTEM DISABLED - Testing missile hit rate", True, (255, 100, 100))
        surface.blit(warning, (WIDTH//2 - warning.get_width()//2, 50))
    elif not auto_intercept:
        warning = font.render("AUTO-INTERCEPT DISABLED - Manual interception only", True, (255, 200, 100))
        surface.blit(warning, (WIDTH//2 - warning.get_width()//2, 50))

def draw_missile(surface, missile):
    """绘制导弹及其轨迹"""
    if not missile.active:
        return
        
    # 选择颜色：真弹用红色，假弹用橙色
    missile_color = REAL_MISSILE_COLOR if missile.is_real else DECOY_MISSILE_COLOR
    
    # 绘制轨迹
    if len(missile.trajectory) > 1:
        points = [(int(p[0]), int(p[1])) for p in missile.trajectory]
        pygame.draw.lines(surface, missile_color, False, points, 2)
    
    # 绘制导弹
    pygame.draw.circle(surface, missile_color, (int(missile.pos[0]), int(missile.pos[1])), 5)
    pygame.draw.circle(surface, (255, 200, 100), (int(missile.pos[0]), int(missile.pos[1])), 3)
    
    # 如果被拦截，绘制爆炸效果
    if missile.intercepted:
        pygame.draw.circle(surface, HIT_COLOR, (int(missile.pos[0]), int(missile.pos[1])), 15, 2)
        pygame.draw.circle(surface, HIT_COLOR, (int(missile.pos[0]), int(missile.pos[1])), 25, 1)

def draw_interceptor(surface, interceptor):
    """绘制拦截弹及其轨迹"""
    if not interceptor.active:
        return
        
    # 绘制轨迹
    if len(interceptor.trajectory) > 1:
        points = [(int(p[0]), int(p[1])) for p in interceptor.trajectory]
        pygame.draw.lines(surface, INTERCEPTOR_COLOR, False, points, 2)
    
    # 绘制拦截弹
    pygame.draw.circle(surface, INTERCEPTOR_COLOR, (int(interceptor.pos[0]), int(interceptor.pos[1])), 5)
    pygame.draw.circle(surface, (200, 255, 200), (int(interceptor.pos[0]), int(interceptor.pos[1])), 3)