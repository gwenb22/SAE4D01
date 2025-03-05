from flask import Blueprint, render_template, jsonify
from utils.database import get_db

# Création d'un blueprint pour les routes des bacs
accueil_bp = Blueprint('accueil', __name__)

@accueil_bp.route('/accueil')
def accueil():
    """
    Affiche la page des bacs.
    
    Returns:
        Rendu du template bacs.html
    """
    return render_template("accueil.html")