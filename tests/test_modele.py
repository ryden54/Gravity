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
        self.assertTrue(isinstance(corps.trajectoire, list))
        self.assertTrue(np.array_equal(corps.trajectoire[0], np.array([1.4960e11, 0, 0])))

    def test_nettoyage_trajectoire(self):
        """Teste le nettoyage des trajectoires après 3 mois."""
        # Création d'un corps céleste
        corps = CorpsCeleste(
            nom="Test",
            masse=1e24,
            rayon=1e6,
            position=np.array([0.0, 0.0, 0.0]),
            vitesse=np.array([0.0, 0.0, 0.0]),
            couleur=(255, 255, 255)
        )
        
        # Ajout de points de trajectoire sur 4 mois
        for i in range(120):  # 4 mois = 120 jours
            position = np.array([float(i), 0.0, 0.0])
            corps.ajouter_point_trajectoire(position, float(i))
        
        # Vérification de la taille initiale
        self.assertEqual(len(corps.trajectoire), 120)
        self.assertEqual(len(corps.temps_trajectoire), 120)
        
        # Nettoyage à 3 mois
        corps.nettoyer_trajectoire(90.0)
        
        # Vérification de la taille après nettoyage
        self.assertEqual(len(corps.trajectoire), 30)  # Les 30 derniers jours
        self.assertEqual(len(corps.temps_trajectoire), 30)
        
        # Vérification que les points conservés sont les plus récents
        self.assertEqual(corps.temps_trajectoire[0], 90.0)
        self.assertEqual(corps.temps_trajectoire[-1], 119.0)


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
        
        self.assertTrue(np.array_equal(soleil.position, np.array([0, 0, 0])))
        self.assertTrue(np.array_equal(terre.position, np.array([1.4960e11, 0, 0])))
    
    def test_obtenir_tous_corps(self):
        """Teste la méthode pour obtenir tous les corps célestes."""
        systeme = SystemeSolaire(self.temp_fichier.name)
        tous_corps = systeme.obtenir_tous_corps()
        
        self.assertEqual(len(tous_corps), 2)
        self.assertEqual(tous_corps[0].nom, "Soleil")
        self.assertEqual(tous_corps[1].nom, "Terre")


if __name__ == '__main__':
    unittest.main() 