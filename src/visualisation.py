import pygame
import numpy as np
from datetime import datetime, timedelta
from typing import Tuple, Dict, List
from src.modele import SystemeSolaire, CorpsCeleste


class Visualisation:
    """Classe gérant l'affichage 2D du système solaire."""
    
    def __init__(self, largeur: int = 800, hauteur: int = 600, duree_trajectoire: float = 90.0):
        """Initialise la visualisation.
        
        Args:
            largeur (int): Largeur de la fenêtre en pixels
            hauteur (int): Hauteur de la fenêtre en pixels
            duree_trajectoire (float): Durée de conservation des trajectoires en jours
        """
        pygame.init()
        self.ecran = pygame.display.set_mode((largeur, hauteur), pygame.RESIZABLE)
        pygame.display.set_caption("Simulation du Système Solaire")
        self.largeur = largeur
        self.hauteur = hauteur
        self.duree_trajectoire = duree_trajectoire
        self.trajectoires: Dict[CorpsCeleste, List[Tuple[np.ndarray, float]]] = {}
        self.temps_actuel = 0.0  # Temps en jours
        self.marge = 50  # Marge en pixels pour éviter que les planètes touchent les bords
        self.date_debut = datetime.now()  # Date de début de la simulation (date actuelle)
        
        # Couleurs
        self.NOIR = (0, 0, 0)
        self.BLANC = (255, 255, 255)
    
    def calculer_echelle(self, systeme: SystemeSolaire) -> float:
        """Calcule l'échelle appropriée pour afficher tous les corps.
        
        Args:
            systeme (SystemeSolaire): Système solaire à afficher
            
        Returns:
            float: Échelle en pixels/mètre
        """
        # Trouve les positions extrêmes
        x_min = y_min = float('inf')
        x_max = y_max = float('-inf')
        
        # Prend en compte toutes les planètes
        for corps in systeme.obtenir_tous_corps():
            x, y = corps.position[0], corps.position[1]
            x_min = min(x_min, x)
            x_max = max(x_max, x)
            y_min = min(y_min, y)
            y_max = max(y_max, y)
            
            # Prend aussi en compte les trajectoires
            if corps in self.trajectoires:
                for position, _ in self.trajectoires[corps]:
                    x, y = position[0], position[1]
                    x_min = min(x_min, x)
                    x_max = max(x_max, x)
                    y_min = min(y_min, y)
                    y_max = max(y_max, y)
        
        # Ajoute une marge de 10% pour éviter que les planètes touchent les bords
        marge_x = (x_max - x_min) * 0.1
        marge_y = (y_max - y_min) * 0.1
        x_min -= marge_x
        x_max += marge_x
        y_min -= marge_y
        y_max += marge_y
        
        # Calcule les dimensions nécessaires
        largeur_necessaire = x_max - x_min
        hauteur_necessaire = y_max - y_min
        
        # Calcule l'échelle pour chaque dimension
        echelle_x = (self.largeur - 2 * self.marge) / largeur_necessaire if largeur_necessaire > 0 else 1e-10
        echelle_y = (self.hauteur - 2 * self.marge) / hauteur_necessaire if hauteur_necessaire > 0 else 1e-10
        
        # Utilise l'échelle la plus petite pour conserver les proportions
        return min(echelle_x, echelle_y)
    
    def convertir_coordonnees(self, position: np.ndarray, echelle: float) -> Tuple[int, int]:
        """Convertit des coordonnées du monde réel en coordonnées d'écran.
        
        Args:
            position (np.ndarray): Position en mètres
            echelle (float): Échelle en pixels/mètre
            
        Returns:
            Tuple[int, int]: Position en pixels
        """
        x = int(position[0] * echelle + self.largeur / 2)
        y = int(position[1] * echelle + self.hauteur / 2)
        return (x, y)
    
    def ajouter_point_trajectoire(self, corps: CorpsCeleste, position: np.ndarray) -> None:
        """Ajoute un point à la trajectoire d'un corps.
        
        Args:
            corps (CorpsCeleste): Corps dont on ajoute un point
            position (np.ndarray): Position du point
        """
        if corps not in self.trajectoires:
            self.trajectoires[corps] = []
        
        self.trajectoires[corps].append((position.copy(), self.temps_actuel))
        self.nettoyer_trajectoire(corps)
    
    def nettoyer_trajectoire(self, corps: CorpsCeleste) -> None:
        """Nettoie les points de trajectoire plus vieux que duree_trajectoire jours.
        
        Args:
            corps (CorpsCeleste): Corps dont on nettoie la trajectoire
        """
        if corps not in self.trajectoires:
            return
            
        # Trouve l'index du premier point à conserver
        index_debut = 0
        for i, (_, temps) in enumerate(self.trajectoires[corps]):
            if self.temps_actuel - temps <= self.duree_trajectoire:
                index_debut = i
                break
        
        # Supprime les points trop anciens
        if index_debut > 0:
            self.trajectoires[corps] = self.trajectoires[corps][index_debut:]
    
    def mettre_a_jour_temps(self, temps: float) -> None:
        """Met à jour le temps actuel.
        
        Args:
            temps (float): Temps en jours
        """
        self.temps_actuel = temps
    
    def afficher(self, systeme: SystemeSolaire) -> None:
        """Affiche le système solaire.
        
        Args:
            systeme (SystemeSolaire): Système solaire à afficher
        """
        # Calcul de l'échelle
        echelle = self.calculer_echelle(systeme)
        
        # Effacement de l'écran
        self.ecran.fill(self.NOIR)
        
        # Calcul de la date actuelle
        jours_entiers = int(self.temps_actuel)
        fraction_jour = self.temps_actuel - jours_entiers
        secondes_totales = int(fraction_jour * 24 * 3600)  # Conversion en secondes
        heures = secondes_totales // 3600
        minutes = (secondes_totales % 3600) // 60
        secondes = secondes_totales % 60
        
        date_actuelle = self.date_debut + timedelta(days=jours_entiers)
        date_str = date_actuelle.strftime("%d/%m/%Y") + f" {heures:02d}:{minutes:02d}:{secondes:02d}"
        
        # Affichage de la date
        font = pygame.font.Font(None, 24)
        texte_date = font.render(date_str, True, self.BLANC)
        self.ecran.blit(texte_date, (10, 10))
        
        # Affichage des trajectoires
        for corps, points in self.trajectoires.items():
            if len(points) > 1:
                # Conversion des points en coordonnées d'écran
                points_ecran = []
                for position, _ in points:
                    x, y = self.convertir_coordonnees(position, echelle)
                    points_ecran.append((int(x), int(y)))
                
                # Dessin de la trajectoire
                pygame.draw.lines(self.ecran, corps.couleur, False, points_ecran, 1)
        
        # Affichage des corps célestes
        for corps in systeme.obtenir_tous_corps():
            # Conversion des coordonnées
            x, y = self.convertir_coordonnees(corps.position, echelle)
            
            # Dessin du corps
            pygame.draw.circle(self.ecran, corps.couleur, (int(x), int(y)), 5)
            
            # Affichage du nom
            font = pygame.font.Font(None, 24)
            texte = font.render(corps.nom, True, self.BLANC)
            self.ecran.blit(texte, (int(x) + 10, int(y) - 10))
            
            # Ajout du point à la trajectoire
            self.ajouter_point_trajectoire(corps, corps.position)
        
        # Mise à jour de l'affichage
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
            elif event.type == pygame.VIDEORESIZE:
                # Mise à jour de la taille de la fenêtre
                self.ecran = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                self.largeur = event.w
                self.hauteur = event.h
        return True
    
    def fermer(self) -> None:
        """Ferme la fenêtre Pygame."""
        pygame.quit() 