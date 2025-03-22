import unittest
import numpy as np
import pygame
from src.modele import SystemeSolaire, CorpsCeleste
from src.visualisation import Visualisation


class TestVisualisation(unittest.TestCase):
    """Tests pour la classe Visualisation."""
    
    def setUp(self):
        """Initialise les données de test."""
        # Création d'un système solaire simplifié pour les tests
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
        
        # Création du système solaire de test
        self.systeme = SystemeSolaire(etoiles=[self.etoile], planetes=[self.planete])
        
        # Création de la visualisation
        self.visu = Visualisation(largeur=800, hauteur=600)
    
    def tearDown(self):
        """Nettoie après chaque test."""
        self.visu.fermer()
    
    def test_initialisation(self):
        """Test de l'initialisation de la visualisation."""
        self.assertIsNotNone(self.visu.ecran)
        self.assertEqual(self.visu.largeur, 800)
        self.assertEqual(self.visu.hauteur, 600)
        self.assertEqual(self.visu.NOIR, (0, 0, 0))
        self.assertEqual(self.visu.BLANC, (255, 255, 255))
    
    def test_convertir_coordonnees(self):
        """Test de la conversion des coordonnées."""
        # Test avec une position au centre
        pos_centre = np.array([0.0, 0.0, 0.0])
        echelle = 1e-9  # 1 pixel = 1e-9 mètres
        x, y = self.visu.convertir_coordonnees(pos_centre, echelle)
        
        # Vérifie que le point est au centre de l'écran
        self.assertEqual(x, 400)  # 800/2
        self.assertEqual(y, 300)  # 600/2
    
    def test_ajouter_point_trajectoire(self):
        """Test de l'ajout d'un point à la trajectoire."""
        position = np.array([1.496e11, 0.0, 0.0])
        self.visu.ajouter_point_trajectoire(self.planete, position)
        
        # Vérifie que le point a été ajouté
        self.assertIn(self.planete, self.visu.trajectoires)
        self.assertEqual(len(self.visu.trajectoires[self.planete]), 1)
        np.testing.assert_array_equal(self.visu.trajectoires[self.planete][0][0], position)
    
    def test_nettoyer_trajectoire(self):
        """Test du nettoyage des trajectoires."""
        # Définit le temps actuel initial
        temps_initial = 100.0
        self.visu.temps_actuel = temps_initial
        
        # Ajoute plusieurs points avec des temps relatifs au temps actuel
        positions = [
            (np.array([1.496e11, 0.0, 0.0]), temps_initial - 80.0),  # 80 jours avant
            (np.array([0.0, 1.496e11, 0.0]), temps_initial - 50.0),  # 50 jours avant
            (np.array([-1.496e11, 0.0, 0.0]), temps_initial - 20.0)  # 20 jours avant
        ]
        self.visu.trajectoires[self.planete] = positions
        
        # Test 1 : Les points sont tous dans la fenêtre de 90 jours
        self.visu.nettoyer_trajectoire(self.planete)
        self.assertEqual(len(self.visu.trajectoires[self.planete]), 3,
                        "Tous les points devraient être conservés car dans la fenêtre de 90 jours")
        
        # Test 2 : Avance le temps de 60 jours
        self.visu.temps_actuel = temps_initial + 60.0
        self.visu.nettoyer_trajectoire(self.planete)
        self.assertEqual(len(self.visu.trajectoires[self.planete]), 1,
                        "Seul le point le plus récent devrait être conservé")
    
    def test_gerer_evenements(self):
        """Test de la gestion des événements."""
        # Vérifie que la méthode ne lève pas d'exception
        self.assertTrue(self.visu.gerer_evenements())


if __name__ == '__main__':
    unittest.main() 