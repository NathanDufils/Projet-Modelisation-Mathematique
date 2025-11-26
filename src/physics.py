import math
from src.settings import GRAVITY, AIR_DENSITY, DRAG_COEFFICIENT

def calculate_trajectory_point(x0, y0, v0, angle, t, mass, radius, gravity=GRAVITY, air_density=AIR_DENSITY, wind_speed=0.0, wind_direction=0.0):
    """
    Calcule la position et la vitesse d'un projectile à un temps donné.
    Utilise l'intégration numérique avec résistance de l'air si radius > 0.
    
    La force de traînée est calculée avec: F_drag = 0.5 * ρ * C_d * A * v_rel²
    où ρ = densité de l'air, C_d = coefficient de traînée, A = surface frontale,
    et v_rel est la vitesse relative du projectile par rapport à l'air (incluant le vent)
    
    Args:
        x0, y0: Position initiale
        v0: Vitesse initiale
        angle: Angle de lancement (radians)
        t: Temps écoulé
        mass: Masse du projectile
        radius: Rayon du projectile
        gravity: Accélération de la pesanteur (défaut: GRAVITY)
        air_density: Densité de l'air (défaut: AIR_DENSITY)
        wind_speed: Vitesse du vent en m/s (défaut: 0.0)
        wind_direction: Direction du vent en degrés, 0°=droite, 90°=haut, 180°=gauche, 270°=bas (défaut: 0.0)
    """
    if radius == 0:
        # Trajectoire parabolique simple sans résistance de l'air
        x = x0 + v0 * math.cos(angle) * t
        y = y0 - v0 * math.sin(angle) * t + 0.5 * gravity * t**2
        
        vx = v0 * math.cos(angle)
        vy = -v0 * math.sin(angle) + gravity * t
        
        return x, y, vx, vy
    else:
        # Intégration numérique avec résistance de l'air
        dt = 0.01  # Pas de temps pour l'intégration
        x, y = x0, y0
        vx = v0 * math.cos(angle)
        vy = -v0 * math.sin(angle)
        
        # Calcul des composantes du vent
        # Direction: 0° = droite (+x), 90° = haut (-y), 180° = gauche (-x), 270° = bas (+y)
        wind_angle_rad = math.radians(wind_direction)
        vx_wind = wind_speed * math.cos(wind_angle_rad)
        vy_wind = -wind_speed * math.sin(wind_angle_rad)  # Négatif car y augmente vers le bas
        
        # Calcul de la surface frontale (aire d'un cercle)
        cross_section_area = math.pi * radius**2
        
        # Constante de traînée: k = 0.5 * ρ * C_d * A
        drag_constant = 0.5 * air_density * DRAG_COEFFICIENT * cross_section_area
        
        current_time = 0
        max_speed = 10000  # Vitesse maximale pour éviter les overflow (10 km/s)
        
        while current_time < t:
            # Limiter les vitesses pour éviter les overflow
            vx = max(-max_speed, min(max_speed, vx))
            vy = max(-max_speed, min(max_speed, vy))
            
            # Calculer la vitesse relative du projectile par rapport à l'air
            vx_rel = vx - vx_wind
            vy_rel = vy - vy_wind
            
            # Calculer la vitesse relative avec protection contre overflow
            speed_sq = vx_rel**2 + vy_rel**2
            if speed_sq > max_speed**2:
                # Si la vitesse dépasse la limite, on arrête l'intégration
                break
            speed_rel = math.sqrt(speed_sq)
            
            if speed_rel > 0:
                # Force de traînée basée sur la vitesse relative
                drag_force = drag_constant * speed_rel**2
                # Accélération due à la traînée (F = ma, donc a = F/m)
                # La traînée s'oppose à la vitesse relative
                drag_ax = -drag_force * (vx_rel / speed_rel) / mass
                drag_ay = -drag_force * (vy_rel / speed_rel) / mass
                
                # Limiter l'accélération pour éviter l'instabilité numérique
                max_accel = 1000  # m/s² maximum
                drag_ax = max(-max_accel, min(max_accel, drag_ax))
                drag_ay = max(-max_accel, min(max_accel, drag_ay))
            else:
                drag_ax = drag_ay = 0
            
            # Mettre à jour les vitesses (avec gravité et traînée)
            vx += drag_ax * dt
            vy += (gravity + drag_ay) * dt
            
            # Mettre à jour les positions
            x += vx * dt
            y += vy * dt
            
            current_time += dt
        
        return x, y, vx, vy

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