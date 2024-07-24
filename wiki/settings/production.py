from .base import *

DEBUG = False
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['https://sciencewiki-dba83ffdf24f.herokuapp.com/'])

# Security settings
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
