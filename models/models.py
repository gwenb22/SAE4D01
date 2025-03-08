from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

# Exemple de base de données simulée
users = {"testuser": User(1, "testuser")}
