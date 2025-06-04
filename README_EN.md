# Defense Game

This game is developed in Python and features various interception and missile launch modes.

## Usage Instructions
Run the main.py file directly. The environment requires Python 3.12.7.

Install the `numpy` and `pygame` libraries using the package manager pip or conda:

```bash
pip install numpy
pip install pygame
conda install numpy
conda install pygame
```
| key | Function     |  Description                                                                 |  
|------|----------------|--------------------------------------------------------------------------|  
| A    | Guided Missile         | Precision-guided missile capable of automatically tracking high-speed targets with high accuracy.                 |  
| S    | Standard Missile        | Basic interceptor with good cost-effectiveness, suitable for medium-threat targets.                           |  
| D    | Decoy Missile         | Interference decoy that alters enemy missile trajectories, creating secondary interception opportunities.                 |  
| X    | Interception Mode       | Toggle between manual/automatic modes: manual requires precise operations, while automatic enables intelligent interception.
| F    | Defense Toggle       | Disable interception system for testing missile impact effects (debugging/drills).                |

| Mouse Button | Function      | Description Description                                                                 |  
|------|----------------|--------------------------------------------------------------------------| 
| Left-click  | Mark Missile       | Left-click on the yellow predicted trajectory of a missile to place a yellow marker (indicates successful marking).               |  
| Right-click    | Launch Interceptor           | After marking a target, quickly right-click to launch the interceptor missile.

# Configuration Files
## config.py
Global Settings
```python
import pygame
import random
import numpy as np

# Window dimensions
WIDTH, HEIGHT = 1200, 800

# Color definitions
BACKGROUND = (10, 20, 40)
GRID_COLOR = (40, 60, 80)
LAUNCHER_COLOR = (0, 150, 255)
TARGET_COLOR = (255, 50, 50)
INTERCEPTOR_COLOR = (50, 255, 150)
TEXT_COLOR = (200, 220, 255)
PREDICTION_COLOR = (255, 200, 50)
REAL_MISSILE_COLOR = (255, 50, 50)    # Real missile (high hit probability)
DECOY_MISSILE_COLOR = (255, 150, 50)  # Decoy missile (low hit probability)
HIT_COLOR = (255, 255, 0)             # Impact effect color

# Physical parameters
GRAVITY = 0.2          # Gravity coefficient
CORIOLIS_FACTOR = 0.0005  # Coriolis force coefficient

# Missile settings
GUIDANCE_STRENGTH = 0.05  # Guidance accuracy coefficient
MISSILE_SPEED = 10        # Base missile speed
MAX_TURN_RATE_MISSILE = 20
SLEEP_TIME_MISSILE = 800  # Missile spawn interval (ms)

# Interceptor settings
INTERCEPTOR_SPEED = 40
MAX_TURN_RATE_INTERCEPTOR = 1  # Max turning angle (degrees)

# Positions
LAUNCHER_POS = (WIDTH // 4, HEIGHT - 50)
TARGET_POS = (3 * WIDTH // 4, HEIGHT - 100)
DEFENSE_POS = (3 * WIDTH // 4, HEIGHT - 400)

# Environment update interval (ms)
ENVIRONMENT_UPDATE_INTERVAL = 5000

# Cluster launch configuration
COMBO_LAUNCH = {
    "guided": 1,    # Guided missiles per cluster
    "real": 2,      # Standard missiles per cluster
    "decoy": 7      # Decoy missiles per cluster
}
COMBO_LAUNCH_COOLDOWN = 3000  # Cluster launch cooldown (ms)
```
## missile.py
Missile Logic

```python
    self.guidance_start_time = 0          # Modify guidance activation time
    self.guidance_delay = random.randint(6000, 7000)  # Guidance system delay (ms)
```
```python
    if is_real:
        # Real missile: higher accuracy, fixed speed
        angle = random.uniform(50, 60)      # Narrow angle range
        speed = MISSILE_SPEED               # Speed from config
    else:
        # Decoy missile: random angle & speed
        angle = random.uniform(35, 60)      # Wide angle range
        speed = random.uniform(6, 16)       # Variable speed
        
    # Wind influence simulation
    wind_force = np.array([
        wind_x * 1,
        wind_y * 1
    ])
```

## defense_system.py
Defense Logic
```python
    self.launch_cooldown = 500  #Reset cooldown
```
## interceptor.py
Interceptor Missile
## environment.py
Environmental Factors
## draw_utils.py
Rendering Utilities
## interceptor.py
Interceptor Missile
# Contact
If you have any question, please contact w2502754035@gmail.com.
Thank you for your attention!