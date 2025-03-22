#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simulation du système solaire - Script principal
"""

import os
import sys
import time
import argparse
import pygame
import json
from src.modele import SystemeSolaire
from src.simulation import Simulation
from src.visualisation import Visualisation


def main():
    """Point d'entrée principal du programme."""
    parser = argparse.ArgumentParser(description='Simulation du système solaire')
    parser.add_argument('--dt', type=float, default=21600.0, help='Pas de temps en secondes (par défaut 6 heures)')
    parser.add_argument('--fichier', type=str, default="data/planets.json", help='Fichier de données JSON')
    args = parser.parse_args()

    # Charge les données
    try:
        systeme = SystemeSolaire.depuis_json(args.fichier)
    except FileNotFoundError:
        raise FileNotFoundError(f"Le fichier {args.fichier} n'existe pas.")
    except json.JSONDecodeError:
        raise ValueError(f"Le fichier {args.fichier} n'est pas un fichier JSON valide.")

    # Vérifie qu'il y a au moins une étoile et une planète
    if not systeme.etoiles:
        raise ValueError("Aucune étoile trouvée dans le système.")
    if not systeme.planetes:
        raise ValueError("Aucune planète trouvée dans le système.")

    # Crée la simulation et la visualisation
    simulation = Simulation(systeme, args.dt)
    visualisation = Visualisation()  # Utilise les dimensions par défaut

    # Boucle principale
    en_cours = True
    while en_cours:
        # Met à jour la simulation seulement si on n'est pas en pause
        if not visualisation.en_pause:
            simulation.simuler(args.dt)  # Utilise le pas de temps spécifié

        # Met à jour la visualisation
        visualisation.mettre_a_jour_temps(simulation.temps / (24 * 3600))  # Conversion en jours
        visualisation.afficher(systeme)

        # Gère les événements
        en_cours = visualisation.gerer_evenements()


if __name__ == "__main__":
    main() 