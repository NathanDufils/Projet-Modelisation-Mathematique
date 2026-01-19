# Simulateur Balistique Multi-Projectiles

Un simulateur interactif de trajectoires balistiques avec prise en compte de la physique réaliste (gravité, résistance de l'air, vent).

## 📚 Navigation

> **Documentation Complète** : [docs/INDEX.md](docs/INDEX.md) - Table des matières de toute la documentation  
> **Structure du Projet** : [STRUCTURE.md](STRUCTURE.md) - Vue visuelle de l'organisation  
> **Organisation** : [ORGANISATION_DOCS.md](ORGANISATION_DOCS.md) - Comment naviguer dans les docs

## 🚀 Démarrage Rapide

**Nouveau ?** → Lisez **[docs/DEMARRAGE_RAPIDE.md](docs/DEMARRAGE_RAPIDE.md)** pour commencer en 3 minutes !

```bash
# Installation
pip install pygame

# Lancement
python main.py
```

---

## 🎯 Fonctionnalités

### Gestion des Projectiles
- **Ajout multiple** : Créez plusieurs projectiles avec des paramètres différents
- **Contrôle individuel** : Chaque projectile peut être contrôlé indépendamment ⭐
  - Lancer un projectile spécifique 🟢
  - Mettre en pause individuellement 🟡
  - Réinitialiser un projectile 🔵
  - Supprimer un projectile 🔴
  - **[Guide détaillé](GESTION_INDEPENDANTE.md)**
- **Contrôle global** : Actions sur tous les projectiles simultanément
  - Lancer tous les projectiles non lancés
  - Réinitialiser tous les projectiles
  - Effacer tous les projectiles
- **Sélection** : Cliquez sur un projectile pour le sélectionner et modifier ses paramètres
- **Déplacement** : Glissez-déposez les projectiles non lancés pour changer leur position de départ

### Paramètres du Projectile
- **Vitesse initiale** (0-500 m/s) : Contrôle la vitesse de lancement
- **Angle de tir** (0-360°) : Direction du lancement
- **Masse** (0.001-100 kg) : Influence l'inertie et l'effet de la traînée
- **Rayon** (1-100 cm) : Détermine la surface exposée à la résistance de l'air

### Paramètres Environnementaux
- **Gravité** (0.1-20 m/s²) : Modifiable pour simuler différentes planètes
- **Densité de l'air** (0-2 kg/m³) : Contrôle l'intensité de la résistance de l'air
- **Vent** :
  - Vitesse (0-50 m/s)
  - Direction (0-360°) via un compas interactif

### Visualisation
- **Trajectoires** : Affichage en temps réel du chemin parcouru
- **Indicateurs** : Vecteurs de vitesse et angle de tir pour les projectiles non lancés
- **Grille de référence** : Pour une meilleure perception des distances
- **Indicateurs de vent** : Flèches montrant la direction et l'intensité du vent
- **Statut en temps réel** : Position, vitesse, temps de vol
- **Indicateurs d'état** : Couleurs différentes selon l'état du projectile
  - 🔵 Bleu : Prêt (non lancé)
  - 🟢 Vert : En vol
  - 🟡 Jaune : En pause
  - 🔴 Rouge : Terminé

## 🎮 Utilisation

### Contrôles de Base

1. **Ajouter un projectile** : Cliquez sur "Ajouter" dans le panneau "Environnement"
2. **Sélectionner un projectile** : Cliquez sur un projectile dans la zone de simulation
3. **Modifier les paramètres** : Utilisez les sliders du panneau "Objet sélectionné"
4. **Déplacer un projectile** : Glissez-déposez un projectile non lancé

### Contrôles Individuels (Panneau "Objet sélectionné")

Lorsqu'un projectile est sélectionné, vous pouvez :
- **Lancer** : Lance uniquement ce projectile
- **Pause** : Met en pause/reprend uniquement ce projectile
- **Réinit.** : Remet ce projectile à sa position initiale
- **Suppr.** : Supprime ce projectile de la simulation

### Contrôles Globaux (Panneau "Environnement")

- **Ajouter** : Crée un nouveau projectile
- **Lancer** : Lance tous les projectiles non lancés / Reprend tous les projectiles en pause
- **Réinitialiser** : Remet tous les projectiles à leur état initial
- **Effacer** : Supprime tous les projectiles

### Scénarios d'Utilisation

#### Comparaison de Trajectoires
1. Ajoutez plusieurs projectiles
2. Positionnez-les au même endroit
3. Modifiez un paramètre pour chaque (ex: différents angles)
4. Lancez-les tous simultanément pour comparer

#### Simulation Séquentielle
1. Ajoutez plusieurs projectiles avec des paramètres différents
2. Sélectionnez et lancez-les un par un
3. Observez chaque trajectoire individuellement

#### Expérimentation Interactive
1. Ajoutez un projectile et lancez-le
2. Mettez-le en pause à mi-parcours
3. Modifiez les paramètres environnementaux
4. Reprenez pour observer l'effet

## 📦 Installation

### Prérequis
- Python 3.8 ou supérieur
- pip

### Installation des Dépendances

```bash
pip install -r requirements.txt
```

Ou manuellement :
```bash
pip install pygame
```

## 🚀 Lancement

```bash
python main.py
```

## 📁 Structure du Projet

```
Projet-Modelisation-Mathematique/
│
├── main.py                          # Point d'entrée du programme
├── requirements.txt                 # Dépendances Python
├── README.md                        # Ce fichier
│
├── docs/                            # 📚 Documentation complète
│   ├── INDEX.md                     # Navigation dans la documentation
│   ├── DEMARRAGE_RAPIDE.md          # Guide de démarrage (3 min)
│   ├── RESUME.md                    # Vue d'ensemble (5 min)
│   ├── GUIDE_UTILISATION.md         # Manuel utilisateur détaillé
│   ├── DOCUMENTATION_MATHEMATIQUES.md # Toutes les équations et formules
│   ├── ARCHITECTURE.md              # Structure technique du code
│   └── CHANGEMENTS.md               # Historique des modifications
│
└── src/                             # 💻 Code source
    ├── simulation.py                # Boucle principale et gestion des événements
    ├── projectile.py                # Classe Projectile avec gestion d'état
    ├── physics.py                   # Calculs physiques et intégration numérique
    ├── ui.py                        # Interface utilisateur (sliders, boutons, panneaux)
    └── settings.py                  # Constantes et configuration
```

## 🔬 Modèle Physique

Le simulateur implémente un modèle balistique réaliste avec :

### Forces Appliquées
1. **Gravité** : $\vec{F}_g = m \cdot g \cdot \vec{e}_y$
2. **Traînée aérodynamique** : $\vec{F}_d = -\frac{1}{2} \rho \cdot C_d \cdot A \cdot |\vec{v}_{rel}| \cdot \vec{v}_{rel}$
3. **Influence du vent** : Modifie la vitesse relative pour le calcul de traînée

### Méthode d'Intégration
- **Euler semi-implicite** (symplectique) pour une meilleure conservation de l'énergie
- Pas de temps : 1/FPS (typiquement 1/60 s)

### Détails Mathématiques
Consultez **[docs/DOCUMENTATION_MATHEMATIQUES.md](docs/DOCUMENTATION_MATHEMATIQUES.md)** pour :
- Équations différentielles complètes
- Dérivation des formules
- Formules analytiques (cas sans résistance)
- Exemples de calculs
- Validation du modèle
- Références bibliographiques

## ⚙️ Configuration

Les paramètres par défaut peuvent être modifiés dans `src/settings.py` :

```python
# Physique
GRAVITY = 9.81          # m/s²
AIR_DENSITY = 1.225     # kg/m³
DRAG_COEFFICIENT = 0.47 # Sphère lisse
WIND_SPEED = 0.0        # m/s
WIND_DIRECTION = 0.0    # degrés

# Simulation
FPS = 60                # Images par seconde
TIME_STEP = 1.0 / FPS   # Pas de temps

# Affichage
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
SCALE = 1.0             # Échelle d'affichage
```

## 🎓 Contexte Pédagogique

Ce projet a été développé dans le cadre du cours de **Modélisation Mathématique** (S5) et illustre :

### Concepts Mathématiques
- Équations différentielles du second ordre
- Systèmes dynamiques
- Intégration numérique
- Méthodes symplectiques
- Analyse vectorielle

### Concepts Physiques
- Cinématique et dynamique
- Mécanique des fluides (traînée)
- Forces conservatives et dissipatives
- Conditions initiales et conditions aux limites

### Concepts Informatiques
- Programmation orientée objet
- Architecture MVC (Modèle-Vue-Contrôleur)
- Boucle de jeu temps réel
- Interface utilisateur interactive
- Gestion d'état

## 🐛 Résolution de Problèmes

### Le projectile disparaît instantanément
- Vérifiez que la vitesse initiale n'est pas trop élevée
- Réduisez la densité de l'air si elle est trop importante
- Vérifiez que le rayon n'est pas trop grand

### La simulation est lente
- Réduisez le nombre de projectiles actifs
- Vérifiez que le FPS cible est raisonnable (60)

### Les trajectoires semblent incorrectes
- Consultez **[docs/DOCUMENTATION_MATHEMATIQUES.md](docs/DOCUMENTATION_MATHEMATIQUES.md)** pour valider les équations
- Vérifiez que les unités sont cohérentes
- Testez avec la traînée désactivée (rayon = 0) pour comparer avec la théorie

## 📚 Références

### Documentation Complète
**Toute la documentation est dans le dossier `docs/` :**
- **[docs/INDEX.md](docs/INDEX.md)** - Table des matières
- **[docs/DEMARRAGE_RAPIDE.md](docs/DEMARRAGE_RAPIDE.md)** - Démarrage en 3 étapes
- **[docs/GUIDE_UTILISATION.md](docs/GUIDE_UTILISATION.md)** - Manuel utilisateur
- **[docs/DOCUMENTATION_MATHEMATIQUES.md](docs/DOCUMENTATION_MATHEMATIQUES.md)** - Toutes les équations
- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** - Structure technique

### Bibliothèques Utilisées
- [Pygame](https://www.pygame.org/) : Bibliothèque de développement de jeux en Python

### Ressources Pédagogiques
- Khan Academy - Projectile Motion
- MIT OpenCourseWare - Classical Mechanics
- The Physics Classroom - 2D Kinematics

## 👥 Auteurs

Projet réalisé dans le cadre du cours de Modélisation Mathématique (S5)

## 📝 Licence

Ce projet est développé à des fins éducatives.

---

## 🎯 Objectifs Pédagogiques Atteints

✅ Modélisation d'un système physique réel  
✅ Résolution numérique d'équations différentielles  
✅ Implémentation d'une méthode d'intégration stable  
✅ Validation par comparaison avec solutions analytiques  
✅ Interface utilisateur interactive pour l'expérimentation  
✅ Gestion d'état complexe (multi-projectiles indépendants)  
✅ Documentation mathématique rigoureuse  

---

**🚀 Bon vol balistique !**
