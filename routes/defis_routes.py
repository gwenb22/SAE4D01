from flask import Blueprint, render_template, session, redirect
from functools import wraps

# Création du blueprint pour les routes de défis
defis_bp = Blueprint('defis', __name__)

# Décorateur de connexion requise
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

@defis_bp.route('/defis')
@login_required
def defis():
    """
    Affiche la page des défis.
    
    Returns:
        Rendu du template defis.html
    """
    return render_template('defis.html')