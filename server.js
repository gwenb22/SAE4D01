const express = require("express");
const sqlite3 = require("sqlite3").verbose();
const cors = require("cors");
require("dotenv").config();

const app = express();
const PORT = process.env.PORT || 5000;

app.use(express.json()); // Pour lire le JSON dans les requêtes
app.use(cors()); // Autorise les requêtes cross-origin

// Connexion à la base SQLite
const db = new sqlite3.Database("./plants_management.db", (err) => {
    if (err) console.error("Erreur de connexion à la base:", err);
    else console.log("Connecté à SQLite");
});

// Route de test
app.get("/", (req, res) => {
    res.send("API de gestion des plantes opérationnelle 🌱");
});

const plantRoutes = require("./routes/plants");
app.use("/plants", plantRoutes);

// Démarrer le serveur
app.listen(PORT, () => {
    console.log(`Serveur démarré sur http://localhost:${PORT}`);
});
