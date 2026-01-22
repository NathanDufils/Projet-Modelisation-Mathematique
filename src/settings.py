# Paramètres physiques
GRAVITY = 9.81  # m/s^2
AIR_DENSITY = 1.225  # kg/m^3 (au niveau de la mer)
DRAG_COEFFICIENT = 0.47  # Coefficient de traînée pour une sphère
WIND_SPEED = 0.0  # m/s (vitesse du vent)
WIND_DIRECTION = 0.0  # degrés (0° = droite, 90° = haut, 180° = gauche, 270° = bas)

# Fenêtre
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800

# Layout - Marges et espacements
MARGIN = 15           # Marge extérieure
PADDING = 15          # Espacement interne des panneaux
SPACING = 10          # Espacement entre éléments

# Panneaux de contrôle
PANEL_WIDTH = 280     # Largeur fixe des panneaux

# Positions calculées des panneaux
SIMULATION_PANEL_X = MARGIN
SIMULATION_PANEL_Y = MARGIN
SIMULATION_PANEL_WIDTH = PANEL_WIDTH
# Hauteur = moitié de l'espace disponible
SIMULATION_PANEL_HEIGHT = (SCREEN_HEIGHT - 3 * MARGIN) // 2

OBJECT_PANEL_X = MARGIN
OBJECT_PANEL_Y = SIMULATION_PANEL_Y + SIMULATION_PANEL_HEIGHT + MARGIN
OBJECT_PANEL_WIDTH = PANEL_WIDTH
OBJECT_PANEL_HEIGHT = SCREEN_HEIGHT - OBJECT_PANEL_Y - MARGIN

# Zone de simulation (exclut les panneaux UI)
SIM_AREA_X = PANEL_WIDTH + 2 * MARGIN
SIM_AREA_Y = MARGIN
SIM_AREA_WIDTH = SCREEN_WIDTH - SIM_AREA_X - MARGIN
SIM_AREA_HEIGHT = SCREEN_HEIGHT - 2 * MARGIN

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
