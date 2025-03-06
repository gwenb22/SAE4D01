from utils.database import get_db

class User:
    """
    Classe User pour Flask-Login
    Doit implémenter les propriétés et méthodes requises par Flask-Login
    """
    
    def __init__(self, user_id, email=None, prenom=None, nom=None):
        self.id = user_id
        self.email = email
        self.prenom = prenom
        self.nom = nom
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False
    
    def get_id(self):
        """
        Méthode requise par Flask-Login pour obtenir l'ID de l'utilisateur
        """
        return str(self.id)

    @classmethod
    def get(cls, user_id):
        """
        Méthode pour récupérer un utilisateur par son ID
        """
        db = get_db()
        result = db.execute('SELECT * FROM utilisateur WHERE id_utilisateur = ?', (user_id,)).fetchone()
        if result:
            return cls(result['id_utilisateur'], result['email'], result['prenom'], result['nom'])
        return None
