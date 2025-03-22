import json
import numpy as np
from dataclasses import dataclass
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
    trajectoire: Optional[List[np.ndarray]] = None
    
    def __post_init__(self):
        """Convertit les listes en tableaux numpy si nécessaire et initialise la trajectoire."""
        if isinstance(self.position, list):
            self.position = np.array(self.position, dtype=float)
        if isinstance(self.vitesse, list):
            self.vitesse = np.array(self.vitesse, dtype=float)
        if self.trajectoire is None:
            self.trajectoire = [self.position.copy()]


class SystemeSolaire:
    """Classe représentant le système solaire avec ses étoiles et planètes."""
    
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
            
            # Charger les planètes
            for planete_data in donnees.get('planetes', []):
                planete = CorpsCeleste(
                    nom=planete_data['nom'],
                    masse=planete_data['masse'],
                    rayon=planete_data['rayon'],
                    position=planete_data['position'],
                    vitesse=planete_data['vitesse'],
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