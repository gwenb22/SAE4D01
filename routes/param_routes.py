from flask import Blueprint, render_template, jsonify, redirect, url_for, flash, session
from flask_login import login_required, current_user
from utils.database import get_db
import logging

logger = logging.getLogger(__name__)

# Création d'un blueprint pour les routes des paramètres
parametre_bp = Blueprint('parametre', __name__)

@parametre_bp.route('/parametre')
@login_required  # Utilise le décorateur Flask-Login pour la protection
def parametre():
    """
    Affiche la page des paramètres.
    
    Returns:
        Rendu du template parametre.html
    """
    logger.debug(f"Accès à /parametre - user_id in session: {session.get('user_id')}")
    logger.debug(f"current_user.is_authenticated: {current_user.is_authenticated}")
    
    return render_template("parametre.html")

@parametre_bp.route('/profil')
@login_required  # Utilise le décorateur Flask-Login pour la protection
def profil():
    """
    Affiche la page de profil de l'utilisateur.
    
    Returns:
        Rendu du template profil.html avec les informations de l'utilisateur
    """
    # Récupérer l'ID utilisateur depuis Flask-Login
    user_id = current_user.id
    
    # Récupérer les informations de l'utilisateur depuis la base de données
    db = get_db()
    
    # Utiliser une requête qui récupère les colonnes par nom
    query = """
    SELECT id_utilisateur, nom, prenom, tel, email, classe 
    FROM utilisateur 
    WHERE id_utilisateur = ?
    """
    
    cursor = db.execute(query, (user_id,))
    user_data = cursor.fetchone()
    
    if not user_data:
        flash("Erreur lors de la récupération des données utilisateur", "error")
        return redirect(url_for('parametre.parametre'))
    
    # Si vous utilisez fetchone() avec SQLite et get_db() qui permet d'accéder aux colonnes par nom
    user_info = {
        'id': user_data['id_utilisateur'],
        'nom': user_data['nom'],
        'prenom': user_data['prenom'],
        'tel': user_data['tel'],
        'email': user_data['email'],
    }
    
    return render_template("profil.html", user=user_info)