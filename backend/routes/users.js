const express = require('express');
const router = express.Router();
const db = require('../db');

// 🟢 Inscription utilisateur
router.post('/register', (req, res) => {
    const { username, password } = req.body;
    db.run('INSERT INTO users (username, password) VALUES (?, ?)', [username, password], function (err) {
        if (err) {
            res.status(500).json({ error: err.message });
        } else {
            res.status(201).json({ id: this.lastID, username });
        }
    });
});

// 🔵 Connexion utilisateur (simplifiée, sans hash de mot de passe)
router.post('/login', (req, res) => {
    const { username, password } = req.body;
    db.get('SELECT * FROM users WHERE username = ? AND password = ?', [username, password], (err, row) => {
        if (err) {
            res.status(500).json({ error: err.message });
        } else if (!row) {
            res.status(401).json({ error: "Identifiants incorrects" });
        } else {
            res.json({ message: "Connexion réussie", user: row });
        }
    });
});

module.exports = router;
