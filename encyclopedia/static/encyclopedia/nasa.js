document.addEventListener('DOMContentLoaded', function() {
    const apodImage = document.getElementById('apod-image');
    const apodDescription = document.getElementById('apod-description');

    const defaultDescription = 'Science is a dynamic field that delves into the fundamental mysteries of the universe, providing a compelling exploration of the natural world. It fosters a deep sense of curiosity by revealing how the cosmos functions, from the immense reaches of space to the smallest details of microscopic life. Engaging in scientific study involves more than just memorizing information; it entails actively participating in a process of continuous discovery that evolves over time and continually challenges and refines our understanding of the world around us.';


    fetch('/api/apod/')
        .then(response => response.json())
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
            apodImage.src = 'images/space.png';
        });
});