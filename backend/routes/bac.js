const express = require('express');
const router = express.Router();
const db = require('../db');

router.get('/', (req, res) => {
    db.all('SELECT * FROM bacs', [], (err, rows) => {
        if (err) {
            res.status(500).json({ error: err.message });
        } else {
            res.json(rows);
        }
    });
});

router.post('/', (req, res) => {
    const { name, location, humidity, temperature } = req.body;
    
    db.run('INSERT INTO bacs (name, location, humidity, temperature) VALUES (?, ?, ?, ?)', 
        [name, location, humidity, temperature], function (err) {
        if (err) {
            res.status(500).json({ error: err.message });
        } else {
            res.status(201).json({ 
                id: this.lastID, 
                name, 
                location, 
                humidity, 
                temperature 
            });
        }
    });
});

router.put('/:id', (req, res) => {
    const { humidity, temperature } = req.body;
    
    db.run('UPDATE bacs SET humidity = ?, temperature = ? WHERE id = ?', 
        [humidity, temperature, req.params.id], function (err) {
        if (err) {
            res.status(500).json({ error: err.message });
        } else if (this.changes === 0) {
            res.status(404).json({ message: "Bac non trouvé" });
        } else {
            res.json({ message: "Bac mis à jour", changes: this.changes });
        }
    });
});

module.exports = router;