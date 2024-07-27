window.addEventListener('load', function() {
    window.cookieconsent.initialise({
      palette: {
        popup: { background: '#333', text: '#fff' },
        button: { background: '#009900', text: '#fff' }
      },
      theme: 'classic',
      position: 'bottom-right',
      content: {
        message: 'We use cookies to improve your experience on our site. By continuing to browse, you agree to our use of cookies.',
        dismiss: 'I accept',
        link: 'Learn more',
        href: '#'
      },
      onInitialise: function() {
        const container = document.querySelector('.cc-window');
        if (container) {
          container.classList.add('custom-cookie-consent-container');
        }
      }
    });
  });