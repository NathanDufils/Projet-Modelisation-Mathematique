# Guide de Démarrage Rapide

## Installation & Lancement en 3 Étapes

### 1. Installer les Dépendances
```bash
pip install pygame
```

### 2. Lancer le Simulateur
```bash
python main.py
```

### 3. Créer Votre Premier Projectile
1. Cliquez sur **"Ajouter"** (panneau Environnement)
2. Ajustez les paramètres avec les sliders
3. Cliquez sur **"Lancer"** (panneau Environnement)
4. Observez la trajectoire !

---

## Actions Rapides

### Gestion Globale (Panneau "Environnement")
- `Ajouter` : Crée un nouveau projectile
- `Lancer` : Lance tous les projectiles / Met tous en pause
- `Réinitialiser` : Reset tous les projectiles
- `Effacer` : Supprime tous les projectiles

### Gestion Individuelle (Panneau "Objet sélectionné")
1. **Cliquez sur un projectile** pour le sélectionner
2. Utilisez les boutons :
   - `Réinit.` (Bleu) : Reset ce projectile
   - `Suppr.` (Rouge) : Supprime ce projectile

---

## Expériences Rapides

### Test 1 : Trajectoire Simple (30 secondes)
```
1. Ajouter un projectile
2. Vitesse = 100 m/s, Angle = 45°
3. Lancer (global)
4. Observer !
```

### Test 2 : Comparaison d'Angles (1 minute)
```
1. Ajouter 3 projectiles
2. Glisser-déposer au même endroit
3. Angles : 30°, 45°, 60°
4. Lancer (global)
5. Comparer les portées !
```

### Test 3 : Effet du Vent (1 minute)
```
1. Ajouter un projectile
2. Vent : Vitesse = 20 m/s, Direction = 0° (droite)
3. Lancer
4. Observer la déviation !
```

### Test 4 : Résistance de l'Air (2 minutes)
```
1. Ajouter 2 projectiles
2. Projectile A : Rayon = 1 cm (petit)
3. Projectile B : Rayon = 50 cm (gros)
4. Même vitesse et angle
5. Lancer les deux
6. Le gros ralentit plus vite !
```

---

## Documentation

| Fichier | Contenu |
|---------|---------|
| **README.md** | Documentation complète du projet |
| **GUIDE_UTILISATION.md** | Mode d'emploi détaillé avec scénarios |
| **DOCUMENTATION_MATHEMATIQUES.md** | Toutes les équations et formules |
| **ARCHITECTURE.md** | Structure technique du code |

---

## Raccourcis Clavier

*Actuellement, le simulateur utilise uniquement la souris*

---

## Paramètres Recommandés

### Pour une Trajectoire Visible
- Vitesse : 50-150 m/s
- Angle : 30-60°
- Masse : 1-10 kg
- Rayon : 5-20 cm
- Gravité : 9.81 m/s²

### Pour Tester la Résistance de l'Air
- Rayon : 50+ cm (gros objet)
- Densité de l'air : 1.225 kg/m³
- Observez la différence !

### Pour Simuler l'Espace (Pas d'Atmosphère)
- Gravité : 1.62 m/s² (Lune) ou 3.71 m/s² (Mars)
- Densité de l'air : 0 kg/m³
- Trajectoires paraboliques parfaites !

---

## Résolution Rapide

| Problème | Solution |
|----------|----------|
| Projectile ne bouge pas | Vérifier vitesse > 0 et pas en pause |
| Disparaît trop vite | Réduire densité air ou rayon |
| Simulation lente | Supprimer les projectiles inutiles |
| Paramètres bloqués | Réinitialiser avant de modifier |

---

## Conseil Pro

**Utilisez la pause globale pour examiner vos projectiles !**
1. Lancez vos projectiles
2. Cliquez "Lancer" (Global) pour mettre en pause
3. Sélectionnez un projectile pour voir ses détails
4. Cliquez "Lancer" (Global) pour reprendre

---

## Pour Aller Plus Loin

### Comprendre les Maths
→ Lisez **DOCUMENTATION_MATHEMATIQUES.md**
- Équations de Newton
- Force de traînée
- Méthode d'Euler semi-implicite

### Maîtriser le Simulateur
→ Lisez **GUIDE_UTILISATION.md**
- Scénarios détaillés
- Expériences suggérées
- Astuces avancées

### Explorer le Code
→ Lisez **ARCHITECTURE.md**
- Structure du projet
- Flux de données
- Diagrammes

---

**C'est parti ! Amusez-vous bien !**

*Projet de Modélisation Mathématique - S5*
