document.addEventListener('DOMContentLoaded', function() {
    console.log("nasa.js loaded");

    const apodImage = document.getElementById('apod-image');
    const apodDescription = document.getElementById('apod-description');


    const defaultDescription = 'I have been impressed with the urgency of doing. Knowing is not enough; we must apply. Being willing is not enough; we must do — Leonardo da Vinci';

    const apiUrl = '/api/apod/?format=json&hasfast=true&authuser=0';

    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            console.log("API data processed", data);
            if (data.media_type === 'image') {
                apodImage.src = data.url;
                apodImage.alt = data.title;
                apodDescription.textContent = `${data.title}: ${data.explanation}`;
            } else {
                apodDescription.textContent = defaultDescription;
            }
        })
        .catch(error => {
            console.error('Error fetching the NASA APOD:', error);
            apodDescription.textContent = defaultDescription;
        });
});