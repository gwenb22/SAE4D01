import os
import json
import logging
import requests

# Configuration du logger
logging.basicConfig(level=logging.DEBUG)

# Clé API et configuration PlantNet
PLANTNET_API_KEY = "2b10YUu9ziZH7Ay8lM8YyPQc"
PROJECT = "all"
PLANTNET_API_URL = f"https://my-api.plantnet.org/v2/identify/{PROJECT}?api-key={PLANTNET_API_KEY}&lang=fr"


def validate_plant_image(image_path):
    """
    Valide les caractéristiques de base d'une image de plante.
    
    Args:
        image_path (str): Chemin vers le fichier image
    
    Returns:
        dict: Résultat de la validation
    """
    try:
        # Vérification de l'existence du fichier
        if not os.path.exists(image_path):
            return {"valid": False, "error": "Fichier inexistant"}
        
        # Vérification de la taille du fichier
        file_size = os.path.getsize(image_path)
        if file_size > 10 * 1024 * 1024:  # Limite à 10 Mo
            return {"valid": False, "error": "Fichier trop volumineux"}
        
        # Vérification du type de fichier (simple vérification)
        valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
        file_ext = os.path.splitext(image_path)[1].lower()
        if file_ext not in valid_extensions:
            return {"valid": False, "error": "Format de fichier non supporté"}
        
        return {"valid": True}
    
    except Exception as e:
        logging.error(f"Erreur lors de la validation de l'image : {e}")
        return {"valid": False, "error": str(e)}

def identify_plant(image_path, organs=None):
    """
    Identifie une plante à partir d'une image en utilisant l'API PlantNet.
    
    Args:
        image_path (str): Chemin complet vers le fichier image
        organs (list, optional): Liste des organes à analyser. 
                                 Défaut: ['flower', 'leaf']
    
    Returns:
        dict: Informations sur la plante identifiée
    """
    # Configuration par défaut des organes si non spécifié
    if organs is None:
        organs = ['flower', 'leaf']  # Ajout de leaf par défaut
    
    try:
        # Vérification de l'existence du fichier
        if not os.path.exists(image_path):
            return {"error": "Le fichier image n'existe pas."}
        
        # Ouverture et préparation de l'image
        with open(image_path, "rb") as image_data:
            files = [("images", (os.path.basename(image_path), image_data))]
            data = {"organs": organs}

            # Création et envoi de la requête
            req = requests.Request("POST", url=PLANTNET_API_URL, files=files, data=data)
            prepared = req.prepare()

            session = requests.Session()
            response = session.send(prepared)

            logging.debug(f"Réponse API PlantNet : {response.status_code}")
            logging.debug(f"Contenu de la réponse : {response.text}")

            # Traitement de la réponse
            if response.status_code == 200:
                json_result = json.loads(response.text)
                
                # Vérification des résultats
                if json_result.get("results"):
                    # Récupération des informations principales
                    plant_data = json_result["results"][0]["species"]
                    
                    # Extraction des informations
                    return {
                        "common_name": plant_data.get("commonNames", ["Inconnu"])[0],
                        "scientific_name": plant_data.get("scientificName", "Inconnu"),
                        "score": json_result["results"][0].get("score", 0),
                        "organs_analyzed": organs,  # Ajout des organes analysés
                        "details": {
                            "genus": plant_data.get("genus", {}).get("scientificName", "Inconnu"),
                            "family": plant_data.get("family", {}).get("scientificName", "Inconnu")
                        }
                    }
                else:
                    return {"error": "Aucune plante identifiée."}
            else:
                return {
                    "error": f"Erreur API PlantNet (Code {response.status_code})",
                    "message": response.text
                }

    except requests.RequestException as req_error:
        logging.error(f"Erreur de requête réseau : {req_error}")
        return {"error": f"Erreur de connexion : {str(req_error)}"}
    
    except json.JSONDecodeError as json_error:
        logging.error(f"Erreur de décodage JSON : {json_error}")
        return {"error": "Impossible de traiter la réponse de l'API"}
    
    except Exception as e:
        logging.error(f"Erreur inattendue lors de l'identification : {e}")
        return {"error": f"Erreur inattendue : {str(e)}"}

def get_plant_care_recommendations(plant_info):
    """
    Génère des recommandations de base pour la culture d'une plante.
    
    Args:
        plant_info (dict): Informations sur la plante identifiée
    
    Returns:
        dict: Recommandations de culture
    """
    # Dictionnaire de recommandations (à enrichir)
    care_recommendations = {
        "default": {
            "light": "Lumière indirecte modérée",
            "water": "Arrosage modéré, laisser sécher entre les arrosages",
            "soil": "Terreau bien drainé",
            "temperature": "Entre 18-24°C"
        }
    }
    
    # Ajout de recommandations spécifiques basées sur le genre ou la famille
    genus = plant_info.get("details", {}).get("genus", "").lower()
    
    # Exemples de recommandations spécifiques
    specific_recommendations = {
        "ficus": {
            "light": "Lumière brillante mais sans soleil direct",
            "water": "Garder le sol légèrement humide",
            "soil": "Mélange de terreau et de perlite"
        }
    }
    
    # Sélection des recommandations
    recommendations = specific_recommendations.get(genus, care_recommendations["default"])
    
    return {
        "scientific_name": plant_info.get("scientific_name", "Inconnu"),
        "care_recommendations": recommendations
    }