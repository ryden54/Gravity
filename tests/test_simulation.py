import unittest
import numpy as np
from src.modele import SystemeSolaire, CorpsCeleste
from src.simulation import Simulation


class TestSimulation(unittest.TestCase):
    """Tests pour la classe Simulation."""
    
    def setUp(self):
        """Initialise les données de test."""
        # Création d'un système solaire simplifié avec le Soleil et la Terre
        self.planete = CorpsCeleste(
            nom="Terre",
            masse=5.97e24,  # 5.97e24 kg
            rayon=6.38e6,   # 6 380 km
            position=np.array([1.496e11, 0.0, 0.0]),  # 149.6 millions de km
            vitesse=np.array([0.0, 29.783e3, 0.0]),  # 29.783 km/s
            couleur=(0, 0, 255)
        )
        
        self.etoile = CorpsCeleste(
            nom="Soleil",
            masse=1.99e30,  # 1.99e30 kg
            rayon=6.95e8,   # 695 000 km
            position=np.zeros(3),
            vitesse=np.zeros(3),
            couleur=(255, 255, 0)
        )
        
        self.systeme = SystemeSolaire("data/planets.json")
        self.simulation = Simulation(self.systeme, dt=3600.0)  # Pas de temps de 1 heure
    
    def test_calculer_forces(self):
        """Test du calcul des forces sur un corps."""
        force = self.simulation.calculer_forces(self.planete)
        
        # Vérifie que la force est un vecteur 3D
        self.assertEqual(len(force), 3)
        
        # Vérifie que la force est dirigée vers le Soleil (axe x négatif)
        self.assertLess(force[0], 0)
        self.assertAlmostEqual(force[1], 0)
        self.assertAlmostEqual(force[2], 0)
    
    def test_une_iteration(self):
        """Test d'une itération de simulation."""
        # Position et vitesse initiales
        position_initiale = self.planete.position.copy()
        vitesse_initiale = self.planete.vitesse.copy()
        
        # Une itération
        self.simulation.une_iteration()
        
        # Vérifie que la position a changé
        self.assertFalse(np.array_equal(self.planete.position, position_initiale))
        
        # Vérifie que la vitesse a changé
        self.assertFalse(np.array_equal(self.planete.vitesse, vitesse_initiale))
        
        # Vérifie que le temps a été mis à jour
        self.assertEqual(self.simulation.obtenir_temps(), 3600.0)
    
    def test_executer(self):
        """Test de l'exécution de plusieurs itérations."""
        nombre_iterations = 10
        temps_initial = self.simulation.obtenir_temps()
        
        self.simulation.executer(nombre_iterations)
        
        # Vérifie que le temps a été mis à jour correctement
        temps_attendu = temps_initial + nombre_iterations * self.simulation.dt
        self.assertEqual(self.simulation.obtenir_temps(), temps_attendu)
        
        # Vérifie que la trajectoire contient toutes les positions
        self.assertEqual(len(self.planete.trajectoire), nombre_iterations + 1)
    
    def test_conservation_energie(self):
        """Test de la conservation de l'énergie mécanique."""
        def calculer_energie_mecanique(corps: CorpsCeleste) -> float:
            """Calcule l'énergie mécanique d'un corps."""
            # Énergie cinétique
            v = np.linalg.norm(corps.vitesse)
            ec = 0.5 * corps.masse * v * v
            
            # Énergie potentielle (par rapport au Soleil)
            r = np.linalg.norm(corps.position)
            ep = -SystemeSolaire.G * corps.masse * self.etoile.masse / r
            
            return ec + ep
        
        # Énergie initiale
        energie_initiale = calculer_energie_mecanique(self.planete)
        
        # Simulation sur quelques itérations
        self.simulation.executer(5)
        
        # Énergie finale
        energie_finale = calculer_energie_mecanique(self.planete)
        
        # Vérifie que l'énergie est conservée (à une tolérance près)
        self.assertAlmostEqual(energie_initiale, energie_finale, places=2)


if __name__ == '__main__':
    unittest.main() 