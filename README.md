# Simulation du Système Solaire

Une simulation interactive du système solaire utilisant Python et Pygame.

## Fonctionnalités

- Simulation physique réaliste des orbites planétaires
- Visualisation interactive avec Pygame
- Chargement des données depuis un fichier JSON
- Affichage des trajectoires des planètes
- Grille de référence avec distances en UA
- Affichage de la date et du temps écoulé
- Possibilité de mettre en pause la simulation
- Redimensionnement de la fenêtre en temps réel

## Prérequis

- Python 3.8 ou supérieur
- Pygame
- NumPy

## Installation

1. Clonez le dépôt :
```bash
git clone https://github.com/votre-username/simulation-systeme-solaire.git
cd simulation-systeme-solaire
```

2. Créez un environnement virtuel et activez-le :
```bash
python -m venv venv
source venv/bin/activate  # Sur Unix/macOS
venv\Scripts\activate     # Sur Windows
```

3. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## Utilisation

Pour lancer la simulation :

```bash
cd src
python main.py [options]
```

### Options disponibles

- `--dt <heures>` : Définit l'unité de temps de la simulation en heures (défaut : 24.0)
- `--fichier <chemin>` : Spécifie le chemin du fichier JSON contenant les données du système solaire (défaut : ../data/planets.json)

### Exemples

```bash
# Lancer avec les paramètres par défaut
python main.py

# Lancer avec un pas de temps de 12 heures
python main.py --dt 12.0

# Lancer avec un fichier de données personnalisé
python main.py --fichier ../data/autre_systeme.json

# Combiner les options
python main.py --fichier ../data/autre_systeme.json --dt 12.0
```

### Contrôles

- `Échap` : Quitter la simulation
- `Espace` : Mettre en pause/reprendre la simulation
- Redimensionnez la fenêtre pour ajuster la vue

## Structure du projet

```
simulation-systeme-solaire/
├── data/
│   └── planets.json      # Données du système solaire
├── src/
│   ├── main.py          # Point d'entrée du programme
│   ├── modele.py        # Classes de base (CorpsCeleste, SystemeSolaire)
│   ├── simulation.py    # Logique de simulation
│   └── visualisation.py # Interface graphique
├── tests/
│   ├── test_gravite.py
│   ├── test_modele.py
│   ├── test_simulation.py
│   ├── test_trajectoire.py
│   └── test_visualisation.py
├── requirements.txt
└── README.md
```

## Tests

Pour exécuter les tests :

```bash
python -m pytest tests/ -v
```

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails. 