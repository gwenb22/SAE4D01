import sqlite3

def get_top_users(limit=5):
    """
    Récupère les utilisateurs avec les meilleurs scores généraux
    
    Args:
        limit (int): Nombre d'utilisateurs à récupérer
        
    Returns:
        list: Liste de tuples contenant (id_utilisateur, nom, prenom, score_general)
    """
    conn = sqlite3.connect("./backend/plantes.db")
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT u.id_utilisateur, u.nom, u.prenom, p.general 
    FROM utilisateur u
    JOIN progression p ON u.id_utilisateur = p.id_utilisateur
    ORDER BY p.general DESC
    LIMIT ?
    ''', (limit,))
    
    results = cursor.fetchall()
    conn.close()
    
    return results

def get_top_three_users():
    """
    Récupère les 3 meilleurs utilisateurs pour le podium
    
    Returns:
        list: Liste de tuples contenant (id_utilisateur, nom, prenom, score_general)
    """
    return get_top_users(3)

def get_user_progression(user_id):
    """
    Récupère les informations et la progression d'un utilisateur spécifique
    
    Args:
        user_id (int): ID de l'utilisateur
        
    Returns:
        tuple: (informations utilisateur, données de progression)
            - informations utilisateur: (id, nom, prenom, email, classe)
            - données de progression: (general, arrosage, desherbage, heures_passees)
    """
    conn = sqlite3.connect("./backend/plantes.db")
    cursor = conn.cursor()
    
    # Récupérer les informations de l'utilisateur
    cursor.execute('''
    SELECT id_utilisateur, nom, prenom, email, classe
    FROM utilisateur
    WHERE id_utilisateur = ?
    ''', (user_id,))
    
    user_info = cursor.fetchone()
    
    # Si l'utilisateur n'existe pas, retourner None
    if not user_info:
        conn.close()
        return None, None
    
    # Récupérer les données de progression
    cursor.execute('''
    SELECT general, arrosage, desherbage, heures_passees
    FROM progression
    WHERE id_utilisateur = ?
    ''', (user_id,))
    
    progression_data = cursor.fetchone()
    
    conn.close()
    
    return user_info, progression_data

# Ajoutez ces méthodes à votre classe DatabaseManager existante

@staticmethod
def get_all_info():
    """
    Récupère toutes les informations de la table 'info'
    
    Returns:
        list: Liste de dictionnaires contenant les informations
    """
    conn = sqlite3.connect("./backend/plantes.db")
    conn.row_factory = sqlite3.Row  # Pour obtenir les résultats sous forme de dictionnaires
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM info')
    results = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    return results

@staticmethod
def get_info_by_id(info_id):
    """
    Récupère les informations d'un article spécifique
    
    Args:
        info_id (int): ID de l'information à récupérer
        
    Returns:
        dict: Dictionnaire contenant les informations de l'article
    """
    conn = sqlite3.connect("./backend/plantes.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM info WHERE id_info = ?', (info_id,))
    result = cursor.fetchone()
    
    conn.close()
    
    if result:
        return dict(result)
    return None