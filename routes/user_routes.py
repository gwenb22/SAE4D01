from flask import Blueprint, jsonify
from utils.database import get_db

# Création d'un blueprint pour les routes des utilisateurs
user_bp = Blueprint('user', __name__)

@user_bp.route("/users", methods=["GET"])
def get_users():
    """
    Récupère la liste de tous les utilisateurs.
    
    Returns:
        JSON: Liste des utilisateurs
    """
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM utilisateur")
    users = cursor.fetchall()
    return jsonify([dict(user) for user in users])

@user_bp.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    """
    Récupère les informations d'un utilisateur spécifique.
    
    Args:
        user_id (int): Identifiant de l'utilisateur
    
    Returns:
        JSON: Informations de l'utilisateur
    """
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM utilisateur WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    if user:
        return jsonify(dict(user))
    else:
        return jsonify({"error": "Utilisateur non trouvé"}), 404

@user_bp.route("/user/<int:user_id>/progression", methods=["GET"])
def get_user_progression(user_id):
    """
    Récupère la progression d'un utilisateur.
    
    Args:
        user_id (int): Identifiant de l'utilisateur
    
    Returns:
        JSON: Progression de l'utilisateur
    """
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM progression WHERE id_utilisateur = ?", (user_id,))
    progression = cursor.fetchone()
    if progression:
        return jsonify(dict(progression))
    else:
        return jsonify({"error": "Progression non trouvée"}), 404