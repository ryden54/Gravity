# Plan de développement : Simulation du système solaire

## Phase 1 : Mise en place de l'environnement et du modèle de données (Itération 1)

1.  **Configuration de l'environnement de développement :**
    * Installer Python 3.x et les bibliothèques nécessaires : `pygame`, `numpy`, `scipy`, `json`.
    * Créer un environnement virtuel pour isoler le projet.
    * Configurer un gestionnaire de versions (Git) pour le suivi des modifications.
2.  **Création du modèle de données :**
    * Définir une structure de données (dictionnaire ou classe) pour représenter les planètes : nom, position (vecteur 2D), vitesse (vecteur 2D), masse.
    * Créer une fonction pour lire les paramètres des planètes à partir du fichier JSON (nom, distance, vitesse initiale).
    * Initialiser les positions et les vitesses des planètes à partir des données lues.
3.  **Tests unitaires :**
    * Écrire des tests pour vérifier que la lecture du fichier JSON et l'initialisation des données sont correctes.

## Phase 2 : Implémentation de la simulation 2D (Itérations 2-4)

4.  **Calcul de la gravité :**
    * Implémenter la fonction `calculer_gravite(planete1, planete2)` qui calcule la force de gravité entre deux planètes (vecteur 2D).
    * Tests unitaires : vérifier que la fonction renvoie la force correcte pour différentes configurations de planètes.
5.  **Calcul des trajectoires :**
    * Implémenter la fonction `calculer_trajectoire(planete, force, dt)` qui met à jour la position et la vitesse d'une planète en fonction de la force de gravité et du pas de temps `dt`.
    * Tests unitaires : vérifier que la fonction met à jour correctement la position et la vitesse pour différentes forces et pas de temps.
6.  **Boucle temporelle et mise à jour des positions :**
    * Créer une boucle principale qui simule le passage du temps.
    * À chaque itération de la boucle, calculer les forces de gravité entre toutes les paires de planètes.
    * Mettre à jour les positions et les vitesses de chaque planète en utilisant la fonction `calculer_trajectoire`.
    * Tests : vérifier que les positions et les vitesses des planètes évoluent de manière cohérente au fil du temps.
7.  **Affichage 2D :**
    * Utiliser `pygame` pour afficher les planètes sous forme de cercles colorés.
    * Afficher les trajectoires passées des planètes (3 derniers mois) en traçant des lignes entre les positions précédentes.
    * Afficher le nom de chaque planète en dessous de celle-ci.
    * Tests visuels : vérifier que les planètes sont affichées correctement et que les trajectoires sont cohérentes.

## Phase 3 : Ajout de la 3D (Itérations 5-7)

8.  **Adaptation du modèle de données pour la 3D :**
    * Modifier la structure de données des planètes pour inclure une coordonnée Z pour la position et la vitesse (vecteurs 3D).
    * Adapter la fonction de lecture du fichier JSON pour gérer les coordonnées Z.
    * Tests unitaires : vérifier que les données 3D sont lues et initialisées correctement.
9.  **Calcul de la gravité et des trajectoires en 3D :**
    * Adapter les fonctions `calculer_gravite` et `calculer_trajectoire` pour fonctionner avec des vecteurs 3D.
    * Tests unitaires : vérifier que les calculs 3D sont corrects.
10. **Affichage 3D avec PyOpenGL :**
    * Configurer PyOpenGL pour afficher une scène 3D centrée sur le Soleil.
    * Afficher les planètes sous forme de sphères colorées.
    * Implémenter les contrôles au clavier pour la rotation et le zoom de la caméra.
    * Ajouter une grille 3D discrète pour faciliter la visualisation des distances.
    * Tests visuels : vérifier que la scène 3D est affichée correctement et que les contrôles fonctionnent.

## Phase 4 : Finalisation et tests (Itérations 8-9)

11. **Gestion des modes 2D/3D :**
    * Ajouter un argument en ligne de commande `--mode` pour choisir entre les modes 2D et 3D.
    * Adapter le code pour utiliser les fonctions d'affichage et de calcul appropriées en fonction du mode choisi.
    * Tests : vérifier que les deux modes fonctionnent correctement.
12. **Tests et documentation :**
    * Effectuer des tests complets pour vérifier la précision de la simulation et la cohérence des résultats.
    * Rédiger la documentation du code et du projet.

## Phase 5 : Développement futur (Itération 10+)

13. **Ajout de fonctionnalités avancées :**
    * Implémenter des modèles de gravité plus complexes (par exemple, relativité générale).
    * Ajouter des textures réalistes pour les planètes.
    * Ajouter des effets de lumière et d'ombre.
    * Ajouter une interface graphique pour personnaliser la simulation.
    * Optimiser les performances pour simuler un plus grand nombre de corps célestes.