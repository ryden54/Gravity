import unittest
import numpy as np
import pygame
from src.visualisation import Visualisation
from src.modele import SystemeSolaire, CorpsCeleste


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
        self.visu.systeme = self.systeme  # Initialise le système dans la visualisation
    
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
        
        # Test avec une position décalée
        pos_decalee = np.array([1.496e11, 0.0, 0.0])
        x, y = self.visu.convertir_coordonnees(pos_decalee, echelle)
        self.assertNotEqual(x, 400)  # Ne devrait pas être au centre
        self.assertEqual(y, 300)  # Devrait être sur l'axe horizontal
    
    def test_ajouter_point_trajectoire(self):
        """Test de l'ajout d'un point à la trajectoire."""
        position = np.array([1.496e11, 0.0, 0.0])
        self.visu.ajouter_point_trajectoire(self.planete, position)
        
        # Vérifie que le point a été ajouté
        self.assertIn(self.planete, self.visu.trajectoires)
        self.assertEqual(len(self.visu.trajectoires[self.planete]), 1)
        np.testing.assert_array_equal(self.visu.trajectoires[self.planete][0][0], position)
        
        # Test avec un autre point
        position2 = np.array([0.0, 1.496e11, 0.0])
        self.visu.ajouter_point_trajectoire(self.planete, position2)
        self.assertEqual(len(self.visu.trajectoires[self.planete]), 2)
    
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
    
    def test_mettre_a_jour_temps(self):
        """Test de la mise à jour du temps."""
        temps_test = 42.5
        self.visu.mettre_a_jour_temps(temps_test)
        self.assertEqual(self.visu.temps_actuel, temps_test)
    
    def test_calculer_echelle(self):
        """Test du calcul de l'échelle."""
        # Test avec un système simple
        echelle = self.visu.calculer_echelle(self.systeme)
        self.assertGreater(echelle, 0)

        # Test avec un système vide
        systeme_vide = SystemeSolaire(etoiles=[], planetes=[])
        echelle_vide = self.visu.calculer_echelle(systeme_vide)
        self.assertEqual(echelle_vide, 1e-10)  # Échelle par défaut

        # Test avec un système très grand
        grande_planete = CorpsCeleste(
            nom="Jupiter",
            masse=1.9e27,
            rayon=7.1e7,
            position=np.array([5.2 * 1.496e11, 0.0, 0.0]),  # 5.2 UA
            vitesse=np.array([0.0, 13.1e3, 0.0]),
            couleur=(255, 165, 0)
        )
        systeme_grand = SystemeSolaire(etoiles=[self.etoile], planetes=[grande_planete])
        echelle_grand = self.visu.calculer_echelle(systeme_grand)
        self.assertLess(echelle_grand, echelle)  # Échelle plus petite pour le grand système

        # Test avec un système très petit
        petite_planete = CorpsCeleste(
            nom="Mercure",
            masse=3.3e23,
            rayon=2.4e6,
            position=np.array([0.4 * 1.496e11, 0.0, 0.0]),  # 0.4 UA
            vitesse=np.array([0.0, 47.9e3, 0.0]),
            couleur=(169, 169, 169)
        )
        systeme_petit = SystemeSolaire(etoiles=[self.etoile], planetes=[petite_planete])
        echelle_petit = self.visu.calculer_echelle(systeme_petit)
        self.assertGreater(echelle_petit, echelle)  # Échelle plus grande pour le petit système
    
    def test_gerer_evenements(self):
        """Test de la gestion des événements."""
        # Vérifie que la méthode ne lève pas d'exception
        self.assertTrue(self.visu.gerer_evenements())
        
        # Test de la pause
        self.assertFalse(self.visu.en_pause)
        # Simule l'appui sur la touche espace
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_SPACE}))
        self.visu.gerer_evenements()
        self.assertTrue(self.visu.en_pause)
        
        # Test du redimensionnement
        nouvelle_largeur = 1024
        nouvelle_hauteur = 768
        pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE, {'w': nouvelle_largeur, 'h': nouvelle_hauteur}))
        self.visu.gerer_evenements()
        self.assertEqual(self.visu.largeur, nouvelle_largeur)
        self.assertEqual(self.visu.hauteur, nouvelle_hauteur)
    
    def test_afficher(self):
        """Test de l'affichage du système solaire."""
        # Vérifie que la méthode ne lève pas d'exception
        self.visu.afficher(self.systeme)
        
        # Test avec un système vide
        systeme_vide = SystemeSolaire(etoiles=[], planetes=[])
        self.visu.afficher(systeme_vide)
        
        # Test avec un système en pause
        self.visu.en_pause = True
        self.visu.afficher(self.systeme)
        self.visu.en_pause = False


if __name__ == '__main__':
    unittest.main() 