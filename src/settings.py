# Paramètres physiques
GRAVITY = 9.81  # m/s^2
AIR_DENSITY = 1.225  # kg/m^3 (au niveau de la mer)
DRAG_COEFFICIENT = 0.47  # Coefficient de traînée pour une sphère

# Fenêtre
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 700

# Panneaux de contrôle
SIMULATION_PANEL_X = 20
SIMULATION_PANEL_Y = 20
SIMULATION_PANEL_WIDTH = 280
SIMULATION_PANEL_HEIGHT = 300

OBJECT_PANEL_X = 20
OBJECT_PANEL_Y = 340
OBJECT_PANEL_WIDTH = 280
OBJECT_PANEL_HEIGHT = 340

# Zone de simulation (exclut les panneaux UI)
SIM_AREA_X = 320
SIM_AREA_Y = 20
SIM_AREA_WIDTH = SCREEN_WIDTH - SIM_AREA_X - 20
SIM_AREA_HEIGHT = SCREEN_HEIGHT - 40

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (64, 64, 64)

# Simulation
FPS = 60
TIME_STEP = 0.016  # 1/60 seconde

# Échelle de conversion (pixels par mètre)
SCALE = 2.0  # 2 pixels = 1 mètre

# Position de départ du projectile
START_X = SIM_AREA_X + 50
START_Y = SIM_AREA_Y + SIM_AREA_HEIGHT - 50
