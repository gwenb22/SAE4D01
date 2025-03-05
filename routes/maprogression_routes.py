from flask import Blueprint, render_template, jsonify
from utils.database import get_db

# Création d'un blueprint pour les routes des bacs
maprogression_bp = Blueprint('maprogression', __name__)

@maprogression_bp.route('/maprogression')
def maprogression():
    """
    Affiche la page des bacs.
    
    Returns:
        Rendu du template bacs.html
    """
    return render_template("maprogression.html")