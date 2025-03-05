import os
import logging
from flask import Flask, session, redirect, url_for, render_template
from flask_cors import CORS
from flask_login import LoginManager, current_user, logout_user
from utils import init_db, DatabaseManager

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Initialisation du LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"  # Assurez-vous que cette route existe

    # Configuration de la clé secrète
    app.secret_key = os.urandom(24)

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

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(bacs_bp)
    app.register_blueprint(defis_bp)
    app.register_blueprint(scan_bp)

    # Définition de la route index
    @app.route('/')
    def index():
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        return render_template('index.html')

    # Fonction pour charger un utilisateur
    @login_manager.user_loader
    def load_user(user_id):
        return DatabaseManager.get_user_by_id(user_id)  # Récupère l'utilisateur par ID
    
    @app.route('/scan')
    def scan():
        return render_template('scan.html')

    # Route de déconnexion
    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('auth.login'))

    return app



# Configuration du logger
logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
