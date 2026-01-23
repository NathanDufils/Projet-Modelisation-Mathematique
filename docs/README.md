# Documentation du Simulateur de Trajectoires Multi-Projectiles

Bienvenue dans la documentation complète du projet ! Cette documentation est organisée pour vous permettre de trouver rapidement l'information dont vous avez besoin.

## Navigation Rapide

### Je veux commencer rapidement
→ **[DEMARRAGE_RAPIDE.md](DEMARRAGE_RAPIDE.md)** (lecture : 3 minutes)
- Installation en 1 commande
- Premier projectile en 3 étapes
- Expériences rapides (30 sec à 2 min)

### Je veux apprendre à utiliser le simulateur
→ **[GUIDE_UTILISATION.md](GUIDE_UTILISATION.md)** (lecture : 10 minutes)
- Explication détaillée de tous les contrôles
- Différences entre contrôles globaux et individuels
- Scénarios pas-à-pas
- Expériences scientifiques suggérées
- Astuces et cas particuliers

### Je veux comprendre les mathématiques
→ **[DOCUMENTATION_MATHEMATIQUES.md](DOCUMENTATION_MATHEMATIQUES.md)** (lecture : 45 minutes)
- Équations différentielles du mouvement
- Forces physiques détaillées (gravité, traînée, vent)
- Méthode d'intégration numérique (Euler semi-implicite)
- Formules analytiques complètes
- Exemples de calculs numériques
- Validation et tests du modèle
- Références bibliographiques
- Glossaire des termes techniques

### Je veux comprendre le code
→ **[ARCHITECTURE.md](ARCHITECTURE.md)** (lecture : 15 minutes)
- Structure globale du projet
- Diagrammes de composants
- Flux de données et événements
- États des projectiles
- Hiérarchie des contrôles
- Tests de validation

### Je veux voir ce qui a changé
→ **[CHANGEMENTS.md](CHANGEMENTS.md)** (lecture : 8 minutes)
- Résumé de toutes les modifications
- Fichiers modifiés et créés
- Nouvelles fonctionnalités détaillées
- Statistiques du projet

### Je veux naviguer dans toute la documentation
→ **[INDEX.md](INDEX.md)**
- Table des matières complète
- Navigation par besoin
- Recherche par mot-clé
- Ordre de lecture suggéré selon profil

---

## Organisation des Fichiers

```
docs/
├── INDEX.md                          # Table des matières complète
├── DEMARRAGE_RAPIDE.md               # Démarrage en 3 minutes
├── GUIDE_UTILISATION.md              # Manuel utilisateur complet
├── DOCUMENTATION_MATHEMATIQUES.md    # Toutes les équations
├── ARCHITECTURE.md                   # Structure technique
├── CHANGEMENTS.md                    # Historique des modifications
└── README.md                         # Ce fichier
```

---

## Parcours de Lecture Recommandés

### Pour un Utilisateur Débutant (15 minutes)
1. **DEMARRAGE_RAPIDE.md** (3 min) - Lancez le simulateur
2. **GUIDE_UTILISATION.md** (12 min) - Maîtrisez les contrôles

### Pour un Étudiant en Sciences (1 heure)
1. **DEMARRAGE_RAPIDE.md** (3 min) - Installation
2. **GUIDE_UTILISATION.md** (10 min) - Utilisation
3. **DOCUMENTATION_MATHEMATIQUES.md** (45 min) - Théorie complète

### Pour un Développeur (1 heure)
1. **ARCHITECTURE.md** (15 min) - Structure du code
2. **DOCUMENTATION_MATHEMATIQUES.md** (40 min) - Modèle physique
3. **GUIDE_UTILISATION.md** (5 min) - Survol des fonctionnalités

### Pour un Enseignant (1h30)
1. **GUIDE_UTILISATION.md** (10 min) - Expériences pédagogiques
2. **DOCUMENTATION_MATHEMATIQUES.md** (45 min) - Contenu théorique
3. **ARCHITECTURE.md** (15 min) - Aspects techniques
4. **CHANGEMENTS.md** (8 min) - Évolution du projet

---

## Contenu de Chaque Document

| Document | Taille | Contenu Principal |
|----------|--------|-------------------|
| **DEMARRAGE_RAPIDE** | 3 KB | Installation, premiers pas, tests rapides |
| **GUIDE_UTILISATION** | 6 KB | Manuel complet, scénarios, expériences |
| **DOCUMENTATION_MATHEMATIQUES** | 15 KB | Équations, formules, validation, références |
| **ARCHITECTURE** | 8 KB | Structure code, flux données, diagrammes |
| **CHANGEMENTS** | 5 KB | Modifications, statistiques |
| **INDEX** | 7 KB | Navigation complète, recherche |
| **Total Documentation** | **45 KB** | **~2 heures de lecture** |

