#py3.12.7
import pygame
import numpy as np
import random
import config
from importlib import reload  # 用于重新加载模块
from missile import Missile
from defense_system import DefenseSystem
from environment import Environment
from draw_utils import *

def main():
    """主程序入口"""
    pygame.init()
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
    pygame.display.set_caption("Advanced Missile Defense System")
    clock = pygame.time.Clock()
    running = True
    
    # 创建环境对象
    environment = Environment()
    
    # 游戏状态
    missiles = []
    defense_system = DefenseSystem(environment)
    missiles_launched = 0
    missiles_intercepted = 0
    missiles_hit = 0
    last_missile_time = 0
    last_combo_time = 0
    sleep_time = config.SLEEP_TIME_MISSILE
    defense_enabled = True  # 防御系统默认启用
    auto_intercept = False   # 自动发射默认关闭
    
    # 重置游戏的函数
    def reset_game():
        """重置游戏并重新加载配置"""
        nonlocal missiles, defense_system, missiles_launched, missiles_intercepted, missiles_hit
        nonlocal last_missile_time, sleep_time, defense_enabled, auto_intercept
        
        # 重新加载config模块以获取最新配置
        reload(config)
        
        missiles = []
        defense_system = DefenseSystem(environment)
        missiles_launched = 0
        missiles_intercepted = 0
        missiles_hit = 0
        last_missile_time = 0
        last_combo_time = 0
        sleep_time = config.SLEEP_TIME_MISSILE
        defense_enabled = True
        auto_intercept = False  
    
    # 初始化游戏
    reset_game()
    
    while running:
        current_time = pygame.time.get_ticks()
        
        # 更新环境
        environment.update_environment(current_time)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # 重置游戏
                    reset_game()
                elif event.key == pygame.K_s:
                    # 发射真弹（有冷却时间）
                    if current_time - last_missile_time > sleep_time:
                        missiles.append(Missile(config.LAUNCHER_POS, config.TARGET_POS, 
                                              is_real=True, environment=environment))
                        missiles_launched += 1
                        last_missile_time = current_time
                elif event.key == pygame.K_d:
                    # 发射假弹（有冷却时间）
                    if current_time - last_missile_time > sleep_time: 
                        missiles.append(Missile(config.LAUNCHER_POS, config.TARGET_POS, 
                                              is_real=False, environment=environment))
                        missiles_launched += 1
                        last_missile_time = current_time
                elif event.key == pygame.K_a:
                    if current_time - last_missile_time > sleep_time:
                        missiles.append(Missile(config.LAUNCHER_POS, config.TARGET_POS, 
                                              is_real=True, environment=environment, guided=True))
                        missiles_launched += 1
                        last_missile_time = current_time
                elif event.key == pygame.K_f:
                    # 切换防御系统状态
                    defense_enabled = not defense_enabled
                    # 清除所有跟踪器和拦截弹
                    defense_system.clear_all_trackers()
                    defense_system.interceptors = []
                elif event.key == pygame.K_x:  # 添加自动发射开关
                    # 切换自动发射状态
                    auto_intercept = not auto_intercept
                elif event.key == pygame.K_SPACE:  # 添加组合发射按键
                    # 检查组合发射冷却时间
                    if current_time - last_combo_time > config.COMBO_LAUNCH_COOLDOWN:
                        last_combo_time = current_time
                        
                        # 发射制导导弹
                        for _ in range(config.COMBO_LAUNCH["guided"]):
                            missiles.append(Missile(config.LAUNCHER_POS, config.TARGET_POS, 
                                                  is_real=True, environment=environment, guided=True))
                            missiles_launched += 1
                        
                        # 发射真弹
                        for _ in range(config.COMBO_LAUNCH["real"]):
                            missiles.append(Missile(config.LAUNCHER_POS, config.TARGET_POS, 
                                                  is_real=True, environment=environment))
                            missiles_launched += 1
                        
                        # 发射假弹
                        for _ in range(config.COMBO_LAUNCH["decoy"]):
                            missiles.append(Missile(config.LAUNCHER_POS, config.TARGET_POS, 
                                                  is_real=False, environment=environment))
                            missiles_launched += 1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 处理鼠标点击
                if event.button == 1:  # 左键点击
                    defense_system.handle_click(event.pos)
                elif event.button == 3:  # 右键点击
                    # 右键点击向选择的点发射拦截弹
                    defense_system.launch_to_selected_point(current_time)    
                    
        # 更新导弹 - 优先处理拦截事件
        for missile in missiles[:]:
            # 检查是否被拦截
            if missile.intercepted:
                missiles_intercepted += 1
                missiles.remove(missile)
                defense_system.remove_tracker(id(missile))
                continue
                
            # 更新导弹状态
            status = missile.update(current_time)
            if status == "hit":
                missiles_hit += 1
                missiles.remove(missile)
                # 移除该导弹的跟踪器
                defense_system.remove_tracker(id(missile))
            elif status == "miss":
                missiles.remove(missile)
                # 移除该导弹的跟踪器
                defense_system.remove_tracker(id(missile))
        
        # 更新防御系统（仅在防御启用时）
        if defense_enabled:
            for missile in missiles:
                if missile.active:
                    # 记录导弹位置
                    defense_system.record_missile_position(missile, current_time)
                    
                    # 预测轨迹
                    predicted_trajectory = defense_system.predict_trajectory(missile, current_time)
                    
                    # 自动发射拦截弹（仅在自动发射开启时）
                    if auto_intercept and predicted_trajectory and len(predicted_trajectory) > 5:
                        # 选择预测轨迹上的一个点作为目标
                        target_point = predicted_trajectory[5]
                        defense_system.launch_interceptor(config.DEFENSE_POS, target_point, id(missile), current_time)
            
            # 更新拦截弹
            if missiles and defense_system.interceptors:
                intercept_results = defense_system.update_interceptors(missiles)
                # 拦截结果已经在拦截弹类中处理，这里不需要额外计数
        
        # 绘制游戏环境
        draw_environment(screen)
        
        # 绘制发射器和目标
        draw_launcher(screen, config.LAUNCHER_POS)
        draw_target(screen, config.TARGET_POS)
        draw_launcher(screen, config.DEFENSE_POS)
        
        # 绘制导弹
        for missile in missiles:
            draw_missile(screen, missile)
        
        # 仅在防御启用时绘制防御系统
        if defense_enabled:
            defense_system.draw(screen)
        
        # 绘制物理信息和防御状态（左上角）
        draw_physics_info(screen, environment, defense_enabled)
        
        # 绘制统计数据（右上角）
        draw_stats(screen, missiles_launched, missiles_intercepted, missiles_hit, defense_enabled, auto_intercept)  # 添加auto_intercept参数
        
        # 绘制操作说明（底部）
        draw_instructions(screen, defense_enabled,auto_intercept)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
if __name__ == "__main__":
    main()