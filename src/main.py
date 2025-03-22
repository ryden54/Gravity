#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simulation du système solaire - Script principal
"""

import os
import sys
import time
from src.modele import SystemeSolaire
from src.simulation import Simulation
from src.visualisation import Visualisation


def main():
    """Fonction principale du programme."""
    # Création du système solaire
    systeme = SystemeSolaire("data/planets.json")
    
    # Création de la simulation avec un pas de temps d'une heure
    simulation = Simulation(systeme, dt=3600.0)
    
    # Création de la visualisation
    visu = Visualisation()
    
    # Durée de simulation (1 jour)
    duree_simulation = 24 * 3600.0  # 24 heures en secondes
    
    print("Démarrage de la simulation...")
    print("Appuyez sur Échap pour quitter")
    temps_debut = time.time()
    
    # Boucle principale de simulation
    try:
        while True:
            # Gestion des événements Pygame
            if not visu.gerer_evenements():
                break
            
            # Fait avancer la simulation d'une journée
            simulation.simuler(duree_simulation)
            
            # Affiche l'état actuel
            temps_ecoule = simulation.obtenir_temps()
            jours = temps_ecoule / (24 * 3600.0)
            print(f"Temps écoulé : {jours:.1f} jours", end='\r')
            
            # Met à jour l'affichage
            visu.dessiner_systeme(systeme)
            
            # Limite le framerate à 60 FPS
            time.sleep(1/60)
            
    except KeyboardInterrupt:
        print("\nSimulation arrêtée par l'utilisateur")
    finally:
        visu.fermer()
    
    temps_fin = time.time()
    duree_reelle = temps_fin - temps_debut
    print(f"\nSimulation terminée en {duree_reelle:.1f} secondes")


if __name__ == "__main__":
    main() 