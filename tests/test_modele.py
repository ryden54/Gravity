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
    """Teste la classe SystemeSolaire."""
    
    def setUp(self):
        """Prépare les données de test."""
        # Création des corps célestes de test
        self.soleil = CorpsCeleste(
            nom="Soleil",
            masse=1.989e30,
            rayon=6.96e8,
            position=np.zeros(3),
            vitesse=np.zeros(3),
            couleur=(255, 255, 0)
        )
        
        self.terre = CorpsCeleste(
            nom="Terre",
            masse=5.97e24,
            rayon=6.37e6,
            position=np.array([1.496e11, 0.0, 0.0]),
            vitesse=np.array([0.0, 29.78e3, 0.0]),
            couleur=(0, 0, 255)
        )
        
        # Création du système solaire de test
        self.systeme = SystemeSolaire(
            etoiles=[self.soleil],
            planetes=[self.terre]
        )
    
    def test_obtenir_tous_corps(self):
        """Teste la méthode pour obtenir tous les corps célestes."""
        tous_corps = self.systeme.obtenir_tous_corps()
        
        self.assertEqual(len(tous_corps), 2)
        self.assertIn(self.soleil, tous_corps)
        self.assertIn(self.terre, tous_corps)
        
    def test_calculer_gravite(self):
        """Teste le calcul de la force de gravité entre deux corps."""
        # La force est exercée par le soleil sur la terre
        force = self.systeme.calculer_gravite(self.terre, self.soleil)
        self.assertEqual(len(force), 3)
        self.assertLess(force[0], 0)  # Force attractive vers le soleil (axe x négatif)
        
    def test_calculer_acceleration(self):
        """Teste le calcul de l'accélération d'un corps sous l'effet d'une force."""
        # Force test de 1N dans chaque direction
        force = np.array([1.0, 1.0, 1.0])
        dt = 1.0
        
        acceleration = self.systeme.calculer_acceleration(self.terre, force, dt)
        self.assertEqual(len(acceleration), 3)
        self.assertGreater(acceleration[0], 0)  # Accélération positive en x


class TestSystemeSolaireFactory(unittest.TestCase):
    """Teste la factory de SystemeSolaire."""
    
    def setUp(self):
        """Prépare les données de test."""
        self.temp_fichier = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.json')
        self.temp_fichier.write('''{
            "etoiles": [
                {
                    "nom": "Soleil",
                    "masse": 1.989e30,
                    "rayon": 6.96e8,
                    "position": [0, 0, 0],
                    "vitesse": [0, 0, 0],
                    "couleur": [255, 255, 0]
                }
            ],
            "planetes": [
                {
                    "nom": "Terre",
                    "masse": 5.97e24,
                    "rayon": 6.37e6,
                    "position": [1.496e11, 0, 0],
                    "vitesse": [0, 29.78e3, 0],
                    "couleur": [0, 0, 255]
                }
            ]
        }''')
        self.temp_fichier.close()
        
    def tearDown(self):
        """Nettoie les données de test."""
        os.unlink(self.temp_fichier.name)
        
    def test_charger_donnees(self):
        """Teste le chargement des données depuis un fichier JSON."""
        systeme = SystemeSolaire.depuis_json(self.temp_fichier.name)
        
        self.assertEqual(len(systeme.etoiles), 1)
        self.assertEqual(len(systeme.planetes), 1)
        self.assertEqual(systeme.etoiles[0].nom, "Soleil")
        self.assertEqual(systeme.planetes[0].nom, "Terre")
        
    def test_fichier_inexistant(self):
        """Teste la gestion des fichiers inexistants."""
        systeme = SystemeSolaire.depuis_json("fichier_inexistant.json")
        self.assertEqual(len(systeme.etoiles), 0)
        self.assertEqual(len(systeme.planetes), 0)
        
    def test_fichier_invalide(self):
        """Teste la gestion des fichiers JSON invalides."""
        with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.json') as f:
            f.write("{ json invalide }")
            f.close()
            
        systeme = SystemeSolaire.depuis_json(f.name)
        self.assertEqual(len(systeme.etoiles), 0)
        self.assertEqual(len(systeme.planetes), 0)
        
        os.unlink(f.name)


if __name__ == '__main__':
    unittest.main() 