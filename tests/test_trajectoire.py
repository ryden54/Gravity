import unittest
import numpy as np
from src.modele import SystemeSolaire, CorpsCeleste


class TestTrajectoire(unittest.TestCase):
    """Tests pour les fonctions de calcul d'accélération et de mise à jour de position."""
    
    def setUp(self):
        """Initialise les données de test."""
        # Création d'une planète de test
        self.planete = CorpsCeleste(
            nom="Test",
            masse=1e24,  # 1e24 kg
            rayon=1e6,   # 1000 km
            position=np.array([0.0, 0.0, 0.0]),
            vitesse=np.array([0.0, 0.0, 0.0]),
            couleur=(255, 0, 0)
        )
        
        self.systeme = SystemeSolaire("data/planets.json")
    
    def test_acceleration_force_nulle(self):
        """Test que l'accélération est nulle sans force."""
        force = np.zeros(3)
        dt = 1.0  # 1 seconde
        
        delta_vitesse = self.systeme.calculer_acceleration(self.planete, force, dt)
        np.testing.assert_array_almost_equal(delta_vitesse, np.zeros(3))
    
    def test_acceleration_force_constante(self):
        """Test que l'accélération est correcte sous une force constante."""
        force = np.array([0.0, 1.0, 0.0])  # 1 N vers le haut
        dt = 1.0  # 1 seconde
        
        delta_vitesse = self.systeme.calculer_acceleration(self.planete, force, dt)
        
        # Vérifie que l'accélération est correcte (F = ma)
        acceleration = force / self.planete.masse
        delta_vitesse_attendue = acceleration * dt
        np.testing.assert_array_almost_equal(delta_vitesse, delta_vitesse_attendue)
    
    def test_acceleration_gravite(self):
        """Test que l'accélération est correcte sous l'effet de la gravité."""
        # Création d'une étoile de test
        etoile = CorpsCeleste(
            nom="Etoile",
            masse=2e30,  # 2e30 kg (comme le Soleil)
            rayon=1e8,   # 100 000 km
            position=np.array([1e8, 0.0, 0.0]),  # 100 000 km à droite
            vitesse=np.zeros(3),
            couleur=(255, 255, 0)
        )
        
        # Calcul de la force de gravité
        force = self.systeme.calculer_gravite(self.planete, etoile)
        dt = 1.0  # 1 seconde
        
        delta_vitesse = self.systeme.calculer_acceleration(self.planete, force, dt)
        
        # Vérifie que l'accélération est correcte (F = ma)
        acceleration = force / self.planete.masse
        delta_vitesse_attendue = acceleration * dt
        np.testing.assert_array_almost_equal(delta_vitesse, delta_vitesse_attendue)
    
    def test_mise_a_jour_position_vitesse_constante(self):
        """Test que la position est mise à jour correctement avec une vitesse constante."""
        dt = 1.0  # 1 seconde
        vitesse = np.array([1.0, 0.0, 0.0])  # 1 m/s vers la droite
        self.planete.vitesse = vitesse
        
        position_initiale = self.planete.position.copy()
        self.systeme.mettre_a_jour_position(self.planete, dt)
        
        # Vérifie que la position a été mise à jour correctement
        position_attendue = position_initiale + vitesse * dt
        np.testing.assert_array_almost_equal(self.planete.position, position_attendue)
        
        # Vérifie que la trajectoire contient la nouvelle position
        self.assertEqual(len(self.planete.trajectoire), 2)
        np.testing.assert_array_almost_equal(self.planete.trajectoire[-1], position_attendue)
    
    def test_mise_a_jour_position_vitesse_variable(self):
        """Test que la position est mise à jour correctement avec une vitesse variable."""
        dt = 1.0  # 1 seconde
        vitesse = np.array([1.0, 2.0, 0.0])  # Vitesse en x et y
        self.planete.vitesse = vitesse
        
        position_initiale = self.planete.position.copy()
        self.systeme.mettre_a_jour_position(self.planete, dt)
        
        # Vérifie que la position a été mise à jour correctement
        position_attendue = position_initiale + vitesse * dt
        np.testing.assert_array_almost_equal(self.planete.position, position_attendue)


if __name__ == '__main__':
    unittest.main() 