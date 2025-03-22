from typing import List
import numpy as np
from modele import SystemeSolaire, CorpsCeleste


class Simulation:
    """Classe gérant la boucle principale de simulation."""
    
    def __init__(self, systeme: SystemeSolaire, dt: float = 3600.0):
        """Initialise la simulation.
        
        Args:
            systeme (SystemeSolaire): Système solaire à simuler
            dt (float): Pas de temps en secondes (par défaut 1 heure)
        """
        self.systeme = systeme
        self.dt = dt
        self.temps = 0.0  # Temps écoulé en secondes
    
    def calculer_forces(self, corps: CorpsCeleste) -> np.ndarray:
        """Calcule la force totale exercée sur un corps par tous les autres corps.
        
        Args:
            corps (CorpsCeleste): Corps sur lequel calculer la force totale
            
        Returns:
            np.ndarray: Force totale en N
        """
        force_totale = np.zeros(3)
        
        # Calcul de la force exercée par chaque autre corps
        for autre_corps in self.systeme.obtenir_tous_corps():
            if autre_corps != corps:
                force = self.systeme.calculer_gravite(corps, autre_corps)
                force_totale += force
        
        return force_totale
    
    def simuler(self, duree: float) -> None:
        """Fait avancer la simulation d'une durée donnée.
        
        Args:
            duree (float): Durée en secondes sur laquelle faire avancer la simulation
        """
        nombre_iterations = int(duree / self.dt)
        
        for _ in range(nombre_iterations):
            # Calcul des forces sur tous les corps
            forces = {}
            for corps in self.systeme.obtenir_tous_corps():
                forces[corps] = self.calculer_forces(corps)
            
            # Mise à jour des vitesses
            for corps, force in forces.items():
                delta_vitesse = self.systeme.calculer_acceleration(corps, force, self.dt)
                corps.vitesse += delta_vitesse
            
            # Mise à jour des positions
            for corps in self.systeme.obtenir_tous_corps():
                self.systeme.mettre_a_jour_position(corps, self.dt)
            
            # Mise à jour du temps
            self.temps += self.dt
    
    def obtenir_temps(self) -> float:
        """Retourne le temps écoulé depuis le début de la simulation.
        
        Returns:
            float: Temps écoulé en secondes
        """
        return self.temps 