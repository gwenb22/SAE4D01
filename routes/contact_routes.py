from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from utils.database import get_db

contact_bp = Blueprint('contact', __name__)

@contact_bp.route('/contact')
def contact():
    """
    Affiche la page de contact.
    
    Returns:
        Rendu du template contact.html
    """
    # Vérification de l'authentification basée sur la session
    if not session.get('user_id'):
        flash("Veuillez vous connecter pour accéder à la page de contact.", "warning")
        return redirect(url_for('auth.login'))
        
    return render_template("contact.html")

@contact_bp.route('/envoyer-message', methods=['POST'])
def envoyer_message():
    """
    Traite l'envoi d'un message de contact.
    
    Returns:
        Redirection vers la page de contact avec un message de confirmation
    """
    # Vérification de l'authentification
    if not session.get('user_id'):
        flash("Veuillez vous connecter pour envoyer un message.", "warning")
        return redirect(url_for('auth.login'))
        
    sujet = request.form.get('sujet')
    message = request.form.get('message')
    
    # Récupérer les informations de l'utilisateur
    user_id = session.get('user_id')
    db = get_db()
    user = db.execute('SELECT email FROM utilisateur WHERE id_utilisateur = ?', (user_id,)).fetchone()
    user_email = user['email'] if user else "Utilisateur inconnu"
    
    # Vous pourriez stocker les messages dans une nouvelle table dans votre base de données
    try:
        db.execute('''
            INSERT INTO messages (id_utilisateur, sujet, contenu, date_envoi)
            VALUES (?, ?, ?, datetime('now'))
        ''', (user_id, sujet, message))
        db.commit()
        flash("Votre message a été envoyé avec succès!", "success")
    except Exception as e:
        # Si la table n'existe pas encore, on enregistre dans un fichier
        with open('messages.log', 'a') as f:
            f.write(f"Message de {user_email} (ID: {user_id}) - Sujet: {sujet}\n")
            f.write(f"Contenu: {message}\n")
            f.write("-" * 50 + "\n")
        flash("Votre message a été enregistré!", "success")
    
    return redirect(url_for('contact.contact'))