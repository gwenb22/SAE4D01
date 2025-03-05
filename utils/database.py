import os
import sqlite3
import hashlib
import re
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_db():
    """
    Établit une connexion à la base de données SQLite.
    Returns:
        sqlite3.Connection: Connexion à la base de données
    """
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backend', 'plantes.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialise la base de données avec la table utilisateur."""
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backend', 'plantes.db')
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS utilisateur (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT NOT NULL,
                    prenom TEXT NOT NULL,
                    tel TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    mdp TEXT NOT NULL
                )
            """)
            conn.commit()
            logger.info("Base de données initialisée avec succès")
    except sqlite3.Error as e:
        logger.error(f"Erreur lors de l'initialisation de la base de données: {e}")

class DatabaseManager:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backend', 'plantes.db')
        logger.debug(f"Chemin de la base de données: {self.db_path}")

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def validate_email(self, email):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email) is not None

    def register_user(self, name, phone, email, password):
        logger.debug(f"Tentative d'inscription pour: {email}")
        
        if not all([name, phone, email, password]):
            return False, "Tous les champs sont obligatoires"

        if not self.validate_email(email):
            return False, "Format d'email invalide"

        try:
            prenom, nom = name.split(' ', 1)
        except ValueError:
            prenom = name
            nom = name

        hashed_password = self._hash_password(password)

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("SELECT * FROM utilisateur WHERE email = ?", (email,))
                if cursor.fetchone():
                    return False, "Cet email est déjà utilisé"

                cursor.execute("""
                    INSERT INTO utilisateur 
                    (nom, prenom, tel, email, mdp) 
                    VALUES (?, ?, ?, ?, ?)
                """, (nom, prenom, phone, email, hashed_password))
                
                conn.commit()
                logger.info(f"Inscription réussie pour {email}")
                return True, "Inscription réussie"

        except sqlite3.Error as e:
            logger.error(f"Erreur lors de l'inscription: {e}")
            return False, f"Erreur d'inscription : {str(e)}"

    def login_user(self, email, password):
        logger.debug(f"Tentative de connexion pour: {email}")
        
        hashed_password = self._hash_password(password)

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM utilisateur 
                    WHERE email = ? AND mdp = ?
                """, (email, hashed_password))
                
                user = cursor.fetchone()
                
                if user:
                    logger.info(f"Connexion réussie pour {email}")
                    return True, "Connexion réussie"
                else:
                    return False, "Email ou mot de passe incorrect"

        except sqlite3.Error as e:
            logger.error(f"Erreur lors de la connexion: {e}")
            return False, f"Erreur de connexion : {str(e)}"
