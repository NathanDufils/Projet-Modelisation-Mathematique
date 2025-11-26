import pygame
import math
from src.settings import *
from src.projectile import Projectile
from src.ui import UI

class Simulation:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Simulateur Balistique Multi-Projectiles")
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False

        # Interface utilisateur
        self.ui = UI()
        
        # Liste des projectiles
        self.projectiles = []
        
        # Paramètres d'environnement
        self.gravity = GRAVITY
        self.air_density = AIR_DENSITY
        self.wind_speed = WIND_SPEED
        self.wind_direction = WIND_DIRECTION
        
        # Variables pour le déplacement
        self.dragging = False
        self.drag_offset = (0, 0)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()  # Toujours mettre à jour (pour les paramètres)
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # Gérer les clics de souris pour sélection et déplacement
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    mouse_x, mouse_y = event.pos
                    
                    # Vérifier si le clic est dans la zone de simulation
                    if (SIM_AREA_X <= mouse_x <= SIM_AREA_X + SIM_AREA_WIDTH and
                        SIM_AREA_Y <= mouse_y <= SIM_AREA_Y + SIM_AREA_HEIGHT):
                        
                        # Chercher un projectile à cette position
                        clicked_projectile = None
                        for projectile in self.projectiles:
                            if projectile.is_at_position(mouse_x, mouse_y):
                                clicked_projectile = projectile
                                break
                        
                        if clicked_projectile:
                            # Sélectionner le projectile
                            self.select_projectile(clicked_projectile)
                            
                            # Commencer le déplacement si pas lancé
                            if not clicked_projectile.launched:
                                self.dragging = True
                                self.drag_offset = (mouse_x - clicked_projectile.x, mouse_y - clicked_projectile.y)
                        else:
                            # Désélectionner si clic dans le vide
                            self.select_projectile(None)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.dragging = False
            
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging and self.ui.selected_projectile:
                    mouse_x, mouse_y = event.pos
                    new_x = mouse_x - self.drag_offset[0]
                    new_y = mouse_y - self.drag_offset[1]
                    
                    # Limiter aux bordures de la zone de simulation
                    new_x = max(SIM_AREA_X + 10, min(SIM_AREA_X + SIM_AREA_WIDTH - 10, new_x))
                    new_y = max(SIM_AREA_Y + 10, min(SIM_AREA_Y + SIM_AREA_HEIGHT - 10, new_y))
                    
                    self.ui.selected_projectile.set_position(new_x, new_y)
            
            # Gérer les événements de l'UI
            ui_action = self.ui.handle_event(event)
            if ui_action:
                self.handle_ui_action(ui_action)

    def select_projectile(self, projectile):
        """Sélectionne un projectile et met à jour l'UI."""
        # Désélectionner l'ancien projectile
        if self.ui.selected_projectile:
            self.ui.selected_projectile.selected = False
        
        # Sélectionner le nouveau projectile
        if projectile:
            projectile.selected = True
        
        self.ui.set_selected_projectile(projectile)
    
    def handle_ui_action(self, action):
        """Gère les actions de l'interface utilisateur."""
        if action == 'add_object':
            # Ajouter un nouveau projectile
            new_projectile = Projectile(START_X, START_Y)
            self.projectiles.append(new_projectile)
            self.select_projectile(new_projectile)
            
        elif action == 'launch_pause':
            if self.ui.simulation_running:
                # Lancer ou reprendre tous les projectiles
                self.paused = False
                for projectile in self.projectiles:
                    if not projectile.launched:
                        # Lancer les projectiles non lancés
                        projectile.launch()
                    else:
                        # Reprendre les projectiles en pause
                        projectile.paused = False
            else:
                # Mettre en pause tous les projectiles actifs
                self.paused = True
                for projectile in self.projectiles:
                    if projectile.launched:
                        projectile.paused = True
                    
        elif action == 'reset':
            # Remettre tous les projectiles à leur position initiale
            for projectile in self.projectiles:
                projectile.reset()
            self.ui.simulation_running = False
                
        elif action == 'clear':
            # Effacer tous les projectiles
            self.projectiles.clear()
            self.select_projectile(None)
            self.ui.simulation_running = False
    
    def update(self):
        # Mettre à jour les paramètres d'environnement
        env_params = self.ui.get_environment_parameters()
        self.gravity = env_params['gravity']
        self.air_density = env_params['air_density']
        self.wind_speed = env_params['wind_speed']
        self.wind_direction = env_params['wind_direction']
        
        # Mettre à jour les paramètres du projectile sélectionné
        if self.ui.selected_projectile:
            params = self.ui.get_object_parameters()
            self.ui.selected_projectile.set_parameters(
                v0=params['v0'],
                angle=params['angle'],
                mass=params['mass'],
                radius=params['radius']
            )
        
        # Mettre à jour l'état du bouton lancer/pause
        has_projectiles = len(self.projectiles) > 0
        any_launched = any(p.launched for p in self.projectiles)
        self.ui.update_launch_pause_button(has_projectiles, any_launched)
        
        # Verrouiller les paramètres si des projectiles sont lancés (même en pause)
        # Cela évite le "téléport" causé par le recalcul de trajectoire avec de nouveaux paramètres
        self.ui.lock_parameters(any_launched)
        
        # Mettre à jour tous les projectiles avec les paramètres d'environnement
        for projectile in self.projectiles:
            projectile.update(TIME_STEP, self.gravity, self.air_density, self.wind_speed, self.wind_direction)
            
        # Vérifier si la simulation doit s'arrêter automatiquement
        if self.ui.simulation_running and any_launched:
            # Si tous les projectiles lancés sont inactifs, arrêter la simulation
            if not any(p.active for p in self.projectiles if p.launched):
                self.ui.simulation_running = False

    def draw(self):
        self.screen.fill(WHITE)
        
        # Dessiner la zone de simulation
        sim_rect = pygame.Rect(SIM_AREA_X, SIM_AREA_Y, SIM_AREA_WIDTH, SIM_AREA_HEIGHT)
        pygame.draw.rect(self.screen, (250, 250, 250), sim_rect)
        pygame.draw.rect(self.screen, BLACK, sim_rect, 2)
        
        # Dessiner une grille de référence
        self.draw_grid()
        
        # Dessiner les indicateurs de vent
        self.draw_wind_indicators()
        
        # Dessiner le sol
        ground_y = SIM_AREA_Y + SIM_AREA_HEIGHT - 10
        pygame.draw.line(self.screen, DARK_GRAY, 
                        (SIM_AREA_X, ground_y), 
                        (SIM_AREA_X + SIM_AREA_WIDTH, ground_y), 3)
        
        # Dessiner tous les projectiles
        for projectile in self.projectiles:
            projectile.draw(self.screen)
        
        # Dessiner l'interface utilisateur
        self.ui.draw(self.screen)
        self.ui.draw_info(self.screen, self.projectiles)
        
        # Afficher le statut
        if self.ui.simulation_running and any(p.launched and p.paused for p in self.projectiles):
            pause_text = pygame.font.Font(None, 36).render("PAUSE", True, RED)
            self.screen.blit(pause_text, (SCREEN_WIDTH // 2 - 40, 50))
        
        pygame.display.flip()
    
    def draw_grid(self):
        """Dessine une grille de référence dans la zone de simulation."""
        grid_spacing = 50  # pixels
        
        # Lignes verticales
        for x in range(SIM_AREA_X, SIM_AREA_X + SIM_AREA_WIDTH, grid_spacing):
            pygame.draw.line(self.screen, LIGHT_GRAY, 
                           (x, SIM_AREA_Y), (x, SIM_AREA_Y + SIM_AREA_HEIGHT), 1)
        
        # Lignes horizontales
        for y in range(SIM_AREA_Y, SIM_AREA_Y + SIM_AREA_HEIGHT, grid_spacing):
            pygame.draw.line(self.screen, LIGHT_GRAY, 
                           (SIM_AREA_X, y), (SIM_AREA_X + SIM_AREA_WIDTH, y), 1)
    
    def draw_wind_indicators(self):
        """Dessine des indicateurs visuels du vent dans la zone de simulation."""
        if self.wind_speed < 0.5:
            return  # Ne rien afficher si le vent est négligeable
        
        # Calculer les composantes du vent pour l'affichage
        wind_angle_rad = math.radians(self.wind_direction)
        
        # Dessiner plusieurs flèches de vent espacées dans la zone de simulation
        spacing_x = 150
        spacing_y = 150
        arrow_length = min(50, self.wind_speed * 3)  # Longueur proportionnelle à la vitesse
        
        # Couleur en fonction de la vitesse (plus foncé = plus rapide)
        intensity = min(255, int(100 + self.wind_speed * 5))
        wind_color = (100, 100, intensity)
        
        for x in range(SIM_AREA_X + 80, SIM_AREA_X + SIM_AREA_WIDTH - 50, spacing_x):
            for y in range(SIM_AREA_Y + 80, SIM_AREA_Y + SIM_AREA_HEIGHT - 50, spacing_y):
                # Point de départ de la flèche
                start_x = x
                start_y = y
                
                # Point d'arrivée de la flèche (direction du vent)
                end_x = start_x + arrow_length * math.cos(wind_angle_rad)
                end_y = start_y - arrow_length * math.sin(wind_angle_rad)
                
                # Dessiner la ligne principale
                pygame.draw.line(self.screen, wind_color, 
                               (int(start_x), int(start_y)), 
                               (int(end_x), int(end_y)), 2)
                
                # Dessiner la pointe de flèche
                arrow_angle = 0.5
                arrow_size = 10
                arrow_x1 = end_x - arrow_size * math.cos(wind_angle_rad - arrow_angle)
                arrow_y1 = end_y + arrow_size * math.sin(wind_angle_rad - arrow_angle)
                arrow_x2 = end_x - arrow_size * math.cos(wind_angle_rad + arrow_angle)
                arrow_y2 = end_y + arrow_size * math.sin(wind_angle_rad + arrow_angle)
                
                pygame.draw.line(self.screen, wind_color, 
                               (int(end_x), int(end_y)), 
                               (int(arrow_x1), int(arrow_y1)), 2)
                pygame.draw.line(self.screen, wind_color, 
                               (int(end_x), int(end_y)), 
                               (int(arrow_x2), int(arrow_y2)), 2)
    
