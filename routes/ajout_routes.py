from flask import Blueprint, request, redirect, url_for, render_template
import sqlite3
from datetime import datetime

ajout_bp = Blueprint('ajout', __name__)

@ajout_bp.route('/ajout_plante', methods=['GET'])
def formulaire_ajout_plante():
    # Récupérer la liste des plantes disponibles
    conn = sqlite3.connect("./backend/plantes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id_plante, nom FROM plante")
    plantes = cursor.fetchall()
    
    # Récupérer la liste des bacs disponibles
    cursor.execute("SELECT id_bac FROM bac")
    bacs = cursor.fetchall()
    
    conn.close()
    
    return render_template('ajout_bac.html', plantes=plantes, bacs=bacs)

@ajout_bp.route('/ajouter_plante', methods=['POST'])
def ajouter_plante():
    id_plante = request.form.get('plante')
    id_bac = request.form.get('bac_id')
    # Supposons que l'utilisateur est authentifié et que son ID est stocké en session
    # Si vous n'avez pas encore de système d'authentification, vous pouvez utiliser un ID par défaut
    id_utilisateur = 1  # À remplacer par l'ID réel de l'utilisateur connecté
    
    date_plantation = datetime.now().strftime('%Y-%m-%d')

    if id_plante and id_bac:
        conn = sqlite3.connect("./backend/plantes.db")
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO plantation (id_plante, id_utilisateur, id_bac, date_plantation) VALUES (?, ?, ?, ?)", 
                (id_plante, id_utilisateur, id_bac, date_plantation)
            )
            conn.commit()
            conn.close()
            return redirect(url_for('bacs.bacs_page'))
        except sqlite3.IntegrityError:
            conn.close()
            # Gérer l'erreur si la plante est déjà dans ce bac
            return "Cette plante est déjà dans ce bac ou une contrainte de clé étrangère n'est pas respectée."
    
    return redirect(url_for('bacs.bacs_page'))  # Redirige vers la page des bacs après l'ajout