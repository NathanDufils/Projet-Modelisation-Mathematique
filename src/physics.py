import math
from src.settings import GRAVITY, AIR_DENSITY, DRAG_COEFFICIENT

def update_physics_step(x, y, vx, vy, dt, mass, radius, gravity=GRAVITY, air_density=AIR_DENSITY, wind_speed=0.0, wind_direction=0.0):
    """
    Calcule la nouvelle position et vitesse après un pas de temps dt.
    Utilise l'intégration d'Euler semi-implicite.
    
    Args:
        x, y: Position actuelle
        vx, vy: Vitesse actuelle
        dt: Pas de temps
        mass: Masse du projectile
        radius: Rayon du projectile (si 0, pas de traînée)
        gravity: Accélération de la pesanteur
        air_density: Densité de l'air
        wind_speed: Vitesse du vent
        wind_direction: Direction du vent
    """
    # Forces initiales (gravité)
    fx = 0
    fy = mass * gravity
    
    # Ajout de la traînée de l'air si applicable
    if radius > 0 and air_density > 0:
        # Calcul des composantes du vent
        wind_angle_rad = math.radians(wind_direction)
        vx_wind = wind_speed * math.cos(wind_angle_rad)
        vy_wind = -wind_speed * math.sin(wind_angle_rad)
        
        # Vitesse relative par rapport à l'air
        vx_rel = vx - vx_wind
        vy_rel = vy - vy_wind
        v_rel_sq = vx_rel**2 + vy_rel**2
        v_rel = math.sqrt(v_rel_sq)
        
        if v_rel > 0:
            area = math.pi * radius**2
            drag_force = 0.5 * air_density * DRAG_COEFFICIENT * area * v_rel_sq
            
            # La traînée s'oppose à la vitesse relative
            fx -= drag_force * (vx_rel / v_rel)
            fy -= drag_force * (vy_rel / v_rel)
    
    # Accélération (F = ma => a = F/m)
    ax = fx / mass
    ay = fy / mass
    
    # Intégration (Euler semi-implicite: v_new = v + a*dt, x_new = x + v_new*dt)
    # Plus stable que Euler explicite pour les systèmes conservatifs
    new_vx = vx + ax * dt
    new_vy = vy + ay * dt
    
    new_x = x + new_vx * dt
    new_y = y + new_vy * dt
    
    return new_x, new_y, new_vx, new_vy

def calculate_range(v0, angle, height=0):
    """Calcule la portée théorique d'un projectile."""
    return (v0 * v0 * math.sin(2 * angle)) / GRAVITY + height

def calculate_max_height(v0, angle, y0=0):
    """Calcule la hauteur maximale d'un projectile."""
    vy0 = v0 * math.sin(angle)
    return y0 - (vy0 * vy0) / (2 * GRAVITY)

def calculate_flight_time(v0, angle, y0=0):
    """Calcule le temps de vol d'un projectile."""
    vy0 = -v0 * math.sin(angle)
    discriminant = vy0 * vy0 + 2 * GRAVITY * y0
    if discriminant < 0:
        return 0
    return (-vy0 + math.sqrt(discriminant)) / GRAVITY