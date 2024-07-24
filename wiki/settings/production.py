from .base import *

# Set debug to False for production
DEBUG = False

# Configure allowed hosts
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

# Security settings
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # Apply HSTS to all subdomains
SECURE_HSTS_PRELOAD = True  # Enable HSTS preload list

SECURE_SSL_REDIRECT = True  # Redirect all HTTP requests to HTTPS
SESSION_COOKIE_SECURE = True  # Ensure cookies are sent only over HTTPS
CSRF_COOKIE_SECURE = True  # Ensure CSRF cookies are sent only over HTTPS
