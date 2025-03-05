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
    from routes.bac_routes import bac_bp
    from routes.defis_routes import defis_bp
    from routes.scan_routes import scan_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(bac_bp)
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

    # Route de déconnexion
    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('auth.login'))

    return app

# Configuration du logger
logging.basicConfig(level=logging.DEBUG)

# 🔹 Clé API PlantNet (Remplacez par votre clé API)
PLANTNET_API_KEY = "2b10YUu9ziZH7Ay8lM8YyPQc"  # Insérez votre clé API ici
PROJECT = "all"  # Vous pouvez changer en "weurope", "canada", etc.
PLANTNET_API_URL = f"https://my-api.plantnet.org/v2/identify/{PROJECT}?api-key={PLANTNET_API_KEY}"

# 🔹 Secret key pour les flash messages Flask
app.secret_key = "secret_key" 

# 🔹 Dossier d'uploads des images
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Connexion à SQLite
def get_db():
    conn = sqlite3.connect('./backend/plantes.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/defis")
def defis():
    return render_template("defis.html")

@app.route("/information")
def information():
    return render_template("information.html")

@app.route("/bac1")
def bac1():
    return render_template("bac1.html")

@app.route("/progression")
def progression():
    return render_template("progression.html")

# Route de test
@app.route("/")
def scan():
    return render_template("scan.html")

@app.route("/scan_info", methods=["POST"])
def scan_info():
    if "image" not in request.files:
        flash("Aucune image n'a été envoyée.", "error")
        return render_template("scan_pas_info.html")
    
    uploaded_file = request.files["image"]
    
    if uploaded_file.filename == "":
        flash("Aucun fichier sélectionné.", "error")
        return render_template("scan_pas_info.html")

    try:
        # 🔹 Sauvegarde de l'image dans le dossier uploads
        image_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(image_path)
        logging.info(f"Image sauvegardée : {image_path}")

        # 🔹 Appel à l'API PlantNet pour identifier la plante
        plant_info = identify_plant(image_path)

        if plant_info.get("error"):
            flash(plant_info["error"], "error")
            return render_template("scan_pas_info.html")  # Si erreur, revenir à scan.html
        else:
            # 🔹 Rediriger vers scan_info.html avec les infos de la plante
            return render_template("scan_info.html", plant_info=plant_info, image_path=image_path)

    except Exception as e:
        logging.error(f"Erreur lors du traitement de l'image : {e}")
        flash(f"Erreur : {e}", "error")
        return render_template("scan_pas_info.html")


def identify_plant(image_path):
    """Envoie une image à l'API PlantNet et récupère les informations sur la plante."""
    try:
        with open(image_path, "rb") as image_data:
            files = [("images", (image_path, image_data))]
            data = {"organs": ["flower"]}  # Vous pouvez changer les organes

            # 🔹 Création et envoi de la requête avec requests.Request()
            req = requests.Request("POST", url=PLANTNET_API_URL, files=files, data=data)
            prepared = req.prepare()

            s = requests.Session()
            response = s.send(prepared)

            logging.debug(f"Réponse API : {response.status_code}, {response.text}")

            if response.status_code == 200:
                json_result = json.loads(response.text)
                if json_result.get("results"):
                    plant_data = json_result["results"][0]["species"]
                    common_name = plant_data.get("commonNames", ["Inconnu"])[0]
                    scientific_name = plant_data.get("scientificName", "Inconnu")
                    return {"common_name": common_name, "scientific_name": scientific_name}
                else:
                    return {"error": "Aucune plante identifiée."}
            else:
                return {"error": f"Erreur API PlantNet (Code {response.status_code})"}

    except Exception as e:
        logging.error(f"Erreur API PlantNet : {e}")
        return {"error": f"Erreur API : {str(e)}"}

# 🔹 Routes supplémentaires pour les données de la base

@app.route("/plants", methods=["GET"])
def get_plants():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM plants")
    plants = cursor.fetchall()
    return jsonify([dict(plant) for plant in plants])

@app.route("/users", methods=["GET"])
def get_users():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return jsonify([dict(user) for user in users])

@app.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    if user:
        return jsonify(dict(user))
    else:
        return jsonify({"error": "Utilisateur non trouvé"}), 404

@app.route("/user/<int:user_id>/progression", methods=["GET"])
def get_user_progression(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM progression WHERE id_utilisateur = ?", (user_id,))
    progression = cursor.fetchone()
    if progression:
        return jsonify(dict(progression))
    else:
        return jsonify({"error": "Progression non trouvée pour cet utilisateur"}), 404

@app.route("/plantations", methods=["GET"])
def get_plantations():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM plantation")
    plantations = cursor.fetchall()
    return jsonify([dict(plantation) for plantation in plantations])

@app.route("/infos", methods=["GET"])
def get_infos():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM info")
    infos = cursor.fetchall()
    return jsonify([dict(info) for info in infos])

@app.route("/bac", methods=["GET"])
def get_bacs():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bac")
    bacs = cursor.fetchall()
    return jsonify([dict(bac) for bac in bacs])

# 🔹 Routes pour les pages de connexion et d'inscription

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Logique d'inscription (validation, création de l'utilisateur)
        pass
    return render_template("inscription.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Logique de connexion (vérification des identifiants)
        pass
    return render_template("connexion.html")

@app.route('/bacs')
def bacs():
    return render_template("bacs.html")

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
