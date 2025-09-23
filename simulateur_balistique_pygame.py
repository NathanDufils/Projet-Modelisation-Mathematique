"""
Simulateur balistique interactif (pygame)
----------------------------------------

Fonctionnalités principales
- Lancer de projectile en 2D avec gravité, vent et frottement (linéaire ou quadratique).
- Réglage en direct via UI :
  vitesse initiale, angle, masse, coefficient de traînée (Cd), section (A), densité de l'air (rho),
  gravité (g), vent Vx/Vy, pas de temps (dt).
- Choix du modèle de frottement : linéaire (k*v) ou quadratique (0.5*rho*Cd*A*||v_rel||*v_rel).
- Intégration numérique : Runge-Kutta 4 (stable et précis) ou Euler (pour comparaison).
- Boutons : Lancer / Pause / Réinitialiser / Effacer trace / Placer cible / Presets.
- Affichages : position/temps/vitesse, portée atteinte, distance à une cible, énergie.
- Échelle : unité en SI. 1 m ≈ scale pixels à l'écran (réglable si besoin).

Dépendances : pygame (pip install pygame)

Exécution :
    python simulateur_balistique_pygame.py

Contrôles rapides :
- ESPACE : Lancer/Pause
- R : Réinitialiser projectile
- C : Effacer la trajectoire
- T : Bascule frottement linéaire/quadratique
- I : Preset "intérieur" (pas de vent, faible rho)
- O : Preset "extérieur" (vent léger, rho standard)
- G : Bascule intégrateur Euler/RK4
- Clique droit : placer une cible à la position de la souris

Remarque : pour les valeurs physiques, utiliser SI (m, kg, s, N). Le vent est en m/s.
"""

import math
import pygame
from dataclasses import dataclass

# ---------------------------- Configs générales ---------------------------- #
WIDTH, HEIGHT = 1200, 700
FPS = 120
SCALE = 1.0  # pixels par mètre (1 m = 1 px pour commencer; ajusté dans draw_world)
MARGIN_RIGHT = 360  # largeur du panneau UI
FONT_NAME = "consolas"

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (210, 210, 210)
DARK = (35, 35, 35)
BLUE = (60, 120, 255)
GREEN = (60, 200, 120)
RED = (230, 70, 70)
ORANGE = (255, 160, 60)
YELLOW = (250, 220, 80)

# ---------------------------- Utilitaires UI ------------------------------ #
class Slider:
    def __init__(self, rect, min_val, max_val, value, step=None, label="", fmt="{:.2f}"):
        self.rect = pygame.Rect(rect)
        self.min = min_val
        self.max = max_val
        self.value = value
        self.step = step
        self.label = label
        self.fmt = fmt
        self.dragging = False

    def handle(self, ev):
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            if self.rect.collidepoint(ev.pos):
                self.dragging = True
                self._set_from_mouse(ev.pos)
        elif ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
            self.dragging = False
        elif ev.type == pygame.MOUSEMOTION and self.dragging:
            self._set_from_mouse(ev.pos)

    def _set_from_mouse(self, pos):
        x = max(self.rect.left, min(pos[0], self.rect.right))
        t = (x - self.rect.left) / max(1, self.rect.width)
        v = self.min + t * (self.max - self.min)
        if self.step:
            v = round(v / self.step) * self.step
        self.value = max(self.min, min(self.max, v))

    def draw(self, surf, font):
        # Track
        pygame.draw.rect(surf, GRAY, self.rect, border_radius=6)
        # Thumb
        t = (self.value - self.min) / (self.max - self.min)
        x = self.rect.left + t * self.rect.width
        pygame.draw.circle(surf, BLUE, (int(x), self.rect.centery), 10)
        # Label
        txt = f"{self.label}: {self.fmt.format(self.value)}"
        surf.blit(font.render(txt, True, WHITE), (self.rect.left, self.rect.top - 20))

