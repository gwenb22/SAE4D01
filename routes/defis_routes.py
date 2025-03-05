from flask import Blueprint, render_template, session, redirect
from functools import wraps
from backend.database_functions import get_top_users, get_top_three_users

# Création du blueprint pour les routes de défis
defis_bp = Blueprint('defis', __name__)

# Décorateur de connexion requise
""" 
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function
"""

@defis_bp.route('/defis')
# @login_required
def defis():
    """
    Affiche la page des défis.
    
    Returns:
        Rendu du template defis.html avec les données des meilleurs utilisateurs
    """
    # Récupérer les 5 meilleurs utilisateurs
    top_users = get_top_users(5)
    
    # Récupérer les 3 utilisateurs du podium
    podium_users = get_top_three_users()
    
    return render_template('defis.html', top_users=top_users, podium_users=podium_users)