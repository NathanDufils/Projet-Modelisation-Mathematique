import math
from src.settings import GRAVITY

def calculate_trajectory_point(x0, y0, v0, angle, t, mass, drag_coefficient):
    """
    Calcule la position et la vitesse d'un projectile à un temps donné.
    Utilise l'intégration numérique pour la résistance de l'air si drag_coefficient > 0.
    """
    if drag_coefficient == 0:
        # Trajectoire parabolique simple sans résistance de l'air
        x = x0 + v0 * math.cos(angle) * t
        y = y0 - v0 * math.sin(angle) * t + 0.5 * GRAVITY * t**2
        
        vx = v0 * math.cos(angle)
        vy = -v0 * math.sin(angle) + GRAVITY * t
        
        return x, y, vx, vy
    else:
        # Intégration numérique avec résistance de l'air
        dt = 0.01  # Pas de temps pour l'intégration
        x, y = x0, y0
        vx = v0 * math.cos(angle)
        vy = -v0 * math.sin(angle)
        
        current_time = 0
        while current_time < t:
            # Calculer la force de traînée (F = k * v²)
            speed = math.sqrt(vx**2 + vy**2)
            if speed > 0:
                # Coefficient de traînée normalisé
                drag_force = drag_coefficient * speed**2
                # Accélération due à la traînée (F = ma, donc a = F/m)
                drag_ax = -drag_force * (vx / speed) / mass
                drag_ay = -drag_force * (vy / speed) / mass
            else:
                drag_ax = drag_ay = 0
            
            # Mettre à jour les vitesses (avec gravité et traînée)
            vx += drag_ax * dt
            vy += (GRAVITY + drag_ay) * dt
            
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