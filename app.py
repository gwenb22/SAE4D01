import os
import logging
from flask import Flask, session, redirect, url_for, render_template
from flask_cors import CORS
from utils import init_db, DatabaseManager

# Configuration du logger
logging.basicConfig(level=logging.DEBUG)

def create_app():
    app = Flask(__name__)
    CORS(app)

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
    from routes.bac_routes import bac_bp
    from routes.defis_routes import defis_bp
    from routes.scan_routes import scan_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(bac_bp)
    app.register_blueprint(defis_bp)
    app.register_blueprint(scan_bp)

    # Définition de la route index à l'intérieur de create_app
    @app.route('/')
    def index():
        if 'user_email' not in session:
            return redirect(url_for('auth.login'))
        return render_template('index.html')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
