from flask import Blueprint, render_template, redirect, url_for
import sqlite3
from utils import DatabaseManager

# Définition du blueprint sans préfixe d'URL
information_bp = Blueprint('info', __name__)

@information_bp.route('/information')
def index():
    """Affiche la page d'information avec tous les articles"""
    info_data = DatabaseManager.get_all_info()
    return render_template('information.html', info_data=info_data)

@information_bp.route('/information/<int:article_id>')
def article_detail(article_id):
    """Affiche les détails d'un article spécifique"""
    article = DatabaseManager.get_info_by_id(article_id)
    if not article:
        return redirect(url_for('info.index'))
    return render_template('article_detail.html', article=article)

@information_bp.route('/add-sample-info')
def add_sample_info():
    """Route temporaire pour ajouter des données d'exemple à la base de données"""
    conn = sqlite3.connect("./backend/plantes.db")
    cursor = conn.cursor()
    
    sample_data = [
        (
            "Disparition des pollinisateurs du cassis Noir de Bourgogne",
            "static/images/abeilleinfo.jpg",
            "Le document intitulé \"Projet Cassis : Approche pluridisciplinaire pour des mesures agro-écologiques\" examine l'impact de la disparition des pollinisateurs sauvages sur la production de cassis 'Noir de Bourgogne' en Bourgogne-Franche-Comté. Cette disparition a entraîné une baisse significative des rendements agricoles, avec une diminution de 99 % des pollinisateurs en moins de 40 ans. Les auteurs suggèrent que la production pourrait potentiellement être triplée si les populations de pollinisateurs étaient restaurées. Des mesures comme la création de zones de refuge et la réduction des pesticides sont recommandées."
        ),
        (
            "Déforestation et artificialisation des sols",
            "static/images/deforestation.webp",
            "Entre 1990 et 2018, la France métropolitaine a perdu 58 691 hectares de prairies, pelouses et pâturages naturels en raison de l'artificialisation des sols. Cette transformation des espaces naturels en zones urbanisées ou industrielles entraîne une accélération de la perte de biodiversité, une augmentation des risques d'inondation et contribue au réchauffement climatique. Pour contrer ces effets, la loi Climat et Résilience vise un objectif de zéro artificialisation nette des sols d'ici 2050."
        ),
        (
            "Les zones humides",
            "static/images/france.gif",
            "Les zones humides de France métropolitaine ont perdu environ 64 % de leur surface depuis le début du XXᵉ siècle, avec une accélération notable entre 1960 et 1990. Cette régression, due principalement à l'urbanisation et au drainage des terres, menace la biodiversité et les services écosystémiques associés à ces milieux. Les zones humides sont essentielles pour la filtration de l'eau, la prévention des inondations et l'habitat de nombreuses espèces."
        ),
        (
            "Déclin des chauves-souris",
            "static/images/chauves.jpeg",
            "Entre 2006 et 2021, les populations de chauves-souris les plus communes en France métropolitaine ont diminué de 43 %. Cette tendance générale masque des disparités entre les espèces. Par exemple, la Noctule commune a subi un déclin de près de 88 % entre 2006 et 2019. Les principales causes de ce déclin incluent les collisions avec les éoliennes, qui affectent particulièrement les espèces migratrices volant à haute altitude, telles que la Noctule commune et la Pipistrelle de Nathusius."
        ),
        (
            "Flore sauvage menacée",
            "static/images/fleur.jpeg",
            "En France métropolitaine, 15 % des espèces de flore sauvage sont menacées d'extinction, soit 742 espèces sur les 4 982 recensées. Cette situation résulte principalement de l'urbanisation, de l'intensification agricole et du changement climatique, qui dégradent les habitats naturels. Parmi les espèces en danger critique figurent la Saxifrage œil-de-bouc et le Panicaut vivipare. Des actions de conservation, telles que des plans nationaux, sont mises en place pour préserver ces plantes menacées."
        )
    ]
    
    for title, img, description in sample_data:
        cursor.execute(
            'INSERT INTO info (titre, img, description) VALUES (?, ?, ?)',
            (title, img, description)
        )
    
    conn.commit()
    conn.close()
    return "Données d'exemple ajoutées avec succès!"