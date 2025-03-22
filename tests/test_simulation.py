import unittest
import numpy as np
from src.modele import SystemeSolaire, CorpsCeleste
from src.simulation import Simulation


class TestSimulation(unittest.TestCase):
    """Tests pour la classe Simulation."""
    
    def setUp(self):
        """Initialise les données de test."""
        # Création d'un système solaire simplifié pour les tests
        self.etoile = CorpsCeleste(
            nom="Soleil",
            masse=1.989e30,
            rayon=6.95e8,
            position=np.zeros(3),
            vitesse=np.zeros(3),
            couleur=(255, 255, 0)
        )
        
        self.planete = CorpsCeleste(
            nom="Terre",
            masse=5.97e24,
            rayon=6.37e6,
            position=np.array([1.496e11, 0.0, 0.0]),  # 1 UA
            vitesse=np.array([0.0, 29.783e3, 0.0]),   # Vitesse orbitale de la Terre
            couleur=(0, 0, 255)
        )
        
        # Création du système solaire de test
        self.systeme = SystemeSolaire(etoiles=[self.etoile], planetes=[self.planete])
        
        # Création de la simulation
        self.simulation = Simulation(self.systeme, dt=3600.0)  # Pas de temps de 1 heure
    
    def test_calculer_forces(self):
        """Test du calcul des forces sur un corps."""
        # Calcule la force sur la planète
        force = self.simulation.calculer_forces(self.planete)
        
        # Vérifie que la force est un vecteur 3D
        self.assertEqual(len(force), 3)
        
        # Vérifie que la force est dirigée vers le Soleil (axe x négatif)
        self.assertLess(force[0], 0)  # Force négative en x car la planète est à droite du Soleil
        self.assertAlmostEqual(force[1], 0)  # Pas de force en y car les planètes sont dans le plan x
        self.assertAlmostEqual(force[2], 0)  # Pas de force en z car les planètes sont dans le plan xy
    
    def test_simuler(self):
        """Test de la simulation sur plusieurs itérations."""
        # Position et vitesse initiales
        position_initiale = self.planete.position.copy()
        vitesse_initiale = self.planete.vitesse.copy()
        temps_initial = self.simulation.obtenir_temps()
        
        # Simulation sur 10 heures
        self.simulation.simuler(36000.0)  # 10 heures = 36000 secondes
        
        # Vérifie que la position a changé
        self.assertFalse(np.array_equal(self.planete.position, position_initiale))
        
        # Vérifie que la vitesse a changé
        self.assertFalse(np.array_equal(self.planete.vitesse, vitesse_initiale))
        
        # Vérifie que le temps a été mis à jour
        self.assertEqual(self.simulation.obtenir_temps(), temps_initial + 36000.0)
    
    def test_conservation_energie(self):
        """Test de la conservation de l'énergie mécanique."""
        def calculer_energie_mecanique(corps: CorpsCeleste) -> float:
            """Calcule l'énergie mécanique d'un corps."""
            # Énergie cinétique
            v = np.linalg.norm(corps.vitesse)
            ec = 0.5 * corps.masse * v * v
            
            # Énergie potentielle (par rapport au Soleil)
            r = np.linalg.norm(corps.position)
            ep = -SystemeSolaire.G * corps.masse * self.systeme.etoiles[0].masse / r
            
            return ec + ep
        
        # Énergie initiale
        energie_initiale = calculer_energie_mecanique(self.planete)
        
        # Simulation sur 5 heures
        self.simulation.simuler(18000.0)  # 5 heures = 18000 secondes
        
        # Énergie finale
        energie_finale = calculer_energie_mecanique(self.planete)
        
        # Vérifie que l'énergie est conservée (à une tolérance près)
        # On utilise une tolérance relative car les énergies sont très grandes
        tolerance = 1e-6  # 0.0001% de différence relative
        difference_relative = abs((energie_finale - energie_initiale) / energie_initiale)
        self.assertLess(difference_relative, tolerance)


if __name__ == '__main__':
    unittest.main() 