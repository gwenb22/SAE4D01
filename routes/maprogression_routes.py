from flask import Blueprint, render_template, session, redirect, url_for
from utils.database import get_db

# Création d'un blueprint pour la progression de l'utilisateur
maprogression_bp = Blueprint('maprogression', __name__)

@maprogression_bp.route('/maprogression')
def maprogression():
    """
    Affiche la page de progression de l'utilisateur.
    
    Returns:
        Rendu du template maprogression.html avec les données de progression
    """
    print("Session avant accès à maprogression :", session)  # Vérifier si user_id est bien en session

    # Vérifier si l'utilisateur est connecté
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))  # Redirection si non connecté

    user_id = session['user_id']
    
    # Connexion à la base de données
    db = get_db()
    
    # Récupérer les données de progression de l'utilisateur
    progression = db.execute('''
        SELECT general, arrosage, desherbage, heures_passees 
        FROM progression 
        WHERE id_utilisateur = ?
    ''', (user_id,)).fetchone()

    # Préparer les données à passer au template
    progression_data = {
        'general': progression[0] if progression else 0,
        'arrosage': progression[1] if progression else 0,
        'desherbage': progression[2] if progression else 0,
        'heures_passees': progression[3] if progression else 0
    }
    
    return render_template("maprogression.html", progression=progression_data)
