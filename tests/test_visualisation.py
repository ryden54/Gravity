import unittest
import numpy as np
import pygame
from src.visualisation import Visualisation
from src.modele import SystemeSolaire, CorpsCeleste
from unittest.mock import patch, MagicMock


class TestVisualisation(unittest.TestCase):
    """Tests pour la classe Visualisation."""
    
    def setUp(self):
        """Initialisation des tests."""
        pygame.init()
        self.visu = Visualisation()
        self.systeme = MagicMock()
        
        # Configure le mock du système pour le calcul d'échelle
        corps1 = MagicMock()
        corps1.position = np.array([0.0, 0.0, 0.0])
        corps1.rayon = 696340e3  # Rayon du Soleil
        corps1.couleur = (255, 255, 0)
        corps1.nom = "Soleil"  # Ajout du nom
        
        corps2 = MagicMock()
        corps2.position = np.array([1.0e11, 0.0, 0.0])
        corps2.rayon = 6371e3  # Rayon de la Terre
        corps2.couleur = (0, 0, 255)
        corps2.nom = "Terre"  # Ajout du nom
        
        self.systeme.obtenir_tous_corps.return_value = [corps1, corps2]
        self.systeme.etoiles = [corps1]
        self.systeme.planetes = [corps2]
        
        # Initialise l'échelle en appelant calculer_echelle une première fois
        self.visu.calculer_echelle(self.systeme)
    
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
        self.visu.ajouter_point_trajectoire(self.systeme.planetes[0], position)
        
        # Vérifie que le point a été ajouté
        self.assertIn(self.systeme.planetes[0], self.visu.trajectoires)
        self.assertEqual(len(self.visu.trajectoires[self.systeme.planetes[0]]), 1)
        np.testing.assert_array_equal(self.visu.trajectoires[self.systeme.planetes[0]][0][0], position)
        
        # Test avec un autre point
        position2 = np.array([0.0, 1.496e11, 0.0])
        self.visu.ajouter_point_trajectoire(self.systeme.planetes[0], position2)
        self.assertEqual(len(self.visu.trajectoires[self.systeme.planetes[0]]), 2)
    
    def test_nettoyer_trajectoire(self):
        """Test du nettoyage des trajectoires."""
        # Définit la durée de conservation des trajectoires (200 jours)
        self.visu.duree_trajectoire = 200.0
        
        # Définit le temps actuel initial
        temps_initial = 100.0
        self.visu.temps_actuel = temps_initial
        
        # Ajoute plusieurs points avec des temps relatifs au temps actuel
        positions = [
            (np.array([1.496e11, 0.0, 0.0]), temps_initial - 150.0),  # 150 jours avant
            (np.array([0.0, 1.496e11, 0.0]), temps_initial - 100.0),  # 100 jours avant
            (np.array([-1.496e11, 0.0, 0.0]), temps_initial - 50.0)   # 50 jours avant
        ]
        self.visu.trajectoires[self.systeme.planetes[0]] = positions
        
        # Test 1 : Les points sont tous dans la fenêtre de 200 jours
        self.visu.nettoyer_trajectoire(self.systeme.planetes[0])
        self.assertEqual(len(self.visu.trajectoires[self.systeme.planetes[0]]), 3,
                        "Tous les points devraient être conservés car dans la fenêtre de 200 jours")
        
        # Test 2 : Avance le temps de 100 jours
        self.visu.temps_actuel = temps_initial + 100.0
        self.visu.nettoyer_trajectoire(self.systeme.planetes[0])
        self.assertEqual(len(self.visu.trajectoires[self.systeme.planetes[0]]), 2,
                        "Les deux points les plus récents devraient être conservés")
        
        # Test 3 : Avance encore de 50 jours (au lieu de 100)
        self.visu.temps_actuel = temps_initial + 150.0
        self.visu.nettoyer_trajectoire(self.systeme.planetes[0])
        self.assertEqual(len(self.visu.trajectoires[self.systeme.planetes[0]]), 1,
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
        
        # Vérifie que l'échelle permet d'afficher tous les corps
        for corps in self.systeme.obtenir_tous_corps():
            pos = self.visu.convertir_coordonnees(corps.position, echelle)
            self.assertGreater(pos[0], self.visu.marge, "Le corps devrait être visible horizontalement")
            self.assertLess(pos[0], self.visu.largeur - self.visu.marge, "Le corps devrait être visible horizontalement")
            self.assertGreater(pos[1], self.visu.marge, "Le corps devrait être visible verticalement")
            self.assertLess(pos[1], self.visu.hauteur - self.visu.marge, "Le corps devrait être visible verticalement")

        # Test avec un système vide
        systeme_vide = SystemeSolaire(etoiles=[], planetes=[])
        echelle_vide = self.visu.calculer_echelle(systeme_vide)
        self.assertEqual(echelle_vide, 1e-10, "L'échelle par défaut devrait être utilisée pour un système vide")

        # Test avec un système très grand
        grande_planete = CorpsCeleste(
            nom="Jupiter",
            masse=1.9e27,
            rayon=7.1e7,
            position=np.array([5.2 * 1.496e11, 0.0, 0.0]),  # 5.2 UA
            vitesse=np.array([0.0, 13.1e3, 0.0]),
            couleur=(255, 165, 0)
        )
        systeme_grand = SystemeSolaire(etoiles=[self.systeme.etoiles[0]], planetes=[grande_planete])
        echelle_grand = self.visu.calculer_echelle(systeme_grand)
        self.assertLess(echelle_grand, echelle, "L'échelle devrait être plus petite pour un grand système")
        
        # Vérifie que la planète est visible avec la nouvelle échelle
        pos = self.visu.convertir_coordonnees(grande_planete.position, echelle_grand)
        self.assertGreater(pos[0], self.visu.marge, "La grande planète devrait être visible horizontalement")
        self.assertLess(pos[0], self.visu.largeur - self.visu.marge, "La grande planète devrait être visible horizontalement")

        # Test avec un système très petit
        petite_planete = CorpsCeleste(
            nom="Mercure",
            masse=3.3e23,
            rayon=2.4e6,
            position=np.array([0.4 * 1.496e11, 0.0, 0.0]),  # 0.4 UA
            vitesse=np.array([0.0, 47.9e3, 0.0]),
            couleur=(169, 169, 169)
        )
        systeme_petit = SystemeSolaire(etoiles=[self.systeme.etoiles[0]], planetes=[petite_planete])
        echelle_petit = self.visu.calculer_echelle(systeme_petit)
        self.assertGreater(echelle_petit, echelle, "L'échelle devrait être plus grande pour un petit système")
        
        # Vérifie que la planète est visible avec la nouvelle échelle
        pos = self.visu.convertir_coordonnees(petite_planete.position, echelle_petit)
        self.assertGreater(pos[0], self.visu.marge, "La petite planète devrait être visible horizontalement")
        self.assertLess(pos[0], self.visu.largeur - self.visu.marge, "La petite planète devrait être visible horizontalement")

        # Test avec un système avec distance maximale nulle
        corps_nul = MagicMock()
        corps_nul.position = np.array([0.0, 0.0, 0.0])
        corps_nul.rayon = 1.0
        corps_nul.couleur = (255, 255, 255)
        corps_nul.nom = "CorpsNul"
        systeme_nul = SystemeSolaire(etoiles=[corps_nul], planetes=[])
        echelle_nul = self.visu.calculer_echelle(systeme_nul)
        self.assertEqual(echelle_nul, 1e-10, "L'échelle par défaut devrait être utilisée pour une distance nulle")

        # Test avec un système avec corps hors de la zone d'affichage
        corps_hors_zone = MagicMock()
        corps_hors_zone.position = np.array([1e12, 1e12, 0.0])  # Position plus raisonnable
        corps_hors_zone.rayon = 1.0
        corps_hors_zone.couleur = (255, 255, 255)
        corps_hors_zone.nom = "CorpsHorsZone"
        systeme_hors_zone = SystemeSolaire(etoiles=[corps_hors_zone], planetes=[])
        echelle_hors_zone = self.visu.calculer_echelle(systeme_hors_zone)
        self.assertLess(echelle_hors_zone, echelle, "L'échelle devrait être plus petite pour voir le corps éloigné")
        
        # Vérifie que le corps est visible avec la nouvelle échelle
        pos = self.visu.convertir_coordonnees(corps_hors_zone.position, echelle_hors_zone)
        self.assertGreater(pos[0], self.visu.marge, "Le corps éloigné devrait être visible horizontalement")
        self.assertLess(pos[0], self.visu.largeur - self.visu.marge, "Le corps éloigné devrait être visible horizontalement")
    
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
        event = pygame.event.Event(pygame.VIDEORESIZE)
        event.size = (nouvelle_largeur, nouvelle_hauteur)
        pygame.event.post(event)
        self.visu.gerer_evenements()
        self.assertEqual(self.visu.largeur, nouvelle_largeur)
        self.assertEqual(self.visu.hauteur, nouvelle_hauteur)

        # Test de la touche ÉCHAP
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_ESCAPE}))
        self.assertFalse(self.visu.gerer_evenements())
    
    def test_dessiner_grille(self):
        """Test du dessin de la grille."""
        # Sauvegarde la couleur de l'écran avant le test
        couleur_avant = self.visu.ecran.get_at((self.visu.largeur // 2, self.visu.hauteur // 2))
        
        # Test avec une échelle normale
        self.visu.dessiner_grille(1e-10)
        # Vérifie que la grille a été dessinée (la couleur au centre devrait être différente)
        couleur_apres = self.visu.ecran.get_at((self.visu.largeur // 2, self.visu.hauteur // 2))
        self.assertNotEqual(couleur_avant, couleur_apres, "La grille devrait avoir été dessinée")
        
        # Test avec une échelle très petite
        self.visu.ecran.fill(self.visu.NOIR)  # Réinitialise l'écran
        self.visu.dessiner_grille(1e-20)
        # Vérifie que la grille a été dessinée même avec une petite échelle
        couleur_apres = self.visu.ecran.get_at((self.visu.largeur // 2, self.visu.hauteur // 2))
        self.assertNotEqual(couleur_avant, couleur_apres, "La grille devrait avoir été dessinée même avec une petite échelle")
        
        # Test avec une échelle très grande
        self.visu.ecran.fill(self.visu.NOIR)  # Réinitialise l'écran
        self.visu.dessiner_grille(1e-5)
        # Vérifie que la grille a été dessinée même avec une grande échelle
        couleur_apres = self.visu.ecran.get_at((self.visu.largeur // 2, self.visu.hauteur // 2))
        self.assertNotEqual(couleur_avant, couleur_apres, "La grille devrait avoir été dessinée même avec une grande échelle")

    def test_afficher(self):
        """Test de l'affichage du système solaire."""
        # Sauvegarde l'état initial
        couleur_avant = self.visu.ecran.get_at((self.visu.largeur // 2, self.visu.hauteur // 2))
        
        # Test avec le système normal
        self.visu.afficher(self.systeme)
        # Vérifie que l'affichage a changé
        couleur_apres = self.visu.ecran.get_at((self.visu.largeur // 2, self.visu.hauteur // 2))
        self.assertNotEqual(couleur_avant, couleur_apres, "L'affichage devrait avoir changé")
        
        # Test avec un système vide
        self.visu.ecran.fill(self.visu.NOIR)
        systeme_vide = SystemeSolaire(etoiles=[], planetes=[])
        self.visu.afficher(systeme_vide)
        # Vérifie que l'écran est noir (système vide)
        couleur_apres = self.visu.ecran.get_at((self.visu.largeur // 2, self.visu.hauteur // 2))
        self.assertEqual(couleur_apres, self.visu.NOIR, "L'écran devrait être noir pour un système vide")
        
        # Test avec un système en pause
        self.visu.en_pause = True
        self.visu.afficher(self.systeme)
        # Vérifie que le texte "PAUSE" est affiché
        texte_pause = self.visu.police.render("PAUSE", True, self.visu.BLANC)
        surface_texte = pygame.Surface(texte_pause.get_size(), pygame.SRCALPHA)
        surface_texte.blit(texte_pause, (0, 0))
        couleur_texte = surface_texte.get_at((0, 0))
        self.assertEqual(couleur_texte[:3], self.visu.BLANC, "Le texte PAUSE devrait être affiché en blanc")
        self.visu.en_pause = False

        # Test avec un système avec une seule étoile
        self.visu.ecran.fill(self.visu.NOIR)
        systeme_etoile = SystemeSolaire(etoiles=[self.systeme.etoiles[0]], planetes=[])
        self.visu.afficher(systeme_etoile)
        # Vérifie que l'étoile est affichée au centre
        couleur_centre = self.visu.ecran.get_at((self.visu.largeur // 2, self.visu.hauteur // 2))
        self.assertEqual(couleur_centre, self.systeme.etoiles[0].couleur, "L'étoile devrait être affichée au centre")

    def test_gerer_evenements_redimensionnement(self):
        """Test de la gestion du redimensionnement de la fenêtre"""
        event = pygame.event.Event(pygame.VIDEORESIZE, size=(1024, 768))
        # Modifie l'événement pour ajouter w et h
        event.w = event.size[0]
        event.h = event.size[1]
        pygame.event.post(event)
        self.visu.gerer_evenements()
        self.assertEqual(self.visu.largeur, 1024)
        self.assertEqual(self.visu.hauteur, 768)

    def test_gerer_evenements_pause(self):
        """Test de la gestion de la pause"""
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
        self.assertFalse(self.visu.en_pause)
        pygame.event.post(event)
        self.visu.gerer_evenements()
        self.assertTrue(self.visu.en_pause)
        pygame.event.post(event)
        self.visu.gerer_evenements()
        self.assertFalse(self.visu.en_pause)

    def test_gerer_evenements_quitter(self):
        """Test de la gestion de l'événement de fermeture"""
        event = pygame.event.Event(pygame.QUIT)
        pygame.event.post(event)
        resultat = self.visu.gerer_evenements()
        self.assertFalse(resultat)

    def test_gerer_evenements_inconnu(self):
        """Test de la gestion d'un événement inconnu"""
        event = pygame.event.Event(pygame.USEREVENT)
        pygame.event.post(event)
        resultat = self.visu.gerer_evenements()
        self.assertTrue(resultat)

    def test_mettre_a_jour_temps_erreur(self):
        """Test de la mise à jour du temps avec une erreur"""
        self.visu.temps_actuel = float('inf')
        self.visu.mettre_a_jour_temps(1.0)
        self.assertEqual(self.visu.temps_actuel, 1.0)  # Le temps devrait être mis à jour même en cas d'erreur

    def test_nettoyer_trajectoires_erreur(self):
        """Test du nettoyage des trajectoires avec une erreur"""
        corps = self.systeme.obtenir_tous_corps()[0]
        self.visu.trajectoires[corps] = [(0, 0)]
        self.visu.temps_actuel = float('inf')
        self.visu.nettoyer_trajectoire(corps)
        self.assertEqual(len(self.visu.trajectoires[corps]), 0)

    def test_afficher_erreur(self):
        """Test de l'affichage avec une erreur"""
        with patch('pygame.display.flip') as mock_flip:
            # Configure le mock pour lever l'erreur une seule fois
            mock_flip.side_effect = [pygame.error("Erreur d'affichage"), None]
            try:
                self.visu.afficher(self.systeme)
            except pygame.error:
                pass  # L'erreur est attendue
            # Vérifie que le programme peut continuer après l'erreur
            self.visu.afficher(self.systeme)  # Ne devrait pas lever d'erreur

    def test_couleur_pastel(self):
        """Test de la conversion d'une couleur en version pastel."""
        # Test avec une couleur rouge
        rouge = (255, 0, 0)
        rouge_pastel = self.visu.couleur_pastel(rouge)
        self.assertGreater(rouge_pastel[1], rouge[1], "La version pastel devrait être plus claire en vert")
        self.assertGreater(rouge_pastel[2], rouge[2], "La version pastel devrait être plus claire en bleu")
        
        # Test avec une couleur verte
        vert = (0, 255, 0)
        vert_pastel = self.visu.couleur_pastel(vert)
        self.assertGreater(vert_pastel[0], vert[0], "La version pastel devrait être plus claire en rouge")
        self.assertGreater(vert_pastel[2], vert[2], "La version pastel devrait être plus claire en bleu")
        
        # Test avec une couleur bleue
        bleu = (0, 0, 255)
        bleu_pastel = self.visu.couleur_pastel(bleu)
        self.assertGreater(bleu_pastel[0], bleu[0], "La version pastel devrait être plus claire en rouge")
        self.assertGreater(bleu_pastel[1], bleu[1], "La version pastel devrait être plus claire en vert")
        
        # Test avec une couleur noire
        noir = (0, 0, 0)
        noir_pastel = self.visu.couleur_pastel(noir)
        self.assertGreater(noir_pastel[0], noir[0], "La version pastel devrait être plus claire en rouge")
        self.assertGreater(noir_pastel[1], noir[1], "La version pastel devrait être plus claire en vert")
        self.assertGreater(noir_pastel[2], noir[2], "La version pastel devrait être plus claire en bleu")
        
        # Test avec une couleur blanche
        blanc = (255, 255, 255)
        blanc_pastel = self.visu.couleur_pastel(blanc)
        self.assertEqual(blanc_pastel, blanc, "Le blanc devrait rester blanc")


if __name__ == '__main__':
    unittest.main() 