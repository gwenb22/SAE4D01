from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from utils.database import get_db
from flask_login import current_user

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
                return render_template('inscription.html')

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
        return redirect(url_for('maprogression.maprogression'))  

    if request.method == 'POST':  # Vérifier que la méthode est bien POST
        email = request.form.get('email')
        mdp = request.form.get('mdp')

        print(f"Tentative de connexion : email={email}, mdp={mdp}")  # Debug

        if not email or not mdp:  # Vérifier si les champs sont vides
            flash("Veuillez entrer un email et un mot de passe.", "warning")
            return redirect(url_for('auth.login'))  # Retourner sur la page de login

        db = get_db()
        user = db.execute('SELECT id_utilisateur, mdp FROM utilisateur WHERE email = ?', (email,)).fetchone()

        if not user:
            print("Utilisateur non trouvé")
            flash("Email ou mot de passe incorrect.", "error")
            return redirect(url_for('auth.login'))

        print(f"Utilisateur trouvé : {user}")  # Debug

        if check_password_hash(user['mdp'], mdp): 
            session.clear()  
            session.permanent = True  
            session['user_id'] = user['id_utilisateur']  

            print("Connexion réussie, session enregistrée :", session)  # Debug

            flash("Connexion réussie.", "success")
            return redirect(url_for('maprogression.maprogression'))  
        else:
            print("Mot de passe incorrect")
            flash("Email ou mot de passe incorrect.", "error")
            return redirect(url_for('auth.login'))  # Si mot de passe incorrect, revenir à la page de login
    return render_template('connexion.html')

@auth_bp.route('/logout')
def logout():
    """
    Route pour la déconnexion de l'utilisateur.
    """
    session.clear()  # Supprime toutes les données de session
    flash("Déconnexion réussie.", "success")
    return redirect(url_for('auth.login'))
