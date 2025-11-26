import pygame
import math
from src.settings import *

class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, initial_val, label):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.val = initial_val
        self.label = label
        self.dragging = False
        self.enabled = True  # Nouveau: état d'activation du slider
        
        self.handle_radius = height // 2
        self.handle_x = self._value_to_x(initial_val)
        
        self.font = pygame.font.Font(None, 24)
        
    def _value_to_x(self, value):
        ratio = (value - self.min_val) / (self.max_val - self.min_val)
        return self.rect.x + ratio * self.rect.width
        
    def _x_to_value(self, x):
        ratio = (x - self.rect.x) / self.rect.width
        ratio = max(0, min(1, ratio))
        return self.min_val + ratio * (self.max_val - self.min_val)
    
    def handle_event(self, event):
        if not self.enabled:
            return  # Ignorer tous les événements si le slider est désactivé
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            handle_rect = pygame.Rect(
                self.handle_x - self.handle_radius,
                self.rect.y,
                self.handle_radius * 2,
                self.rect.height
            )
            if handle_rect.collidepoint(mouse_x, mouse_y):
                self.dragging = True
                
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
            
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mouse_x, mouse_y = event.pos
            self.handle_x = max(self.rect.x, min(self.rect.x + self.rect.width, mouse_x))
            self.val = self._x_to_value(self.handle_x)
    
    def draw(self, screen):
        # Couleurs en fonction de l'état
        if self.enabled:
            bar_color = (200, 200, 200)
            handle_color = BLUE
            border_color = BLACK
            text_color = BLACK
        else:
            bar_color = (230, 230, 230)
            handle_color = GRAY
            border_color = LIGHT_GRAY
            text_color = GRAY
        
        # Dessiner la barre du slider
        pygame.draw.rect(screen, bar_color, self.rect)
        pygame.draw.rect(screen, border_color, self.rect, 2)
        
        # Dessiner le handle
        pygame.draw.circle(screen, handle_color, (int(self.handle_x), self.rect.centery), self.handle_radius)
        pygame.draw.circle(screen, border_color, (int(self.handle_x), self.rect.centery), self.handle_radius, 2)
        
        # Dessiner le label et la valeur
        label_text = self.font.render(f"{self.label}: {self.val:.1f}", True, text_color)
        screen.blit(label_text, (self.rect.x, self.rect.y - 25))

class RadiusSlider(Slider):
    """Slider spécialisé pour le rayon qui affiche en cm mais retourne en mètres."""
    def __init__(self, x, y, width, height, min_cm, max_cm, initial_cm, label):
        # Convertir cm en m pour le stockage interne
        super().__init__(x, y, width, height, min_cm, max_cm, initial_cm, label)
    
    def draw(self, screen):
        # Couleurs en fonction de l'état
        if self.enabled:
            bar_color = (200, 200, 200)
            handle_color = BLUE
            border_color = BLACK
            text_color = BLACK
        else:
            bar_color = (230, 230, 230)
            handle_color = GRAY
            border_color = LIGHT_GRAY
            text_color = GRAY
        
        # Dessiner la barre du slider
        pygame.draw.rect(screen, bar_color, self.rect)
        pygame.draw.rect(screen, border_color, self.rect, 2)
        
        # Dessiner le handle
        pygame.draw.circle(screen, handle_color, (int(self.handle_x), self.rect.centery), self.handle_radius)
        pygame.draw.circle(screen, border_color, (int(self.handle_x), self.rect.centery), self.handle_radius, 2)
        
        # Dessiner le label et la valeur en cm
        label_text = self.font.render(f"{self.label}: {self.val:.1f}", True, text_color)
        screen.blit(label_text, (self.rect.x, self.rect.y - 25))
    
    def get_value_in_meters(self):
        """Retourne la valeur en mètres."""
        return self.val / 100.0

