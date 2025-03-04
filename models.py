import sqlite3
import re

DB_NAME = "plants_management.db"

class Database:
    """Classe pour gérer la connexion à la base de données."""
    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()

    def close(self):
        """Ferme la connexion à la base de données."""
        self.conn.close()


class Validator:
    """Classe pour valider les entrées utilisateur."""
    
    @staticmethod
    def validate_email(email):
        """Vérifie que l'email est valide."""
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, email) is not None

    @staticmethod
    def validate_password(password):
        """Vérifie que le mot de passe a au moins 6 caractères."""
        return len(password) >= 6


class User:
    """Modèle pour les utilisateurs."""
    
    def __init__(self, db):
        self.db = db

    def create_user(self, username, email, password):
        """Ajoute un utilisateur avec validation."""
        if not Validator.validate_email(email):
            return "Email invalide"
        if not Validator.validate_password(password):
            return "Mot de passe trop court"

        try:
            self.db.cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                (username, email, password)
            )
            self.db.conn.commit()
            return "Utilisateur créé avec succès"
        except sqlite3.IntegrityError:
            return "Nom d'utilisateur ou email déjà pris"

    def get_user(self, user_id):
        """Récupère un utilisateur par son ID."""
        self.db.cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return self.db.cursor.fetchone()


class Plant:
    """Modèle pour les plantes."""
    
    def __init__(self, db):
        self.db = db

    def add_plant(self, name, humidity, temperature):
        """Ajoute une nouvelle plante."""
        self.db.cursor.execute(
            "INSERT INTO plants (name, humidity, temperature) VALUES (?, ?, ?)",
            (name, humidity, temperature)
        )
        self.db.conn.commit()

    def get_plant(self, plant_id):
        """Récupère une plante par son ID."""
        self.db.cursor.execute("SELECT * FROM plants WHERE id = ?", (plant_id,))
        return self.db.cursor.fetchone()

    def update_plant(self, plant_id, humidity, temperature):
        """Met à jour les informations d'une plante."""
        self.db.cursor.execute(
            "UPDATE plants SET humidity = ?, temperature = ? WHERE id = ?",
            (humidity, temperature, plant_id)
        )
        self.db.conn.commit()

    def delete_plant(self, plant_id):
        """Supprime une plante de la base de données."""
        self.db.cursor.execute("DELETE FROM plants WHERE id = ?", (plant_id,))
        self.db.conn.commit()
