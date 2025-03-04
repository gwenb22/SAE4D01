const express = require('express');
const router = express.Router();
const db = require('../db');

// 🟢 Inscription utilisateur
router.post('/register', (req, res) => {
    const { username, email, password } = req.body;
    if (!username || !email || !password) {
        return res.status(400).json({ error: "Tous les champs sont requis" });
    }
    
    db.run('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', 
        [username, email, password], function (err) {
        if (err) {
            // Gestion des erreurs spécifiques (email unique)
            if (err.message.includes('UNIQUE constraint failed')) {
                return res.status(409).json({ error: "Cet email est déjà utilisé" });
            }
            res.status(500).json({ error: err.message });
        } else {
            res.status(201).json({ id: this.lastID, username, email });
        }
    });
});

// 🔵 Connexion utilisateur (à améliorer avec un hashage de mot de passe)
router.post('/login', (req, res) => {
    const { email, password } = req.body;
    db.get('SELECT * FROM users WHERE email = ? AND password = ?', 
        [email, password], (err, row) => {
        if (err) {
            res.status(500).json({ error: err.message });
        } else if (!row) {
            res.status(401).json({ error: "Identifiants incorrects" });
        } else {
            res.json({ message: "Connexion réussie", user: { id: row.id, username: row.username } });
        }
    });
});

module.exports = router;