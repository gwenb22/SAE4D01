from flask import Blueprint, render_template, jsonify
import sqlite3

bacs_bp = Blueprint('bacs', __name__)

@bacs_bp.route('/bacs')
def bacs_page():
    return render_template('bacs.html')

@bacs_bp.route('/api/bacs')
def get_bacs():
    try:
        # Connexion à la base de données
        conn = sqlite3.connect("./backend/plantes.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Récupérer tous les bacs
        cursor.execute("SELECT DISTINCT id_bac FROM bac")
        bacs = cursor.fetchall()

        # Préparer la liste des bacs avec leurs plantes
        bacs_data = []
        for bac in bacs:
            bac_info = {
                'id': bac['id_bac'],
                'title': f'Bac {bac["id_bac"]}',
                'plantes': []
            }

            # Récupérer les plantes de ce bac
            cursor.execute("""
                SELECT p.* 
                FROM plante p
                JOIN plantation pl ON p.id_plante = pl.id_plante
                WHERE pl.id_bac = ?
            """, (bac['id_bac'],))
            
            plantes = cursor.fetchall()
            
            for plante in plantes:
                bac_info['plantes'].append({
                    'nom': plante['nom'],
                    'humidite': round(plante['humidite']),
                    'temperature': f"{int(plante['temperature']) - 3} - {int(plante['temperature']) + 3}",
                    'info': plante['info']
                })
            
            bacs_data.append(bac_info)

        conn.close()

        return jsonify(bacs_data)

    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500