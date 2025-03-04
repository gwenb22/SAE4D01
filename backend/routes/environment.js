const express = require('express');
const router = express.Router();
const db = require('../db');

router.get('/', (req, res) => {
    db.all('SELECT * FROM environment_impact', [], (err, rows) => {
        if (err) {
            res.status(500).json({ error: err.message });
        } else {
            res.json(rows);
        }
    });
});

// Ajouter une nouvelle entrée d'impact environnemental
router.post('/', (req, res) => {
    const { user_id, co2_saved, water_saved, biodiversity_score } = req.body;
    
    db.run('INSERT INTO environment_impact (user_id, co2_saved, water_saved, biodiversity_score) VALUES (?, ?, ?, ?)', 
        [user_id, co2_saved, water_saved, biodiversity_score], function(err) {
        if (err) {
            res.status(500).json({ error: err.message });
        } else {
            res.status(201).json({ 
                id: this.lastID, 
                user_id, 
                co2_saved, 
                water_saved, 
                biodiversity_score 
            });
        }
    });
});

module.exports = router;