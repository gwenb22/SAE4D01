import sqlite3
import datetime
import random
from datetime import timedelta

def populate_database():
    conn = sqlite3.connect("./backend/plantes.db")
    cursor = conn.cursor()

    # 1. Ajout des utilisateurs fictifs
    utilisateurs = [
        ("Dupont", "Jean", "0612345678", "jean.dupont@email.com", "motdepasse1", "Terminale"),
        ("Martin", "Sophie", "0623456789", "sophie.martin@email.com", "motdepasse2", "1ère"),
        ("Leroy", "Lucas", "0634567890", "lucas.leroy@email.com", "motdepasse3", "2nde"),
        ("Dubois", "Emma", "0645678901", "emma.dubois@email.com", "motdepasse4", "Terminale"),
        ("Petit", "Thomas", "0656789012", "thomas.petit@email.com", "motdepasse5", "1ère"),
        ("Roux", "Camille", "0667890123", "camille.roux@email.com", "motdepasse6", "2nde"),
        ("Moreau", "Léa", "0678901234", "lea.moreau@email.com", "motdepasse7", "Terminale"),
        ("Simon", "Hugo", "0689012345", "hugo.simon@email.com", "motdepasse8", "1ère"),
        ("Laurent", "Chloé", "0690123456", "chloe.laurent@email.com", "motdepasse9", "2nde"),
        ("Michel", "Antoine", "0601234567", "antoine.michel@email.com", "motdepasse10", "Terminale")
    ]

    for utilisateur in utilisateurs:
        try:
            cursor.execute('''
            INSERT INTO utilisateur (nom, prenom, tel, email, mdp, classe)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', utilisateur)
            print(f"Utilisateur ajouté: {utilisateur[1]} {utilisateur[0]}")
        except sqlite3.IntegrityError:
            print(f"L'utilisateur avec l'email {utilisateur[3]} existe déjà")

    # Récupérer les IDs des utilisateurs insérés pour ensuite ajouter leurs progressions
    cursor.execute("SELECT id_utilisateur FROM utilisateur WHERE email IN ({})".format(
        ','.join(['?'] * len(utilisateurs))
    ), [u[3] for u in utilisateurs])
    
    user_ids = [row[0] for row in cursor.fetchall()]

    # 2. Ajout des progressions pour les nouveaux utilisateurs
    for user_id in user_ids:
        general = random.randint(0, 100)
        arrosage = random.randint(0, 100)
        desherbage = random.randint(0, 100)
        heures_passees = round(random.uniform(0, 30), 1)
        
        cursor.execute('''
        INSERT OR REPLACE INTO progression 
        (id_utilisateur, general, arrosage, desherbage, heures_passees) 
        VALUES (?, ?, ?, ?, ?)
        ''', (user_id, general, arrosage, desherbage, heures_passees))
        print(f"Progression ajoutée pour l'utilisateur ID: {user_id}")

    # 3. Ajout de 10 plantes
    plantes = [
        ("Tomate", 70.5, "Modéré", 22.5, "La tomate est un fruit consommé comme légume. Elle est riche en lycopène.", 1.5),
        ("Basilic", 65.0, "Régulier", 20.0, "Herbe aromatique méditerranéenne, utilisée en cuisine pour son parfum.", 0.8),
        ("Thym", 30.0, "Faible", 18.0, "Plante aromatique résistante à la sécheresse.", 0.5),
        ("Fraisier", 60.0, "Modéré", 21.0, "Plante produisant des fruits rouges sucrés au printemps et en été.", 1.2),
        ("Salade", 75.0, "Régulier", 18.5, "Légume-feuille à croissance rapide, idéal pour les débutants.", 0.7),
        ("Courgette", 65.0, "Modéré", 22.0, "Légume de la famille des cucurbitacées, production abondante en été.", 1.4),
        ("Menthe", 70.0, "Régulier", 19.0, "Plante aromatique envahissante à cultiver en pot.", 0.6),
        ("Radis", 60.0, "Modéré", 17.0, "Légume-racine à croissance très rapide, idéal pour les enfants.", 0.5),
        ("Persil", 65.0, "Modéré", 18.5, "Herbe aromatique riche en vitamines, utilisée comme condiment.", 0.7),
        ("Carotte", 55.0, "Modéré", 16.0, "Légume-racine riche en bêta-carotène, facile à cultiver.", 0.9)
    ]

    for plante in plantes:
        cursor.execute('''
        INSERT INTO plante (nom, humidite, arrosage, temperature, info, impact_environnemental)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', plante)
        print(f"Plante ajoutée: {plante[0]}")

    # 4. Ajout de 10 bacs si nécessaire
    cursor.execute("SELECT COUNT(*) FROM bac")
    bac_count = cursor.fetchone()[0]
    bacs_to_add = max(0, 10 - bac_count + 3)  # +3 car on en supprimera 3 plus tard
    
    for _ in range(bacs_to_add):
        cursor.execute("INSERT INTO bac DEFAULT VALUES")
    print(f"{bacs_to_add} bacs ajoutés")

    # 5. Ajout de 10 plantations
    # Récupérer les IDs des plantes et des bacs
    cursor.execute("SELECT id_plante FROM plante ORDER BY id_plante DESC LIMIT 10")
    plante_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT id_bac FROM bac ORDER BY id_bac ASC LIMIT 10")
    bac_ids = [row[0] for row in cursor.fetchall()]

    # Générer des dates différentes dans les 6 derniers mois
    now = datetime.datetime.now()
    
    for i in range(10):
        plante_id = random.choice(plante_ids)
        user_id = random.choice(user_ids)
        bac_id = random.choice(bac_ids)
        
        # Date aléatoire entre aujourd'hui et il y a 6 mois
        days_ago = random.randint(0, 180)
        date_plantation = (now - timedelta(days=days_ago)).strftime("%Y-%m-%d")
        
        try:
            cursor.execute('''
            INSERT INTO plantation (id_plante, id_utilisateur, id_bac, date_plantation)
            VALUES (?, ?, ?, ?)
            ''', (plante_id, user_id, bac_id, date_plantation))
            print(f"Plantation ajoutée: Plante {plante_id}, Utilisateur {user_id}, Bac {bac_id}, Date {date_plantation}")
        except sqlite3.IntegrityError:
            print(f"Cette plantation existe déjà (Plante {plante_id}, Utilisateur {user_id}, Bac {bac_id})")

    # 6. Ajout de 20 infos
    infos = [
        ("Arrosage efficace", "arrosage.jpg", "Arrosez vos plantes tôt le matin ou en soirée pour limiter l'évaporation."),
        ("Compostage", "compost.jpg", "Le compost maison enrichit le sol et recycle vos déchets organiques."),
        ("Rotation des cultures", "rotation.jpg", "Alternez les familles de plantes pour éviter l'épuisement du sol."),
        ("Économie d'eau", "eau.jpg", "Récupérez l'eau de pluie pour un jardinage plus écologique."),
        ("Protection hivernale", "hiver.jpg", "Protégez vos plantes du gel avec un paillage adapté."),
        ("Lutte biologique", "insectes.jpg", "Favorisez la présence d'insectes auxiliaires pour limiter les ravageurs."),
        ("Engrais naturels", "engrais.jpg", "Utilisez du marc de café comme engrais pour vos plantes d'intérieur."),
        ("Semis réussis", "semis.jpg", "Maintenez une température constante pour favoriser la germination."),
        ("Plantes compagnes", "compagnon.jpg", "Certaines plantes se protègent mutuellement des parasites lorsqu'elles sont plantées ensemble."),
        ("Désherbage écologique", "desherbage.jpg", "L'eau bouillante est efficace pour éliminer les mauvaises herbes sans produits chimiques."),
        ("Jardinage lunaire", "lune.jpg", "Le calendrier lunaire peut influencer la croissance des plantes."),
        ("Boutures faciles", "bouture.jpg", "Multipliez vos plantes facilement grâce à des boutures dans l'eau."),
        ("Protection contre les limaces", "limace.jpg", "La cendre ou la coquille d'œuf pilée forme une barrière naturelle contre les limaces."),
        ("Plantes mellifères", "abeille.jpg", "Plantez des fleurs mellifères pour attirer les pollinisateurs dans votre jardin."),
        ("Jardinage vertical", "vertical.jpg", "Optimisez l'espace en cultivant sur des structures verticales."),
        ("Permaculture", "permaculture.jpg", "La permaculture imite les écosystèmes naturels pour un jardinage durable."),
        ("Outils essentiels", "outils.jpg", "Investissez dans des outils de qualité pour faciliter vos travaux de jardinage."),
        ("Récolte des graines", "graines.jpg", "Récoltez et conservez vos graines pour les replanter l'année suivante."),
        ("Jardinage biologique", "bio.jpg", "Évitez les pesticides chimiques pour préserver la biodiversité."),
        ("Paillage", "paillage.jpg", "Le paillage conserve l'humidité du sol et limite la pousse des mauvaises herbes.")
    ]

    for info in infos:
        cursor.execute('''
        INSERT INTO info (titre, img, description)
        VALUES (?, ?, ?)
        ''', info)
        print(f"Info ajoutée: {info[0]}")

    # 7. Supprimer les 3 derniers bacs
    cursor.execute("SELECT id_bac FROM bac ORDER BY id_bac DESC LIMIT 3")
    last_bacs = [row[0] for row in cursor.fetchall()]
    
    for bac_id in last_bacs:
        try:
            cursor.execute("DELETE FROM bac WHERE id_bac = ?", (bac_id,))
            print(f"Bac supprimé: ID {bac_id}")
        except sqlite3.IntegrityError:
            print(f"Impossible de supprimer le bac ID {bac_id}, il est utilisé dans des plantations")

    conn.commit()
    conn.close()
    print("Base de données peuplée avec succès !")

if __name__ == "__main__":
    populate_database()