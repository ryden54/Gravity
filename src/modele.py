import json
import numpy as np
import uuid
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Any, Optional


@dataclass
class CorpsCeleste:
    """Classe représentant un corps céleste (étoile ou planète)."""
    
    nom: str
    masse: float
    rayon: float
    position: np.ndarray
    vitesse: np.ndarray
    couleur: Tuple[int, int, int]
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    def __post_init__(self):
        """Convertit les listes en tableaux numpy si nécessaire."""
        if isinstance(self.position, list):
            self.position = np.array(self.position, dtype=float)
        if isinstance(self.vitesse, list):
            self.vitesse = np.array(self.vitesse, dtype=float)

    def __eq__(self, autre: object) -> bool:
        """Vérifie si deux corps célestes sont égaux.
        
        Args:
            autre (object): Autre objet à comparer
            
        Returns:
            bool: True si les corps sont égaux, False sinon
        """
        if not isinstance(autre, CorpsCeleste):
            return False
        return self.id == autre.id
    
    def __hash__(self) -> int:
        """Calcule le hash du corps céleste.
        
        Returns:
            int: Hash basé sur l'ID unique du corps
        """
        return hash(self.id)

    def mettre_a_jour_position(self, dt: float) -> None:
        """Met à jour la position d'un corps en fonction de sa vitesse.
        
        Cette méthode met à jour la position d'un corps en utilisant sa vitesse
        actuelle pendant un intervalle de temps dt.
        
        Args:
            dt (float): Pas de temps en secondes
        """
        # Mise à jour de la position (r(t+dt) = r(t) + v(t) * dt)
        self.position += self.vitesse * dt


class SystemeSolaire:
    """Classe représentant le système solaire avec ses étoiles et planètes."""
    
    # Constante gravitationnelle en N⋅m²/kg²
    G = 6.67430e-11
    
    def __init__(self, fichier_json: str):
        """Initialise le système solaire à partir d'un fichier JSON.
        
        Args:
            fichier_json (str): Chemin vers le fichier JSON contenant les données.
        """
        self.etoiles: List[CorpsCeleste] = []
        self.planetes: List[CorpsCeleste] = []
        self.charger_donnees(fichier_json)
    
    def charger_donnees(self, fichier_json: str) -> None:
        """Charge les données des corps célestes depuis un fichier JSON.
        
        Args:
            fichier_json (str): Chemin vers le fichier JSON contenant les données.
        """
        try:
            with open(fichier_json, 'r', encoding='utf-8') as f:
                donnees = json.load(f)
            
            # Charger les étoiles
            for etoile_data in donnees.get('etoiles', []):
                etoile = CorpsCeleste(
                    nom=etoile_data['nom'],
                    masse=etoile_data['masse'],
                    rayon=etoile_data['rayon'],
                    position=etoile_data['position'],
                    vitesse=etoile_data['vitesse'],
                    couleur=tuple(etoile_data['couleur'])
                )
                self.etoiles.append(etoile)
            
            # Charger les planètes avec positions aléatoires
            for planete_data in donnees.get('planetes', []):
                # Calcul de la distance au soleil à partir de la position initiale
                position_initiale = np.array(planete_data['position'], dtype=float)
                vitesse_initiale = np.array(planete_data['vitesse'], dtype=float)
                distance_soleil = np.linalg.norm(position_initiale)
                vitesse_orbitale = np.linalg.norm(vitesse_initiale)
                
                # Génération d'un angle aléatoire entre 0 et 2π
                angle = np.random.uniform(0, 2 * np.pi)
                
                # Calcul de la nouvelle position
                nouvelle_position = np.array([
                    distance_soleil * np.cos(angle),  # x = r * cos(θ)
                    distance_soleil * np.sin(angle),  # y = r * sin(θ)
                    0.0  # z = 0 (plan de l'écliptique)
                ])
                
                # Calcul de la nouvelle vitesse (perpendiculaire à la position)
                nouvelle_vitesse = np.array([
                    -vitesse_orbitale * np.sin(angle),  # vx = -v * sin(θ)
                    vitesse_orbitale * np.cos(angle),   # vy = v * cos(θ)
                    0.0  # vz = 0
                ])
                
                planete = CorpsCeleste(
                    nom=planete_data['nom'],
                    masse=planete_data['masse'],
                    rayon=planete_data['rayon'],
                    position=nouvelle_position,
                    vitesse=nouvelle_vitesse,
                    couleur=tuple(planete_data['couleur'])
                )
                self.planetes.append(planete)
                
            print(f"Chargé {len(self.etoiles)} étoiles et {len(self.planetes)} planètes avec succès.")
            
        except FileNotFoundError:
            print(f"Erreur: Le fichier {fichier_json} n'a pas été trouvé.")
        except json.JSONDecodeError:
            print(f"Erreur: Le fichier {fichier_json} n'est pas un JSON valide.")
        except Exception as e:
            print(f"Erreur lors du chargement des données: {str(e)}")
    
    def obtenir_tous_corps(self) -> List[CorpsCeleste]:
        """Retourne tous les corps célestes (étoiles et planètes).
        
        Returns:
            List[CorpsCeleste]: Liste de tous les corps célestes.
        """
        return self.etoiles + self.planetes
    
    def calculer_gravite(self, corps1: CorpsCeleste, corps2: CorpsCeleste) -> np.ndarray:
        """Calcule la force de gravité exercée par corps2 sur corps1.
        
        Args:
            corps1 (CorpsCeleste): Corps sur lequel la force est calculée
            corps2 (CorpsCeleste): Corps qui exerce la force
            
        Returns:
            np.ndarray: Vecteur force de gravité en N
        """
        # Calcul du vecteur de position relative
        r = corps2.position - corps1.position
        
        # Distance entre les centres des corps
        distance = np.linalg.norm(r)
        
        # Vérification pour éviter la division par zéro
        if distance < 1e-10:
            return np.zeros(3)
        
        # Calcul de la force selon la loi de gravitation universelle
        # F = G * (m1 * m2) / r² * (r/|r|)
        force = self.G * corps1.masse * corps2.masse / (distance ** 2) * (r / distance)
        
        return force
    
    def calculer_acceleration(self, corps: CorpsCeleste, force: np.ndarray, dt: float) -> np.ndarray:
        """Calcule l'accélération d'un corps sous l'effet d'une force.
        
        Cette méthode calcule la variation de vitesse (accélération) d'un corps
        sous l'effet d'une force pendant un intervalle de temps dt.
        
        Args:
            corps (CorpsCeleste): Corps dont on calcule l'accélération
            force (np.ndarray): Force totale exercée sur le corps en N
            dt (float): Pas de temps en secondes
            
        Returns:
            np.ndarray: Variation de vitesse en m/s
        """
        # Calcul de l'accélération (F = ma)
        acceleration = force / corps.masse
        
        # Calcul de la variation de vitesse (Δv = a * dt)
        delta_vitesse = acceleration * dt
        
        return delta_vitesse
    
    def mettre_a_jour_position(self, corps: CorpsCeleste, dt: float) -> None:
        """Met à jour la position d'un corps en fonction de sa vitesse.
        
        Cette méthode met à jour la position d'un corps en utilisant sa vitesse
        actuelle pendant un intervalle de temps dt.
        
        Args:
            corps (CorpsCeleste): Corps dont on met à jour la position
            dt (float): Pas de temps en secondes
        """
        corps.mettre_a_jour_position(dt) 