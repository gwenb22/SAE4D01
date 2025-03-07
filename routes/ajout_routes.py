from flask import Blueprint, render_template, jsonify
import sqlite3

ajout_bp = Blueprint('ajout', __name__)

@ajout_bp.route('/ajout')
def ajout_page():
    return render_template('ajout_bac.html')