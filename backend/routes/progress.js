const express = require('express');
const router = express.Router();
const db = require('../db');

router.post('/', (req, res) => {
    const { user_id, progress_level } = req.body;
    db.run('INSERT INTO progress (user_id, progress_level) VALUES (?, ?)', [user_id, progress_level], function (err) {
        if (err) {
            res.status(500).json({ error: err.message });
        } else {
            res.status(201).json({ id: this.lastID });
        }
    });
});

router.get('/:user_id', (req, res) => {
    db.get('SELECT * FROM progress WHERE user_id = ?', [req.params.user_id], (err, row) => {
        if (err) {
            res.status(500).json({ error: err.message });
        } else {
            res.json(row);
        }
    });
});

module.exports = router;
