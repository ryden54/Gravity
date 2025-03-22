#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests unitaires pour le modèle de données du système solaire.
"""

import os
import sys
import unittest
import numpy as np
import json
import tempfile

# Ajouter le répertoire parent au chemin de recherche des modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.modele import CorpsCeleste, SystemeSolaire


class TestCorpsCeleste(unittest.TestCase):
    """Tests pour la classe CorpsCeleste."""
    
    def test_init(self):
        """Teste l'initialisation d'un corps céleste."""
        corps = CorpsCeleste(
            nom="Terre",
            masse=5.9724e24,
            rayon=6.3781e6,
            position=[1.4960e11, 0, 0],
            vitesse=[0, 2.9783e4, 0],
            couleur=(0, 0, 255)
        )
        
        self.assertEqual(corps.nom, "Terre")
        self.assertEqual(corps.masse, 5.9724e24)
        self.assertEqual(corps.rayon, 6.3781e6)
        self.assertTrue(np.array_equal(corps.position, np.array([1.4960e11, 0, 0])))
        self.assertTrue(np.array_equal(corps.vitesse, np.array([0, 2.9783e4, 0])))
        self.assertEqual(corps.couleur, (0, 0, 255))
        self.assertTrue(isinstance(corps.id, str))

    def test_post_init(self):
        """Teste la conversion des listes en tableaux numpy."""
        corps = CorpsCeleste(
            nom="Test",
            masse=1.0,
            rayon=1.0,
            position=[1.0, 2.0, 3.0],
            vitesse=[4.0, 5.0, 6.0],
            couleur=(255, 255, 255)
        )
        
        self.assertTrue(isinstance(corps.position, np.ndarray))
        self.assertTrue(isinstance(corps.vitesse, np.ndarray))
        self.assertEqual(corps.position.dtype, np.float64)
        self.assertEqual(corps.vitesse.dtype, np.float64)

    def test_mettre_a_jour_position(self):
        """Teste la mise à jour de la position d'un corps céleste."""
        corps = CorpsCeleste(
            nom="Test",
            masse=1.0,
            rayon=1.0,
            position=[0.0, 0.0, 0.0],
            vitesse=[1.0, 2.0, 3.0],
            couleur=(255, 255, 255)
        )
        
        dt = 2.0  # Pas de temps de 2 secondes
        corps.mettre_a_jour_position(dt)
        
        # Position attendue après dt secondes
        position_attendue = np.array([2.0, 4.0, 6.0])  # position = vitesse * dt
        self.assertTrue(np.allclose(corps.position, position_attendue))

    def test_egalite_corps(self):
        """Teste l'égalité entre deux corps célestes."""
        corps1 = CorpsCeleste(
            nom="Test1",
            masse=1.0,
            rayon=1.0,
            position=[0.0, 0.0, 0.0],
            vitesse=[0.0, 0.0, 0.0],
            couleur=(255, 255, 255)
        )
        
        # Même corps avec des attributs différents mais même ID
        corps2 = CorpsCeleste(
            nom="Test2",
            masse=2.0,
            rayon=2.0,
            position=[1.0, 1.0, 1.0],
            vitesse=[1.0, 1.0, 1.0],
            couleur=(0, 0, 0),
            id=corps1.id
        )
        
        # Corps différent
        corps3 = CorpsCeleste(
            nom="Test3",
            masse=1.0,
            rayon=1.0,
            position=[0.0, 0.0, 0.0],
            vitesse=[0.0, 0.0, 0.0],
            couleur=(255, 255, 255)
        )
        
        self.assertEqual(corps1, corps2)  # Même ID
        self.assertNotEqual(corps1, corps3)  # ID différent
        self.assertNotEqual(corps1, "pas un corps")  # Type différent


