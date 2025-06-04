# 反导小游戏

本游戏为python开发，拥有多种拦截与导弹发射模式

## 使用说明
直接运行 `main.py` 

环境为3.12.7

使用包管理器 pip 安装或者 conda 安装  `numpy`  `pygame` 库
```bash
pip install numpy
pip install pygame
conda install numpy
conda install pygame
```
| 按键 | 武器类型       | 功能描述                                                                 |  
|------|----------------|--------------------------------------------------------------------------|  
| A    | 制导弹         | 精确制导导弹，可自动追踪高速或高价值目标，拦截精度高                   |  
| S    | 普通弹         | 基础拦截导弹，性价比高，适合应对中等威胁目标                           |  
| D    | 诱惑弹         | 干扰诱饵弹，可改变敌方导弹飞行轨迹，创造二次拦截窗口                   |  
| X    | 拦截模式切换       | 手动/自动拦截模式切换：手动模式下需玩家精准操作，自动模式可智能拦截     |  
| F    | 防御开关       | 关闭拦截系统，用于测试导弹命中效果（调试或战术演练）                   |  
| 空格  | 集群发射       | 一次性发射多枚同类型导弹，发射数量可在`config.py`中配置                |  
| R    | 重启           | 重新开始游戏                                                     |

| 鼠标 | 功能      | 详细介绍                                                                |  
|------|----------------|--------------------------------------------------------------------------| 
| 鼠标左键  | 标记导弹       | 鼠标左键点击导弹预测的黄色轨迹，会生成一个黄色短点证明标记成功                |  
| 鼠标右键    | 发射拦截导弹           | 标记之后迅速点击右键可以发射拦截导弹  |
# 主要文件
## config.py
可修改多种配置信息
```python
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
```
## missile.py
可以配置导弹信息

```python
    self.guidance_start_time = 0  # 可以修改制导开始时间
    self.guidance_delay = random.randint(6000, 7000)  # 可以修改制导系统启动延迟
```
```python
    if is_real:
        # 真弹有更高的概率直接飞向目标
        angle = random.uniform(50, 60)  # 较小的角度范围
        speed = MISSILE_SPEED   # 真弹速度在config文件
    else:
        # 假弹有更大的角度变化和较低的速度
        angle = random.uniform(35, 60)  # 较大的角度范围
        speed = random.uniform(6, 16)   # 较低的速度
    # 风力影响
    wind_force = np.array([
        wind_x * 1,
        wind_y * 1
    ])
```

## defense_system.py
存放拦截数据
```python
    self.launch_cooldown = 500  # 修改拦截冷却时间
```
## interceptor.py
拦截导弹信息
## environment.py
环境因素
## draw_utils.py
游戏绘制
## interceptor.py
拦截导弹信息
## 联系
如果你遇到任何问题，请联系 w2502754035@gmail.com 感谢你的关注。
