import sqlite3

def create_database():
    conn = sqlite3.connect("./backend/plantes.db")
    cursor = conn.cursor()

    cursor.executescript('''
    PRAGMA foreign_keys = ON;

    CREATE TABLE IF NOT EXISTS utilisateur (
        id_utilisateur INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        prenom TEXT NOT NULL,
        tel TEXT,
        email TEXT UNIQUE NOT NULL,
        mdp TEXT NOT NULL,
        classe TEXT
    );

    CREATE TABLE IF NOT EXISTS plante (
        id_plante INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        humidite REAL,
        arrosage TEXT,
        temperature REAL,
        info TEXT,
        impact_environnemental REAL
    );

    CREATE TABLE IF NOT EXISTS progression (
        id_utilisateur INTEGER,
        general INTEGER DEFAULT 0,
        arrosage INTEGER DEFAULT 0,
        desherbage INTEGER DEFAULT 0,
        heures_passees REAL DEFAULT 0,
        PRIMARY KEY (id_utilisateur),
        FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(id_utilisateur) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS bac (
        id_bac INTEGER PRIMARY KEY AUTOINCREMENT
    );

    CREATE TABLE IF NOT EXISTS info (
        id_info INTEGER PRIMARY KEY AUTOINCREMENT,
        titre TEXT NOT NULL,
        img TEXT,
        description TEXT
    );

    CREATE TABLE IF NOT EXISTS plantation (
        id_plante INTEGER,
        id_utilisateur INTEGER,
        id_bac INTEGER,
        date_plantation TEXT NOT NULL,
        PRIMARY KEY (id_plante, id_utilisateur, id_bac),
        FOREIGN KEY (id_plante) REFERENCES plante(id_plante) ON DELETE CASCADE,
        FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(id_utilisateur) ON DELETE CASCADE,
        FOREIGN KEY (id_bac) REFERENCES bac(id_bac) ON DELETE CASCADE
    );
    ''')

    conn.commit()
    conn.close()

def insert_user_progression(id_utilisateur, general=0, arrosage=0, desherbage=0, heures_passees=0):
    """
    Inserts or updates user progression in the database.
    
    Args:
        user_id (int): ID of the user
        general (int, optional): Overall progression out of 100. Defaults to 0.
        arrosage (int, optional): Watering progression out of 100. Defaults to 0.
        desherbage (int, optional): Weeding progression out of 100. Defaults to 0.
        heures_passees (float, optional): Hours spent. Defaults to 0.
    """
    conn = sqlite3.connect("./backend/plantes.db")
    cursor = conn.cursor()

    cursor.execute('''
    INSERT OR REPLACE INTO progression 
    (id_utilisateur, general, arrosage, desherbage, heures_passees) 
    VALUES (?, ?, ?, ?, ?)
    ''', (id_utilisateur, general, arrosage, desherbage, heures_passees))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    # Example of inserting progression for a user
    insert_user_progression(1, 85, 45, 50, 15)
    print("Base de données créée et progression utilisateur ajoutée avec succès !")