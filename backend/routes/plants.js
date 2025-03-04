const express = require('express');
const router = express.Router();
const db = require('../db');

// 🟢 Créer une plante
router.post('/', (req, res) => {
    const { name, humidity, temperature } = req.body;
    db.run('INSERT INTO plants (name, humidity, temperature) VALUES (?, ?, ?)', 
        [name, humidity, temperature], function (err) {
        if (err) {
            res.status(500).json({ error: err.message });
        } else {
            res.status(201).json({ id: this.lastID, name, humidity, temperature });
        }
    });
});

// 🔵 Récupérer toutes les plantes
router.get('/', (req, res) => {
    db.all('SELECT * FROM plants', [], (err, rows) => {
        if (err) {
            res.status(500).json({ error: err.message });
        } else {
            res.json(rows);
        }
    });
});

// 🟡 Modifier une plante
router.put('/:id', (req, res) => {
    const { humidity, temperature } = req.body;
    db.run('UPDATE plants SET humidity = ?, temperature = ? WHERE id = ?', 
        [humidity, temperature, req.params.id], function (err) {
        if (err) {
            res.status(500).json({ error: err.message });
        } else {
            res.json({ updated: this.changes });
        }
    });
});

// 🔴 Supprimer une plante
router.delete('/:id', (req, res) => {
    db.run('DELETE FROM plants WHERE id = ?', req.params.id, function (err) {
        if (err) {
            res.status(500).json({ error: err.message });
        } else {
            res.json({ deleted: this.changes });
        }
    });
});

module.exports = router;
