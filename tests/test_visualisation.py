import unittest
import numpy as np
import pygame
from src.modele import SystemeSolaire, CorpsCeleste
from src.visualisation import Visualisation


class TestVisualisation(unittest.TestCase):
    """Tests pour la classe Visualisation."""
    
    def setUp(self):
        """Initialise les données de test."""
        # Création d'un système solaire simplifié
        self.planete = CorpsCeleste(
            nom="Terre",
            masse=5.97e24,
            rayon=6.38e6,
            position=np.array([1.496e11, 0.0, 0.0]),
            vitesse=np.array([0.0, 29.783e3, 0.0]),
            couleur=(0, 0, 255)
        )
        
        self.etoile = CorpsCeleste(
            nom="Soleil",
            masse=1.99e30,
            rayon=6.95e8,
            position=np.zeros(3),
            vitesse=np.zeros(3),
            couleur=(255, 255, 0)
        )
        
        self.systeme = SystemeSolaire("data/planets.json")
        self.visu = Visualisation(largeur=800, hauteur=600)
    
    def tearDown(self):
        """Nettoie après chaque test."""
        self.visu.fermer()
    
    def test_initialisation(self):
        """Test de l'initialisation de la visualisation."""
        self.assertIsNotNone(self.visu.fenetre)
        self.assertEqual(self.visu.fenetre.get_width(), 800)
        self.assertEqual(self.visu.fenetre.get_height(), 600)
        self.assertEqual(self.visu.NOIR, (0, 0, 0))
        self.assertEqual(self.visu.BLANC, (255, 255, 255))
    
    def test_convertir_coordonnees(self):
        """Test de la conversion des coordonnées."""
        # Test avec une position au centre
        pos_centre = np.array([0.0, 0.0, 0.0])
        x, y = self.visu.convertir_coordonnees(pos_centre)
        self.assertEqual(x, 400)  # 800/2
        self.assertEqual(y, 300)  # 600/2
        
        # Test avec une position à droite
        pos_droite = np.array([1e12, 0.0, 0.0])
        x, y = self.visu.convertir_coordonnees(pos_droite)
        self.assertGreater(x, 400)
    
    def test_dessiner_corps(self):
        """Test du dessin d'un corps."""
        # Vérifie que la méthode ne lève pas d'exception
        try:
            self.visu.dessiner_corps(self.planete)
        except Exception as e:
            self.fail(f"dessiner_corps a levé une exception : {e}")
    
    def test_dessiner_trajectoire(self):
        """Test du dessin d'une trajectoire."""
        # Ajoute quelques points à la trajectoire
        self.planete.trajectoire = [
            np.array([1.496e11, 0.0, 0.0]),
            np.array([0.0, 1.496e11, 0.0]),
            np.array([-1.496e11, 0.0, 0.0])
        ]
        
        # Vérifie que la méthode ne lève pas d'exception
        try:
            self.visu.dessiner_trajectoire(self.planete)
        except Exception as e:
            self.fail(f"dessiner_trajectoire a levé une exception : {e}")
    
    def test_dessiner_systeme(self):
        """Test du dessin du système complet."""
        # Vérifie que la méthode ne lève pas d'exception
        try:
            self.visu.dessiner_systeme(self.systeme)
        except Exception as e:
            self.fail(f"dessiner_systeme a levé une exception : {e}")
    
    def test_gerer_evenements(self):
        """Test de la gestion des événements."""
        # Simule un événement QUIT
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        self.assertFalse(self.visu.gerer_evenements())
        
        # Simule un événement KEYDOWN avec Échap
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE))
        self.assertFalse(self.visu.gerer_evenements())
        
        # Simule un événement KEYDOWN avec une autre touche
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE))
        self.assertTrue(self.visu.gerer_evenements())


if __name__ == '__main__':
    unittest.main() 