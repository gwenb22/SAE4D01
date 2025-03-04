const express = require('express');
const router = express.Router();
const db = require('../db');

router.get('/', (req, res) => {
    db.all('SELECT * FROM bac', [], (err, rows) => {
        if (err) {
            res.status(500).json({ error: err.message });
        } else {
            res.json(rows);
        }
    });
});

router.post('/', (req, res) => {
    const { name, capacity } = req.body;
    db.run('INSERT INTO bac (name, capacity) VALUES (?, ?)', [name, capacity], function (err) {
        if (err) {
            res.status(500).json({ error: err.message });
        } else {
            res.status(201).json({ id: this.lastID, name, capacity });
        }
    });
});

module.exports = router;
