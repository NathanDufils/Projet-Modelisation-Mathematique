# Simulateur Balistique - Projet de Modélisation Mathématique

Un simulateur interactif pour étudier la trajectoire de projectiles avec différents paramètres physiques.

## Fonctionnalités

- **Simulation en temps réel** : Visualisation de la trajectoire d'un projectile
- **Interface interactive** : Sliders pour ajuster les paramètres en temps réel
- **Physique réaliste** : Calculs balistiques avec ou sans résistance de l'air
- **Visualisation** : Affichage de la trajectoire, du vecteur vitesse et des informations en temps réel

## Paramètres ajustables

- **Vitesse initiale** (10-200 m/s)
- **Angle de tir** (0-90°)
- **Masse du projectile** (0.1-10 kg)
- **Coefficient de traînée** (0.0-1.0)

## Installation

1. Installer les dépendances :

```bash
pip install -r requirements.txt
```

2. Lancer la simulation :

```bash
python main.py
```

## Structure du projet

```
src/
├── simulation.py    # Classe principale de simulation
├── projectile.py    # Classe du projectile
├── physics.py       # Calculs physiques et balistiques
├── ui.py           # Interface utilisateur (sliders, boutons)
└── settings.py     # Configuration et constantes
```

## Contrôles

- **Sliders** : Ajustez les paramètres en temps réel
- **Reset** : Redémarre la simulation avec les nouveaux paramètres
- **Pause/Resume** : Met en pause ou reprend la simulation
- **Fermer** : Cliquez sur la croix pour quitter

## Physique implémentée

- Trajectoire parabolique classique (sans résistance de l'air)
- Approximation de la résistance de l'air avec coefficient de traînée
- Calculs de portée, hauteur maximale et temps de vol
