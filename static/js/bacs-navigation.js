document.addEventListener('DOMContentLoaded', () => {
    // Tableau des bacs avec leurs détails
    const bacs = [
        {
            id: 1,
            title: 'Bac 1',
            plantes: [
                {
                    nom: 'Tomate',
                    humidite: '55%',
                    temperature: '18 - 24 C',
                    description: 'La tomate est une plante facile à cultiver dans un potager, appréciant les sols riches et bien ensoleillés.'
                },
                {
                    nom: 'Aubergine',
                    humidite: '62%',
                    temperature: '18 - 24 C',
                    description: 'L\'aubergine préfère un sol riche et bien drainé, avec un bon ensoleillement et un arrosage modéré.'
                },
                {
                    nom: 'Basilic',
                    humidite: '50%',
                    temperature: '18 - 24 C',
                    description: 'Le basilic aime un sol léger et bien drainé, un ensoleillement direct et un arrosage modéré.'
                }
            ]
        },
        {
            id: 2,
            title: 'Bac 2',
            plantes: [
                {
                    nom: 'Concombre',
                    humidite: '65%',
                    temperature: '20 - 30 C',
                    description: 'Le concombre nécessite un sol riche, beaucoup de soleil et un arrosage constant.'
                },
                {
                    nom: 'Poivron',
                    humidite: '55%',
                    temperature: '18 - 28 C',
                    description: 'Le poivron aime les sols riches, bien drainés, avec un bon ensoleillement.'
                },
                {
                    nom: 'Persil',
                    humidite: '50%',
                    temperature: '15 - 25 C',
                    description: 'Le persil apprécie un sol humide, un mi-ombre et un arrosage régulier.'
                }
            ]
        },
        {
            id: 3,
            title: 'Bac 3',
            plantes: [
                {
                    nom: 'Betterave',
                    humidite: '55%',
                    temperature: '18 - 24 C',
                    description: 'La betterave préfère un sol léger et bien drainé, un bon ensoleillement et un arrosage modéré.'
                },
                {
                    nom: 'Carotte',
                    humidite: '62%',
                    temperature: '18 - 24 C',
                    description: 'La carotte se développe dans un sol meuble et bien drainé, avec un ensoleillement direct et un arrosage modéré.'
                },
                {
                    nom: 'Laitue',
                    humidite: '50%',
                    temperature: '18 - 24 C',
                    description: 'La laitue préfère un sol frais et humide, avec un ensoleillement modéré et un arrosage fréquent.'
                }
            ]
        }
    ];

    const prevBac = document.getElementById('prev-bac');
    const nextBac = document.getElementById('next-bac');
    const bacTitle = document.querySelector('h1');
    const mainPlante = document.querySelector('.plante');
    const autresPlantesContainer = document.querySelector('.autres-plantes');

    let currentBacIndex = 0; // Commence avec Bac 1

    function updateBacContent(bac) {
        // Mettre à jour le titre du bac
        bacTitle.textContent = bac.title;

        // Mettre à jour la plante principale
        const premierePlante = bac.plantes[0];
        mainPlante.querySelector('h2').textContent = premierePlante.nom;
        const mesuresPrincipales = mainPlante.querySelector('.mesures');
        mesuresPrincipales.querySelector('.humidite strong').textContent = premierePlante.humidite;
        mesuresPrincipales.querySelector('.temperature strong').textContent = premierePlante.temperature;
        mainPlante.querySelector('p').textContent = premierePlante.description;

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
                            <strong>${plante.humidite}</strong>
                        </div>
                        <div class="temperature">
                            <span>Température</span>
                            <strong>${plante.temperature}</strong>
                        </div>
                    </div>
                    <p>${plante.description}</p>
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
});