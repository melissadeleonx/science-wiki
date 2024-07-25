document.addEventListener('DOMContentLoaded', function() {
    const apodImage = document.getElementById('apod-image');
    const apodDescription = document.getElementById('apod-description');

    const apiUrl = `https://api.nasa.gov/planetary/apod?api_key=${nasaApiKey}`;

    fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.media_type === 'image') {
                apodImage.src = data.url;
                apodImage.alt = data.title;
                apodDescription.textContent = data.explanation;
            } else {
                apodDescription.textContent = 'APOD is not an image today. Showing default image.';
            }
        })
        .catch(error => {
            console.error('Error fetching the NASA APOD:', error);
            apodDescription.textContent = 'Knowledge is power!.';
        });
});