class Toggle:
    def __init__(self, rect, value=False, label=""):
        self.rect = pygame.Rect(rect)
        self.value = value
        self.label = label

    def handle(self, ev):
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            if self.rect.collidepoint(ev.pos):
                self.value = not self.value

    def draw(self, surf, font):
        color = GREEN if self.value else RED
        pygame.draw.rect(surf, color, self.rect, border_radius=8)
        caption = f"{self.label}: {'ON' if self.value else 'OFF'}"
        text = font.render(caption, True, BLACK)
        surf.blit(text, (self.rect.centerx - text.get_width()//2, self.rect.centery - text.get_height()//2))

class Button:
    def __init__(self, rect, label, color=ORANGE):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.color = color

    def handle(self, ev):
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            if self.rect.collidepoint(ev.pos):
                return True
        return False

    def draw(self, surf, font):
        pygame.draw.rect(surf, self.color, self.rect, border_radius=10)
        text = font.render(self.label, True, BLACK)
        surf.blit(text, (self.rect.centerx - text.get_width()//2, self.rect.centery - text.get_height()//2))

# ---------------------------- Physique ------------------------------------ #
@dataclass
class Params:
    v0: float = 40.0       # m/s
    angle_deg: float = 45.0
    mass: float = 0.145    # kg (balle de baseball)
    Cd: float = 0.47       # sphère
    area: float = 0.0042   # m^2 (diam ~ 7.3 cm)
    rho: float = 1.225     # kg/m^3 (air, 15°C)
    g: float = 9.81        # m/s^2
    wind_x: float = 0.0    # m/s
    wind_y: float = 0.0    # m/s (positif vers le haut)
    dt: float = 0.01       # s, pas de temps
    linear_drag: bool = False  # False => quadratique
    integrator_euler: bool = False  # False => RK4

@dataclass
class State:
    x: float = 0.0
    y: float = 0.0
    vx: float = 0.0
    vy: float = 0.0

class Ballistics:
    def __init__(self, params: Params):
        self.p = params
        self.reset()

    def reset(self):
        th = math.radians(self.p.angle_deg)
        self.state = State(0.0, 0.0, self.p.v0 * math.cos(th), self.p.v0 * math.sin(th))
        self.t = 0.0
        self.trace = [(self.state.x, self.state.y)]
        self.active = False

    def set_from_params(self):
        th = math.radians(self.p.angle_deg)
        self.state.vx = self.p.v0 * math.cos(th)
        self.state.vy = self.p.v0 * math.sin(th)

    # Accélération (ax, ay)
    def acceleration(self, vx, vy):
        p = self.p
        # vitesse relative à l'air (vent)
        vrel_x = vx - p.wind_x
        vrel_y = vy - p.wind_y
        vrel = math.hypot(vrel_x, vrel_y)

        # Force gravité
        Fx_g, Fy_g = 0.0, -p.g * p.mass

        # Force de traînée
        if p.linear_drag:
            k_eff = 0.5 * p.rho * p.Cd * p.area
            Fx_d = -k_eff * vrel_x
            Fy_d = -k_eff * vrel_y
        else:
            if vrel != 0:
                coeff = 0.5 * p.rho * p.Cd * p.area * vrel
                Fx_d = -coeff * vrel_x
                Fy_d = -coeff * vrel_y
            else:
                Fx_d = Fy_d = 0.0

        Fx = Fx_g + Fx_d
        Fy = Fy_g + Fy_d
        ax = Fx / p.mass
        ay = Fy / p.mass
        return ax, ay

    def step_euler(self):
        s = self.state
        ax, ay = self.acceleration(s.vx, s.vy)
        s.x += s.vx * self.p.dt
        s.y += s.vy * self.p.dt
        s.vx += ax * self.p.dt
        s.vy += ay * self.p.dt
        self.t += self.p.dt

    def step_rk4(self):
        p = self.p
        s = self.state

        def deriv(x, y, vx, vy):
            ax, ay = self.acceleration(vx, vy)
            return vx, vy, ax, ay

        dt = p.dt
        k1 = deriv(s.x, s.y, s.vx, s.vy)
        k2 = deriv(
            s.x + 0.5 * dt * k1[0],
            s.y + 0.5 * dt * k1[1],
            s.vx + 0.5 * dt * k1[2],
            s.vy + 0.5 * dt * k1[3],
        )
        k3 = deriv(
            s.x + 0.5 * dt * k2[0],
            s.y + 0.5 * dt * k2[1],
            s.vx + 0.5 * dt * k2[2],
            s.vy + 0.5 * dt * k2[3],
        )
        k4 = deriv(
            s.x + dt * k3[0],
            s.y + dt * k3[1],
            s.vx + dt * k3[2],
            s.vy + dt * k3[3],
        )

        s.x += dt * (k1[0] + 2*k2[0] + 2*k3[0] + k4[0]) / 6
        s.y += dt * (k1[1] + 2*k2[1] + 2*k3[1] + k4[1]) / 6
        s.vx += dt * (k1[2] + 2*k2[2] + 2*k3[2] + k4[2]) / 6
        s.vy += dt * (k1[3] + 2*k2[3] + 2*k3[3] + k4[3]) / 6
        self.t += dt

    def update(self):
        if not self.active:
            return
        if self.p.integrator_euler:
            self.step_euler()
        else:
            self.step_rk4()
        self.trace.append((self.state.x, self.state.y))
        if self.state.y < 0:
            self.active = False
            self.state.y = 0

# ---------------------------- App / Interface ----------------------------- #

def meter_to_screen(px, py, scale, h):
    sx = int(px * scale)
    sy = int(h - py * scale)
    return sx, sy

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH + MARGIN_RIGHT, HEIGHT))
    pygame.display.set_caption("Simulateur balistique (pygame)")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(FONT_NAME, 16)  # Réduire la taille pour plus d'espace
    big = pygame.font.SysFont(FONT_NAME, 24, bold=True)  # Réduire aussi

    params = Params()
    sim = Ballistics(params)

    # UI – sliders
    ui_left = WIDTH + 20
    # Commencer plus haut pour que tous les éléments soient visibles
    y = 160  # Réduire de 200 à 160
    sliders = []
    def add_slider(label, vmin, vmax, v0, step=None, fmt="{:.2f}"):
        nonlocal y
        sld = Slider((ui_left, y, MARGIN_RIGHT - 40, 16), vmin, vmax, v0, step, label, fmt)  # Réduire hauteur à 16
        sliders.append(sld)
        y += 50  # Réduire l'espacement de 60 à 50
        return sld

    s_v0 = add_slider("Vitesse initiale v0 (m/s)", 0, 120, params.v0, step=0.5)
    s_ang = add_slider("Angle (deg)", 0, 90, params.angle_deg, step=0.5)
    s_m = add_slider("Masse (kg)", 0.01, 5.0, params.mass, step=0.01)
    s_cd = add_slider("Coefficient Cd", 0.0, 1.5, params.Cd, step=0.01)
    s_a = add_slider("Section A (m^2)", 0.0001, 0.05, params.area, step=0.0001, fmt="{:.4f}")
    s_rho = add_slider("Densité air rho (kg/m^3)", 0.4, 1.6, params.rho, step=0.01)
    s_g = add_slider("Gravité g (m/s^2)", 0.0, 20.0, params.g, step=0.1)
    s_wx = add_slider("Vent Vx (m/s)", -20.0, 20.0, params.wind_x, step=0.5)
    s_wy = add_slider("Vent Vy (m/s)", -20.0, 20.0, params.wind_y, step=0.5)
    s_dt = add_slider("Pas de temps dt (s)", 0.001, 0.05, params.dt, step=0.001, fmt="{:.3f}")

    # Toggles & boutons
    t_drag = Toggle((ui_left, y, 150, 28), value=params.linear_drag, label="Frottement linéaire")  # Réduire hauteur
    y += 40  # Réduire espacement
    t_int = Toggle((ui_left, y, 150, 28), value=params.integrator_euler, label="Euler (vs RK4)")
    y += 40

    b_launch = Button((ui_left, y, 120, 32), "Lancer")  # Réduire hauteur
    b_pause  = Button((ui_left + 130, y, 120, 32), "Pause", color=YELLOW)
    y += 40
    b_reset  = Button((ui_left, y, 120, 32), "Réinit.")
    b_clear  = Button((ui_left + 130, y, 120, 32), "Effacer", color=RED)
    y += 40
    b_preset_in = Button((ui_left, y, 120, 32), "Preset Int.")
    b_preset_out = Button((ui_left + 130, y, 120, 32), "Preset Ext.")

    # Cible
    target = None

    # Trace persistante
    persistent_traces = []

    running = True
    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_SPACE:
                    sim.active = not sim.active
                elif ev.key == pygame.K_r:
                    sim.reset()
                elif ev.key == pygame.K_c:
                    sim.trace = [(sim.state.x, sim.state.y)]
                    persistent_traces.clear()
                elif ev.key == pygame.K_t:
                    t_drag.value = not t_drag.value
                elif ev.key == pygame.K_g:
                    t_int.value = not t_int.value
                elif ev.key == pygame.K_i:
                    s_wx.value, s_wy.value = 0.0, 0.0
                    s_rho.value = 1.18
                    s_v0.value = 25.0
                elif ev.key == pygame.K_o:
                    s_wx.value, s_wy.value = 2.0, 0.0
                    s_rho.value = 1.225
                    s_v0.value = 40.0
            elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 3:
                mx, my = ev.pos
                if mx < WIDTH:
                    tx = mx / SCALE
                    ty = (HEIGHT - my) / SCALE
                    if ty < 0: ty = 0
                    target = (tx, ty)

            # UI events
            for s in sliders:
                s.handle(ev)
            t_drag.handle(ev)
            t_int.handle(ev)
            if b_launch.handle(ev):
                sim.set_from_params()
                sim.active = True
            if b_pause.handle(ev):
                sim.active = False
            if b_reset.handle(ev):
                # on pousse la trace dans l'historique avant reset
                if len(sim.trace) > 2:
                    persistent_traces.append(sim.trace[:])
                sim.reset()
            if b_clear.handle(ev):
                persistent_traces.clear()
                sim.trace = [(sim.state.x, sim.state.y)]
            if b_preset_in.handle(ev):
                s_wx.value, s_wy.value = 0.0, 0.0
                s_rho.value = 1.18
                s_v0.value = 25.0
                s_cd.value = 0.47
                s_a.value = 0.0042
            if b_preset_out.handle(ev):
                s_wx.value, s_wy.value = 2.0, 0.0
                s_rho.value = 1.225
                s_v0.value = 40.0
                s_cd.value = 0.47
                s_a.value = 0.0042

        # synchroniser les params depuis UI
        params.v0 = s_v0.value
        params.angle_deg = s_ang.value
        params.mass = s_m.value
        params.Cd = s_cd.value
        params.area = s_a.value
        params.rho = s_rho.value
        params.g = s_g.value
        params.wind_x = s_wx.value
        params.wind_y = s_wy.value
        params.dt = s_dt.value
        params.linear_drag = t_drag.value
        params.integrator_euler = t_int.value

        # maj simulation
        sim.update()

        # ------------------ Rendu ------------------ #
        screen.fill(DARK)

        # Zone monde
        world = pygame.Surface((WIDTH, HEIGHT))
        world.fill((15, 18, 22))

        # Sol
        pygame.draw.line(world, GRAY, (0, HEIGHT-1), (WIDTH, HEIGHT-1), 2)

        # Traces persistantes
        for tr in persistent_traces:
            pts = [meter_to_screen(x, y, SCALE, HEIGHT) for (x, y) in tr if y >= 0]
            if len(pts) > 1:
                pygame.draw.lines(world, (70, 90, 130), False, pts, 2)

        # Trace courante
        pts = [meter_to_screen(x, y, SCALE, HEIGHT) for (x, y) in sim.trace if y >= 0]
        if len(pts) > 1:
            pygame.draw.lines(world, BLUE, False, pts, 3)

        # Projectile
        px, py = meter_to_screen(sim.state.x, sim.state.y, SCALE, HEIGHT)
        pygame.draw.circle(world, YELLOW, (px, py), 6)

        # Cible
        info_target = ""
        if target is not None:
            tx, ty = target
            tsx, tsy = meter_to_screen(tx, ty, SCALE, HEIGHT)
            pygame.draw.circle(world, RED, (tsx, tsy), 8, 2)
            # distance courte lorsque au sol
            dx = sim.state.x - tx
            dy = sim.state.y - ty
            dist = math.hypot(dx, dy)
            info_target = f"Cible: ({tx:.1f} m, {ty:.1f} m)  Dist: {dist:.2f} m"

        # Échelle (grille légère tous 10 m)
        for gx in range(0, WIDTH, 100):
            pygame.draw.line(world, (30, 35, 40), (gx, 0), (gx, HEIGHT), 1)
        for gy in range(0, HEIGHT, 100):
            pygame.draw.line(world, (30, 35, 40), (0, gy), (WIDTH, gy), 1)

        screen.blit(world, (0, 0))

        # Panneau UI
        ui = pygame.Surface((MARGIN_RIGHT, HEIGHT))
        ui.fill(WHITE)  # Changer de (25, 25, 30) à WHITE

        # Titre
        title = big.render("Paramètres", True, BLACK)  # Changer de WHITE à BLACK
        ui.blit(title, (20, 10))

        # Infos runtime juste sous le titre
        info_y = 40  # Réduire de 50 à 40
        pygame.draw.rect(ui, GRAY, (10, info_y, MARGIN_RIGHT - 20, 100), border_radius=8)  # Changer de (18, 18, 22) à GRAY
        
        # Calculer les infos
        speed = math.hypot(sim.state.vx, sim.state.vy)
        range_x = sim.state.x if sim.state.y <= 0.1 else 0  # Portée quand au sol
        
        info_lines = [
            f"t = {sim.t:.2f} s",
            f"pos = ({sim.state.x:.1f}, {sim.state.y:.1f}) m",
            f"v = {speed:.1f} m/s",
            f"portée = {range_x:.1f} m" if range_x > 0 else "",
            f"{'linéaire' if params.linear_drag else 'quadratique'} | {'Euler' if params.integrator_euler else 'RK4'}",
        ]
        yy = info_y + 8
        for line in info_lines:
            if line:  # Ne pas afficher les lignes vides
                ui.blit(font.render(line, True, BLACK), (15, yy))  # Changer de WHITE à BLACK
                yy += 18  # Réduire espacement

        # Affichage info cible si présente
        if target is not None:
            dx = sim.state.x - target[0]
            dy = sim.state.y - target[1]
            dist = math.hypot(dx, dy)
            target_text = f"Cible: dist = {dist:.1f} m"
            ui.blit(font.render(target_text, True, RED), (15, yy))

        # Astuces de contrôle sous les infos (une par ligne)
        tips_y = yy + 10
        tips = [
            "ESPACE: Lancer/Pause",
            "R: Réinit",
            "C: Effacer",
            "T: Frottement linéaire/quadratique",
            "G: Euler/RK4",
            "I/O: Presets",
            "Clic droit: placer une cible",
        ]
        for t in tips:
            ui.blit(font.render(t, True, DARK), (20, tips_y))  # Changer de (180, 180, 200) à DARK
            tips_y += 20

        # Dessin sliders, toggles, boutons comme avant
        for s in sliders:
            s.draw(ui, font)
        t_drag.draw(ui, font)
        t_int.draw(ui, font)
        for b in (b_launch, b_pause, b_reset, b_clear, b_preset_in, b_preset_out):
            b.draw(ui, font)

        screen.blit(ui, (WIDTH, 0))
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()