class Button:
    def __init__(self, x, y, width, height, text, color=(200, 200, 200)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.font = pygame.font.Font(None, 24)
        self.clicked = False
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.clicked = True
                return True
        return False
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

class Compass:
    def __init__(self, x, y, radius, initial_angle):
        self.center_x = x
        self.center_y = y
        self.radius = radius
        self.angle = initial_angle
        self.dragging = False
        self.enabled = True
        
    def handle_event(self, event):
        if not self.enabled:
            return False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            dist = math.sqrt((mouse_x - self.center_x)**2 + (mouse_y - self.center_y)**2)
            if dist <= self.radius:
                self.dragging = True
                self._update_angle(mouse_x, mouse_y)
                return True
                
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
            
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mouse_x, mouse_y = event.pos
            self._update_angle(mouse_x, mouse_y)
            return True
            
        return False
    
    def _update_angle(self, mouse_x, mouse_y):
        dx = mouse_x - self.center_x
        dy = self.center_y - mouse_y  # Y inversé en écran
        
        # Calculer l'angle en degrés (0 = Est/Droite, 90 = Nord/Haut)
        angle = math.degrees(math.atan2(dy, dx))
        if angle < 0:
            angle += 360
        self.angle = angle
        
    def set_angle(self, angle):
        self.angle = angle
        
    def draw(self, screen):
        # Dessiner le fond du compas
        pygame.draw.circle(screen, WHITE, (self.center_x, self.center_y), self.radius)
        pygame.draw.circle(screen, BLACK, (self.center_x, self.center_y), self.radius, 2)
            
        # Dessiner l'aiguille
        rad = math.radians(self.angle)
        end_x = self.center_x + (self.radius - 5) * math.cos(rad)
        end_y = self.center_y - (self.radius - 5) * math.sin(rad)
        
        # Couleur selon activation
        color = RED if self.enabled else GRAY
        
        pygame.draw.line(screen, color, (self.center_x, self.center_y), (end_x, end_y), 3)
        pygame.draw.circle(screen, color, (self.center_x, self.center_y), 4)

class SimulationPanel:
    """Panneau de contrôle pour les paramètres d'environnement de la simulation."""
    def __init__(self):
        self.x = SIMULATION_PANEL_X
        self.y = SIMULATION_PANEL_Y
        self.width = SIMULATION_PANEL_WIDTH
        self.height = SIMULATION_PANEL_HEIGHT
        
        # Sliders pour les paramètres d'environnement
        self.sliders = {
            'gravity': Slider(self.x + 15, self.y + 70, 200, 20, 0.1, 20.0, GRAVITY, "Gravité (m/s²)"),
            'air_density': Slider(self.x + 15, self.y + 130, 200, 20, 0.0, 2.0, AIR_DENSITY, "Densité air (kg/m³)"),
            'wind_speed': Slider(self.x + 15, self.y + 190, 200, 20, 0.0, 50.0, WIND_SPEED, "Vent vitesse (m/s)")
        }
        
        # Boutons de contrôle de la simulation
        self.buttons = {
            'add_object': Button(self.x + 15, self.y + 240, 110, 30, "Ajouter"),
            'launch_pause': Button(self.x + 135, self.y + 240, 110, 30, "Lancer"),
            'reset': Button(self.x + 15, self.y + 280, 110, 30, "Réinitialiser"),
            'clear': Button(self.x + 135, self.y + 280, 110, 30, "Effacer")
        }
        
        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 28)
        self.simulation_running = False
    
    def handle_event(self, event):
        """Gère les événements pour ce panneau."""
        for slider in self.sliders.values():
            slider.handle_event(event)
        
        for name, button in self.buttons.items():
            if button.handle_event(event):
                return name
        return None
    
    def draw(self, screen):
        """Dessine le panneau de simulation."""
        # Fond du panneau
        panel_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, (240, 240, 250), panel_rect)
        pygame.draw.rect(screen, BLACK, panel_rect, 3)
        
        # Titre
        title = self.title_font.render("Environnement", True, BLACK)
        screen.blit(title, (self.x + 10, self.y + 10))
        
        # Message si les sliders sont désactivés
        if not self.sliders['gravity'].enabled:
            info_text = self.font.render("Verrouillé pendant le vol", True, GRAY)
            screen.blit(info_text, (self.x + 10, self.y + 40))
        
        # Sliders
        for slider in self.sliders.values():
            slider.draw(screen)
        
        # Boutons
        for button in self.buttons.values():
            button.draw(screen)
    
    def get_environment_parameters(self):
        """Retourne les paramètres d'environnement."""
        return {
            'gravity': self.sliders['gravity'].val,
            'air_density': self.sliders['air_density'].val,
            'wind_speed': self.sliders['wind_speed'].val
        }
    
    def update_launch_pause_button(self, has_objects, any_launched):
        """Met à jour le texte du bouton lancer/pause."""
        if not has_objects:
            self.buttons['launch_pause'].text = "Lancer"
            self.simulation_running = False
        elif any_launched and self.simulation_running:
            self.buttons['launch_pause'].text = "Pause"
        else:
            self.buttons['launch_pause'].text = "Lancer"
    
    def set_sliders_enabled(self, enabled):
        """Active ou désactive tous les sliders du panneau."""
        for slider in self.sliders.values():
            slider.enabled = enabled


