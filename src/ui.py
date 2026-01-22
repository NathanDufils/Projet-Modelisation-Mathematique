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
        
        # Dessiner la barre du slider (arrondie)
        pygame.draw.rect(screen, bar_color, self.rect, border_radius=5)
        pygame.draw.rect(screen, border_color, self.rect, 2, border_radius=5)
        
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
        
        # Dessiner la barre du slider (arrondie)
        pygame.draw.rect(screen, bar_color, self.rect, border_radius=5)
        pygame.draw.rect(screen, border_color, self.rect, 2, border_radius=5)
        
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
        pygame.draw.rect(screen, self.color, self.rect, border_radius=8)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=8)
        
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
        
        # Calcul des dimensions responsive
        slider_width = self.width - 2 * PADDING
        slider_x = self.x + PADDING
        slider_height = 20
        
        # Calcul des positions verticales avec espacement uniforme
        title_height = 40
        slider_spacing = 60  # Espace entre chaque slider (label + slider)
        
        # Sliders pour les paramètres d'environnement
        self.sliders = {
            'gravity': Slider(slider_x, self.y + title_height + 30, slider_width, slider_height, 0.1, 20.0, GRAVITY, "Gravité (m/s²)"),
            'air_density': Slider(slider_x, self.y + title_height + 30 + slider_spacing, slider_width, slider_height, 0.0, 2.0, AIR_DENSITY, "Densité de l'air (kg/m³)"),
            'wind_speed': Slider(slider_x, self.y + title_height + 30 + 2 * slider_spacing, slider_width, slider_height, 0.0, 50.0, WIND_SPEED, "Vitesse du vent (m/s)")
        }
        
        # Calcul des boutons responsive (2 par ligne)
        button_width = (self.width - 3 * PADDING) // 2
        button_height = 35
        button_y1 = self.y + title_height + 30 + 3 * slider_spacing
        button_y2 = button_y1 + button_height + SPACING
        
        # Boutons de contrôle de la simulation
        self.buttons = {
            'add_object': Button(slider_x, button_y1, button_width, button_height, "Ajouter"),
            'launch_pause': Button(slider_x + button_width + PADDING, button_y1, button_width, button_height, "Lancer"),
            'reset': Button(slider_x, button_y2, button_width, button_height, "Réinitialiser"),
            'clear': Button(slider_x + button_width + PADDING, button_y2, button_width, button_height, "Effacer")
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
        # Fond du panneau (arrondi)
        panel_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, (240, 240, 250), panel_rect, border_radius=12)
        pygame.draw.rect(screen, BLACK, panel_rect, 3, border_radius=12)
        
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
        
        # Calcul des dimensions responsive
        slider_width = self.width - 2 * PADDING
        slider_x = self.x + PADDING
        slider_height = 20
        
        # Calcul des positions verticales
        title_height = 40
        status_height = 40
        start_y_sliders = self.y + title_height + status_height + 10
        slider_spacing = 60
        
        # Sliders pour les paramètres de l'objet
        self.sliders = {
            'velocity': Slider(slider_x, start_y_sliders, slider_width, slider_height, 0, 500, 80, "Vitesse (m/s)"),
            'angle': Slider(slider_x, start_y_sliders + slider_spacing, slider_width, slider_height, 0, 360, 45, "Angle (°)"),
            'mass': Slider(slider_x, start_y_sliders + 2 * slider_spacing, slider_width, slider_height, 0.001, 100, 1.0, "Masse (kg)"),
            'radius': RadiusSlider(slider_x, start_y_sliders + 3 * slider_spacing, slider_width, slider_height, 1.0, 100.0, 10.0, "Rayon (cm)")
        }
        
        # Calcul des boutons responsive (2 par ligne)
        button_width = (self.width - 3 * PADDING) // 2
        button_height = 35
        # On place les boutons juste après les sliders avec un peu plus d'espace
        button_y = start_y_sliders + 4 * slider_spacing
        
        # Boutons de contrôle individuel du projectile sélectionné
        # Seuls Réinitialiser et Supprimer sont conservés sur demande utilisateur
        self.buttons = {
            'reset_selected': Button(slider_x, button_y, button_width, button_height, "Réinitialiser", (150, 200, 255)),
            'delete_selected': Button(slider_x + button_width + PADDING, button_y, button_width, button_height, "Supprimer", (255, 150, 150))
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
            
            # Gérer les boutons de contrôle individuel
            for name, button in self.buttons.items():
                if button.handle_event(event):
                    return name
        return None
    
    def draw(self, screen):
        """Dessine le panneau d'objet."""
        # Fond du panneau (arrondi)
        panel_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, (250, 240, 240), panel_rect, border_radius=12)
        pygame.draw.rect(screen, BLACK, panel_rect, 3, border_radius=12)
        
        # Titre
        title = self.title_font.render("Objet sélectionné", True, BLACK)
        screen.blit(title, (self.x + 10, self.y + 10))
        
        # Afficher l'état de sélection
        if self.selected_projectile:
            # Afficher le statut du projectile
            # Afficher le statut du projectile
             # Statut supprimé sur demande utilisateur pour simplifier l'interface
             # Seul le message d'invite est conservé
            
            info_text = self.small_font.render("Modifier les paramètres", True, DARK_GRAY)
            screen.blit(info_text, (self.x + 10, self.y + 40))
            
            # Dessiner les sliders
            for slider in self.sliders.values():
                slider.draw(screen)
            
            # Dessiner les boutons de contrôle individuel
            for button in self.buttons.values():
                button.draw(screen)
        else:
            status_text = self.small_font.render("Aucun objet sélectionné", True, GRAY)
            screen.blit(status_text, (self.x + 10, self.y + 40))
            
            # Dessiner les sliders grisés (arrondis)
            for slider in self.sliders.values():
                pygame.draw.rect(screen, LIGHT_GRAY, slider.rect, border_radius=5)
                pygame.draw.rect(screen, GRAY, slider.rect, 2, border_radius=5)
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

    def set_launch_parameters_enabled(self, enabled):
        """Active ou désactive uniquement les paramètres de lancement (vitesse, angle)."""
        if 'velocity' in self.sliders:
            self.sliders['velocity'].enabled = enabled
        if 'angle' in self.sliders:
            self.sliders['angle'].enabled = enabled