---

## Recherche par Thème

### Physique et Mathématiques
- **Forces** → DOCUMENTATION_MATHEMATIQUES.md (section "Forces Appliquées")
- **Équations** → DOCUMENTATION_MATHEMATIQUES.md (section "Équations du Mouvement")
- **Intégration** → DOCUMENTATION_MATHEMATIQUES.md (section "Méthode d'Intégration")
- **Formules** → DOCUMENTATION_MATHEMATIQUES.md (section "Formules Analytiques")

### Utilisation
- **Contrôles** → GUIDE_UTILISATION.md (section "Panneau Objet sélectionné")
- **Scénarios** → GUIDE_UTILISATION.md (section "Scénarios d'Utilisation")
- **Expériences** → GUIDE_UTILISATION.md (section "Expériences Suggérées")
- **Problèmes** → GUIDE_UTILISATION.md (section "Cas Particuliers")

### Technique
- **Structure** → ARCHITECTURE.md (section "Structure Globale")
- **Flux de données** → ARCHITECTURE.md (section "Flux de Données")
- **États** → ARCHITECTURE.md (section "États d'un Projectile")
- **Code** → ARCHITECTURE.md + Code source dans `../src/`

### Nouveautés
- **Fonctionnalités** → CHANGEMENTS.md
- **Contrôle individuel** → GUIDE_UTILISATION.md (section "Contrôles Individuels")
- **Documentation** → CHANGEMENTS.md (section "Documentation Créée")

---

## Objectifs Pédagogiques Couverts

Cette documentation illustre et explique :

### Mathématiques
- Équations différentielles du second ordre
- Systèmes dynamiques
- Intégration numérique
- Méthodes symplectiques
- Analyse vectorielle

### Physique
- Cinématique et dynamique
- Mécanique des fluides (traînée)
- Forces conservatives et dissipatives
- Conditions initiales et aux limites

### Informatique
- Programmation orientée objet
- Architecture MVC
- Boucle de jeu temps réel
- Interface utilisateur interactive
- Gestion d'état complexe

---

## Conseils de Navigation

### Si vous cherchez quelque chose de spécifique
→ Utilisez **INDEX.md** qui contient une recherche par mot-clé

### Si vous voulez tout lire
→ Suivez l'ordre : DEMARRAGE → GUIDE → MATHEMATIQUES → ARCHITECTURE

### Si vous avez peu de temps
→ Lisez uniquement DEMARRAGE_RAPIDE.md et GUIDE_UTILISATION.md

### Si vous préparez un cours
→ Concentrez-vous sur DOCUMENTATION_MATHEMATIQUES.md et GUIDE_UTILISATION.md

---

## Besoin d'Aide ?

### Pour l'installation
→ DEMARRAGE_RAPIDE.md (section "Installation")

### Pour utiliser le simulateur
→ GUIDE_UTILISATION.md

### Pour comprendre une équation
→ DOCUMENTATION_MATHEMATIQUES.md + Glossaire

### Pour modifier le code
→ ARCHITECTURE.md + Code source commenté

### Pour signaler un bug
→ Consultez d'abord GUIDE_UTILISATION.md (section "Cas Particuliers")

---

## Points Forts de la Documentation

1. **Complète** : Couvre tous les aspects (utilisation, maths, code)
2. **Progressive** : Du démarrage rapide aux détails techniques
3. **Structurée** : Navigation claire et index détaillé
4. **Illustrée** : Diagrammes, exemples, tableaux
5. **Rigoureuse** : Notation mathématique LaTeX, références bibliographiques
6. **Pratique** : Scénarios concrets et expériences suggérées

---

## Contribution

Cette documentation fait partie du projet de **Modélisation Mathématique (S5)**.

Pour toute question ou suggestion d'amélioration :
1. Consultez d'abord l'INDEX.md
2. Vérifiez les sections "Cas Particuliers" et "Résolution de Problèmes"
3. Référez-vous aux fichiers sources dans `../src/`

---

**Bonne lecture et bon apprentissage !**

*Documentation du Simulateur de Trajectoires Multi-Projectiles*  
*Projet de Modélisation Mathématique - Janvier 2026*