class ObjectPanel:
    """Panneau de contrôle pour les paramètres d'un objet sélectionné."""
    def __init__(self):
        self.x = OBJECT_PANEL_X
        self.y = OBJECT_PANEL_Y
        self.width = OBJECT_PANEL_WIDTH
        self.height = OBJECT_PANEL_HEIGHT
        
        # Sliders pour les paramètres de l'objet
        self.sliders = {
            'velocity': Slider(self.x + 15, self.y + 90, 200, 20, 0, 500, 80, "Vitesse (m/s)"),
            'angle': Slider(self.x + 15, self.y + 150, 200, 20, 0, 360, 45, "Angle (°)"),
            'mass': Slider(self.x + 15, self.y + 210, 200, 20, 0.001, 100, 1.0, "Masse (kg)"),
            'radius': RadiusSlider(self.x + 15, self.y + 270, 200, 20, 1.0, 100.0, 10.0, "Rayon (cm)")
        }
        
        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 20)
        self.selected_projectile = None
    
    def set_selected_projectile(self, projectile):
        """Définit le projectile sélectionné et met à jour les sliders."""
        self.selected_projectile = projectile
        if projectile:
            self.sliders['velocity'].val = projectile.v0
            self.sliders['velocity'].handle_x = self.sliders['velocity']._value_to_x(projectile.v0)
            
            self.sliders['angle'].val = projectile.angle_degrees
            self.sliders['angle'].handle_x = self.sliders['angle']._value_to_x(projectile.angle_degrees)
            
            self.sliders['mass'].val = projectile.mass
            self.sliders['mass'].handle_x = self.sliders['mass']._value_to_x(projectile.mass)
            
            # Convertir le rayon en cm
            radius_cm = projectile.radius * 100.0
            radius_cm = max(self.sliders['radius'].min_val, min(self.sliders['radius'].max_val, radius_cm))
            self.sliders['radius'].val = radius_cm
            self.sliders['radius'].handle_x = self.sliders['radius']._value_to_x(radius_cm)
    
    def handle_event(self, event):
        """Gère les événements pour ce panneau."""
        # Gérer les sliders seulement si un projectile est sélectionné
        if self.selected_projectile:
            for slider in self.sliders.values():
                slider.handle_event(event)
        return None
    
    def draw(self, screen):
        """Dessine le panneau d'objet."""
        # Fond du panneau
        panel_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, (250, 240, 240), panel_rect)
        pygame.draw.rect(screen, BLACK, panel_rect, 3)
        
        # Titre
        title = self.title_font.render("Objet sélectionné", True, BLACK)
        screen.blit(title, (self.x + 10, self.y + 10))
        
        # Afficher l'état de sélection
        if self.selected_projectile:
            status_text = self.small_font.render("Modifiez les paramètres", True, DARK_GRAY)
            screen.blit(status_text, (self.x + 10, self.y + 40))
            
            # Dessiner les sliders
            for slider in self.sliders.values():
                slider.draw(screen)
        else:
            status_text = self.small_font.render("Aucun objet sélectionné", True, GRAY)
            screen.blit(status_text, (self.x + 10, self.y + 40))
            
            # Dessiner les sliders grisés
            for slider in self.sliders.values():
                pygame.draw.rect(screen, LIGHT_GRAY, slider.rect)
                pygame.draw.rect(screen, GRAY, slider.rect, 2)
                label_text = slider.font.render(f"{slider.label}: --", True, GRAY)
                screen.blit(label_text, (slider.rect.x, slider.rect.y - 25))
    
    def get_object_parameters(self):
        """Retourne les paramètres de l'objet."""
        return {
            'v0': self.sliders['velocity'].val,
            'angle': self.sliders['angle'].val,
            'mass': self.sliders['mass'].val,
            'radius': self.sliders['radius'].get_value_in_meters()
        }
    
    def set_sliders_enabled(self, enabled):
        """Active ou désactive tous les sliders du panneau."""
        for slider in self.sliders.values():
            slider.enabled = enabled


