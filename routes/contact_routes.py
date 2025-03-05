from flask import Blueprint, render_template, jsonify
from utils.database import get_db

# Création d'un blueprint pour les routes des bacs
contact_bp = Blueprint('contact', __name__)

@contact_bp.route('/contact')
def contact():
    """
    Affiche la page des bacs.
    
    Returns:
        Rendu du template bacs.html
    """
    return render_template("contact.html")