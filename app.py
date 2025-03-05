import os
import logging
from flask import Flask, session, redirect, url_for, render_template
from flask_cors import CORS
from flask_login import LoginManager, current_user
from utils import init_db, DatabaseManager

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Initialisation du LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"  # Assurez-vous que cette route existe

    # Configuration de la clé secrète pour maintenir la session
    app.secret_key = os.urandom(24)
    app.config['SESSION_TYPE'] = 'filesystem'

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
    
    @app.route('/information')
    def information():
        return render_template('information.html')
    
    @app.route('/accueil')
    def accueil():
        return render_template('accueil.html')
    
    @app.route('/defis')
    def defis():
        return render_template('defis.html')

    # Route de déconnexion
    @app.route('/logout')
    def logout():
        return redirect(url_for('auth.logout'))
    
    @app.route('/test_session')
    def test_session():
        session['test'] = 'Hello'
        print(session)  # 🔍 Vérifie que la session est bien stockée
        return "Session testée !"

    return app


# Configuration du logger
logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
