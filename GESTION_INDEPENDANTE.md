# ✅ Fonctionnalités de Gestion Indépendante des Projectiles

## 🎯 Contrôle Complet de Chaque Projectile

Le simulateur permet une gestion **totalement indépendante** de chaque projectile :

### ✨ Actions Individuelles Disponibles

Lorsqu'un projectile est sélectionné (clic dessus), vous pouvez :

#### 🟢 Lancer
- **Action** : Lance uniquement le projectile sélectionné
- **Bouton** : "Lancer" (vert) dans le panneau "Objet sélectionné"
- **Utilisation** : Démarrer la trajectoire de ce projectile sans affecter les autres

#### 🟡 Pause / Reprendre
- **Action** : Met en pause ou reprend uniquement le projectile sélectionné
- **Bouton** : "Pause" (jaune) dans le panneau "Objet sélectionné"
- **Utilisation** : Geler le mouvement pour examiner ou modifier l'environnement

#### 🔵 Réinitialiser
- **Action** : Remet uniquement le projectile sélectionné à sa position initiale
- **Bouton** : "Réinit." (bleu) dans le panneau "Objet sélectionné"
- **Utilisation** : Recommencer avec le même projectile

#### 🔴 Supprimer
- **Action** : Efface uniquement le projectile sélectionné de la simulation
- **Bouton** : "Suppr." (rouge) dans le panneau "Objet sélectionné"
- **Utilisation** : Nettoyer les projectiles inutiles sans tout effacer

---

## 🎮 Exemple d'Utilisation Pratique

### Scénario : Comparer 3 Angles Différents

```
1. Créer 3 projectiles
   - Clic "Ajouter" × 3

2. Configurer chaque projectile individuellement
   - Clic sur projectile 1 → Angle = 30°
   - Clic sur projectile 2 → Angle = 45°
   - Clic sur projectile 3 → Angle = 60°

3. Lancer tous ensemble
   - Clic "Lancer" (bouton global)

4. Observer les résultats

5. Ajuster si nécessaire
   - Clic sur projectile 2
   - Clic "Pause" (individuel)
   - Modifier paramètres
   - Clic "Pause" pour reprendre

6. Nettoyer
   - Clic sur projectile 1
   - Clic "Suppr." (individuel)
   - Projectile 1 disparaît, les autres restent
```

---

## 🔄 Différences Contrôles Globaux vs Individuels

### Contrôles Globaux (Panneau "Environnement")

| Action | Effet |
|--------|-------|
| **Ajouter** | Crée UN nouveau projectile |
| **Lancer** | Lance TOUS les projectiles non lancés |
| **Réinitialiser** | Remet TOUS les projectiles à zéro |
| **Effacer** | Supprime TOUS les projectiles |

### Contrôles Individuels (Panneau "Objet sélectionné") ⭐

| Action | Effet |
|--------|-------|
| **Lancer** | Lance UNIQUEMENT le projectile sélectionné |
| **Pause** | Pause/Reprend UNIQUEMENT le projectile sélectionné |
| **Réinit.** | Réinitialise UNIQUEMENT le projectile sélectionné |
| **Suppr.** | Supprime UNIQUEMENT le projectile sélectionné |

---

## 📊 États Possibles d'un Projectile

Chaque projectile peut être dans l'un de ces états :

| État | Couleur | Description | Actions Possibles |
|------|---------|-------------|-------------------|
| **Prêt** | 🔵 Bleu | Non lancé | Lancer, Supprimer, Modifier paramètres |
| **En vol** | 🟢 Vert | En mouvement | Pause, Modifier masse/rayon |
| **En pause** | 🟡 Jaune | Figé temporairement | Reprendre, Réinitialiser, Modifier |
| **Terminé** | 🔴 Rouge | A atteint le sol | Réinitialiser, Supprimer |

---

## 💡 Cas d'Usage Avancés

### 1. Test Itératif
```
Ajoutez un projectile
→ Lancez-le (individuel)
→ Observez la trajectoire
→ Réinitialisez-le (individuel)
→ Ajustez les paramètres
→ Relancez-le (individuel)
→ Répétez jusqu'à satisfaction
```

### 2. Comparaison Séquentielle
```
Ajoutez projectile A avec vitesse 50 m/s
→ Lancez A (individuel)
→ Laissez-le terminer
Ajoutez projectile B avec vitesse 100 m/s
→ Lancez B (individuel)
→ Comparez visuellement les deux trajectoires
```

### 3. Expérimentation Interactive
```
Lancez un projectile
→ Mettez-le en pause en plein vol (individuel)
→ Modifiez le vent
→ Reprenez-le (individuel)
→ Observez le changement de trajectoire
```

### 4. Nettoyage Sélectif
```
Vous avez 5 projectiles
→ 3 sont terminés, 2 sont en vol
→ Sélectionnez les projectiles terminés un par un
→ Supprimez-les individuellement (bouton Suppr.)
→ Les 2 en vol continuent normalement
```

---

## ⚙️ Implémentation Technique

### Fichiers Modifiés

**`src/simulation.py`**
```python
# Gestion des actions individuelles ajoutée
elif action == 'launch_selected':
    if self.ui.selected_projectile:
        self.ui.selected_projectile.launch()

elif action == 'pause_selected':
    if self.ui.selected_projectile:
        self.ui.selected_projectile.pause()

elif action == 'reset_selected':
    if self.ui.selected_projectile:
        self.ui.selected_projectile.reset()

elif action == 'delete_selected':
    if self.ui.selected_projectile:
        self.projectiles.remove(self.ui.selected_projectile)
        self.select_projectile(None)
```

**`src/ui.py`**
```python
# Nouveaux boutons dans ObjectPanel
self.buttons = {
    'launch_selected': Button(..., "Lancer", (150, 255, 150)),  # Vert
    'pause_selected': Button(..., "Pause", (255, 255, 150)),    # Jaune
    'reset_selected': Button(..., "Réinit.", (150, 200, 255)),  # Bleu
    'delete_selected': Button(..., "Suppr.", (255, 150, 150))   # Rouge
}
```

---

## 🎯 Avantages de la Gestion Indépendante

### ✅ Flexibilité
- Contrôlez précisément chaque projectile
- Expérimentez avec différents paramètres
- Comparez plusieurs scénarios simultanément

### ✅ Pédagogie
- Isolez les variables pour mieux comprendre
- Testez des hypothèses spécifiques
- Analysez les trajectoires individuellement

### ✅ Efficacité
- Pas besoin de tout réinitialiser
- Supprimez seulement ce qui est inutile
- Ajustez en temps réel

### ✅ Interactivité
- Pause pour examiner en détail
- Modifiez l'environnement en cours de vol
- Itérez rapidement sur vos tests

---

## 📚 Documentation Complète

Pour plus de détails, consultez :
- **[docs/GUIDE_UTILISATION.md](docs/GUIDE_UTILISATION.md)** - Scénarios détaillés
- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** - Détails techniques
- **[docs/INDEX.md](docs/INDEX.md)** - Navigation complète

---

**La gestion indépendante des projectiles est entièrement fonctionnelle ! 🚀**
