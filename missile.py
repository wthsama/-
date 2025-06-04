import numpy as np
import math
import random
import pygame
from config import *
from environment import Environment

class Missile:
    def __init__(self, start_pos, target_pos, is_real=True, environment=None, guided=False,max_turn_rate=MAX_TURE_RATE_MISSILE,guidance_strength=GUIDANCE_STRENGTH):
        self.start_pos = np.array(start_pos, dtype=float)
        self.target_pos = np.array(target_pos, dtype=float)
        self.pos = np.array(start_pos, dtype=float)
        self.velocity = np.array([0.0, 0.0])
        self.trajectory = [self.pos.copy()]
        self.active = True
        self.launch_time = pygame.time.get_ticks()
        self.is_real = is_real  # 标记是否为真弹（能击中目标）
        self.intercepted = False  # 是否被拦截
        self.hit_target = False  # 是否击中目标
        self.environment = environment if environment else Environment()
        self.guided = guided  # 是否为制导导弹
        self.guidance_active = False  # 制导系统是否激活
        self.guidance_start_time = 0  # 制导开始时间
        self.guidance_delay = random.randint(6000, 7000)  # 制导系统启动延迟
        
        # 计算距离
        self.distance = np.linalg.norm(self.target_pos - self.start_pos)
        
        # 初始速度计算（抛物线模型） - 添加5%随机误差
        if is_real:
            # 真弹有更高的概率直接飞向目标
            angle = random.uniform(50, 60)  # 较小的角度范围
            speed = MISSILE_SPEED   # 较高的速度
        else:
            # 假弹有更大的角度变化和较低的速度
            angle = random.uniform(35, 60)  # 较大的角度范围
            speed = random.uniform(6, 16)   # 较低的速度
        
        self.velocity = np.array([
            speed * math.cos(math.radians(angle)),
            -speed * math.sin(math.radians(angle))
        ])
        
        # 随机扰动因素
        self.random_factor = random.uniform(0.8, 1.2)
        
        # 制导参数
        self.max_turn_rate = max_turn_rate  # 最大转向角度（度/帧）
        self.guidance_strength = guidance_strength  # 制导强度系数
        
    def update(self, current_time):
        """更新导弹位置和状态（使用抛物线模型）"""
        if not self.active:
            return
            
        # 更新环境
        self.environment.update_environment(current_time)
        
        # 获取实际风力
        wind_x, wind_y = self.environment.get_wind_actual()
        
        # 计算时间因子
        dt = 0.2
        
        # 检查是否激活制导系统
        if self.guided and not self.guidance_active:
            if current_time - self.launch_time > self.guidance_delay:
                self.guidance_active = True
                self.guidance_start_time = current_time
        
        # 如果导弹是制导的且制导系统已激活
        if self.guided and self.guidance_active:
            # 计算目标方向
            target_direction = self.target_pos - self.pos
            distance_to_target = np.linalg.norm(target_direction)
            
            if distance_to_target > 0:
                target_direction = target_direction / distance_to_target
                
                # 计算当前速度方向
                current_speed = np.linalg.norm(self.velocity)
                if current_speed > 0:
                    current_direction = self.velocity / current_speed
                else:
                    current_direction = np.array([1.0, 0.0])
                
                # 计算当前方向与目标方向的夹角
                dot_product = np.dot(current_direction, target_direction)
                angle = np.degrees(np.arccos(np.clip(dot_product, -1.0, 1.0)))
                
                # 如果角度偏差较大，进行制导修正
                if angle > 2:
                    # 计算转向方向（顺时针或逆时针）
                    cross_product = np.cross(current_direction, target_direction)
                    turn_direction = 1 if cross_product > 0 else -1
                    
                    # 计算转向角度（不超过最大转向率）
                    turn_angle = min(angle, self.max_turn_rate) * turn_direction
                    
                    # 创建旋转矩阵
                    turn_rad = math.radians(turn_angle)
                    rotation_matrix = np.array([
                        [math.cos(turn_rad), -math.sin(turn_rad)],
                        [math.sin(turn_rad), math.cos(turn_rad)]
                    ])
                    
                    # 应用旋转
                    new_direction = rotation_matrix @ current_direction
                    
                    # 更新速度方向（保持速度大小不变）
                    self.velocity = new_direction * current_speed
        
        # 计算地转偏向力 (科里奥利力)
        coriolis_force = np.array([
            CORIOLIS_FACTOR * self.velocity[1],
            -CORIOLIS_FACTOR * self.velocity[0]
        ])
        
        # 风力影响
        wind_force = np.array([
            wind_x * 1,
            wind_y * 1
        ])
        
        # 重力
        gravity_force = np.array([0, GRAVITY])
        
        # 计算总加速度
        acceleration = gravity_force + coriolis_force + wind_force
        
        # 更新速度
        self.velocity += acceleration * dt * self.random_factor
        
        # 更新位置
        self.pos += self.velocity * dt
        
        # 记录轨迹
        self.trajectory.append(self.pos.copy())
        
        # 检查是否击中目标
        distance_to_target = np.linalg.norm(self.pos - self.target_pos)
        if distance_to_target < 40:
            self.active = False
            self.hit_target = True
            return "hit"
            
        # 检查是否出界
        if (self.pos[0] < 0 or self.pos[0] > WIDTH or 
            self.pos[1] < 0 or self.pos[1] > HEIGHT):
            self.active = False
            return "miss"
            
        return "flying"