import sqlite3
import re

def insert_plantes():
    # Connexion à la base de données
    conn = sqlite3.connect("./backend/plantes.db")
    cursor = conn.cursor()

    # Données des plantes extraites du document JavaScript
    plantes = [
        # Bac 1
        {"nom": "Tomate", "humidite": 55, "temperature": 21, "info": "La tomate est une plante facile à cultiver dans un potager, appréciant les sols riches et bien ensoleillés.", "arrosage": "Modéré"},
        {"nom": "Aubergine", "humidite": 62, "temperature": 21, "info": "L'aubergine préfère un sol riche et bien drainé, avec un bon ensoleillement et un arrosage modéré.", "arrosage": "Modéré"},
        {"nom": "Basilic", "humidite": 50, "temperature": 21, "info": "Le basilic aime un sol léger et bien drainé, un ensoleillement direct et un arrosage modéré.", "arrosage": "Modéré"},
        
        # Bac 2
        {"nom": "Concombre", "humidite": 65, "temperature": 25, "info": "Le concombre nécessite un sol riche, beaucoup de soleil et un arrosage constant.", "arrosage": "Constant"},
        {"nom": "Poivron", "humidite": 55, "temperature": 23, "info": "Le poivron aime les sols riches, bien drainés, avec un bon ensoleillement.", "arrosage": "Modéré"},
        {"nom": "Persil", "humidite": 50, "temperature": 20, "info": "Le persil apprécie un sol humide, un mi-ombre et un arrosage régulier.", "arrosage": "Régulier"},
        
        # Bac 3
        {"nom": "Betterave", "humidite": 55, "temperature": 21, "info": "La betterave préfère un sol léger et bien drainé, un bon ensoleillement et un arrosage modéré.", "arrosage": "Modéré"},
        {"nom": "Carotte", "humidite": 62, "temperature": 21, "info": "La carotte se développe dans un sol meuble et bien drainé, avec un ensoleillement direct et un arrosage modéré.", "arrosage": "Modéré"},
        {"nom": "Laitue", "humidite": 50, "temperature": 21, "info": "La laitue préfère un sol frais et humide, avec un ensoleillement modéré et un arrosage fréquent.", "arrosage": "Fréquent"}
    ]

    # Insertion des plantes
    for plante in plantes:
        try:
            cursor.execute('''
                INSERT INTO plante (nom, humidite, temperature, info, arrosage) 
                VALUES (?, ?, ?, ?, ?)
            ''', (
                plante['nom'], 
                plante['humidite'], 
                plante['temperature'], 
                plante['info'], 
                plante['arrosage']
            ))
        except sqlite3.IntegrityError:
            print(f"La plante {plante['nom']} existe déjà.")
        except Exception as e:
            print(f"Erreur lors de l'insertion de {plante['nom']}: {e}")

    # Commit et fermeture
    conn.commit()
    conn.close()

    print("Insertion des plantes terminée.")

def verify_plantes():
    # Vérification des données insérées
    conn = sqlite3.connect("./backend/plantes.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM plante")
    plantes = cursor.fetchall()

    print("\nPlantes dans la base de données:")
    for plante in plantes:
        print(f"ID: {plante[0]}, Nom: {plante[1]}, Humidité: {plante[2]}, Température: {plante[4]}")

    conn.close()

if __name__ == "__main__":
    insert_plantes()
    verify_plantes()