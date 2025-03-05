import os
from flask import Blueprint, render_template, request, flash, session, redirect
from utils.plant_identifier import identify_plant, validate_plant_image, get_plant_care_recommendations
from functools import wraps

# Création du blueprint pour les routes de scan
scan_bp = Blueprint('scan', __name__)

@scan_bp.route('/scan')
def scan():
    """
    Affiche la page de scan de plantes.
    
    Returns:
        Rendu du template scan.html
    """
    return render_template('scan.html')

@scan_bp.route('/scan_info', methods=['GET', 'POST'])
def scan_info():
    if 'image' not in request.files:
        flash("Aucune image n'a été envoyée.", "error")
        print("DEBUG: Aucune image dans request.files")
        return render_template("scan_pas_info.html")

    uploaded_file = request.files["image"]

    # Récupérer l'organe sélectionné du formulaire
    selected_organ = request.form.get('organe', 'flower')  # Default to 'flower' if not specified
    print(f"DEBUG: Organe sélectionné : {selected_organ}")

    if uploaded_file.filename == "":
        flash("Aucun fichier sélectionné.", "error")
        print("DEBUG: Fichier vide")
        return render_template("scan_pas_info.html")

    try:
        # Sauvegarde de l'image
        upload_folder = os.path.join('static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        image_path = os.path.join(upload_folder, uploaded_file.filename)
        uploaded_file.save(image_path)
        print(f"DEBUG: Image sauvegardée à {image_path}")

        # Validation de l'image
        validation = validate_plant_image(image_path)
        print(f"DEBUG: Résultat validation: {validation}")
        if not validation['valid']:
            flash(validation['error'], "error")
            return render_template("scan_pas_info.html")

        # Identification de la plante avec l'organe sélectionné
        plant_info = identify_plant(image_path, organs=[selected_organ])
        print(f"DEBUG: Infos plante: {plant_info}")
        if plant_info.get("error"):
            flash(plant_info["error"], "error")
            return render_template("scan_pas_info.html")

        # Obtenir des recommandations
        care_recommendations = get_plant_care_recommendations(plant_info)
        print(f"DEBUG: Recommandations: {care_recommendations}")

        return render_template(
            "scan_info.html",
            plant_info=plant_info,
            care_recommendations=care_recommendations,
            image_path=image_path
        )

    except Exception as e:
        flash(f"Erreur : {str(e)}", "error")
        print(f"DEBUG: Exception levée: {e}")
        return render_template("scan_pas_info.html")