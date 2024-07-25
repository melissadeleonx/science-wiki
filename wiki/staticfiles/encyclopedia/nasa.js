// const apiKey = 'YOUR_NASA_API_KEY'; // Replace with your NASA API key
// const apiUrl = `https://api.nasa.gov/planetary/apod?api_key=${apiKey}`;

document.addEventListener('DOMContentLoaded', function() {
    const apodImage = document.getElementById('apod-image');
    const apodDescription = document.getElementById('apod-description');

const apiUrl = 'https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY';

fetch('apiUrl')
    .then(response => response.json())
    .then(data => {
      apodImage.src = data.url;
      apodImage.alt = data.title;
      apodDescription.textContent = data.explanation;
    })
    .catch(error => {
      console.error('Error fetching the NASA APOD:', error);
    });
});