# Architecture du Simulateur Balistique

## 🏗️ Structure Globale

```
┌─────────────────────────────────────────────────────────────┐
│                         main.py                             │
│                    (Point d'entrée)                         │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    simulation.py                            │
│                  (Boucle principale)                        │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  • Gestion des événements (souris, clavier)        │   │
│  │  • Mise à jour de la physique                       │   │
│  │  • Affichage (draw)                                 │   │
│  │  • Gestion des projectiles (liste)                  │   │
│  └─────────────────────────────────────────────────────┘   │
└────────┬──────────────────────────────┬─────────────────────┘
         │                              │
         ▼                              ▼
┌──────────────────┐          ┌──────────────────┐
│  projectile.py   │          │     ui.py        │
│   (Modèle)       │          │    (Vue)         │
└────────┬─────────┘          └────────┬─────────┘
         │                              │
         ▼                              ▼
┌──────────────────┐          ┌─────────────────────────┐
│   physics.py     │          │  • SimulationPanel      │
│  (Contrôleur)    │          │  • ObjectPanel          │
│                  │          │  • Slider, Button       │
│ • Forces         │          │  • Compass              │
│ • Intégration    │          └─────────────────────────┘
└──────────────────┘
```

## 📦 Composants Principaux

### 1. Projectile (Modèle de Données)

```
Projectile
├── État Initial
│   ├── x0, y0 (position)
│   ├── v0 (vitesse)
│   ├── angle (direction)
│   ├── mass (masse)
│   └── radius (rayon)
│
├── État Actuel
│   ├── x, y (position)
│   ├── vx, vy (vitesse)
│   ├── time (temps écoulé)
│   └── trajectory[] (historique)
│
├── Drapeaux
│   ├── launched (lancé ?)
│   ├── active (en mouvement ?)
│   ├── paused (en pause ?)
│   └── selected (sélectionné ?)
│
└── Méthodes
    ├── launch() ────────────► Lance le projectile
    ├── pause() ─────────────► Pause/Reprend
    ├── reset() ─────────────► Réinitialise
    ├── update(dt) ──────────► Mise à jour physique
    ├── set_position(x, y) ──► Déplace (si pas lancé)
    ├── set_parameters() ────► Modifie les paramètres
    ├── is_at_position() ────► Test de sélection
    └── draw() ──────────────► Affichage
```

### 2. Simulation (Contrôleur Principal)

```
Simulation
├── Composants
│   ├── ui: UI ──────────────► Interface utilisateur
│   ├── projectiles: [] ─────► Liste des projectiles
│   ├── screen ──────────────► Surface Pygame
│   └── clock ───────────────► Horloge pour FPS
│
├── Paramètres Environnementaux
│   ├── gravity
│   ├── air_density
│   ├── wind_speed
│   └── wind_direction
│
├── Boucle Principale
│   ├── handle_events() ─────► Événements utilisateur
│   ├── update() ────────────► Logique de jeu
│   └── draw() ──────────────► Rendu visuel
│
└── Gestion des Actions
    ├── add_object ──────────► Ajoute un projectile
    ├── launch_pause ────────► Contrôle global
    ├── reset ───────────────► Réinitialise tous
    ├── clear ───────────────► Efface tous
    ├── launch_selected ─────► Lance un (NOUVEAU)
    ├── pause_selected ──────► Pause un (NOUVEAU)
    ├── reset_selected ──────► Réinit. un (NOUVEAU)
    └── delete_selected ─────► Supprime un (NOUVEAU)
```

### 3. UI (Interface Utilisateur)

```
UI
├── SimulationPanel (Panneau Environnement)
│   ├── Sliders
│   │   ├── gravity
│   │   ├── air_density
│   │   └── wind_speed
│   │
│   └── Buttons
│       ├── add_object ──────► "Ajouter"
│       ├── launch_pause ────► "Lancer" / "Pause"
│       ├── reset ───────────► "Réinitialiser"
│       └── clear ───────────► "Effacer"
│
├── ObjectPanel (Panneau Objet) ★ MODIFIÉ
│   ├── Sliders
│   │   ├── velocity
│   │   ├── angle
│   │   ├── mass
│   │   └── radius
│   │
│   └── Buttons ★ NOUVEAUX
│       ├── launch_selected ─► "Lancer" (Vert)
│       ├── pause_selected ──► "Pause" (Jaune)
│       ├── reset_selected ──► "Réinit." (Bleu)
│       └── delete_selected ─► "Suppr." (Rouge)
│
└── Compass (Direction du Vent)
    └── Angle interactif (0-360°)
```

### 4. Physics (Moteur Physique)

