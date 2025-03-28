import pygame
import numpy as np
from datetime import datetime, timedelta
from typing import Tuple, Dict, List
from src.modele import SystemeSolaire, CorpsCeleste


class Visualisation:
    """Classe gérant l'affichage 2D du système solaire."""
    
    def __init__(self, largeur: int = 800, hauteur: int = 600, duree_trajectoire: float = 365.0):
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
        self.en_pause = False  # État de pause de la simulation
        self.echelle_courante = None  # Échelle actuelle pour l'affichage
        self._dernier_systeme = None  # Dernier système affiché
        self.police = pygame.font.Font(None, 36)
        
        # Couleurs
        self.NOIR = (0, 0, 0)
        self.BLANC = (255, 255, 255)
        self.GRIS = (80, 80, 80)
    
    def couleur_pastel(self, couleur: Tuple[int, int, int]) -> Tuple[int, int, int]:
        """Convertit une couleur en sa version pastel.
        
        Args:
            couleur (Tuple[int, int, int]): Couleur RGB à convertir
            
        Returns:
            Tuple[int, int, int]: Version pastel de la couleur
        """
        # Pour créer une version pastel, on mélange la couleur avec du blanc
        # et on réduit légèrement la saturation
        r, g, b = couleur
        return (
            int((r + 255) / 2),  # Mélange avec du blanc
            int((g + 255) / 2),
            int((b + 255) / 2)
        )
    
    def calculer_echelle(self, systeme: SystemeSolaire) -> float:
        """Calcule l'échelle appropriée pour afficher tous les corps.
        
        Args:
            systeme (SystemeSolaire): Système solaire à afficher
            
        Returns:
            float: Échelle en pixels/mètre
        """
        # Réinitialise l'échelle courante si c'est un nouveau système
        if not hasattr(self, '_dernier_systeme') or self._dernier_systeme != systeme:
            self._dernier_systeme = systeme
            self.echelle_courante = None
        
        # Si le système est vide, retourne une échelle par défaut
        if not systeme.etoiles and not systeme.planetes:
            return 1e-10
        
        # Trouve la distance maximale entre les corps
        distance_max = 0.0
        for corps in systeme.obtenir_tous_corps():
            distance = np.linalg.norm(corps.position)
            distance_max = max(distance_max, distance)
        
        # Si aucune distance n'est trouvée, retourne une échelle par défaut
        if distance_max == 0.0:
            return 1e-10
        
        # Calcule l'échelle pour que le système tienne dans la fenêtre
        # avec une marge de 20%
        marge = 0.2
        echelle = (min(self.largeur, self.hauteur) * (1 - 2 * marge)) / (2 * distance_max)
        
        # Ajuste l'échelle pour qu'elle soit dans une plage raisonnable
        echelle_min = 1e-12
        echelle_max = 1e-8
        nouvelle_echelle = max(min(echelle, echelle_max), echelle_min)
        
        # Si c'est la première fois qu'on calcule l'échelle
        if self.echelle_courante is None:
            self.echelle_courante = nouvelle_echelle
            return nouvelle_echelle
        
        # Si la nouvelle échelle est plus petite (zoom out nécessaire)
        if nouvelle_echelle < self.echelle_courante:
            # Vérifie si un corps sort de la zone d'affichage avec l'échelle courante
            corps_visible = True
            for corps in systeme.obtenir_tous_corps():
                x = corps.position[0] * self.echelle_courante + self.largeur / 2
                y = corps.position[1] * self.echelle_courante + self.hauteur / 2
                if (x < self.marge or x > self.largeur - self.marge or 
                    y < self.marge or y > self.hauteur - self.marge):
                    corps_visible = False
                    break
            
            # Si un corps n'est plus visible, on applique la nouvelle échelle
            if not corps_visible:
                self.echelle_courante = nouvelle_echelle
        
        # Si la nouvelle échelle est plus grande (zoom in possible)
        elif nouvelle_echelle > self.echelle_courante * 2:
            # Vérifie si tous les corps sont dans la moitié centrale de la zone d'affichage
            tous_proches = True
            zone_centrale = min(self.largeur, self.hauteur) * 0.25  # 25% de la plus petite dimension
            
            for corps in systeme.obtenir_tous_corps():
                x = corps.position[0] * self.echelle_courante
                y = corps.position[1] * self.echelle_courante
                if (abs(x) > zone_centrale or abs(y) > zone_centrale):
                    tous_proches = False
                    break
            
            # Si tous les corps sont proches, on augmente progressivement l'échelle
            if tous_proches:
                self.echelle_courante = self.echelle_courante * 1.1  # Augmente de 10% à chaque fois
        
        return self.echelle_courante
    
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
            
        # Supprime les points plus anciens que duree_trajectoire jours
        self.trajectoires[corps] = [
            (pos, temps) for pos, temps in self.trajectoires[corps]
            if self.temps_actuel - temps <= self.duree_trajectoire
        ]
    
    def mettre_a_jour_temps(self, temps: float) -> None:
        """Met à jour le temps actuel.
        
        Args:
            temps (float): Temps en jours
        """
        self.temps_actuel = temps
    
    def dessiner_grille(self, echelle: float) -> None:
        """Dessine une grille de cercles concentriques pour aider à la lisibilité.
        
        Args:
            echelle (float): Échelle en pixels/mètre
        """
        # Couleur de la grille (gris plus foncé)
        GRIS = (40, 40, 40)
        
        # Centre de l'écran
        centre_x = self.largeur // 2
        centre_y = self.hauteur // 2
        
        # Rayon de la plus grande orbite visible (Mars : 1.524 UA)
        max_rayon = 2.0  # UA
        
        # Nombre de cercles à dessiner
        nb_cercles = int(max_rayon * 3)  # 1 cercle par 1/3 d'UA
        
        # Conversion UA en pixels
        ua_en_pixels = 149597870700 * echelle  # 1 UA = 149597870700 mètres
        
        # Police pour les légendes
        font = pygame.font.Font(None, 20)
        
        # Dessine les cercles concentriques et les légendes
        for i in range(1, nb_cercles + 1):
            rayon = (i / 3) * ua_en_pixels  # Rayon en pixels
            pygame.draw.circle(self.ecran, GRIS, (centre_x, centre_y), int(rayon), 1)
            
            # Affichage de la légende sur l'axe Y
            distance_ua = i / 3  # Distance en UA
            texte = font.render(f"{distance_ua:.1f} UA", True, GRIS)
            # Position du texte à droite du cercle sur l'axe Y
            self.ecran.blit(texte, (centre_x + int(rayon) + 5, centre_y - 10))
        
        # Dessine les lignes radiales
        for angle in range(0, 360, 45):  # Lignes tous les 45 degrés
            rad = np.radians(angle)
            x = centre_x + int(max_rayon * ua_en_pixels * np.cos(rad))
            y = centre_y + int(max_rayon * ua_en_pixels * np.sin(rad))
            pygame.draw.line(self.ecran, GRIS, (centre_x, centre_y), (x, y), 1)
    
    def afficher(self, systeme: SystemeSolaire) -> None:
        """Affiche le système solaire.
        
        Args:
            systeme (SystemeSolaire): Système solaire à afficher
        """
        # Calcul de l'échelle pour les positions
        echelle_position = self.calculer_echelle(systeme)
        
        # Échelle pour la taille des corps (logarithmique)
        # On utilise une échelle plus petite et on applique une fonction logarithmique
        echelle_taille = echelle_position * 100  # Facteur de base plus petit
        facteur_log = 5.0  # Facteur pour la fonction logarithmique (augmenté de 2.0 à 5.0)
        
        # Efface l'écran
        self.ecran.fill(self.NOIR)
        
        # Dessine la grille seulement si le système n'est pas vide
        if systeme.obtenir_tous_corps():
            self.dessiner_grille(echelle_position)
        
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
        texte_date = self.police.render(date_str, True, self.BLANC)
        self.ecran.blit(texte_date, (10, 10))
        
        # Affichage de l'état de pause
        if self.en_pause:
            texte_pause = self.police.render("PAUSE", True, self.BLANC)
            self.ecran.blit(texte_pause, (self.largeur - 100, 10))
        
        # Affichage des trajectoires
        for corps, points in self.trajectoires.items():
            if len(points) > 1:
                # Dessine les lignes de la trajectoire avec la couleur pastel
                couleur_trajectoire = self.couleur_pastel(corps.couleur)
                for i in range(len(points) - 1):
                    pos1 = self.convertir_coordonnees(points[i][0], echelle_position)
                    pos2 = self.convertir_coordonnees(points[i + 1][0], echelle_position)
                    pygame.draw.line(self.ecran, couleur_trajectoire, pos1, pos2, 1)
        
        # Affichage des corps célestes
        for corps in systeme.obtenir_tous_corps():
            # Conversion des coordonnées avec l'échelle de position
            pos = self.convertir_coordonnees(corps.position, echelle_position)
            
            # Calcul de la taille à l'échelle (en pixels)
            # On utilise une fonction logarithmique pour la taille
            taille_reelle = np.log1p(corps.rayon * echelle_taille) * facteur_log
            
            # Taille minimale pour la visibilité (2 pixels)
            taille_min = 2
            taille = max(taille_reelle, taille_min)
            
            # Taille maximale pour éviter que le soleil n'occupe toute la fenêtre
            taille_max = min(self.largeur, self.hauteur) * 0.2  # 20% de la plus petite dimension
            taille = min(taille, taille_max)
            
            # Dessin du corps
            pygame.draw.circle(self.ecran, corps.couleur, pos, int(taille))
            
            # Affichage du nom
            font = pygame.font.Font(None, 24)
            texte = font.render(corps.nom, True, self.BLANC)
            
            # Position du texte
            if corps.nom == "Soleil":
                # Pour le soleil, on place le texte plus loin et on ajoute un contour noir
                texte_x = pos[0] + int(taille) + 15  # Plus loin du soleil
                texte_y = pos[1] - 10
                # Dessine le contour noir
                texte_contour = font.render(corps.nom, True, self.NOIR)
                for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                    self.ecran.blit(texte_contour, (texte_x + dx, texte_y + dy))
            else:
                # Pour les autres corps, on garde le positionnement actuel
                texte_x = pos[0] + 10
                texte_y = pos[1] - 10
            
            self.ecran.blit(texte, (texte_x, texte_y))
            
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
                elif event.key == pygame.K_SPACE:
                    self.en_pause = not self.en_pause
            elif event.type == pygame.VIDEORESIZE:
                # Mise à jour de la taille de la fenêtre
                self.ecran = pygame.display.set_mode((event.size[0], event.size[1]), pygame.RESIZABLE)
                self.largeur = event.size[0]
                self.hauteur = event.size[1]
        return True
    
    def fermer(self) -> None:
        """Ferme la fenêtre Pygame."""
        pygame.quit() 