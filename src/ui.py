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
        # Dessiner la barre du slider
        pygame.draw.rect(screen, (200, 200, 200), self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        
        # Dessiner le handle
        pygame.draw.circle(screen, BLUE, (int(self.handle_x), self.rect.centery), self.handle_radius)
        pygame.draw.circle(screen, BLACK, (int(self.handle_x), self.rect.centery), self.handle_radius, 2)
        
        # Dessiner le label et la valeur
        label_text = self.font.render(f"{self.label}: {self.val:.1f}", True, BLACK)
        screen.blit(label_text, (self.rect.x, self.rect.y - 25))

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

class UI:
    def __init__(self):
        self.sliders = {
            'velocity': Slider(50, 80, 200, 20, 10, 200, 80, "Vitesse (m/s)"),
            'angle': Slider(50, 130, 200, 20, 0, 90, 45, "Angle (°)"),
            'mass': Slider(50, 180, 200, 20, 0.1, 10, 1.0, "Masse (kg)"),
            'drag': Slider(50, 230, 200, 20, 0.0, 2.0, 0.0, "Traînée")
        }
        
        self.buttons = {
            'add_projectile': Button(50, 280, 80, 25, "Ajouter"),
            'launch_pause': Button(140, 280, 80, 25, "Lancer"),
            'reset': Button(50, 315, 80, 25, "Reset"),
            'clear_all': Button(140, 315, 80, 25, "Effacer")
        }
        
        # État de la simulation
        self.simulation_running = False
        
        self.font = pygame.font.Font(None, 24)
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
            
            self.sliders['drag'].val = projectile.drag_coefficient
            self.sliders['drag'].handle_x = self.sliders['drag']._value_to_x(projectile.drag_coefficient)
    
    def update_launch_pause_button(self, has_projectiles, any_launched):
        """Met à jour le texte du bouton lancer/pause selon l'état de la simulation."""
        if not has_projectiles:
            self.buttons['launch_pause'].text = "Lancer"
            self.simulation_running = False
        elif any_launched and self.simulation_running:
            self.buttons['launch_pause'].text = "Pause"
        else:
            self.buttons['launch_pause'].text = "Lancer"
            
    def handle_event(self, event):
        # Gérer les sliders seulement si un projectile est sélectionné
        if self.selected_projectile:
            for slider in self.sliders.values():
                slider.handle_event(event)
            
        for name, button in self.buttons.items():
            if button.handle_event(event):
                if name == 'launch_pause':
                    # Basculer l'état de la simulation
                    self.simulation_running = not self.simulation_running
                    return 'launch_pause'
                else:
                    return name
        return None
    
    def draw(self, screen):
        # Dessiner un panneau de contrôle (ajusté)
        panel_rect = pygame.Rect(20, 20, 280, 370)
        pygame.draw.rect(screen, (240, 240, 240), panel_rect)
        pygame.draw.rect(screen, BLACK, panel_rect, 2)
        
        # Titre avec plus d'espacement
        title = self.font.render("Contrôles de simulation", True, BLACK)
        screen.blit(title, (30, 40))
        
        # Afficher le projectile sélectionné
        if self.selected_projectile:
            selected_text = self.small_font.render(f"Projectile sélectionné", True, DARK_GRAY)
            screen.blit(selected_text, (30, 60))
        else:
            selected_text = self.small_font.render("Aucun projectile sélectionné", True, GRAY)
            screen.blit(selected_text, (30, 60))
        
        # Dessiner les sliders seulement si un projectile est sélectionné
        if self.selected_projectile:
            for slider in self.sliders.values():
                slider.draw(screen)
        else:
            # Afficher les sliders grisés
            for slider in self.sliders.values():
                # Dessiner la barre grisée
                pygame.draw.rect(screen, LIGHT_GRAY, slider.rect)
                pygame.draw.rect(screen, GRAY, slider.rect, 2)
                
                # Label grisé
                label_text = slider.font.render(f"{slider.label}: --", True, GRAY)
                screen.blit(label_text, (slider.rect.x, slider.rect.y - 25))
            
        # Dessiner les boutons
        for button in self.buttons.values():
            button.draw(screen)
            
    def get_parameters(self):
        return {
            'v0': self.sliders['velocity'].val,
            'angle': self.sliders['angle'].val,
            'mass': self.sliders['mass'].val,
            'drag_coefficient': self.sliders['drag'].val
        }
    
    def draw_info(self, screen, projectiles):
        """Affiche des informations sur les projectiles."""
        info_y = 410
        
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
            screen.blit(rendered, (30, info_y + i * 20))