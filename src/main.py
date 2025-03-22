#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simulation du système solaire - Script principal
"""

import os
import sys
import time
from modele import SystemeSolaire
from simulation import Simulation


def main():
    """Fonction principale du programme."""
    # Création du système solaire
    systeme = SystemeSolaire("data/planets.json")
    
    # Création de la simulation avec un pas de temps d'une heure
    simulation = Simulation(systeme, dt=3600.0)
    
    # Durée de simulation (1 jour)
    duree_simulation = 24 * 3600.0  # 24 heures en secondes
    
    print("Démarrage de la simulation...")
    print("Appuyez sur Ctrl+C pour arrêter la simulation")
    temps_debut = time.time()
    
    # Boucle principale de simulation
    try:
        while True:
            # Fait avancer la simulation d'une journée
            simulation.simuler(duree_simulation)
            
            # Affiche l'état actuel
            temps_ecoule = simulation.obtenir_temps()
            jours = temps_ecoule / (24 * 3600.0)
            print(f"Temps écoulé : {jours:.1f} jours")
            
            # Petit délai pour ne pas surcharger le CPU
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\nSimulation arrêtée par l'utilisateur")
    
    temps_fin = time.time()
    duree_reelle = temps_fin - temps_debut
    print(f"\nSimulation terminée en {duree_reelle:.1f} secondes")


if __name__ == "__main__":
    main() 