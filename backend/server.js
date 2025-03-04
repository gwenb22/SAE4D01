const express = require("express");
const sqlite3 = require("sqlite3").verbose();
const cors = require("cors");
require("dotenv").config();

// Initialisation de l'application
const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.json()); // Lecture des requêtes en JSON
app.use(cors()); // Gestion des requêtes cross-origin

// Connexion à SQLite
const db = new sqlite3.Database("./plants_management.db", (err) => {
    if (err) {
        console.error("❌ Erreur de connexion à SQLite :", err.message);
    } else {
        console.log("✅ Connecté à la base SQLite");
    }
});

// Route de test
app.get("/", (req, res) => {
    res.send("🚀 API de gestion des plantes opérationnelle 🌱");
});

// Importation des routes
const plantRoutes = require("./routes/plants");
const userRoutes = require("./routes/users");
const environmentRoutes = require("./routes/environment");
const progressRoutes = require("./routes/progress");
const bacRoutes = require("./routes/bac");

// Utilisation des routes
app.use("/plants", plantRoutes);
app.use("/users", userRoutes);
app.use("/environment", environmentRoutes);
app.use("/progress", progressRoutes);
app.use("/bacs", bacRoutes);

// Gestion des erreurs globales
app.use((err, req, res, next) => {
    console.error("❌ Erreur détectée :", err.message);
    res.status(500).json({ error: "Erreur interne du serveur" });
});

// Démarrer le serveur
app.listen(PORT, () => {
    console.log(`🚀 Serveur démarré sur http://localhost:${PORT}`);
});
