import pygame
import math
from src.settings import *
from src.physics import calculate_trajectory_point

class Projectile:
    def __init__(self, x0, y0, v0=50, angle=45, mass=1.0, radius=0.1, color=RED):
        # Paramètres initiaux (immuables une fois le tir lancé)
        self.x0 = x0
        self.y0 = y0
        self.v0 = v0
        self.angle_degrees = angle
        self.angle = math.radians(angle)
        self.mass = mass
        self.radius = radius
        
        # État actuel
        self.x = x0
        self.y = y0
        self.vx = v0 * math.cos(self.angle)
        self.vy = -v0 * math.sin(self.angle)
        
        # Simulation
        self.time = 0
        self.trajectory = [(x0, y0)]
        self.active = True
        self.launched = False  # Indique si le projectile a été lancé
        self.paused = False
        
        # Apparence
        self.color = color
        self.selected = False
        
    def launch(self):
        """Lance le projectile avec ses paramètres actuels."""
        self.launched = True
        self.trajectory = [(self.x0, self.y0)]
        self.time = 0
        self.x = self.x0
        self.y = self.y0
        self.vx = self.v0 * math.cos(self.angle)
        self.vy = -self.v0 * math.sin(self.angle)
        self.active = True
        
    def update(self, dt, gravity=GRAVITY, air_density=AIR_DENSITY, wind_speed=0.0, wind_direction=0.0):
        """Met à jour la position du projectile si il est lancé et pas en pause.
        
        Args:
            dt: Pas de temps
            gravity: Accélération de la pesanteur
            air_density: Densité de l'air
            wind_speed: Vitesse du vent en m/s
            wind_direction: Direction du vent en degrés
        """
        if not self.active or not self.launched or self.paused:
            return
            
        self.time += dt
        
        try:
            new_x, new_y, new_vx, new_vy = calculate_trajectory_point(
                self.x0, self.y0, self.v0, self.angle, 
                self.time, self.mass, self.radius,
                gravity, air_density, wind_speed, wind_direction
            )
            
            # Vérifier que les valeurs sont valides
            if math.isnan(new_x) or math.isnan(new_y) or math.isinf(new_x) or math.isinf(new_y):
                self.active = False
                return
            
            self.x = new_x
            self.y = new_y
            self.vx = new_vx
            self.vy = new_vy
            
            self.trajectory.append((self.x, self.y))
            
        except (OverflowError, ValueError):
            # En cas d'erreur de calcul, arrêter le projectile
            self.active = False
            return
        
        # Vérifier les limites
        if self.y >= SIM_AREA_Y + SIM_AREA_HEIGHT - 10 or self.x >= SIM_AREA_X + SIM_AREA_WIDTH:
            self.active = False
    
    def pause(self):
        """Met en pause ou reprend le projectile."""
        self.paused = not self.paused
        
    def reset(self):
        """Remet le projectile à sa position initiale."""
        self.x = self.x0
        self.y = self.y0
        self.time = 0
        self.trajectory = [(self.x0, self.y0)]
        self.active = True
        self.launched = False
        self.paused = False
            
    def set_position(self, x, y):
        """Déplace le projectile à une nouvelle position (seulement si pas lancé)."""
        if not self.launched:
            self.x0 = x
            self.y0 = y
            self.x = x
            self.y = y
            self.trajectory = [(x, y)]
    
    def set_parameters(self, v0=None, angle=None, mass=None, radius=None):
        """Modifie les paramètres du projectile (seulement si pas lancé)."""
        if not self.launched:
            if v0 is not None:
                self.v0 = v0
            if angle is not None:
                self.angle_degrees = angle
                self.angle = math.radians(angle)
            if mass is not None:
                self.mass = mass
            if radius is not None:
                self.radius = radius
                
            # Recalculer les vitesses initiales
            self.vx = self.v0 * math.cos(self.angle)
            self.vy = -self.v0 * math.sin(self.angle)
    
    def is_at_position(self, x, y, tolerance=20):
        """Vérifie si un point est proche du projectile."""
        return math.sqrt((self.x - x)**2 + (self.y - y)**2) <= tolerance
    
    def draw(self, screen):
        """Dessine le projectile et sa trajectoire."""
        # Dessiner la trajectoire si lancé
        if self.launched and len(self.trajectory) > 1:
            # Filtrer les points dans la zone de simulation
            sim_trajectory = []
            for tx, ty in self.trajectory:
                if (SIM_AREA_X <= tx <= SIM_AREA_X + SIM_AREA_WIDTH and 
                    SIM_AREA_Y <= ty <= SIM_AREA_Y + SIM_AREA_HEIGHT):
                    sim_trajectory.append((tx, ty))
            
            if len(sim_trajectory) > 1:
                pygame.draw.lines(screen, BLUE, False, sim_trajectory, 2)
        
        # Dessiner le projectile
        if self.active and (SIM_AREA_X <= self.x <= SIM_AREA_X + SIM_AREA_WIDTH and
                           SIM_AREA_Y <= self.y <= SIM_AREA_Y + SIM_AREA_HEIGHT):
            # Calculer le rayon d'affichage en pixels (rayon physique * échelle * facteur d'agrandissement)
            display_radius = int(self.radius * SCALE * 10)
            # Limiter le rayon d'affichage entre 5 et 50 pixels pour la visibilité
            display_radius = max(5, min(50, display_radius))
            
            # Couleur différente si sélectionné
            color = GREEN if self.selected else self.color
            pygame.draw.circle(screen, color, (int(self.x), int(self.y)), display_radius)
            
            # Bordure si sélectionné
            if self.selected:
                pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), display_radius + 2, 2)
        
        # Dessiner les indicateurs si pas lancé ou en pause
        if not self.launched or self.paused:
            self.draw_indicators(screen)
    
    def draw_indicators(self, screen):
        """Dessine les indicateurs d'angle et de vitesse."""
        # Arc pour l'angle
        arc_radius = 30
        pygame.draw.arc(screen, DARK_GRAY,
                      (self.x - arc_radius, self.y - arc_radius,
                       arc_radius * 2, arc_radius * 2),
                      0, self.angle, 2)
        
        # Ligne de référence horizontale
        pygame.draw.line(screen, LIGHT_GRAY,
                        (self.x, self.y),
                        (self.x + 30, self.y), 1)
        
        # Vecteur de vitesse
        vel_scale = 2
        vel_length = self.v0 * vel_scale
        end_x = self.x + vel_length * math.cos(self.angle)
        end_y = self.y - vel_length * math.sin(self.angle)
        
        pygame.draw.line(screen, GREEN,
                        (int(self.x), int(self.y)),
                        (int(end_x), int(end_y)), 3)
        
        # Pointe de flèche
        arrow_length = 10
        arrow_angle = 0.4
        arrow_x1 = end_x - arrow_length * math.cos(self.angle - arrow_angle)
        arrow_y1 = end_y + arrow_length * math.sin(self.angle - arrow_angle)
        arrow_x2 = end_x - arrow_length * math.cos(self.angle + arrow_angle)
        arrow_y2 = end_y + arrow_length * math.sin(self.angle + arrow_angle)
        
        pygame.draw.line(screen, GREEN, (int(end_x), int(end_y)), (int(arrow_x1), int(arrow_y1)), 2)
        pygame.draw.line(screen, GREEN, (int(end_x), int(end_y)), (int(arrow_x2), int(arrow_y2)), 2)