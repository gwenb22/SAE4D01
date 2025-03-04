const express = require("express");
const router = express.Router();
const sqlite3 = require("sqlite3").verbose();

const db = new sqlite3.Database("./plants_management.db");

// 🔹 Récupérer toutes les plantes
router.get("/", (req, res) => {
    db.all("SELECT * FROM plants", [], (err, rows) => {
        if (err) {
            res.status(500).json({ error: err.message });
            return;
        }
        res.json(rows);
    });
});

// 🔹 Ajouter une plante
router.post("/", (req, res) => {
    const { name, humidity, temperature } = req.body;
    db.run(
        "INSERT INTO plants (name, humidity, temperature) VALUES (?, ?, ?)",
        [name, humidity, temperature],
        function (err) {
            if (err) {
                res.status(400).json({ error: err.message });
                return;
            }
            res.json({ id: this.lastID, name, humidity, temperature });
        }
    );
});

// 🔹 Mettre à jour une plante
router.put("/:id", (req, res) => {
    const { humidity, temperature } = req.body;
    db.run(
        "UPDATE plants SET humidity = ?, temperature = ? WHERE id = ?",
        [humidity, temperature, req.params.id],
        function (err) {
            if (err) {
                res.status(400).json({ error: err.message });
                return;
            }
            res.json({ message: "Mise à jour réussie" });
        }
    );
});

// 🔹 Supprimer une plante
router.delete("/:id", (req, res) => {
    db.run("DELETE FROM plants WHERE id = ?", req.params.id, function (err) {
        if (err) {
            res.status(400).json({ error: err.message });
            return;
        }
        res.json({ message: "Plante supprimée" });
    });
});

module.exports = router;
