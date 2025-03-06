from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from utils.database import get_db
from flask_login import login_user, logout_user, login_required, current_user
from datetime import timedelta
from app import User

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
            prenom = request.form['prenom']  # Champ prénom
            nom = request.form['nom']  # Champ nom
            tel = request.form['tel']
            email = request.form['email']
            mdp = request.form['mdp']
            
            # Connexion à la base de données
            db = get_db()
            
            # Vérifier si l'email existe déjà
            existing_user = db.execute('SELECT id_utilisateur FROM utilisateur WHERE email = ?', (email,)).fetchone()
            if existing_user:
                flash("Un compte avec cet email existe déjà.", "danger")
                return render_template('connexion.html')

            # Hasher le mot de passe
            hashed_password = generate_password_hash(mdp)

            # Insérer l'utilisateur en base de données
            db.execute('''
                INSERT INTO utilisateur (prenom, nom, tel, email, mdp) 
                VALUES (?, ?, ?, ?, ?)
            ''', (prenom, nom, tel, email, hashed_password))
            db.commit()

            flash("Inscription réussie. Connectez-vous maintenant.", "success")
            return redirect(url_for('auth.login'))

        except Exception as e:
            logger.error(f"Erreur lors de l'inscription: {e}")
            flash(f"Erreur: {str(e)}", "danger")
    
    return render_template('inscription.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # Si l'utilisateur est déjà connecté, rediriger vers la page principale
        return redirect(url_for('accueil.accueil'))

    if request.method == 'POST':  # Vérifier que la méthode est bien POST
        email = request.form.get('email')
        mdp = request.form.get('mdp')

        logger.debug(f"Tentative de connexion : email={email}")

        if not email or not mdp:  # Vérifier si les champs sont vides
            flash("Veuillez entrer un email et un mot de passe.", "warning")
            return redirect(url_for('auth.login'))  # Retourner sur la page de login
 
        db = get_db()
        user = db.execute('SELECT id_utilisateur, mdp FROM utilisateur WHERE email = ?', (email,)).fetchone()

        if not user:
            logger.debug("Utilisateur non trouvé")
            flash("Email ou mot de passe incorrect.", "error")
            return redirect(url_for('auth.login'))

        logger.debug(f"Utilisateur trouvé : ID={user['id_utilisateur']}")

        if check_password_hash(user['mdp'], mdp): 
            # Configurer la session
            session.clear()  
            session['user_id'] = user['id_utilisateur']  

            # Configurer Flask-Login
            user_obj = User.get(user['id_utilisateur'])  # Utilisation de la méthode get()
            login_user(user_obj, remember=True)

            logger.debug(f"Connexion réussie, session enregistrée : user_id={session.get('user_id')}")

            flash("Connexion réussie.", "success")
            # Rediriger vers la page demandée ou par défaut vers l'accueil
            next_page = request.args.get('next')
            return redirect(next_page or url_for('accueil.accueil'))
        else:
            logger.debug("Mot de passe incorrect")
            flash("Email ou mot de passe incorrect.", "error")
            return redirect(url_for('auth.login'))
    return render_template('connexion.html')

@auth_bp.route('/logout')
def logout():
    """
    Route pour la déconnexion de l'utilisateur.
    """
    logout_user()  # Déconnexion de Flask-Login
    session.clear()  # Supprime toutes les données de session
    flash("Déconnexion réussie.", "success")
    return redirect(url_for('auth.login'))