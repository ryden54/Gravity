import unittest
import numpy as np
from src.modele import SystemeSolaire, CorpsCeleste


class TestTrajectoire(unittest.TestCase):
    """Tests pour les fonctions de calcul d'accélération et de mise à jour de position."""
    
    def setUp(self):
        """Initialise les données de test."""
        # Création d'une planète de test
        self.planete = CorpsCeleste(
            nom="Planete",
            masse=1e24,  # 1e24 kg
            rayon=1e6,   # 1000 km
            position=np.array([1e8, 0.0, 0.0]),  # 100 000 km à droite
            vitesse=np.array([0.0, 1e3, 0.0]),  # 1 km/s vers le haut
            couleur=(255, 0, 0)
        )
        
        # Création d'une étoile de test
        self.etoile = CorpsCeleste(
            nom="Etoile",
            masse=2e30,  # 2e30 kg (comme le Soleil)
            rayon=1e8,   # 100 000 km
            position=np.zeros(3),  # Au centre
            vitesse=np.zeros(3),
            couleur=(255, 255, 0)
        )
        
        # Création du système solaire de test
        self.systeme = SystemeSolaire(etoiles=[self.etoile], planetes=[self.planete])
    
    def test_acceleration_force_constante(self):
        """Test que l'accélération est correcte sous l'effet d'une force constante."""
        force = np.array([1e10, 0.0, 0.0])  # 10e10 N vers la droite
        dt = 1.0  # 1 seconde
        
        delta_vitesse = self.systeme.calculer_acceleration(self.planete, force, dt)
        
        # Vérifie que l'accélération est correcte (F = ma)
        acceleration = force / self.planete.masse
        delta_vitesse_attendue = acceleration * dt
        np.testing.assert_array_almost_equal(delta_vitesse, delta_vitesse_attendue)
    
    def test_acceleration_force_nulle(self):
        """Test que l'accélération est nulle sous l'effet d'une force nulle."""
        force = np.zeros(3)
        dt = 1.0  # 1 seconde
        
        delta_vitesse = self.systeme.calculer_acceleration(self.planete, force, dt)
        
        # Vérifie que la variation de vitesse est nulle
        np.testing.assert_array_almost_equal(delta_vitesse, np.zeros(3))
    
    def test_acceleration_gravite(self):
        """Test que l'accélération est correcte sous l'effet de la gravité."""
        # Calcul de la force de gravité
        force = self.systeme.calculer_gravite(self.planete, self.etoile)
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
        self.planete.mettre_a_jour_position(dt)
        
        # Vérifie que la position a été mise à jour correctement
        position_attendue = position_initiale + vitesse * dt
        np.testing.assert_array_almost_equal(self.planete.position, position_attendue)
    
    def test_mise_a_jour_position_vitesse_variable(self):
        """Test que la position est mise à jour correctement avec une vitesse variable."""
        dt = 1.0  # 1 seconde
        vitesse = np.array([1.0, 0.0, 0.0])  # 1 m/s vers la droite
        self.planete.vitesse = vitesse
        
        position_initiale = self.planete.position.copy()
        
        # Mise à jour de la position
        self.planete.mettre_a_jour_position(dt)
        
        # Vérifie que la position a été mise à jour correctement
        position_attendue = position_initiale + vitesse * dt
        np.testing.assert_array_almost_equal(self.planete.position, position_attendue)


if __name__ == '__main__':
    unittest.main() 