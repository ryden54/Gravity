import unittest
import numpy as np
from src.modele import SystemeSolaire, CorpsCeleste


class TestGravite(unittest.TestCase):
    """Tests pour la fonction de calcul de gravité."""
    
    def setUp(self):
        """Initialise les données de test."""
        # Création de deux corps célestes de test
        self.planete1 = CorpsCeleste(
            nom="Test1",
            masse=1e24,  # 1e24 kg
            rayon=1e6,   # 1000 km
            position=np.array([0.0, 0.0, 0.0]),
            vitesse=np.array([0.0, 0.0, 0.0]),
            couleur=(255, 0, 0)
        )
        
        self.planete2 = CorpsCeleste(
            nom="Test2",
            masse=1e24,  # 1e24 kg
            rayon=1e6,   # 1000 km
            position=np.array([1e8, 0.0, 0.0]),  # 100 000 km
            vitesse=np.array([0.0, 0.0, 0.0]),
            couleur=(0, 255, 0)
        )
        
        self.systeme = SystemeSolaire("data/planets.json")
    
    def test_gravite_basique(self):
        """Test du calcul de gravité entre deux planètes."""
        force = self.systeme.calculer_gravite(self.planete1, self.planete2)
        
        # Vérifie que la force est un vecteur 3D
        self.assertEqual(len(force), 3)
        
        # Vérifie que la force est dirigée vers la planète2 (axe x positif)
        self.assertGreater(force[0], 0)
        self.assertAlmostEqual(force[1], 0)
        self.assertAlmostEqual(force[2], 0)
        
        # Vérifie que la force est égale à -G * m1 * m2 / r²
        distance = 1e8
        force_attendue = SystemeSolaire.G * self.planete1.masse * self.planete2.masse / (distance ** 2)
        self.assertAlmostEqual(np.linalg.norm(force), force_attendue)
    
    def test_gravite_reciproque(self):
        """Test que les forces sont réciproques (F12 = -F21)."""
        force12 = self.systeme.calculer_gravite(self.planete1, self.planete2)
        force21 = self.systeme.calculer_gravite(self.planete2, self.planete1)
        
        np.testing.assert_array_almost_equal(force12, -force21)
    
    def test_gravite_distance_nulle(self):
        """Test que la force est nulle quand les corps sont au même endroit."""
        self.planete2.position = self.planete1.position.copy()
        force = self.systeme.calculer_gravite(self.planete1, self.planete2)
        
        np.testing.assert_array_almost_equal(force, np.zeros(3))


if __name__ == '__main__':
    unittest.main() 