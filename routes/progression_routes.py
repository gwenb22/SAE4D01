from flask import Blueprint, render_template, session, redirect, request
from functools import wraps
from backend.database_functions import get_top_users, get_top_three_users, get_user_progression

# Mise à jour du blueprint
progression_bp = Blueprint('progression', __name__)

# Nouvelle route pour la page de progression d'un utilisateur spécifique
@progression_bp.route('/progression/<int:user_id>')
# @login_required
def user_progression(user_id):
    """
    Affiche la page de progression pour un utilisateur spécifique.
    
    Args:
        user_id (int): ID de l'utilisateur
        
    Returns:
        Rendu du template progression.html avec les données de progression de l'utilisateur
    """
    # Récupérer les informations de progression de l'utilisateur
    user_info, progression_data = get_user_progression(user_id)
    
    # Si l'utilisateur n'existe pas, rediriger vers la page des défis
    if not user_info:
        return redirect('/defis')
    
    return render_template('progression.html', user=user_info, progression=progression_data)