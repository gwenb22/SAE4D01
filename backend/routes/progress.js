const express = require('express');
const router = express.Router();
const db = require('../db');  // Assurez-vous que db.js est correctement configuré

// Ajouter un progrès
router.post('/', (req, res) => {
    const { user_id, total_plants, environment_impact } = req.body;
    
    db.run('INSERT INTO user_progress (user_id, total_plants, environment_impact) VALUES (?, ?, ?)', 
        [user_id, total_plants, environment_impact], function (err) {
        if (err) {
            res.status(500).json({ error: err.message });
        } else {
            res.status(201).json({ 
                id: this.lastID, 
                user_id, 
                total_plants, 
                environment_impact 
            });
        }
    });
});

// Obtenir les progrès d'un utilisateur
router.get('/:user_id', (req, res) => {
    db.get('SELECT * FROM user_progress WHERE user_id = ?', 
        [req.params.user_id], (err, row) => {
        if (err) {
            res.status(500).json({ error: err.message });
        } else if (!row) {
            res.status(404).json({ message: "Aucun progrès trouvé pour cet utilisateur" });
        } else {
            res.json(row);
        }
    });
});

// Mettre à jour les progrès d'un utilisateur
router.put('/:user_id', (req, res) => {
    const { total_plants, environment_impact } = req.body;
    
    db.run('UPDATE user_progress SET total_plants = ?, environment_impact = ?, last_updated = CURRENT_TIMESTAMP WHERE user_id = ?', 
        [total_plants, environment_impact, req.params.user_id], function (err) {
        if (err) {
            res.status(500).json({ error: err.message });
        } else if (this.changes === 0) {
            res.status(404).json({ message: "Aucun progrès trouvé pour cet utilisateur" });
        } else {
            res.json({ message: "Progrès mis à jour", changes: this.changes });
        }
    });
});

module.exports = router;