class UI:
    """Classe principale gérant l'interface utilisateur complète."""
    def __init__(self):
        self.simulation_panel = SimulationPanel()
        self.object_panel = ObjectPanel()
        
        # Compas pour la direction du vent (en haut à droite de l'écran)
        # SCREEN_WIDTH = 1400, on le place à 1330, 70 pour plus de marge
        self.compass = Compass(1330, 70, 30, WIND_DIRECTION)
        
        # État de la simulation
        self.simulation_running = False
        
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 20)
        self.selected_projectile = None
        
    def set_selected_projectile(self, projectile):
        """Définit le projectile sélectionné et met à jour les sliders."""
        self.selected_projectile = projectile
        self.object_panel.set_selected_projectile(projectile)
    
    def update_launch_pause_button(self, has_projectiles, any_launched):
        """Met à jour le texte du bouton lancer/pause selon l'état de la simulation."""
        self.simulation_panel.update_launch_pause_button(has_projectiles, any_launched)
        self.simulation_running = self.simulation_panel.simulation_running
    
    def lock_parameters(self, lock):
        """Verrouille ou déverrouille les paramètres de l'environnement et de l'objet.
        
        Args:
            lock: True pour verrouiller, False pour déverrouiller
        """
        # Verrouiller les paramètres d'environnement
        self.simulation_panel.set_sliders_enabled(not lock)
        self.compass.enabled = not lock
        
        # Verrouiller les paramètres d'objet si un objet est sélectionné
        if self.selected_projectile:
            self.object_panel.set_sliders_enabled(not lock)
            
    def handle_event(self, event):
        """Gère les événements pour toute l'interface."""
        # Gérer les événements du panneau de simulation
        sim_action = self.simulation_panel.handle_event(event)
        if sim_action:
            if sim_action == 'launch_pause':
                self.simulation_running = not self.simulation_running
                self.simulation_panel.simulation_running = self.simulation_running
            return sim_action
            
        # Gérer les événements du compas
        self.compass.handle_event(event)
        
        # Gérer les événements du panneau d'objet
        self.object_panel.handle_event(event)
        
        return None
    
    def draw(self, screen):
        """Dessine toute l'interface utilisateur."""
        self.simulation_panel.draw(screen)
        self.object_panel.draw(screen)
        self.compass.draw(screen)
            
    def get_object_parameters(self):
        """Retourne les paramètres de l'objet sélectionné."""
        return self.object_panel.get_object_parameters()
    
    def get_environment_parameters(self):
        """Retourne les paramètres d'environnement."""
        params = self.simulation_panel.get_environment_parameters()
        params['wind_direction'] = self.compass.angle
        return params
    
    def draw_info(self, screen, projectiles):
        """Affiche des informations sur les projectiles en haut à gauche de la zone de simulation."""
        info_x = SIM_AREA_X + 10
        info_y = SIM_AREA_Y + 10
        
        if self.selected_projectile and self.selected_projectile in projectiles:
            proj = self.selected_projectile
            if proj.launched and proj.active:
                speed = math.sqrt(proj.vx**2 + proj.vy**2)
                info_texts = [
                    f"Position: ({proj.x:.1f}, {proj.y:.1f})",
                    f"Vitesse: {speed:.1f} m/s",
                    f"Temps: {proj.time:.2f} s"
                ]
            elif proj.launched and not proj.active:
                max_x = max([pos[0] for pos in proj.trajectory]) if proj.trajectory else 0
                info_texts = [
                    f"Portée: {max_x - proj.x0:.1f} m",
                    f"Temps de vol: {proj.time:.2f} s",
                    f"Trajectoire terminée"
                ]
            else:
                info_texts = [
                    f"Position: ({proj.x:.1f}, {proj.y:.1f})",
                    f"Vitesse: {proj.v0:.1f} m/s",
                    f"Angle: {proj.angle_degrees:.1f}°"
                ]
        else:
            info_texts = [
                f"Projectiles: {len(projectiles)}",
                f"Actifs: {sum(1 for p in projectiles if p.launched and p.active)}",
                "Cliquez pour sélectionner"
            ]
            
        for i, text in enumerate(info_texts):
            rendered = self.small_font.render(text, True, BLACK)
            screen.blit(rendered, (info_x, info_y + i * 20))