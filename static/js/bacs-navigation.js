document.addEventListener('DOMContentLoaded', () => {
    // Fonction pour récupérer les bacs et leurs plantes depuis le serveur
    async function fetchBacsData() {
        try {
            const response = await fetch('/api/bacs');
            if (!response.ok) {
                throw new Error('Erreur de récupération des données');
            }
            return await response.json();
        } catch (error) {
            console.error('Erreur:', error);
            alert('Impossible de charger les données des bacs');
            return [];
        }
    }

    // Variables pour la navigation
    const prevBac = document.getElementById('prev-bac');
    const nextBac = document.getElementById('next-bac');
    const bacTitle = document.querySelector('h1');
    const mainPlante = document.querySelector('.plante');
    const autresPlantesContainer = document.querySelector('.autres-plantes');

    let bacs = []; // Tableau qui va stocker les données des bacs
    let currentBacIndex = 0; // Commence avec le premier bac

    function updateBacContent(bac) {
        // Mettre à jour le titre du bac
        bacTitle.textContent = bac.title;

        // Mettre à jour la plante principale
        const premierePlante = bac.plantes[0];
        mainPlante.querySelector('h2').textContent = premierePlante.nom;
        const mesuresPrincipales = mainPlante.querySelector('.mesures');
        mesuresPrincipales.querySelector('.humidite strong').textContent = `${premierePlante.humidite}%`;
        mesuresPrincipales.querySelector('.temperature strong').textContent = `${premierePlante.temperature} C`;
        mainPlante.querySelector('p').textContent = premierePlante.info;

        // Mettre à jour les autres plantes
        const autresPlantes = bac.plantes.slice(1);
        autresPlantesContainer.innerHTML = ''; // Vider le conteneur

        autresPlantes.forEach(plante => {
            const planteElement = document.createElement('div');
            planteElement.classList.add('plante');
            planteElement.innerHTML = `
                <h2>${plante.nom}</h2>
                <div class="plante-details">
                    <div class="mesures">
                        <div class="humidite">
                            <span>Humidité</span>
                            <strong>${plante.humidite}%</strong>
                        </div>
                        <div class="temperature">
                            <span>Température</span>
                            <strong>${plante.temperature} C</strong>
                        </div>
                    </div>
                    <p>${plante.info}</p>
                </div>
            `;
            autresPlantesContainer.appendChild(planteElement);
        });
    }

    // Fonctions de navigation
    function goToPrevBac() {
        currentBacIndex = (currentBacIndex - 1 + bacs.length) % bacs.length;
        updateBacContent(bacs[currentBacIndex]);
    }

    function goToNextBac() {
        currentBacIndex = (currentBacIndex + 1) % bacs.length;
        updateBacContent(bacs[currentBacIndex]);
    }

    // Initialisation et chargement des données
    async function initBacs() {
        bacs = await fetchBacsData();
        
        if (bacs.length > 0) {
            // Ajouter des écouteurs d'événements sur les flèches de navigation
            prevBac.addEventListener('click', (e) => {
                e.preventDefault();
                goToPrevBac();
            });

            nextBac.addEventListener('click', (e) => {
                e.preventDefault();
                goToNextBac();
            });

            // Navigation au clavier (optionnel)
            document.addEventListener('keydown', (e) => {
                if (e.key === 'ArrowLeft') {
                    goToPrevBac();
                } else if (e.key === 'ArrowRight') {
                    goToNextBac();
                }
            });

            // Afficher le premier bac
            updateBacContent(bacs[currentBacIndex]);
        }
    }

    // Lancer l'initialisation
    initBacs();
});