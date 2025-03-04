import sqlite3

def create_database():
    conn = sqlite3.connect("plants_management.db")
    cursor = conn.cursor()

    cursor.executescript('''
    PRAGMA foreign_keys = ON;
    
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    );
    
    CREATE TABLE IF NOT EXISTS plants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        humidity REAL,
        temperature REAL
    );
    
    CREATE TABLE IF NOT EXISTS bacs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        location TEXT,
        humidity REAL,
        temperature REAL
    );
    
    CREATE TABLE IF NOT EXISTS plantings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        plant_id INTEGER NOT NULL,
        bac_id INTEGER NOT NULL,
        date_planted TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (plant_id) REFERENCES plants(id) ON DELETE CASCADE,
        FOREIGN KEY (bac_id) REFERENCES bacs(id) ON DELETE CASCADE
    );
    
    CREATE TABLE IF NOT EXISTS user_progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        total_plants INTEGER DEFAULT 0,
        environment_impact REAL DEFAULT 0,
        last_updated TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    
    CREATE TABLE IF NOT EXISTS environment_impact (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        co2_saved REAL DEFAULT 0,
        water_saved REAL DEFAULT 0,
        biodiversity_score REAL DEFAULT 0,
        last_updated TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    
    CREATE TABLE IF NOT EXISTS watering_schedule (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bac_id INTEGER NOT NULL,
        frequency INTEGER NOT NULL,
        last_watered TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        next_watering TEXT NOT NULL,
        FOREIGN KEY (bac_id) REFERENCES bacs(id) ON DELETE CASCADE
    );
    ''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    print("Base de données créée avec succès !")
