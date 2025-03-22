#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simulation du système solaire - Script principal
"""

import os
import sys
from modele import SystemeSolaire


def main():
    """Fonction principale."""
    # Détermine le chemin du fichier JSON contenant les données des planètes
    chemin_script = os.path.dirname(os.path.abspath(__file__))
    chemin_racine = os.path.dirname(chemin_script)
    chemin_donnees = os.path.join(chemin_racine, 'data', 'planets.json')
    
    print(f"Chargement des données depuis {chemin_donnees}")
    
    # Initialise le système solaire
    systeme = SystemeSolaire(chemin_donnees)
    
    # Affiche les informations sur les corps célestes
    print("\nÉtoiles:")
    for etoile in systeme.etoiles:
        print(f"  - {etoile.nom}: masse={etoile.masse:.2e} kg, rayon={etoile.rayon:.2e} m")
    
    print("\nPlanètes:")
    for planete in systeme.planetes:
        print(f"  - {planete.nom}: masse={planete.masse:.2e} kg, rayon={planete.rayon:.2e} m")
        print(f"    Position: {planete.position}, Vitesse: {planete.vitesse}")


if __name__ == "__main__":
    main() 