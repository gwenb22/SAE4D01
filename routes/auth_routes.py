from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from utils.database import DatabaseManager
import logging

logger = logging.getLogger(__name__)

# Création du Blueprint pour la gestion de l'authentification
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Route pour l'inscription des utilisateurs.
    """
    if request.method == 'POST':
        try:
            # Récupération des données du formulaire
            name = request.form['name']
            phone = request.form['phone']
            email = request.form['email']
            password = request.form['password']
            
            # Création d'une instance du gestionnaire de base de données
            db_manager = DatabaseManager()
            success, message = db_manager.register_user(name, phone, email, password)
            
            if success:
                logger.info(f"Inscription réussie pour {email}")
                flash("Inscription réussie.", "success")
                return render_template('scan.html',)
            else:
                logger.warning(f"Échec de l'inscription pour {email}: {message}")
                flash(message, "danger")
                
        except Exception as e:
            logger.error(f"Erreur lors de l'inscription: {e}")
            flash(f"Erreur: {str(e)}", "danger")
    
    return render_template('inscription.html')

# Exemple de fonction de connexion (modification dans routes/auth_routes.py)
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Récupération des données utilisateur (cette partie doit retourner un dictionnaire)
        user_email = request.form['email']
        user_data = DatabaseManager.get_user_by_email(user_email)  # Assurez-vous que cette méthode renvoie un dictionnaire

        # Vérification que l'utilisateur existe
        if user_data:  # Si l'utilisateur existe
            session['user_email'] = user_data.get('email')
            session['user_name'] = user_data.get('name')  # Stocke le nom de l'utilisateur
            return redirect(url_for('index'))
        else:
            flash("Utilisateur non trouvé", "danger")
    return render_template('scan.html')

@auth_bp.route('/logout')
def logout():
    """
    Route pour la déconnexion de l'utilisateur.
    """
    session.clear()  # Supprime toutes les données de session
    flash("Déconnexion réussie.", "success")
    return redirect(url_for('auth.login'))
