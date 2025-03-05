import os
from flask import Blueprint, render_template, request, flash, session, redirect
from utils.plant_identifier import identify_plant, validate_plant_image, get_plant_care_recommendations
from functools import wraps

# Création du blueprint pour les routes de scan
scan_bp = Blueprint('scan', __name__)

# Décorateur de connexion requise
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

@scan_bp.route('/scan')
@login_required
def scan():
    """
    Affiche la page de scan de plantes.
    
    Returns:
        Rendu du template scan.html
    """
    return render_template('scan.html')

@scan_bp.route('/scan_info', methods=['GET', 'POST'])
@login_required
def scan_info():
    """
    Gère l'identification et l'affichage des informations d'une plante.
    
    Returns:
        Rendu des templates scan_info.html ou scan_pas_info.html
    """
    if 'image' not in request.files:
        flash("Aucune image n'a été envoyée.", "error")
        return render_template("scan_pas_info.html")
    
    uploaded_file = request.files["image"]
    
    if uploaded_file.filename == "":
        flash("Aucun fichier sélectionné.", "error")
        return render_template("scan_pas_info.html")

    try:
        # Sauvegarde de l'image
        upload_folder = os.path.join('static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        image_path = os.path.join(upload_folder, uploaded_file.filename)
        uploaded_file.save(image_path)

        # Validation de l'image
        validation = validate_plant_image(image_path)
        if not validation['valid']:
            flash(validation['error'], "error")
            return render_template("scan_pas_info.html")

        # Identification de la plante
        plant_info = identify_plant(image_path)

        if plant_info.get("error"):
            flash(plant_info["error"], "error")
            return render_template("scan_pas_info.html")
        
        # Obtenir des recommandations de culture
        care_recommendations = get_plant_care_recommendations(plant_info)

        return render_template(
            "scan_info.html", 
            plant_info=plant_info, 
            care_recommendations=care_recommendations,
            image_path=image_path
        )

    except Exception as e:
        flash(f"Erreur : {str(e)}", "error")
        return render_template("scan_pas_info.html")