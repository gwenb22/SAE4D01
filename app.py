import os
import logging
from flask import Flask, session, redirect, url_for, render_template, request, jsonify
from flask_cors import CORS
from flask_login import LoginManager, current_user, UserMixin
from utils import init_db, DatabaseManager
from datetime import timedelta

# Définition de la classe User directement dans app.py
class User(UserMixin):
    def __init__(self, id_utilisateur, nom, prenom, tel, email, mdp, classe=None):
        self.id = id_utilisateur  # Flask-Login utilise .id
        self.id_utilisateur = id_utilisateur
        self.nom = nom
        self.prenom = prenom
        self.tel = tel
        self.email = email
        self.mdp = mdp
        self.classe = classe

    @classmethod
    def from_dict(cls, user_dict):
        """Crée un objet User à partir d'un dictionnaire"""
        if not user_dict:
            return None
        return cls(
            id_utilisateur=user_dict['id_utilisateur'],
            nom=user_dict['nom'],
            prenom=user_dict['prenom'],
            tel=user_dict.get('tel'),
            email=user_dict['email'],
            mdp=user_dict['mdp'],
            classe=user_dict.get('classe')
        )
        
    @classmethod
    def get(cls, user_id):
        """Récupère un utilisateur par son ID depuis la base de données"""
        user_dict = DatabaseManager.get_user_by_id(user_id)
        return cls.from_dict(user_dict) if user_dict else None

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Configuration de l'application
    app.secret_key = 'votre_clé_secrète_statique'  # Utilisez une clé statique pour maintenir les sessions
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # Session dure 7 jours

    # Middleware exécuté avant chaque requête pour vérifier l'état de la session
    @app.before_request
    def before_request():
        """
        Middleware exécuté avant chaque requête pour vérifier l'état de la session
        """
        if 'user_id' in session:
            logging.debug(f"[DEBUG] Requête reçue: {request.path}, utilisateur en session: {session['user_id']}")
        else:
            logging.debug(f"[DEBUG] Requête reçue: {request.path}, pas d'utilisateur en session")

    # Route de débogage pour vérifier l'état de la session
    @app.route('/debug/session')
    def debug_session():
        """
        Route de débogage pour afficher l'état de la session
        """
        session_info = {
            'session_active': 'user_id' in session,
            'user_id': session.get('user_id', 'Non défini'),
            'session_details': dict(session),
            'flask_login_authenticated': current_user.is_authenticated if hasattr(current_user, 'is_authenticated') else False
        }
        return jsonify(session_info)

    # Initialisation du LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"  # Redirige vers cette route si @login_required échoue
    login_manager.login_message = "Veuillez vous connecter pour accéder à cette page."
    login_manager.login_message_category = "warning"

    # Configuration du dossier d'uploads
    UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # Création du dossier backend s'il n'existe pas
    backend_folder = os.path.join(app.root_path, 'backend')
    if not os.path.exists(backend_folder):
        os.makedirs(backend_folder)

    # Initialisation de la base de données
    init_db()

    # Importation et enregistrement des blueprints
    from routes.auth_routes import auth_bp
    from routes.user_routes import user_bp
    from routes.bac_routes import bacs_bp
    from routes.defis_routes import defis_bp
    from routes.scan_routes import scan_bp
    from routes.maprogression_routes import maprogression_bp
    from routes.param_routes import parametre_bp
    from routes.contact_routes import contact_bp
    from routes.progression_routes import progression_bp
    from routes.info_routes import information_bp
    from routes.accueil_routes import accueil_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(bacs_bp)
    app.register_blueprint(defis_bp)
    app.register_blueprint(scan_bp)
    app.register_blueprint(maprogression_bp)
    app.register_blueprint(parametre_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(progression_bp)
    app.register_blueprint(information_bp)
    app.register_blueprint(accueil_bp)

    # Définition de la route index
    @app.route('/')
    def index():
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        return redirect(url_for('accueil.accueil'))

    # Fonction pour charger un utilisateur
    @login_manager.user_loader
    def load_user(user_id):
        user_dict = DatabaseManager.get_user_by_id(user_id)
        if user_dict:
            user = User.from_dict(user_dict)
            logging.debug(f"load_user appelé avec user_id={user_id}, retourne: {user}")
            return user
        return None

    return app

# Configuration du logger
logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)