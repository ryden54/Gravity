# Cahier des charges : Simulation du système solaire

## 1. Introduction

Ce document présente les spécifications techniques et fonctionnelles pour la création d'une simulation du système solaire en 2D, puis en 3D. Cette simulation permettra de visualiser les trajectoires des planètes et d'observer l'influence de la gravité sur leurs orbites.

## 2. Objectifs

* Créer une simulation réaliste du système solaire en 2D, puis en 3D.
* Permettre aux développeurs de tester différents scénarios et paramètres.
* Fournir une base pour des simulations plus avancées à l'avenir.

## 3. Fonctionnalités

### 3.1. Simulation 2D

* Affichage des planètes du système solaire sous forme de cercles colorés.
* Calcul des trajectoires des planètes en fonction de la gravité.
* Affichage des trajectoires passées des planètes (3 derniers mois).
* Affichage du nom de chaque planète en dessous de celle-ci.
* Échelle de temps : 1 année de simulation = 1 minute de temps réel.
* Paramètres configurables via un fichier JSON (voir section 4).

### 3.2. Simulation 3D

* Affichage des planètes du système solaire sous forme de sphères colorées.
* Calcul des trajectoires des planètes en 3D.
* Affichage des trajectoires passées des planètes (3 derniers mois).
* Affichage du nom de chaque planète en dessous de celle-ci.
* Vue centrée sur le Soleil, avec caméra orientable et zoomable (contrôles au clavier).
* Grille 3D discrète pour faciliter la visualisation des distances.
* Paramètres configurables via le même fichier JSON que pour la 2D.
* Choix du mode 2D ou 3D via un argument en ligne de commande (--mode 2d ou 3d).

## 4. Fichier de configuration (JSON)

Le fichier de configuration contiendra les paramètres suivants pour chaque planète :

* Nom (chaîne de caractères).
* Distance au Soleil (unité astronomique).
* Vitesse initiale (kilomètres par seconde).

Exemple :

```json
{
  "planetes": [
    { "nom": "Terre", "distance": 1, "vitesse": 29.78 },
    { "nom": "Mars", "distance": 1.52, "vitesse": 24.07 }
  ]
}

## 5. Architecture
* Langage de programmation : Python.
* Bibliothèque graphique 2D : à définir (par exemple, Pygame).
* Bibliothèque graphique 3D : PyOpenGL.
* Calcul de la gravité : lois de la gravitation universelle.
* Calcul des trajectoires : intégration numérique (par exemple, méthode d'Euler).

## 6. Tests unitaires

* Tests pour vérifier la précision des calculs de gravité.
* Tests pour vérifier la précision des calculs de trajectoire.
* Tests pour vérifier le bon fonctionnement des contrôles de la vue 3D.
* Vérification visuelle de la cohérence des simulations 2D et 3D.

## 7. Gestion des erreurs

* Gestion des erreurs de lecture du fichier de configuration.
* Gestion des erreurs de calcul (par exemple, division par zéro).
* Affichage de messages d'erreur clairs et informatifs.

## 8. Interface utilisateur

* Interface graphique simple et intuitive.
* Contrôles au clavier pour la vue 3D (rotation, zoom).
* Affichage des noms des planètes en dessous de celles-ci.
* Grille 3D discrète pour faciliter la visualisation des distances.

## 9. Développement futur

* Ajout de textures réalistes pour les planètes.
* Ajout d'effets de lumière et d'ombre.
* Ajout d'options de personnalisation pour l'utilisateur.
* Implémentation de modèles de gravité plus complexes.

## 10. Annexes

### 10.1 Liste des bibliothèques Python recommandées

* **Pygame** : Bibliothèque 2D simple et facile à utiliser pour l'affichage des planètes et de leurs trajectoires.
* **PyOpenGL** : Bibliothèque 3D pour l'affichage des planètes, de la grille et de la caméra orientable.
* **NumPy** : Bibliothèque pour les calculs numériques, notamment les vecteurs et les matrices.
* **SciPy** : Bibliothèque pour les fonctions scientifiques, notamment l'intégration numérique pour le calcul des trajectoires.
* **json** : Bibliothèque pour la lecture et l'écriture du fichier de configuration.
* **math** : Bibliothèque pour les fonctions mathématiques de base.

### 10.2 : Exemples de code pour les calculs de gravité et de trajectoire

### Calcul de la gravité et de trajectoire

```python
def calculer_gravite(planete1, planete2):
  """Calcule la force de gravité entre deux planètes."""
  G = 6.674e-11  # Constante gravitationnelle
  m1 = planete1["masse"]
  m2 = planete2["masse"]
  r = distance(planete1["position"], planete2["position"])
  force = G * m1 * m2 / r**2
  return force


```python
  def calculer_trajectoire(planete, force, dt):
  """Calcule la nouvelle position d'une planète."""
  acceleration = force / planete["masse"]
  planete["vitesse"] += acceleration * dt
  planete["position"] += planete["vitesse"] * dt
  return planete
  