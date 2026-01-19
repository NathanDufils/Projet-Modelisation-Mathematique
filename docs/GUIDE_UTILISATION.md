# Guide d'Utilisation - Contrôle Individuel des Projectiles

## 🎯 Nouveautés

Le simulateur permet maintenant de **gérer chaque projectile indépendamment** ! Vous pouvez lancer, mettre en pause et réinitialiser chaque projectile séparément.

## 📋 Panneau "Objet sélectionné"

Lorsque vous sélectionnez un projectile (en cliquant dessus), le panneau "Objet sélectionné" affiche :

### Indicateur de Statut
- **🔵 Prêt** : Le projectile n'a pas encore été lancé
- **🟢 En vol** : Le projectile est en mouvement
- **🟡 En pause** : Le projectile est en pause
- **🔴 Terminé** : Le projectile a terminé sa trajectoire

### Boutons de Contrôle Individuel

#### 🚀 Lancer
- Lance uniquement le projectile sélectionné
- Disponible uniquement si le projectile n'est pas déjà lancé ou s'il est en pause

#### ⏸️ Pause
- Met en pause ou reprend uniquement le projectile sélectionné
- Le projectile reste visible mais ne bouge plus
- Vous pouvez modifier les paramètres environnementaux pendant la pause

#### 🔄 Réinit.
- Remet le projectile sélectionné à sa position initiale
- Efface sa trajectoire
- Le projectile revient à l'état "Prêt"

#### ❌ Suppr.
- Supprime le projectile sélectionné de la simulation
- Attention : cette action est irréversible !

## 🎮 Scénarios d'Utilisation

### Scénario 1 : Comparaison d'Angles

**Objectif** : Comparer l'effet de différents angles de tir

1. Cliquez sur "Ajouter" 3 fois pour créer 3 projectiles
2. Positionnez-les tous au même endroit (glisser-déposer)
3. Pour chaque projectile :
   - Cliquez dessus pour le sélectionner
   - Ajustez l'angle (ex: 30°, 45°, 60°)
   - Gardez les autres paramètres identiques
4. Cliquez sur "Lancer" (panneau Environnement) pour lancer tous les projectiles simultanément
5. Observez les différentes trajectoires !

### Scénario 2 : Expérimentation Séquentielle

**Objectif** : Tester différentes vitesses l'une après l'autre

1. Ajoutez un projectile
2. Réglez une vitesse (ex: 50 m/s)
3. Cliquez sur "Lancer" dans le panneau "Objet sélectionné"
4. Observez la trajectoire complète
5. Ajoutez un nouveau projectile
6. Réglez une vitesse différente (ex: 100 m/s)
7. Lancez-le individuellement
8. Comparez les deux trajectoires côte à côte

### Scénario 3 : Effet du Vent en Temps Réel

**Objectif** : Voir l'effet d'un changement de vent pendant le vol

1. Ajoutez un projectile et configurez-le
2. Cliquez sur "Lancer" (individuel)
3. Pendant le vol, cliquez sur "Pause" (individuel)
4. Modifiez la direction ou la vitesse du vent
5. Cliquez à nouveau sur "Pause" pour reprendre
6. Le projectile continue avec les nouvelles conditions de vent !

### Scénario 4 : Raffinement Itératif

**Objectif** : Ajuster les paramètres pour atteindre une cible

1. Ajoutez un projectile
2. Lancez-le individuellement
3. Observez où il atterrit
4. Cliquez sur "Réinit." (individuel)
5. Ajustez les paramètres (angle, vitesse)
6. Relancez-le
7. Répétez jusqu'à atteindre votre objectif !

## 🔄 Différences entre Contrôles Globaux et Individuels

### Contrôles Globaux (Panneau "Environnement")

| Bouton | Action |
|--------|--------|
| **Lancer** | Lance TOUS les projectiles non lancés / Reprend TOUS les projectiles en pause |
| **Réinitialiser** | Remet TOUS les projectiles à leur état initial |
| **Effacer** | Supprime TOUS les projectiles |

### Contrôles Individuels (Panneau "Objet sélectionné")

| Bouton | Action |
|--------|--------|
| **Lancer** | Lance uniquement le projectile SÉLECTIONNÉ |
| **Pause** | Met en pause/reprend uniquement le projectile SÉLECTIONNÉ |
| **Réinit.** | Remet uniquement le projectile SÉLECTIONNÉ à son état initial |
| **Suppr.** | Supprime uniquement le projectile SÉLECTIONNÉ |

## 💡 Astuces

### Gestion Multiple
- Vous pouvez avoir plusieurs projectiles en vol simultanément
- Certains peuvent être en pause pendant que d'autres bougent
- Chaque projectile conserve ses propres paramètres

### Modification des Paramètres
- **Avant le lancement** : Tous les paramètres sont modifiables
- **Pendant le vol** : Seuls la masse et le rayon peuvent être modifiés
- **En pause** : Tous les paramètres restent modifiables
- **Les paramètres environnementaux** (gravité, air, vent) affectent tous les projectiles actifs

### Couleurs et Sélection
- **Projectile sélectionné** : Entouré d'une bordure verte
- **Projectile non sélectionné** : Couleur rouge normale
- **Trajectoire** : Ligne bleue indiquant le chemin parcouru

### Performance
- Plus vous avez de projectiles actifs, plus le calcul peut ralentir
- Si la simulation ralentit, essayez de :
  - Supprimer les projectiles terminés
  - Utiliser le bouton "Effacer" pour tout recommencer

## 🎓 Expériences Suggérées

### Expérience 1 : Angle Optimal
**Question** : Quel angle donne la portée maximale ?
- Sans résistance de l'air (rayon = 0 ou densité = 0) : 45°
- Avec résistance de l'air : < 45° (à tester !)

### Expérience 2 : Masse et Résistance
**Question** : Comment la masse affecte-t-elle la trajectoire ?
- Créez plusieurs projectiles avec des masses différentes mais même rayon
- Lancez-les tous et observez

### Expérience 3 : Vitesse Terminale
**Question** : Un objet peut-il atteindre une vitesse limite en chute ?
- Lancez un projectile verticalement vers le haut (angle = 90°)
- Observez la vitesse pendant la descente
- Elle devrait se stabiliser (vitesse terminale)

### Expérience 4 : Effet du Vent
**Question** : Comment le vent affecte-t-il les différents projectiles ?
- Créez des projectiles de tailles différentes
- Ajoutez du vent fort (ex: 20 m/s)
- Les petits projectiles sont-ils plus affectés ?

## 🐞 Cas Particuliers

### Projectile Immobile
Si un projectile ne bouge pas après avoir cliqué sur "Lancer" :
- Vérifiez que la vitesse initiale n'est pas nulle
- Assurez-vous que le projectile n'est pas en pause
- Vérifiez que la gravité n'est pas nulle

### Trajectoire Courte
Si le projectile disparaît rapidement :
- La résistance de l'air est peut-être trop forte (réduire densité ou rayon)
- La vitesse initiale est peut-être trop faible
- Vérifiez que le projectile n'est pas sorti de la zone de simulation

### Modification Impossible
Si vous ne pouvez pas modifier certains paramètres :
- **Vitesse et angle** : Non modifiables pendant le vol (réinitialisez d'abord)
- **Masse et rayon** : Toujours modifiables
- **Environnement** : Toujours modifiable

## 📖 Pour Aller Plus Loin

Consultez `DOCUMENTATION_MATHEMATIQUES.md` pour :
- Les équations complètes du modèle physique
- Les formules analytiques
- La validation du modèle
- Les références bibliographiques

---

**Amusez-vous bien avec le simulateur ! 🚀**
