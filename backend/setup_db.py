import sqlite3

def create_database():
    conn = sqlite3.connect("/backend/plantes.db")
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
        general TEXT,
        arrosage TEXT,
        desherbage TEXT,
        heures_passees REAL,
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

if __name__ == "__main__":
    create_database()
    print("Base de données créée avec succès !")
