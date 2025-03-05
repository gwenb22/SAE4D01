from flask import Blueprint, render_template, jsonify
from utils.database import get_db

# Création d'un blueprint pour les routes des bacs
parametre_bp = Blueprint('parametre', __name__)

@parametre_bp.route('/parametre')
def parametre():
    """
    Affiche la page des bacs.
    
    Returns:
        Rendu du template bacs.html
    """
    return render_template("parametre.html")