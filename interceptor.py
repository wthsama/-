import numpy as np
import pygame
from config import *

class Interceptor:
    def __init__(self, start_pos, target_pos, missile_id, speed=INTERCEPTOR_SPEED,max_turn_rate=MAX_TURE_RATE_INTERCEPTOR):
        self.start_pos = np.array(start_pos, dtype=float)
        self.target_pos = np.array(target_pos, dtype=float)
        self.missile_id = missile_id  # 要拦截的导弹ID
        self.pos = np.array(start_pos, dtype=float)
        self.velocity = np.array([0.0, 0.0])
        self.trajectory = [self.pos.copy()]
        self.active = True
        self.speed = speed
        self.max_turn_rate = max_turn_rate  # 最大转向角度（度）
        
        
        # 计算初始方向
        direction = self.target_pos - self.start_pos
        distance = np.linalg.norm(direction)
        if distance > 0:
            direction = direction / distance
            self.velocity = direction * speed
    
    def update(self, missiles):
        """更新拦截弹位置和状态"""
        if not self.active:
            return "inactive"
            
        dt = 0.2
        
        # 查找要拦截的导弹
        target_missile = None
        for missile in missiles:
            if missile.active and id(missile) == self.missile_id:
                target_missile = missile
                break
        
        # 如果找到目标导弹，进行预测制导
        if target_missile:
            # 预测导弹下一帧位置
            predicted_pos = target_missile.pos + target_missile.velocity * dt * 3
            
            # 计算理想方向
            ideal_direction = predicted_pos - self.pos
            distance = np.linalg.norm(ideal_direction)
            
            if distance > 0:
                ideal_direction = ideal_direction / distance
                
                # 计算当前方向
                current_speed = np.linalg.norm(self.velocity)
                if current_speed > 0:
                    current_direction = self.velocity / current_speed
                else:
                    current_direction = np.array([1.0, 0.0])
                
                # 计算当前方向与理想方向的夹角
                dot_product = np.dot(current_direction, ideal_direction)
                angle = np.degrees(np.arccos(np.clip(dot_product, -1.0, 1.0)))
                
                # 比例导航法：只在角度变化较大时调整方向
                if angle > self.max_turn_rate:
                    # 计算转向方向（顺时针或逆时针）
                    cross_product = np.cross(current_direction, ideal_direction)
                    turn_direction = 1 if cross_product > 0 else -1
                    
                    # 计算转向角度（不超过最大转向率）
                    turn_angle = np.radians(min(angle, self.max_turn_rate) * turn_direction)
                    
                    # 创建旋转矩阵
                    rotation_matrix = np.array([
                        [np.cos(turn_angle), -np.sin(turn_angle)],
                        [np.sin(turn_angle), np.cos(turn_angle)]
                    ])
                    
                    # 应用旋转
                    new_direction = rotation_matrix @ current_direction
                    
                    # 更新速度方向（保持速度大小不变）
                    self.velocity = new_direction * current_speed
                # 如果角度变化在阈值内，保持当前方向
        
        # 更新位置
        self.pos += self.velocity * dt
        
        # 记录轨迹
        self.trajectory.append(self.pos.copy())
        
        # 检查是否击中目标导弹
        if target_missile:
            # 使用动态碰撞阈值
            relative_velocity = target_missile.velocity - self.velocity
            relative_position = target_missile.pos - self.pos
            
            # 计算接近速度
            if np.linalg.norm(relative_position) > 0:
                closing_speed = np.dot(relative_velocity, relative_position) / np.linalg.norm(relative_position)
            else:
                closing_speed = 0
                
            # 动态调整碰撞阈值
            dynamic_threshold = max(8, 12 - abs(closing_speed) * 0.15)
            
            if np.linalg.norm(relative_position) < dynamic_threshold:
                self.active = False
                target_missile.intercepted = True
                target_missile.active = False
                return "hit"
                
        # 检查是否出界
        if (self.pos[0] < 0 or self.pos[0] > WIDTH or 
            self.pos[1] < 0 or self.pos[1] > HEIGHT):
            self.active = False
            return "miss"
            
        return "flying"