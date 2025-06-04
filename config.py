# 全局配置和常量
import pygame
import random
import numpy as np

# 窗口尺寸
WIDTH, HEIGHT = 1200, 800

# 颜色定义
BACKGROUND = (10, 20, 40)
GRID_COLOR = (40, 60, 80)
LAUNCHER_COLOR = (0, 150, 255)
TARGET_COLOR = (255, 50, 50)
INTERCEPTOR_COLOR = (50, 255, 150)
TEXT_COLOR = (200, 220, 255)
PREDICTION_COLOR = (255, 200, 50)
REAL_MISSILE_COLOR = (255, 50, 50)  # 普通弹（高概率击中目标）颜色
DECOY_MISSILE_COLOR = (255, 150, 50)  # 诱饵弹（低概率击中目标）颜色
HIT_COLOR = (255, 255, 0)  # 命中效果颜色

# 物理参数
GRAVITY = 0.2#重力系数
CORIOLIS_FACTOR = 0.0005  # 地转偏向力系数
# 导弹设置
GUIDANCE_STRENGTH = 0.05#制导强度系数
MISSILE_SPEED = 10#导弹速度
# random.uniform(10, 12)
MAX_TURE_RATE_MISSILE = 20
SLEEP_TIME_MISSILE = 800 ##可在游戏运行中修改
# 拦截弹速度设置
INTERCEPTOR_SPEED = 40
MAX_TURE_RATE_INTERCEPTOR = 1#最大转向角度
# 发射器和目标位置
LAUNCHER_POS = (WIDTH//4, HEIGHT - 50)
TARGET_POS = (3*WIDTH//4, HEIGHT - 100)
DEFENSE_POS = (3*WIDTH//4, HEIGHT - 400)

# 环境参数更新间隔（毫秒）
ENVIRONMENT_UPDATE_INTERVAL = 5000

# 组合发射配置
COMBO_LAUNCH = {
    "guided": 1,    # 制导导弹数量
    "real": 2,      # 普通弹数量
    "decoy": 7      # 诱饵弹数量
}
COMBO_LAUNCH_COOLDOWN = 3000  # 组合发射冷却时间（毫秒）