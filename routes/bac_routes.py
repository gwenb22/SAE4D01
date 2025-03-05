from flask import Blueprint, render_template, jsonify
from utils.database import get_db

# Création d'un blueprint pour les routes des bacs
bac_bp = Blueprint('bac', __name__)

@bac_bp.route('/bacs')
def bacs():
    """
    Affiche la page des bacs.
    
    Returns:
        Rendu du template bacs.html
    """
    return render_template("bacs.html")