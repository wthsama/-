import numpy as np
import pygame
from interceptor import Interceptor
from config import *
from environment import Environment
from draw_utils import draw_interceptor

class DefenseSystem:
    def __init__(self, environment):
        self.trackers = {}  # 导弹ID -> 跟踪器数据
        self.interceptors = []
        self.last_launch_time = 0
        self.launch_cooldown = 500  # 0.5秒冷却时间
        self.environment = environment
        self.selected_point = None  # 用户选择的点
        self.selected_missile_id = None  # 用户选择的导弹ID
    
    def record_missile_position(self, missile, current_time):
        # 如果导弹已被拦截或失效，则清除其跟踪器
        if not missile.active:
            self.remove_tracker(id(missile))
            return
            
        missile_id = id(missile)
        
        # 如果是新导弹，创建跟踪器
        if missile_id not in self.trackers:
            self.trackers[missile_id] = {
                'positions': [],
                'times': [],
                'velocities': [],
                'predicted_trajectory': [],
                'last_prediction_time': 0,
                'prediction_points': []  # 存储预测点的屏幕坐标
            }
        
        # 记录位置、时间和速度
        tracker = self.trackers[missile_id]
        tracker['positions'].append(missile.pos.copy())
        tracker['times'].append(current_time)
        tracker['velocities'].append(missile.velocity.copy())
        
        # 保留最近20个点
        if len(tracker['positions']) > 20:
            tracker['positions'].pop(0)
            tracker['times'].pop(0)
            tracker['velocities'].pop(0)
    
    def predict_trajectory(self, missile, current_time):
        """预测导弹轨迹（使用三次多项式拟合）"""
        # 如果导弹已被拦截或失效，则清除其跟踪器
        if not missile.active:
            self.remove_tracker(id(missile))
            return []
            
        missile_id = id(missile)
        
        if missile_id not in self.trackers:
            return []
        
        tracker = self.trackers[missile_id]
        
        # 限制预测频率
        if current_time - tracker['last_prediction_time'] < 300:
            return tracker['predicted_trajectory']
        
        tracker['last_prediction_time'] = current_time
        
        if len(tracker['positions']) < 5:
            return []
            
        # 获取带误差的风力测量值
        wind_x, wind_y = self.environment.get_wind_with_error()
        
        # 使用多项式拟合轨迹
        x = np.array([p[0] for p in tracker['positions']])
        y = np.array([p[1] for p in tracker['positions']])
        t = np.array(tracker['times'])
        
        try:
            # 使用三次多项式拟合
            coeffs_x = np.polyfit(t, x, 3)
            poly_x = np.poly1d(coeffs_x)
            
            coeffs_y = np.polyfit(t, y, 3)
            poly_y = np.poly1d(coeffs_y)
            
            # 预测未来轨迹
            predicted_trajectory = []
            prediction_points = []  # 存储预测点的屏幕坐标
            for time_offset in np.arange(0, 1000, 30):
                pred_time = current_time + time_offset
                pred_x = poly_x(pred_time)
                pred_y = poly_y(pred_time)
                
                # 确保预测点在屏幕内
                if 0 <= pred_x <= WIDTH and 0 <= pred_y <= HEIGHT:
                    point = (pred_x, pred_y)
                    predicted_trajectory.append(point)
                    prediction_points.append((int(pred_x), int(pred_y)))
            
            tracker['predicted_trajectory'] = predicted_trajectory
            tracker['prediction_points'] = prediction_points
            
            return predicted_trajectory
        except:
            # 如果多项式拟合失败，使用简单外推法
            if len(tracker['positions']) >= 2:
                last_pos = tracker['positions'][-1]
                last_vel = tracker['velocities'][-1]
                
                predicted_trajectory = []
                prediction_points = []
                for time_offset in np.arange(0, 1000, 30):
                    dt = time_offset / 1000.0
                    pred_x = last_pos[0] + last_vel[0] * dt
                    pred_y = last_pos[1] + last_vel[1] * dt + 0.5 * GRAVITY * dt**2
                    
                    # 添加风力影响
                    pred_x += wind_x * dt * 10
                    pred_y += wind_y * dt * 10
                    
                    if 0 <= pred_x <= WIDTH and 0 <= pred_y <= HEIGHT:
                        point = (pred_x, pred_y)
                        predicted_trajectory.append(point)
                        prediction_points.append((int(pred_x), int(pred_y)))
                
                tracker['predicted_trajectory'] = predicted_trajectory
                tracker['prediction_points'] = prediction_points
                return predicted_trajectory
            return []
    
    def handle_click(self, pos):
        """处理用户点击，选择预测点作为拦截目标"""
        # 清除之前的选择
        self.selected_point = None
        self.selected_missile_id = None
        
        # 检查点击是否在某个预测点上
        for missile_id, tracker in self.trackers.items():
            for point in tracker['prediction_points']:
                distance = np.linalg.norm(np.array(pos) - np.array(point))
                if distance < 10:  # 如果点击点在10像素范围内
                    self.selected_point = point
                    self.selected_missile_id = missile_id
                    return True  # 找到匹配点
        
        return False  # 未找到匹配点
    
    def launch_interceptor(self, start_pos, target_pos, missile_id, current_time):
        """发射拦截弹"""
        if current_time - self.last_launch_time < self.launch_cooldown:
            return False
            
        self.last_launch_time = current_time
        interceptor = Interceptor(start_pos, target_pos, missile_id, speed=INTERCEPTOR_SPEED)
        self.interceptors.append(interceptor)
        return True
    
    def launch_to_selected_point(self, current_time):
        """向用户选择的点发射拦截弹"""
        if self.selected_point and self.selected_missile_id:
            return self.launch_interceptor(DEFENSE_POS, self.selected_point, self.selected_missile_id, current_time)
        return False
    
    def update_interceptors(self, missiles):
        """更新所有拦截弹状态"""
        results = []
        for interceptor in self.interceptors[:]:
            status = interceptor.update(missiles)
            if status != "flying":
                self.interceptors.remove(interceptor)
                results.append(status)
        return results
    
    def remove_tracker(self, missile_id):
        """移除导弹跟踪器"""
        if missile_id in self.trackers:
            del self.trackers[missile_id]
            
            # 如果移除的是当前选择的导弹，清除选择
            if missile_id == self.selected_missile_id:
                self.selected_point = None
                self.selected_missile_id = None
    
    def clear_all_trackers(self):
        """清除所有跟踪器"""
        self.trackers = {}
        self.selected_point = None
        self.selected_missile_id = None
    
    def draw(self, surface):
        """绘制防御系统相关元素"""
        # 绘制拦截弹
        for interceptor in self.interceptors:
            draw_interceptor(surface, interceptor)
            
        # 绘制所有导弹的预测轨迹
        for missile_id, tracker in list(self.trackers.items()):
            # 确保预测轨迹存在且有足够点绘制
            if tracker['predicted_trajectory'] and len(tracker['predicted_trajectory']) > 1:
                points = [(int(p[0]), int(p[1])) for p in tracker['predicted_trajectory']]
                pygame.draw.lines(surface, PREDICTION_COLOR, False, points, 1)
                
                # 绘制预测点
                for point in tracker['prediction_points']:
                    # 如果是选中的点，用不同颜色绘制
                    if point == self.selected_point and missile_id == self.selected_missile_id:
                        pygame.draw.circle(surface, (255, 255, 0), point, 5)  # 黄色表示选中
                    else:
                        pygame.draw.circle(surface, PREDICTION_COLOR, point, 2)