class UI:
    """Classe principale gérant l'interface utilisateur complète."""
    def __init__(self):
        self.simulation_panel = SimulationPanel()
        self.object_panel = ObjectPanel()
        
        # Compas pour la direction du vent (en haut à droite de l'écran)
        compass_radius = 30
        compass_x = SCREEN_WIDTH - compass_radius - 2 * MARGIN
        compass_y = compass_radius + 2 * MARGIN
        self.compass = Compass(compass_x, compass_y, compass_radius, WIND_DIRECTION)
        
        # État de la simulation
        self.simulation_running = False
        
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 20)
        self.selected_projectile = None
        
    def set_selected_projectile(self, projectile):
        """Définit le projectile sélectionné et met à jour les sliders."""
        self.selected_projectile = projectile
        self.object_panel.set_selected_projectile(projectile)
        
    def lock_launch_parameters(self, lock):
        """Verrouille ou déverrouille les paramètres de lancement."""
        self.object_panel.set_launch_parameters_enabled(not lock)
    
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
        
        # Gérer les événements du panneau d'objet (y compris les boutons individuels)
        obj_action = self.object_panel.handle_event(event)
        if obj_action:
            return obj_action
        
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
                # Calul de l'angle courant en degrés
                current_angle = math.degrees(math.atan2(-proj.vy, proj.vx))
                if current_angle < 0:
                    current_angle += 360
                    
                info_texts = [
                    f"Position: ({proj.x:.1f}, {proj.y:.1f})",
                    f"Vitesse: {speed:.1f} m/s",
                    f"Angle: {current_angle:.1f}°"
                ]
                
                # Affichage du temps en bas à gauche
                time_text = f"Temps: {proj.time:.2f} s"
                time_surface = self.small_font.render(time_text, True, BLACK)
                screen.blit(time_surface, (SIM_AREA_X + 10, SIM_AREA_Y + SIM_AREA_HEIGHT - 30))
                
            elif proj.launched and not proj.active:
                max_x = max([pos[0] for pos in proj.trajectory]) if proj.trajectory else 0
                
                # Calcul de l'angle final (ou d'impact)
                current_angle = math.degrees(math.atan2(-proj.vy, proj.vx))
                if current_angle < 0:
                    current_angle += 360
                    
                info_texts = [
                    f"Portée: {max_x - proj.x0:.1f} m",
                    f"Angle impact: {current_angle:.1f}°",
                    "Trajectoire terminée"
                ]
                
                # Affichage du temps total en bas à gauche
                time_text = f"t = {proj.time:.2f} s"
                time_surface = self.small_font.render(time_text, True, BLACK)
                screen.blit(time_surface, (SIM_AREA_X + 10, SIM_AREA_Y + SIM_AREA_HEIGHT - 30))
                
            else:
                info_texts = [
                    f"Position: ({proj.x:.1f}, {proj.y:.1f})",
                    f"Vitesse: {proj.v0:.1f} m/s",
                    f"Angle: {proj.angle_degrees:.1f}°"
                ]
        else:
            info_texts = [
                f"Projectiles: {len(projectiles)}",
                # "Actifs: ..." supprimé sur demande utilisateur
                "Cliquez pour sélectionner"
            ]
            
        for i, text in enumerate(info_texts):
            rendered = self.small_font.render(text, True, BLACK)
            screen.blit(rendered, (info_x, info_y + i * 20))