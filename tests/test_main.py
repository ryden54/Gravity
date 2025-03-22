import unittest
from unittest.mock import patch, MagicMock
import sys
from src.main import main

class TestMain(unittest.TestCase):
    """Tests du script principal."""

    def setUp(self):
        """Préparation des tests."""
        # Sauvegarde des arguments originaux
        self.original_args = sys.argv

    def tearDown(self):
        """Nettoyage après les tests."""
        # Restauration des arguments originaux
        sys.argv = self.original_args

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

        # Capture la sortie standard
        with patch('builtins.print') as mock_print:
            sys.argv = ['main.py']
            main()
            mock_print.assert_called_with("Erreur : Aucune étoile trouvée dans le système.")

    @patch('src.main.SystemeSolaire')
    def test_main_sans_planetes(self, mock_systeme):
        """Test du script principal sans planètes."""
        # Configure le mock
        mock_systeme.depuis_json.return_value = MagicMock(
            etoiles=[MagicMock()],
            planetes=[]
        )

        # Capture la sortie standard
        with patch('builtins.print') as mock_print:
            sys.argv = ['main.py']
            main()
            mock_print.assert_called_with("Erreur : Aucune planète trouvée dans le système.")

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