import sqlite3

def populate_bacs_and_plantations():
    # Connexion à la base de données
    conn = sqlite3.connect("./backend/plantes.db")
    cursor = conn.cursor()

    # Insérer des bacs
    cursor.executemany("INSERT INTO bac DEFAULT VALUES", [()] * 3)
    conn.commit()

    # Récupérer les IDs des bacs et des plantes
    cursor.execute("SELECT id_bac FROM bac")
    bacs = [bac[0] for bac in cursor.fetchall()]

    cursor.execute("SELECT id_plante, nom FROM plante")
    plantes = cursor.fetchall()

    # Créer des plantations
    plantations = []
    utilisateur_id = 1  # Supposons que vous ayez un utilisateur avec id 1

    # Bac 1 : Tomate, Aubergine, Basilic
    plantations.extend([
        (plantes[0][0], utilisateur_id, bacs[0], '2024-03-05'),  # Tomate
        (plantes[1][0], utilisateur_id, bacs[0], '2024-03-05'),  # Aubergine
        (plantes[2][0], utilisateur_id, bacs[0], '2024-03-05')   # Basilic
    ])

    # Bac 2 : Concombre, Poivron, Persil
    plantations.extend([
        (plantes[3][0], utilisateur_id, bacs[1], '2024-03-05'),  # Concombre
        (plantes[4][0], utilisateur_id, bacs[1], '2024-03-05'),  # Poivron
        (plantes[5][0], utilisateur_id, bacs[1], '2024-03-05')   # Persil
    ])

    # Bac 3 : Betterave, Carotte, Laitue
    plantations.extend([
        (plantes[6][0], utilisateur_id, bacs[2], '2024-03-05'),  # Betterave
        (plantes[7][0], utilisateur_id, bacs[2], '2024-03-05'),  # Carotte
        (plantes[8][0], utilisateur_id, bacs[2], '2024-03-05')   # Laitue
    ])

    # Insérer les plantations
    cursor.executemany("""
        INSERT INTO plantation (id_plante, id_utilisateur, id_bac, date_plantation) 
        VALUES (?, ?, ?, ?)
    """, plantations)

    conn.commit()
    conn.close()

    print("Bacs et plantations peuplés avec succès !")

if __name__ == "__main__":
    populate_bacs_and_plantations()