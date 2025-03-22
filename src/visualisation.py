import pygame
import numpy as np
from typing import Tuple
from src.modele import SystemeSolaire, CorpsCeleste


class Visualisation:
    """Classe gérant l'affichage du système solaire avec Pygame."""
    
    def __init__(self, largeur: int = 1200, hauteur: int = 800):
        """Initialise la fenêtre de visualisation.
        
        Args:
            largeur (int): Largeur de la fenêtre en pixels
            hauteur (int): Hauteur de la fenêtre en pixels
        """
        pygame.init()
        self.fenetre = pygame.display.set_mode((largeur, hauteur))
        pygame.display.set_caption("Simulation du Système Solaire")
        
        # Couleurs
        self.NOIR = (0, 0, 0)
        self.BLANC = (255, 255, 255)
        
        # Facteur d'échelle pour convertir les distances en pixels
        self.echelle = min(largeur, hauteur) / 2e12  # 2e12 m = 2 Tm
    
    def convertir_coordonnees(self, position: np.ndarray) -> Tuple[int, int]:
        """Convertit les coordonnées réelles en coordonnées d'écran.
        
        Args:
            position (np.ndarray): Position en mètres
            
        Returns:
            Tuple[int, int]: Position en pixels
        """
        x = int(position[0] * self.echelle + self.fenetre.get_width() / 2)
        y = int(position[1] * self.echelle + self.fenetre.get_height() / 2)
        return (x, y)
    
    def dessiner_corps(self, corps: CorpsCeleste) -> None:
        """Dessine un corps céleste à l'écran.
        
        Args:
            corps (CorpsCeleste): Corps à dessiner
        """
        # Position à l'écran
        x, y = self.convertir_coordonnees(corps.position)
        
        # Taille du corps (rayon en pixels, minimum 2 pixels)
        rayon = max(2, int(corps.rayon * self.echelle))
        
        # Dessine le corps
        pygame.draw.circle(self.fenetre, corps.couleur, (x, y), rayon)
        
        # Dessine le nom
        police = pygame.font.Font(None, 20)
        texte = police.render(corps.nom, True, self.BLANC)
        self.fenetre.blit(texte, (x + rayon + 5, y - 10))
    
    def dessiner_trajectoire(self, corps: CorpsCeleste) -> None:
        """Dessine la trajectoire d'un corps.
        
        Args:
            corps (CorpsCeleste): Corps dont on dessine la trajectoire
        """
        if len(corps.trajectoire) < 2:
            return
            
        # Dessine la trajectoire avec une couleur plus claire
        couleur = tuple(min(255, c + 100) for c in corps.couleur)
        
        # Convertit tous les points en coordonnées d'écran
        points = [self.convertir_coordonnees(pos) for pos in corps.trajectoire]
        
        # Dessine la ligne
        pygame.draw.lines(self.fenetre, couleur, False, points, 1)
    
    def dessiner_systeme(self, systeme: SystemeSolaire) -> None:
        """Dessine le système solaire complet.
        
        Args:
            systeme (SystemeSolaire): Système à dessiner
        """
        # Efface l'écran
        self.fenetre.fill(self.NOIR)
        
        # Dessine les trajectoires d'abord
        for corps in systeme.obtenir_tous_corps():
            self.dessiner_trajectoire(corps)
        
        # Puis les corps
        for corps in systeme.obtenir_tous_corps():
            self.dessiner_corps(corps)
        
        # Met à jour l'affichage
        pygame.display.flip()
    
    def gerer_evenements(self) -> bool:
        """Gère les événements Pygame.
        
        Returns:
            bool: True si le programme doit continuer, False sinon
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
        return True
    
    def fermer(self) -> None:
        """Ferme la fenêtre Pygame."""
        pygame.quit() 