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
from modele import SystemeSolaire
from simulation import Simulation
from visualisation import Visualisation


def main():
    """Point d'entrée principal du programme."""
    # Analyse des arguments en ligne de commande
    parser = argparse.ArgumentParser(description="Simulation du système solaire")
    parser.add_argument("--dt", type=float, default=24.0,
                      help="Unité de temps de la simulation en heures (défaut: 24.0)")
    parser.add_argument("--fichier", type=str, default="../data/planets.json",
                      help="Chemin du fichier JSON contenant les données du système solaire")
    args = parser.parse_args()
    
    # Conversion des heures en secondes
    dt = args.dt * 3600.0
    
    # Chargement du système solaire
    systeme = SystemeSolaire.depuis_json(args.fichier)
    
    # Vérification du chargement des corps célestes
    if not systeme.etoiles:
        print("Erreur : Aucune étoile n'a été chargée. La simulation ne peut pas démarrer.")
        return
    
    if not systeme.planetes:
        print("Erreur : Aucune planète n'a été chargée. La simulation ne peut pas démarrer.")
        return
    
    print(f"Démarrage de la simulation (dt = {args.dt:.1f} heures)...")
    print("Appuyez sur Échap pour quitter")
    print("Vous pouvez redimensionner la fenêtre à tout moment")
    
    # Création de la simulation
    simulation = Simulation(systeme)
    
    # Création de la visualisation
    visualisation = Visualisation(duree_trajectoire=90.0)  # 3 mois
    
    # Boucle principale
    en_cours = True
    while en_cours:
        # Gestion des événements
        if not visualisation.gerer_evenements():
            en_cours = False
            break
        
        # Mise à jour de la simulation si pas en pause
        if not visualisation.en_pause:
            simulation.simuler(dt)  # Avance d'un pas de temps
            # Mise à jour du temps dans la visualisation
            temps_jours = simulation.obtenir_temps() / (24 * 3600)
            visualisation.mettre_a_jour_temps(temps_jours)
            # Affichage du temps écoulé
            print(f"\rTemps écoulé : {temps_jours:.1f} jours", end="")
        
        # Affichage
        visualisation.afficher(systeme)
    
    print("\nSimulation arrêtée par l'utilisateur")
    visualisation.fermer()


if __name__ == "__main__":
    main() 