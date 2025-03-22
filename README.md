# Simulation du Système Solaire

Une simulation interactive du système solaire interne (jusqu'à Mars) utilisant Python et Pygame.

## Pré-requis

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
python -m venv venv
# Sur Windows :
venv\Scripts\activate
# Sur Linux/Mac :
source venv/bin/activate
```

3. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## Lancement

Pour lancer la simulation :

```bash
# Sur Windows :
$env:PYTHONPATH="."; python src/main.py

# Sur Linux/Mac :
PYTHONPATH=. python src/main.py
```

### Options de lancement

- `--dt` : Définit l'unité de temps de la simulation en heures (défaut : 24.0)
  ```bash
  python src/main.py --dt 12.0  # Simulation avec pas de temps de 12 heures
  ```

## Contrôles

- `Échap` : Quitter la simulation
- Redimensionnez la fenêtre à tout moment pour ajuster la vue

## Fonctionnalités

- Simulation réaliste des orbites des planètes jusqu'à Mars
- Affichage des trajectoires des planètes
- Grille de référence avec distances en UA
- Date et heure en temps réel
- Interface graphique interactive

## Licence

Ce projet est sous licence GNU General Public License v3.0 (GPL-3.0). Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request 