```
Physics
├── update_physics_step()
│   │
│   ├── 1. Calcul des Forces
│   │   ├── Gravité: Fy = m·g
│   │   └── Traînée: Fd = ½·ρ·Cd·A·v²
│   │       ├── Vitesse relative (avec vent)
│   │       ├── Magnitude
│   │       └── Direction
│   │
│   ├── 2. Accélération
│   │   ├── ax = Fx / m
│   │   └── ay = Fy / m
│   │
│   ├── 3. Intégration (Euler semi-implicite)
│   │   ├── v_new = v + a·dt
│   │   └── x_new = x + v_new·dt
│   │
│   └── 4. Retour (x, y, vx, vy)
│
└── Formules Analytiques
    ├── calculate_range() ───► Portée théorique
    ├── calculate_max_height()► Hauteur max
    └── calculate_flight_time()► Temps de vol
```

## 🔄 Flux de Données

### Lancement d'un Projectile Individuel (NOUVEAU)

```
1. Utilisateur clique sur un projectile
   │
   ▼
2. Simulation.select_projectile(proj)
   │
   ├─► proj.selected = True
   └─► UI.set_selected_projectile(proj)
       │
       └─► ObjectPanel affiche les paramètres
           │
           └─► Affiche le statut (Prêt/Vol/Pause/Terminé)

3. Utilisateur clique sur "Lancer" (ObjectPanel)
   │
   ▼
4. ObjectPanel.handle_event() retourne 'launch_selected'
   │
   ▼
5. UI.handle_event() transmet l'action
   │
   ▼
6. Simulation.handle_ui_action('launch_selected')
   │
   └─► selected_projectile.launch()
       │
       ├─► launched = True
       ├─► active = True
       ├─► Reset trajectory
       └─► Recalcule vitesses initiales

7. Boucle de mise à jour (chaque frame)
   │
   ▼
8. Simulation.update()
   │
   └─► Pour chaque projectile:
       │
       └─► projectile.update(dt, gravity, air_density, wind_speed, wind_direction)
           │
           ├─► SI launched AND active AND NOT paused:
           │   │
           │   └─► physics.update_physics_step(...)
           │       │
           │       ├─► Calcule nouvelles positions
           │       ├─► Ajoute à trajectory
           │       └─► Vérifie les limites
           │
           └─► SINON: Ne fait rien

9. Simulation.draw()
   │
   └─► projectile.draw(screen)
       │
       ├─► Dessine trajectory (si launched)
       ├─► Dessine le projectile (cercle coloré)
       └─► Dessine indicateurs (si pas lancé ou en pause)
```

### Mise en Pause d'un Projectile (NOUVEAU)

```
1. Utilisateur clique sur "Pause" (ObjectPanel)
   │
   ▼
2. Action 'pause_selected' transmise
   │
   ▼
3. selected_projectile.pause()
   │
   └─► paused = NOT paused
       │
       ├─► SI paused = True:
       │   └─► Le projectile reste visible mais ne bouge plus
       │
       └─► SI paused = False:
           └─► Le projectile reprend son mouvement
```

### Réinitialisation d'un Projectile (NOUVEAU)

```
1. Utilisateur clique sur "Réinit." (ObjectPanel)
   │
   ▼
2. Action 'reset_selected' transmise
   │
   ▼
3. selected_projectile.reset()
   │
   ├─► x = x0, y = y0
   ├─► time = 0
   ├─► trajectory = [(x0, y0)]
   ├─► launched = False
   ├─► paused = False
   └─► active = True
```

### Suppression d'un Projectile (NOUVEAU)

```
1. Utilisateur clique sur "Suppr." (ObjectPanel)
   │
   ▼
2. Action 'delete_selected' transmise
   │
   ▼
3. projectiles.remove(selected_projectile)
   │
   └─► select_projectile(None)
       │
       └─► UI désélectionne le projectile
```

## 🎨 États d'un Projectile

```
                   ┌─────────────┐
                   │   INITIAL   │
                   │  (Création) │
                   └──────┬──────┘
                          │
                          ▼
                   ┌─────────────┐
              ┌────│    PRÊT     │◄───┐
              │    │  (Ready)    │    │ reset()
              │    │ launched=F  │    │
              │    │ active=T    │    │
              │    └──────┬──────┘    │
              │           │           │
              │    launch()           │
              │           │           │
              │           ▼           │
              │    ┌─────────────┐    │
    pause()   │    │   EN VOL    │    │
    (paused=T)│◄───│  (Flying)   │────┤
              │    │ launched=T  │    │
              │    │ active=T    │    │
              │    │ paused=F    │    │
              │    └──────┬──────┘    │
              │           │           │
              │    pause()           │
    pause()   │    (paused=F)        │
    (paused=F)│           │           │
              │           ▼           │
              │    ┌─────────────┐    │
              └───►│  EN PAUSE   │    │
                   │  (Paused)   │    │
                   │ launched=T  │    │
                   │ active=T    │    │
                   │ paused=T    │    │
                   └─────────────┘    │
                                      │
                   Sol atteint ou     │
                   hors limites       │
                          │           │
                          ▼           │
                   ┌─────────────┐    │
                   │   TERMINÉ   │    │
                   │ (Finished)  │────┘
                   │ launched=T  │
                   │ active=F    │
                   └─────────────┘
```