class TestSystemeSolaire(unittest.TestCase):
    """Tests pour la classe SystemeSolaire."""
    
    def setUp(self):
        """Crée un fichier JSON temporaire pour les tests."""
        self.donnees_test = {
            "etoiles": [
                {
                    "nom": "Soleil",
                    "masse": 1.989e30,
                    "rayon": 6.95e8,
                    "position": [0, 0, 0],
                    "vitesse": [0, 0, 0],
                    "couleur": [255, 255, 0]
                }
            ],
            "planetes": [
                {
                    "nom": "Terre",
                    "masse": 5.9724e24,
                    "rayon": 6.3781e6,
                    "position": [1.4960e11, 0, 0],
                    "vitesse": [0, 2.9783e4, 0],
                    "couleur": [0, 0, 255]
                }
            ]
        }
        
        self.temp_fichier = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.json')
        json.dump(self.donnees_test, self.temp_fichier)
        self.temp_fichier.close()
    
    def tearDown(self):
        """Supprime le fichier temporaire après les tests."""
        os.unlink(self.temp_fichier.name)
    
    def test_charger_donnees(self):
        """Teste le chargement des données depuis un fichier JSON."""
        systeme = SystemeSolaire(self.temp_fichier.name)
        
        self.assertEqual(len(systeme.etoiles), 1)
        self.assertEqual(len(systeme.planetes), 1)
        
        soleil = systeme.etoiles[0]
        terre = systeme.planetes[0]
        
        self.assertEqual(soleil.nom, "Soleil")
        self.assertEqual(terre.nom, "Terre")
        
        # Vérification que la position de la Terre est sur son orbite
        distance_soleil = np.linalg.norm(terre.position)
        self.assertAlmostEqual(distance_soleil, 1.4960e11, delta=1e6)
        
        # Vérification que la vitesse est perpendiculaire à la position
        produit_scalaire = np.dot(terre.position, terre.vitesse)
        self.assertAlmostEqual(produit_scalaire, 0.0, delta=1e6)
        
        # Vérification que la norme de la vitesse est conservée
        vitesse = np.linalg.norm(terre.vitesse)
        self.assertAlmostEqual(vitesse, 2.9783e4, delta=1.0)
    
    def test_obtenir_tous_corps(self):
        """Teste la méthode pour obtenir tous les corps célestes."""
        systeme = SystemeSolaire(self.temp_fichier.name)
        tous_corps = systeme.obtenir_tous_corps()
        
        self.assertEqual(len(tous_corps), 2)
        self.assertEqual(tous_corps[0].nom, "Soleil")
        self.assertEqual(tous_corps[1].nom, "Terre")
    
    def test_calculer_gravite(self):
        """Teste le calcul de la force de gravité entre deux corps."""
        systeme = SystemeSolaire(self.temp_fichier.name)
        soleil = systeme.etoiles[0]
        terre = systeme.planetes[0]
        
        # Calcul de la force de gravité
        force = systeme.calculer_gravite(terre, soleil)
        
        # La force doit être dirigée vers le soleil
        direction = -terre.position / np.linalg.norm(terre.position)
        force_normalisee = force / np.linalg.norm(force)
        
        # Vérification de la direction
        self.assertTrue(np.allclose(direction, force_normalisee, rtol=1e-10))
        
        # Vérification de l'intensité (loi de Newton)
        distance = np.linalg.norm(terre.position)
        intensite_attendue = systeme.G * terre.masse * soleil.masse / (distance ** 2)
        intensite_calculee = np.linalg.norm(force)
        
        self.assertAlmostEqual(intensite_calculee, intensite_attendue, delta=1e20)
    
    def test_calculer_acceleration(self):
        """Teste le calcul de l'accélération d'un corps sous l'effet d'une force."""
        systeme = SystemeSolaire(self.temp_fichier.name)
        terre = systeme.planetes[0]
        
        # Force test de 1N dans chaque direction
        force = np.array([1.0, 1.0, 1.0])
        dt = 1.0
        
        # Calcul de l'accélération
        delta_v = systeme.calculer_acceleration(terre, force, dt)
        
        # Vérification que a = F/m
        acceleration_attendue = force / terre.masse * dt
        self.assertTrue(np.allclose(delta_v, acceleration_attendue))
    
    def test_erreur_fichier_inexistant(self):
        """Teste la gestion des fichiers inexistants."""
        systeme = SystemeSolaire("fichier_inexistant.json")
        self.assertEqual(len(systeme.etoiles), 0)
        self.assertEqual(len(systeme.planetes), 0)
    
    def test_erreur_fichier_invalide(self):
        """Teste la gestion des fichiers JSON invalides."""
        with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.json') as f:
            f.write("{ json invalide }")
            f.close()
            
        systeme = SystemeSolaire(f.name)
        self.assertEqual(len(systeme.etoiles), 0)
        self.assertEqual(len(systeme.planetes), 0)
        
        os.unlink(f.name)


if __name__ == '__main__':
    unittest.main() 