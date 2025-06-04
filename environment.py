import numpy as np
import random
from config import ENVIRONMENT_UPDATE_INTERVAL

class Environment:
    def __init__(self):
        self.wind_x = random.uniform(-0.03, 0.03)
        self.wind_y = random.uniform(-0.02, 0.02)
        self.last_update_time = 0
    
    def update_environment(self, current_time):
        """更新环境参数（风力）"""
        if current_time - self.last_update_time > ENVIRONMENT_UPDATE_INTERVAL:
            self.wind_x = random.uniform(-0.03, 0.03)
            self.wind_y = random.uniform(-0.02, 0.02)
            self.last_update_time = current_time
    
    def get_wind_with_error(self):
        """获取带误差的风力测量值（带误差）"""
        error_factor = 1 + random.uniform(-0.0000005, 0.0000005)
        return self.wind_x * error_factor, self.wind_y * error_factor
    
    def get_wind_actual(self):
        """获取实际风力值"""
        return self.wind_x, self.wind_y