import unittest
from models import Database, User, Plant

class TestDatabase(unittest.TestCase):
    """Tests pour les modèles de la base de données."""

    @classmethod
    def setUpClass(cls):
        """Créer une base de test."""
        cls.db = Database()
        cls.user_model = User(cls.db)
        cls.plant_model = Plant(cls.db)

    def test_create_user(self):
        """Test de la création d'un utilisateur."""
        result = self.user_model.create_user("testuser", "test@email.com", "securepass")
        self.assertEqual(result, "Utilisateur créé avec succès")

    def test_get_user(self):
        """Test de la récupération d'un utilisateur."""
        user = self.user_model.get_user(1)
        self.assertIsNotNone(user)

    def test_add_plant(self):
        """Test d'ajout de plante."""
        self.plant_model.add_plant("Aloe Vera", 60.0, 20.0)
        plant = self.plant_model.get_plant(1)
        self.assertIsNotNone(plant)

    def test_update_plant(self):
        """Test de mise à jour d'une plante."""
        self.plant_model.update_plant(1, 65.0, 22.0)
        plant = self.plant_model.get_plant(1)
        self.assertEqual(plant[2], 65.0)  # Vérifie l'humidité mise à jour

    def test_delete_plant(self):
        """Test de suppression d'une plante."""
        self.plant_model.delete_plant(1)
        plant = self.plant_model.get_plant(1)
        self.assertIsNone(plant)

    @classmethod
    def tearDownClass(cls):
        """Nettoyage après les tests."""
        cls.db.close()

if __name__ == "__main__":
    unittest.main()
