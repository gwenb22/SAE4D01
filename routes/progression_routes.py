from flask import Blueprint, render_template, jsonify
from utils.database import get_db

# Création d'un blueprint pour les routes des bacs
progression_bp = Blueprint('progression', __name__)

@progression_bp.route('/progression')
def progression():
    """
    Affiche la page des bacs.
    
    Returns:
        Rendu du template bacs.html
    """
    return render_template("progression.html")