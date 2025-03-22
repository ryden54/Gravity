# Simulation du Système Solaire

Une simulation interactive du système solaire utilisant Python et Pygame.

## Prérequis

- Python 3.8 ou supérieur
- Pygame 2.6.1 ou supérieur
- NumPy 1.24.0 ou supérieur

## Installation

1. Clonez le dépôt :
```bash
git clone https://github.com/votre-username/Gravity.git
cd Gravity
```

2. Créez un environnement virtuel et activez-le :
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Installez les dépendances :
```bash
# Pour simplement lancer la simulation
pip install -r requirements.txt

# Pour le développement (tests, etc.)
pip install -r requirements-dev.txt
```

## Lancement

Pour lancer la simulation :

```bash
# Windows
$env:PYTHONPATH="."; python src/main.py

# Linux/Mac
PYTHONPATH=. python src/main.py
```

Vous pouvez spécifier l'unité de temps de la simulation en utilisant l'option `--time-unit` :
```bash
python src/main.py --time-unit 24  # 24 heures par seconde
```

## Contrôles

- `Échap` : Quitter la simulation
- `Espace` : Mettre en pause/reprendre la simulation
- Redimensionnez la fenêtre à tout moment

## Fonctionnalités

- Simulation réaliste des orbites planétaires
- Affichage des trajectoires
- Grille de référence avec distances en UA
- Mise à l'échelle automatique
- Pause/Reprise de la simulation
- Positions initiales aléatoires des planètes

## Licence

Ce projet est sous licence GNU General Public License v3.0 (GPL-3.0). Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Commiter vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Pousser vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request 