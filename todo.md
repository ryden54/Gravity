# To-Do : Simulation du système solaire

## Phase 1 : Mise en place de l'environnement et du modèle de données (Itération 1)

* [x] Configuration de l'environnement de développement
    * [x] Installer Python 3.x et les bibliothèques nécessaires : `pygame`, `numpy`, `scipy`, `json`
    * [x] Créer un environnement virtuel
    * [x] Configurer Git
* [x] Création du modèle de données
    * [x] Définir la structure de données pour les planètes
    * [x] Créer la fonction de lecture du fichier JSON
    * [x] Initialiser les positions et vitesses des planètes
* [x] Tests unitaires
    * [x] Vérifier la lecture du fichier JSON
    * [x] Vérifier l'initialisation des données

## Phase 2 : Implémentation de la simulation 2D (Itérations 2-4)

* [x] Calcul de la gravité
    * [x] Implémenter la fonction `calculer_gravite(planete1, planete2)`
    * [x] Tests unitaires : vérifier la précision des calculs
* [x] Calcul des trajectoires
    * [x] Implémenter la fonction `calculer_acceleration(corps, force, dt)`
    * [x] Implémenter la fonction `mettre_a_jour_position(corps, dt)`
    * [x] Tests unitaires : vérifier la précision des calculs
* [x] Boucle temporelle et mise à jour des positions
    * [x] Créer la boucle principale de simulation
    * [x] Calculer les forces de gravité à chaque itération
    * [x] Mettre à jour les positions et vitesses des planètes
    * [x] Tests : vérifier la cohérence des évolutions
* [x] Affichage 2D
    * [x] Afficher les planètes avec `pygame`
    * [x] Afficher les trajectoires passées
    * [x] Afficher les noms des planètes
    * [x] Tests visuels : vérifier l'affichage et les trajectoires

## Phase 3 : Ajout de la 3D (Itérations 5-7)

* [ ] Adaptation du modèle de données pour la 3D
    * [ ] Modifier la structure de données pour inclure la coordonnée Z
    * [ ] Adapter la fonction de lecture du fichier JSON
    * [ ] Tests unitaires : vérifier la lecture et l'initialisation des données 3D
* [ ] Calcul de la gravité et des trajectoires en 3D
    * [ ] Adapter les fonctions pour utiliser les coordonnées Z non nulles
    * [ ] Tests unitaires : vérifier la précision des calculs 3D
* [ ] Affichage 3D avec PyOpenGL
    * [ ] Configurer PyOpenGL pour la scène 3D
    * [ ] Afficher les planètes sous forme de sphères
    * [ ] Implémenter les contrôles de la caméra (clavier)
    * [ ] Ajouter une grille 3D
    * [ ] Tests visuels : vérifier l'affichage et les contrôles

## Phase 4 : Finalisation et tests (Itérations 8-9)

* [ ] Gestion des modes 2D/3D
    * [ ] Ajouter l'argument `--mode` en ligne de commande
    * [ ] Adapter le code pour les modes 2D et 3D
    * [ ] Tests : vérifier le fonctionnement des deux modes
* [ ] Tests et documentation
    * [ ] Effectuer des tests complets
    * [ ] Rédiger la documentation du code et du projet

## Phase 5 : Développement futur (Itération 10+)

* [ ] Ajout de fonctionnalités avancées
    * [ ] Implémenter des modèles de gravité complexes
    * [ ] Ajouter des textures réalistes pour les planètes
    * [ ] Ajouter des effets de lumière et d'ombre
    * [ ] Ajouter une interface graphique pour personnaliser la simulation
    * [ ] Optimiser les performances pour un grand nombre de corps célestes