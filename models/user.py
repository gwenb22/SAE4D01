class User:
    """
    Classe User pour Flask-Login
    Doit implémenter les propriétés et méthodes requises par Flask-Login
    """
    
    def __init__(self, user_id):
        self.id = user_id
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False
    
    def get_id(self):
        """
        Méthode requise par Flask-Login pour obtenir l'ID de l'utilisateur
        """
        return str(self.id)