const API_URL = "http://localhost:5000/plants";

// Fonction pour récupérer et afficher les plantes
async function fetchPlants() {
    const response = await fetch(API_URL);
    const plants = await response.json();

    const plantList = document.getElementById("plantList");
    plantList.innerHTML = ""; // Réinitialise la liste

    plants.forEach(plant => {
        const li = document.createElement("li");
        li.innerHTML = `
            <strong>${plant.name}</strong> - 
            Humidité: ${plant.humidity}% - 
            Température: ${plant.temperature}°C 
            <button onclick="deletePlant(${plant.id})">🗑 Supprimer</button>
        `;
        plantList.appendChild(li);
    });
}

// Fonction pour ajouter une plante
document.getElementById("plantForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const name = document.getElementById("plantName").value;
    const humidity = document.getElementById("plantHumidity").value;
    const temperature = document.getElementById("plantTemperature").value;

    const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, humidity, temperature })
    });

    if (response.ok) {
        fetchPlants(); // Met à jour la liste
    }
});

// Fonction pour supprimer une plante
async function deletePlant(id) {
    await fetch(`${API_URL}/${id}`, { method: "DELETE" });
    fetchPlants(); // Rafraîchit la liste après suppression
}

// Charger les plantes au démarrage
fetchPlants();
