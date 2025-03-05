"""
Package utils contenant des utilitaires et des fonctions réutilisables.

Ce module centralise les outils partagés par différentes parties de l'application.
"""

# Imports optionnels des modules principaux du package
from .database import DatabaseManager, get_db, init_db
from .plant_identifier import identify_plant

# Configuration optionnelle
__all__ = [
    'DatabaseManager',
    'get_db',
    'identify_plant'
]
