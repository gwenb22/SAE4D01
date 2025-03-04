from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Ajoute la gestion des requêtes CORS

# Connexion à SQLite
def get_db():
    conn = sqlite3.connect('./backend/plants_management.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route de test
@app.route("/")
def index():
    return "🚀 API de gestion des plantes opérationnelle 🌱"

# Exemples de routes pour les plantes
@app.route("/plants", methods=["GET"])
def get_plants():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM plants")
    plants = cursor.fetchall()
    return jsonify([dict(plant) for plant in plants])

# Exemple pour les utilisateurs
@app.route("/users", methods=["GET"])
def get_users():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return jsonify([dict(user) for user in users])

# Exemple pour l'environnement
@app.route("/environment", methods=["GET"])
def get_environment():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM environment")
    environment_data = cursor.fetchall()
    return jsonify([dict(record) for record in environment_data])

# Ajouter d'autres routes similaires pour les autres entités

if __name__ == "__main__":
    app.run(debug=True)
