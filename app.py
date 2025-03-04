import os
import json
import requests
import logging
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)

# 🔹 Configuration du logger pour le débogage
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

@app.route("/")
def scan():
    return render_template("scan.html")

@app.route("/scan_info", methods=["POST"])
def scan_info():
    if "image" not in request.files:
        flash("Aucune image n'a été envoyée.", "error")
        return redirect(url_for("scan"))

    uploaded_file = request.files["image"]
    
    if uploaded_file.filename == "":
        flash("Aucun fichier sélectionné.", "error")
        return redirect(url_for("scan"))

    try:
        # 🔹 Sauvegarde de l'image dans le dossier uploads
        image_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(image_path)
        logging.info(f"Image sauvegardée : {image_path}")

        # 🔹 Appel à l'API PlantNet pour identifier la plante
        plant_info = identify_plant(image_path)

        if plant_info.get("error"):
            flash(plant_info["error"], "error")
            return redirect(url_for("scan"))  # Si erreur, revenir à scan.html
        else:
            # 🔹 Rediriger vers scan_info.html avec les infos de la plante
            return render_template("scan_info.html", plant_info=plant_info, image_path=image_path)

    except Exception as e:
        logging.error(f"Erreur lors du traitement de l'image : {e}")
        flash(f"Erreur : {e}", "error")
        return redirect(url_for("scan"))


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

if __name__ == "__main__":
    app.run(debug=True)



def validate_plant_data(name, humidity, temperature, watering_frequency):
    errors = []

    if not name or not isinstance(name, str):
        errors.append("Le nom de la plante est invalide.")

    if not isinstance(humidity, (int, float)) or not (0 <= humidity <= 100):
        errors.append("L'humidité doit être un nombre entre 0 et 100.")

    if not isinstance(temperature, (int, float)) or not (-50 <= temperature <= 50):
        errors.append("La température doit être un nombre entre -50 et 50.")

    if not isinstance(watering_frequency, int) or watering_frequency < 0:
        errors.append("La fréquence d'arrosage doit être un entier positif.")

    return errors  # Renvoie une liste d'erreurs (vide si tout est bon)
