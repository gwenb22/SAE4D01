from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def scan():
    return render_template("scan.html")

if __name__ == "__main__":
    app.run(debug=True)

def validate_plant_data(name, humidity, temperature, watering_frequency):
    errors = []

    if not name or not isinstance(name, str):
        errors.append("Le nom de la plante est invalide.")

    if not isinstance(humidity, (int, float)) or not (0 <= humidity <= 100):
        errors.append("L'humidité doit être un nombre entre 0 et 100.")

    if not isinstance(temperature, (int, float)) or not (-50 <= temperature <= 50):
        errors.append("La température doit être un nombre entre -50 et 50.")

    if not isinstance(watering_frequency, int) or watering_frequency < 0:
        errors.append("La fréquence d'arrosage doit être un entier positif.")

    return errors  # Renvoie une liste d'erreurs (vide si tout est bon)

