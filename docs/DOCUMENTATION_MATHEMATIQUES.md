# Documentation Mathématique - Simulateur Balistique

## Table des Matières
1. [Introduction](#introduction)
2. [Équations du Mouvement](#équations-du-mouvement)
3. [Forces Appliquées](#forces-appliquées)
4. [Méthode d'Intégration Numérique](#méthode-dintégration-numérique)
5. [Formules Analytiques](#formules-analytiques)
6. [Paramètres Physiques](#paramètres-physiques)
7. [Références](#références)

---

## Introduction

Ce simulateur modélise le mouvement balistique de projectiles dans un environnement 2D. Il prend en compte :
- La gravité terrestre
- La résistance de l'air (force de traînée)
- L'influence du vent
- Les propriétés physiques du projectile (masse, rayon)

---

## Équations du Mouvement

### Système de Coordonnées

Le simulateur utilise un système de coordonnées 2D :
- **x** : position horizontale (m)
- **y** : position verticale (m), avec y croissant vers le bas (convention écran)

### Équations Différentielles

Le mouvement du projectile est décrit par un système d'équations différentielles du second ordre :

$$
\begin{cases}
\frac{d^2x}{dt^2} = \frac{F_x}{m} = a_x \\
\frac{d^2y}{dt^2} = \frac{F_y}{m} = a_y
\end{cases}
$$

où :
- $m$ : masse du projectile (kg)
- $F_x, F_y$ : composantes de la force totale (N)
- $a_x, a_y$ : composantes de l'accélération (m/s²)

### Décomposition en Vitesse et Position

Le système peut être décomposé en équations du premier ordre :

$$
\begin{cases}
\frac{dx}{dt} = v_x \\
\frac{dy}{dt} = v_y \\
\frac{dv_x}{dt} = a_x \\
\frac{dv_y}{dt} = a_y
\end{cases}
$$

où $v_x, v_y$ sont les composantes de la vitesse (m/s).

---

## Forces Appliquées

### 1. Force de Gravité

La gravité est modélisée comme une force constante dirigée vers le bas :

$$
\vec{F}_g = m \cdot g \cdot \vec{e}_y
$$

où :
- $g$ : accélération gravitationnelle (m/s²), typiquement 9.81 m/s²
- $\vec{e}_y$ : vecteur unitaire vertical pointant vers le bas

**Composantes :**
$$
\begin{cases}
F_{g,x} = 0 \\
F_{g,y} = m \cdot g
\end{cases}
$$

### 2. Force de Traînée Aérodynamique

La force de traînée s'oppose au mouvement relatif du projectile par rapport à l'air :

$$
\vec{F}_d = -\frac{1}{2} \rho \cdot C_d \cdot A \cdot |\vec{v}_{rel}| \cdot \vec{v}_{rel}
$$

où :
- $\rho$ : densité de l'air (kg/m³), environ 1.225 kg/m³ au niveau de la mer
- $C_d$ : coefficient de traînée (sans dimension), environ 0.47 pour une sphère
- $A$ : aire de la section transversale du projectile (m²)
- $\vec{v}_{rel}$ : vitesse relative du projectile par rapport à l'air (m/s)

#### Calcul de la Vitesse Relative

La vitesse relative prend en compte le vent :

$$
\vec{v}_{rel} = \vec{v}_{projectile} - \vec{v}_{vent}
$$

**Composantes du vent :**
$$
\begin{cases}
v_{vent,x} = V_{vent} \cdot \cos(\theta_{vent}) \\
v_{vent,y} = -V_{vent} \cdot \sin(\theta_{vent})
\end{cases}
$$

où $\theta_{vent}$ est la direction du vent en radians (0° = Est, 90° = Nord).

#### Aire de la Section Transversale

Pour un projectile sphérique de rayon $r$ :

$$
A = \pi r^2
$$

#### Magnitude de la Force de Traînée

La magnitude de la force de traînée est :

$$
F_d = \frac{1}{2} \rho \cdot C_d \cdot A \cdot v_{rel}^2
$$

où $v_{rel} = \sqrt{v_{rel,x}^2 + v_{rel,y}^2}$ est la norme de la vitesse relative.

#### Composantes de la Force de Traînée

La force de traînée est dirigée dans le sens opposé à la vitesse relative :

$$
\begin{cases}
F_{d,x} = -F_d \cdot \frac{v_{rel,x}}{v_{rel}} \\
F_{d,y} = -F_d \cdot \frac{v_{rel,y}}{v_{rel}}
\end{cases}
$$

### 3. Force Totale

La force totale appliquée au projectile est la somme vectorielle :

$$
\vec{F}_{total} = \vec{F}_g + \vec{F}_d
$$

**Composantes :**
$$
\begin{cases}
F_x = F_{d,x} \\
F_y = m \cdot g + F_{d,y}
\end{cases}
$$

---

## Méthode d'Intégration Numérique

### Méthode d'Euler Semi-Implicite (Symplectique)

Le simulateur utilise la méthode d'Euler semi-implicite, qui est plus stable que la méthode d'Euler explicite pour les systèmes conservatifs.

**Algorithme :**

À chaque pas de temps $\Delta t$ :

1. **Calcul de l'accélération** à partir de la position et vitesse actuelles :
   $$
   \begin{cases}
   a_x = \frac{F_x(x, y, v_x, v_y)}{m} \\
   a_y = \frac{F_y(x, y, v_x, v_y)}{m}
   \end{cases}
   $$

2. **Mise à jour de la vitesse** (méthode explicite pour l'accélération) :
   $$
   \begin{cases}
   v_x^{n+1} = v_x^n + a_x \cdot \Delta t \\
   v_y^{n+1} = v_y^n + a_y \cdot \Delta t
   \end{cases}
   $$

3. **Mise à jour de la position** (méthode implicite pour la vitesse) :
   $$
   \begin{cases}
   x^{n+1} = x^n + v_x^{n+1} \cdot \Delta t \\
   y^{n+1} = y^n + v_y^{n+1} \cdot \Delta t
   \end{cases}
   $$

### Avantages de la Méthode Semi-Implicite

- **Stabilité** : Meilleure conservation de l'énergie pour les systèmes conservatifs
- **Précision** : Erreur de l'ordre de $O(\Delta t^2)$ pour la trajectoire
- **Simplicité** : Facile à implémenter et peu coûteuse en calcul

### Pas de Temps

Le pas de temps est défini par :

$$
\Delta t = \frac{1}{\text{FPS}}
$$

où FPS est le nombre d'images par seconde (typiquement 60).

---

## Formules Analytiques

### Cas Sans Résistance de l'Air

Lorsque la résistance de l'air est négligeable ($\rho = 0$ ou $r = 0$), le mouvement devient celui d'un projectile en chute libre.

#### Conditions Initiales

- Position initiale : $(x_0, y_0)$
- Vitesse initiale : $v_0$ à un angle $\alpha$ (positif vers le haut)
  $$
  \begin{cases}
  v_{x,0} = v_0 \cdot \cos(\alpha) \\
  v_{y,0} = -v_0 \cdot \sin(\alpha)
  \end{cases}
  $$
  (Note : $v_{y,0}$ est négatif car l'angle est mesuré depuis l'horizontale vers le haut, mais y augmente vers le bas)

#### Équations du Mouvement

$$
\begin{cases}
x(t) = x_0 + v_{x,0} \cdot t \\
y(t) = y_0 + v_{y,0} \cdot t + \frac{1}{2} g \cdot t^2
\end{cases}
$$

$$
\begin{cases}
v_x(t) = v_{x,0} \\
v_y(t) = v_{y,0} + g \cdot t
\end{cases}
$$

#### Portée Théorique

La portée horizontale $R$ (distance parcourue lorsque le projectile retombe à la hauteur initiale $y = y_0$) est :

$$
R = \frac{v_0^2 \cdot \sin(2\alpha)}{g}
$$

Cette formule est valable pour un lancement et un atterrissage à la même altitude.

#### Hauteur Maximale

La hauteur maximale $h_{max}$ atteinte par le projectile (par rapport à $y_0$) est :

$$
h_{max} = \frac{v_{y,0}^2}{2g} = \frac{(v_0 \cdot \sin(\alpha))^2}{2g}
$$

#### Temps de Vol

Le temps de vol total $T$ (temps pour revenir à la hauteur initiale) est :

$$
T = \frac{2 v_0 \cdot \sin(\alpha)}{g}
$$

Pour un lancement depuis une hauteur $h$ au-dessus du sol :

$$
T = \frac{-v_{y,0} + \sqrt{v_{y,0}^2 + 2gh}}{g}
$$

### Angle Optimal

Pour maximiser la portée (sans résistance de l'air), l'angle optimal est :

$$
\alpha_{opt} = 45°
$$

Avec résistance de l'air, l'angle optimal est généralement inférieur à 45°.

---

## Paramètres Physiques

### Constantes Physiques

| Paramètre | Symbole | Valeur par Défaut | Unité | Description |
|-----------|---------|-------------------|-------|-------------|
| Gravité | $g$ | 9.81 | m/s² | Accélération gravitationnelle terrestre |
| Densité de l'air | $\rho$ | 1.225 | kg/m³ | Densité de l'air au niveau de la mer (15°C) |
| Coefficient de traînée | $C_d$ | 0.47 | - | Coefficient pour une sphère lisse |

### Paramètres du Projectile

| Paramètre | Symbole | Plage de Valeurs | Unité | Description |
|-----------|---------|------------------|-------|-------------|
| Vitesse initiale | $v_0$ | 0 - 500 | m/s | Vitesse de lancement |
| Angle de lancement | $\alpha$ | 0 - 360 | ° | Angle par rapport à l'horizontale |
| Masse | $m$ | 0.001 - 100 | kg | Masse du projectile |
| Rayon | $r$ | 0.01 - 1.0 | m | Rayon du projectile sphérique |

### Paramètres Environnementaux

| Paramètre | Symbole | Plage de Valeurs | Unité | Description |
|-----------|---------|------------------|-------|-------------|
| Vitesse du vent | $V_{vent}$ | 0 - 50 | m/s | Vitesse du vent |
| Direction du vent | $\theta_{vent}$ | 0 - 360 | ° | Direction du vent (0° = Est, 90° = Nord) |

---

## Effets de la Résistance de l'Air

### Nombre de Reynolds

Le régime d'écoulement autour du projectile peut être caractérisé par le nombre de Reynolds :

$$
Re = \frac{\rho \cdot v \cdot d}{\mu}
$$

où :
- $d = 2r$ : diamètre du projectile
- $\mu$ : viscosité dynamique de l'air ($\approx 1.81 \times 10^{-5}$ Pa·s)

Pour $Re > 10^3$, le coefficient de traînée est approximativement constant ($C_d \approx 0.47$ pour une sphère).

### Vitesse Terminale

En chute libre verticale, le projectile atteint une vitesse terminale $v_t$ lorsque la force de traînée équilibre le poids :

$$
v_t = \sqrt{\frac{2mg}{\rho \cdot C_d \cdot A}}
$$

Pour une sphère :

$$
v_t = \sqrt{\frac{2mg}{\rho \cdot C_d \cdot \pi r^2}}
$$

### Influence sur la Trajectoire

La résistance de l'air :
- **Réduit la portée** du projectile
- **Réduit la hauteur maximale** atteinte
- **Rend la trajectoire asymétrique** (descente plus raide que montée)
- **Diminue l'angle optimal** pour la portée maximale (< 45°)

---

## Exemple de Calcul

### Conditions

- Vitesse initiale : $v_0 = 50$ m/s
- Angle : $\alpha = 45°$
- Masse : $m = 1.0$ kg
- Rayon : $r = 0.1$ m (10 cm)
- Gravité : $g = 9.81$ m/s²
- Densité de l'air : $\rho = 1.225$ kg/m³
- Coefficient de traînée : $C_d = 0.47$
- Pas vent

### Sans Résistance de l'Air

**Vitesse initiale :**
$$
\begin{cases}
v_{x,0} = 50 \cdot \cos(45°) = 35.36 \text{ m/s} \\
v_{y,0} = -50 \cdot \sin(45°) = -35.36 \text{ m/s}
\end{cases}
$$

**Portée théorique :**
$$
R = \frac{50^2 \cdot \sin(90°)}{9.81} = 255 \text{ m}
$$

**Hauteur maximale :**
$$
h_{max} = \frac{35.36^2}{2 \cdot 9.81} = 63.8 \text{ m}
$$

**Temps de vol :**
$$
T = \frac{2 \cdot 50 \cdot \sin(45°)}{9.81} = 7.21 \text{ s}
$$

### Avec Résistance de l'Air

**Aire de section :**
$$
A = \pi \cdot 0.1^2 = 0.0314 \text{ m}^2
$$

**Force de traînée initiale :**
$$
F_d = \frac{1}{2} \cdot 1.225 \cdot 0.47 \cdot 0.0314 \cdot 50^2 = 22.6 \text{ N}
$$

**Vitesse terminale :**
$$
v_t = \sqrt{\frac{2 \cdot 1.0 \cdot 9.81}{1.225 \cdot 0.47 \cdot 0.0314}} = 36.9 \text{ m/s}
$$

La résistance de l'air réduira significativement la portée et la hauteur maximale par rapport aux valeurs théoriques.

---

## Limitations et Approximations

### Hypothèses du Modèle

1. **Projectile sphérique** : Le coefficient de traînée est constant ($C_d = 0.47$)
2. **Coefficient de traînée constant** : Valable pour $Re > 10^3$
3. **Air homogène** : Densité et propriétés constantes (pas de variation avec l'altitude)
4. **Gravité constante** : Néglige la variation avec l'altitude
5. **2D** : Pas de mouvement hors du plan (pas de dérive latérale complexe)
6. **Pas de rotation** : Néglige l'effet Magnus (portance due à la rotation)
7. **Pas de turbulence** : Le vent est modélisé comme un écoulement laminaire uniforme

### Améliorations Possibles

- **Coefficient de traînée variable** en fonction de $Re$ et de la vitesse
- **Modèle atmosphérique** avec variation de densité avec l'altitude
- **Effet Magnus** pour les projectiles en rotation
- **Méthode d'intégration d'ordre supérieur** (Runge-Kutta 4)
- **Modèle de vent turbulent** avec fluctuations aléatoires

---

## Références

### Littérature Scientifique

1. **Mécanique Classique**
   - Goldstein, H., Poole, C., & Safko, J. (2002). *Classical Mechanics* (3rd ed.). Addison-Wesley.

2. **Mécanique des Fluides**
   - White, F. M. (2011). *Fluid Mechanics* (7th ed.). McGraw-Hill.

3. **Balistique**
   - McCoy, R. L. (2012). *Modern Exterior Ballistics* (2nd ed.). Schiffer Publishing.

### Ressources en Ligne

- NASA Glenn Research Center - [Drag Equation](https://www.grc.nasa.gov/www/k-12/airplane/drageq.html)
- Khan Academy - [Projectile Motion](https://www.khanacademy.org/science/physics/two-dimensional-motion/two-dimensional-projectile-mot)
- Physics Classroom - [Projectile Motion](https://www.physicsclassroom.com/class/vectors/Lesson-2/Horizontally-Launched-Projectiles)

### Méthodes Numériques

1. **Intégration Numérique**
   - Press, W. H., et al. (2007). *Numerical Recipes: The Art of Scientific Computing* (3rd ed.). Cambridge University Press.

2. **Méthodes Symplectiques**
   - Hairer, E., Lubich, C., & Wanner, G. (2006). *Geometric Numerical Integration* (2nd ed.). Springer.

---

## Glossaire

| Terme | Définition |
|-------|------------|
| **Balistique** | Science qui étudie le mouvement des projectiles |
| **Traînée** | Force de résistance exercée par un fluide sur un objet en mouvement |
| **Coefficient de traînée** | Grandeur sans dimension caractérisant la résistance aérodynamique d'un objet |
| **Nombre de Reynolds** | Nombre sans dimension caractérisant le régime d'écoulement (laminaire/turbulent) |
| **Vitesse terminale** | Vitesse constante atteinte lorsque la force de traînée équilibre le poids |
| **Méthode symplectique** | Méthode d'intégration numérique qui conserve certaines propriétés géométriques du système |
| **Angle de lancement** | Angle initial entre la direction de la vitesse et l'horizontale |
| **Portée** | Distance horizontale parcourue par le projectile |
| **Effet Magnus** | Force de portance due à la rotation d'un objet en mouvement dans un fluide |

---

## Notes de Mise en Œuvre

### Fichier `physics.py`

La fonction `update_physics_step` implémente :
1. Calcul de la force de gravité : $F_y = m \cdot g$
2. Calcul de la vitesse relative par rapport au vent
3. Calcul de la force de traînée avec sa magnitude et sa direction
4. Calcul de l'accélération totale : $\vec{a} = \vec{F} / m$
5. Intégration semi-implicite pour mettre à jour vitesse et position

### Système de Coordonnées

⚠️ **Important** : Le système de coordonnées utilise la convention graphique où :
- x croît vers la droite (positif → Est)
- y croît vers le bas (positif → Sud)

Les angles sont mesurés depuis l'horizontale (Est = 0°) dans le sens anti-horaire :
- 0° = Est (droite)
- 90° = Nord (haut)
- 180° = Ouest (gauche)
- 270° = Sud (bas)

Pour la vitesse initiale, l'angle est converti en composantes avec :
- $v_x = v_0 \cdot \cos(\alpha)$
- $v_y = -v_0 \cdot \sin(\alpha)$ (négatif car l'angle positif pointe vers le haut mais y croît vers le bas)

---

## Validation du Modèle

### Tests de Cohérence

1. **Conservation de l'énergie (sans traînée)** :
   $$E = \frac{1}{2}m(v_x^2 + v_y^2) + mgy = \text{constante}$$

2. **Symétrie de la trajectoire (sans traînée)** :
   - Le temps de montée doit égaler le temps de descente
   - La trajectoire doit être une parabole symétrique

3. **Vitesse terminale (avec traînée)** :
   - En chute libre verticale, vérifier que $v \rightarrow v_t$

4. **Effet du vent** :
   - Un vent constant doit décaler horizontalement la trajectoire
   - La portée doit augmenter (vent favorable) ou diminuer (vent contraire)

### Cas Limites

1. **Rayon → 0** : Le modèle doit converger vers le mouvement sans résistance
2. **Densité → 0** : Idem (pas d'atmosphère)
3. **Angle = 0°** : Mouvement horizontal pur
4. **Angle = 90°** : Mouvement vertical pur

---

*Document rédigé pour le projet de Modélisation Mathématique - S5*
*Dernière mise à jour : Janvier 2026*
