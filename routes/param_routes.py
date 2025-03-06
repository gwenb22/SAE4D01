from flask import Blueprint, render_template, jsonify, redirect, url_for, flash, session, request
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

@parametre_bp.route('/modifier-profil', methods=['GET', 'POST'])
@login_required
def modifier_profil():
    """
    Permet à l'utilisateur de modifier ses informations de profil.
    
    GET: Affiche le formulaire de modification
    POST: Traite les données du formulaire et met à jour le profil
    
    Returns:
        GET: Rendu du template avec les données utilisateur
        POST: Redirection vers la page de profil après mise à jour
    """
    # Récupérer l'ID utilisateur depuis Flask-Login
    user_id = current_user.id
    
    # Récupérer les informations de l'utilisateur depuis la base de données
    db = get_db()
    
    # Requête pour obtenir les données utilisateur
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
    
    # Convertir en dictionnaire
    user_info = {
        'id': user_data['id_utilisateur'],
        'nom': user_data['nom'],
        'prenom': user_data['prenom'],
        'tel': user_data['tel'],
        'email': user_data['email'],
        'classe': user_data['classe']
    }
    
    # Traitement du formulaire soumis
    if request.method == 'POST':
        # Récupérer les données du formulaire
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        email = request.form.get('email')
        tel = request.form.get('tel')
        classe = request.form.get('classe')
        
        # Données de mot de passe
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        # Vérifier si les champs obligatoires sont remplis
        if not nom or not prenom or not email:
            flash("Les champs nom, prénom et email sont obligatoires", "error")
            return render_template('modifier_profil.html', user=user_info)
        
        try:
            # Mise à jour des informations de base
            update_query = """
            UPDATE utilisateur
            SET nom = ?, prenom = ?, email = ?, tel = ?, classe = ?
            WHERE id_utilisateur = ?
            """
            db.execute(update_query, (nom, prenom, email, tel, classe, user_id))
            
            # Gestion du changement de mot de passe
            if old_password and new_password and confirm_password:
                # Vérifier si l'ancien mot de passe est correct
                password_query = "SELECT mdp FROM utilisateur WHERE id_utilisateur = ?"
                cursor = db.execute(password_query, (user_id,))
                password_data = cursor.fetchone()
                
                from werkzeug.security import check_password_hash, generate_password_hash
                
                if not check_password_hash(password_data['mdp'], old_password):
                    flash("L'ancien mot de passe est incorrect", "error")
                    return render_template('modifier_profil.html', user=user_info)
                
                # Vérifier que les nouveaux mots de passe correspondent
                if new_password != confirm_password:
                    flash("Les nouveaux mots de passe ne correspondent pas", "error")
                    return render_template('modifier_profil.html', user=user_info)
                
                # Hasher et mettre à jour le mot de passe
                hashed_password = generate_password_hash(new_password)
                db.execute("UPDATE utilisateur SET mdp = ? WHERE id_utilisateur = ?", 
                           (hashed_password, user_id))
            
            # Valider les changements
            db.commit()
            flash("Profil mis à jour avec succès", "success")
            return redirect(url_for('parametre.profil'))
            
        except Exception as e:
            db.rollback()
            logger.error(f"Erreur lors de la mise à jour du profil: {e}")
            flash("Une erreur est survenue lors de la mise à jour du profil", "error")
            return render_template('modifier_profil.html', user=user_info)
        finally:
            db.close()
    
    # Affichage du formulaire de modification
    return render_template('modifier_profil.html', user=user_info)