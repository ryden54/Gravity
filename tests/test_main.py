import unittest
from unittest.mock import patch, MagicMock
import sys
from src.main import main
import os
import json
import pytest

class TestMain(unittest.TestCase):
    """Tests du script principal."""

    def setUp(self):
        """Initialisation des tests"""
        self.test_file = "test_systeme.json"
        self.create_test_file()
        self.original_argv = sys.argv

    def tearDown(self):
        """Nettoyage après les tests"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        sys.argv = self.original_argv

    def create_test_file(self):
        """Crée un fichier de test valide"""
        data = {
            "etoiles": [{
                "nom": "Soleil",
                "masse": 1.989e30,
                "position": [0, 0, 0],
                "vitesse": [0, 0, 0],
                "rayon": 696340e3,
                "couleur": [255, 255, 0]
            }],
            "planetes": [{
                "nom": "Terre",
                "masse": 5.972e24,
                "position": [149.6e9, 0, 0],
                "vitesse": [0, 29.78e3, 0],
                "rayon": 6371e3,
                "couleur": [0, 0, 255]
            }]
        }
        with open(self.test_file, 'w') as f:
            json.dump(data, f)

    def test_main_execution_normale(self):
        """Test de l'exécution normale du programme"""
        with patch('src.main.SystemeSolaire') as mock_systeme, \
             patch('src.main.Simulation') as mock_simulation, \
             patch('src.main.Visualisation') as mock_visu:
            
            # Configuration des mocks
            mock_systeme.depuis_json.return_value = MagicMock(
                etoiles=[MagicMock()],
                planetes=[MagicMock()]
            )
            mock_simulation.return_value = MagicMock()
            mock_visu.return_value = MagicMock(
                gerer_evenements=MagicMock(side_effect=[False])  # Termine la boucle immédiatement
            )
            
            # Configuration des arguments
            sys.argv = ['main.py', '--fichier', self.test_file]
            
            # Exécution
            main()
            
            # Vérifications
            mock_systeme.depuis_json.assert_called_once_with(self.test_file)
            mock_simulation.assert_called_once()
            mock_visu.assert_called_once()

    def test_main_avec_fichier_invalide(self):
        """Test avec un fichier de données invalide"""
        with open(self.test_file, 'w') as f:
            f.write("Données invalides")
        
        with patch('src.main.SystemeSolaire') as mock_systeme:
            mock_systeme.depuis_json.side_effect = ValueError("Format de fichier invalide")
            sys.argv = ['main.py', '--fichier', self.test_file]
            with pytest.raises(ValueError, match="Format de fichier invalide"):
                main()

    def test_main_avec_fichier_inexistant(self):
        """Test avec un fichier inexistant"""
        with patch('src.main.SystemeSolaire') as mock_systeme:
            mock_systeme.depuis_json.side_effect = FileNotFoundError()
            sys.argv = ['main.py', '--fichier', 'fichier_inexistant.json']
            with pytest.raises(FileNotFoundError):
                main()

    def test_main_avec_pas_de_temps_personnalise(self):
        """Test avec un pas de temps personnalisé"""
        with patch('src.main.SystemeSolaire') as mock_systeme, \
             patch('src.main.Simulation') as mock_simulation, \
             patch('src.main.Visualisation') as mock_visu:
            
            # Configuration des mocks
            mock_systeme.depuis_json.return_value = MagicMock(
                etoiles=[MagicMock()],
                planetes=[MagicMock()]
            )
            mock_simulation_instance = MagicMock()
            mock_simulation.return_value = mock_simulation_instance
            mock_visu_instance = MagicMock()
            mock_visu_instance.gerer_evenements.side_effect = [True, False]  # Une itération puis fin
            mock_visu_instance.en_pause = False  # Pas en pause pour que la simulation s'exécute
            mock_visu.return_value = mock_visu_instance
            
            # Configuration des arguments avec pas de temps personnalisé
            sys.argv = ['main.py', '--fichier', self.test_file, '--dt', '7200']
            
            # Exécution
            main()
            
            # Vérification que la simulation utilise le bon pas de temps
            mock_simulation.assert_called_once()
            args, _ = mock_simulation.call_args
            self.assertEqual(args[1], 7200)
            # Vérifie que simuler() a été appelé avec le bon pas de temps
            mock_simulation_instance.simuler.assert_called_with(7200)

    def test_main_avec_erreur_initialisation(self):
        """Test avec une erreur lors de l'initialisation de la simulation"""
        with patch('src.main.SystemeSolaire') as mock_systeme, \
             patch('src.main.Simulation') as mock_simulation, \
             pytest.raises(Exception):
            
            mock_systeme.depuis_json.return_value = MagicMock()
            mock_simulation.side_effect = Exception("Erreur d'initialisation")
            
            sys.argv = ['main.py', '--fichier', self.test_file]
            main()
            mock_systeme.depuis_json.assert_called_once_with(self.test_file)
            mock_simulation.assert_called_once()

    @patch('src.main.SystemeSolaire')
    @patch('src.main.Simulation')
    @patch('src.main.Visualisation')
    def test_main_sans_options(self, mock_visualisation, mock_simulation, mock_systeme):
        """Test du script principal sans options."""
        # Configure les mocks
        mock_systeme.depuis_json.return_value = MagicMock(
            etoiles=[MagicMock()],
            planetes=[MagicMock()]
        )
        mock_visualisation.return_value = MagicMock(
            gerer_evenements=MagicMock(side_effect=[True, False])
        )

        # Simule l'exécution sans arguments
        sys.argv = ['main.py']
        main()

    @patch('src.main.SystemeSolaire')
    def test_main_sans_etoiles(self, mock_systeme):
        """Test du script principal sans étoiles."""
        # Configure le mock
        mock_systeme.depuis_json.return_value = MagicMock(
            etoiles=[],
            planetes=[MagicMock()]
        )

        # Vérifie que l'exception est levée
        sys.argv = ['main.py', '--fichier', self.test_file]
        with pytest.raises(ValueError, match="Aucune étoile trouvée dans le système."):
            main()

    @patch('src.main.SystemeSolaire')
    def test_main_sans_planetes(self, mock_systeme):
        """Test du script principal sans planètes."""
        # Configure le mock
        mock_systeme.depuis_json.return_value = MagicMock(
            etoiles=[MagicMock()],
            planetes=[]
        )

        # Vérifie que l'exception est levée
        sys.argv = ['main.py', '--fichier', self.test_file]
        with pytest.raises(ValueError, match="Aucune planète trouvée dans le système."):
            main()

    @patch('src.main.SystemeSolaire')
    @patch('src.main.Simulation')
    @patch('src.main.Visualisation')
    def test_main_avec_options(self, mock_visualisation, mock_simulation, mock_systeme):
        """Test du script principal avec options."""
        # Configure les mocks
        mock_systeme.depuis_json.return_value = MagicMock(
            etoiles=[MagicMock()],
            planetes=[MagicMock()]
        )
        mock_visualisation.return_value = MagicMock(
            gerer_evenements=MagicMock(side_effect=[True, False])
        )

        # Simule l'exécution avec des options
        sys.argv = ['main.py', '--dt', '0.1', '--fichier', 'test.json']
        main()


if __name__ == '__main__':
    unittest.main() 