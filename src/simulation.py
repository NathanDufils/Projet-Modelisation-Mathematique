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
        
        # Mettre à jour tous les projectiles avec les paramètres d'environnement
        for projectile in self.projectiles:
            projectile.update(TIME_STEP, self.gravity, self.air_density)
            
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
    