## 📊 Hiérarchie des Contrôles

```
Contrôles
│
├── Globaux (SimulationPanel)
│   ├── Ajouter ────────────────► Crée 1 nouveau projectile
│   ├── Lancer/Pause ───────────► Agit sur TOUS les projectiles
│   ├── Réinitialiser ──────────► Reset TOUS les projectiles
│   └── Effacer ────────────────► Supprime TOUS les projectiles
│
└── Individuels (ObjectPanel) ★ NOUVEAUX
    ├── Lancer ─────────────────► Lance 1 projectile sélectionné
    ├── Pause ──────────────────► Pause 1 projectile sélectionné
    ├── Réinit. ────────────────► Reset 1 projectile sélectionné
    └── Suppr. ─────────────────► Supprime 1 projectile sélectionné
```

## 🔍 Exemple de Scénario Multi-Projectiles

```
État Initial:
┌──────────────────────────────────────┐
│  Projectile A (30°, rouge)   ○       │
│  Projectile B (45°, rouge)   ○       │
│  Projectile C (60°, rouge)   ○       │
│                                      │
└──────────────────────────────────────┘
Tous: launched=False, active=True

───────────────────────────────────────

Action: Lancer tous (bouton global)
┌──────────────────────────────────────┐
│                        ○ ╱            │
│                      ○ ╱   ○          │
│                    ○ ╱   ○   ╲        │
│  Start: ●────────○╱  ○──────○─○      │
│                 ╱   ○          ╲      │
│                ╱  ○              ○    │
└──────────────────────────────────────┘
Tous: launched=True, active=True

───────────────────────────────────────

Action: Pause projectile B (bouton individuel)
┌──────────────────────────────────────┐
│                        ○ ╱            │
│                      ○ ╱   ○ (pause) │
│                    ○ ╱   ◉   ╲        │
│  Start: ●────────○╱  ●──────○─○      │
│                 ╱   ○          ╲      │
│                ╱  ○              ○    │
└──────────────────────────────────────┘
A: active=T, paused=F (continue)
B: active=T, paused=T (gelé)
C: active=T, paused=F (continue)

───────────────────────────────────────

Action: Réinitialiser projectile A (bouton individuel)
┌──────────────────────────────────────┐
│  Projectile A (30°, rouge)   ○       │
│                      ○ ╱   ○ (pause) │
│                    ○ ╱   ◉   ╲        │
│                   ○╱  ●──────○─○      │
│                  ╱  ○          ╲      │
│                 ╱ ○              ○    │
└──────────────────────────────────────┘
A: launched=False, active=True (réinitialisé)
B: active=T, paused=T (toujours en pause)
C: active=F (terminé)

───────────────────────────────────────

Action: Supprimer projectile B (bouton individuel)
┌──────────────────────────────────────┐
│  Projectile A (30°, rouge)   ○       │
│                                      │
│                    ○ ╱       ╲        │
│                   ○╱  ●──────○─○      │
│                  ╱  ○          ╲      │
│                 ╱ ○              ○    │
└──────────────────────────────────────┘
A: toujours là
B: supprimé !
C: toujours là (terminé)
```

## 🧪 Tests de Validation

### Test 1: Lancement Individuel
```
1. Créer 3 projectiles
2. Sélectionner le premier
3. Cliquer "Lancer" (individuel)
✓ Seul le premier doit bouger
✓ Les autres restent immobiles
```

### Test 2: Pause Individuelle
```
1. Lancer tous les projectiles
2. Sélectionner le deuxième
3. Cliquer "Pause" (individuel)
✓ Le deuxième se fige
✓ Les autres continuent
```

### Test 3: Réinitialisation Individuelle
```
1. Lancer un projectile
2. Attendre qu'il avance
3. Cliquer "Réinit." (individuel)
✓ Le projectile retourne au début
✓ Sa trajectoire est effacée
✓ launched = False
```

### Test 4: Suppression Individuelle
```
1. Créer plusieurs projectiles
2. Sélectionner un
3. Cliquer "Suppr." (individuel)
✓ Le projectile disparaît
✓ Les autres ne sont pas affectés
✓ L'UI désélectionne automatiquement
```

### Test 5: Contrôles Globaux vs Individuels
```
1. Créer 5 projectiles
2. Lancer 3 avec bouton individuel
3. Cliquer "Lancer" global
✓ Les 2 non lancés démarrent
✓ Les 3 déjà lancés continuent
```

---

**Documentation Technique - Simulateur Balistique**
*Architecture et Flux de Données*
