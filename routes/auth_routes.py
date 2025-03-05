from flask import Blueprint, request, render_template, redirect, url_for, session
from utils.database import DatabaseManager
import logging

logger = logging.getLogger(__name__)
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            name = request.form['name']
            phone = request.form['phone']
            email = request.form['email']
            password = request.form['password']
            
            db_manager = DatabaseManager()
            success, message = db_manager.register_user(name, phone, email, password)
            
            if success:
                logger.info(f"Inscription réussie pour {email}")
                return render_template('accueil.html', error=message)
            else:
                logger.warning(f"Échec de l'inscription pour {email}: {message}")
                return render_template('inscription.html', error=message)
                
        except Exception as e:
            logger.error(f"Erreur lors de l'inscription: {e}")
            return render_template('inscription.html', error=f"Erreur: {str(e)}")
    
    return render_template('inscription.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        db_manager = DatabaseManager()
        success, message = db_manager.login_user(email, password)
        
        if success:
            session['user_email'] = email
            return render_template('accueil.html', error=message) # Redirection vers la page d'accueil
        else:
            return render_template('connexion.html', error=message)
    
    return render_template('connexion.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user_email', None)
    return redirect(url_for('auth.login'))
