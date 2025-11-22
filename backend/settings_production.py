# backend/backend/settings_production.py
import os
import dj_database_url

# Import base settings FIRST
from .settings import *

# ============================================================================
# PRODUCTION SETTINGS ONLY - DO NOT REDEFINE ALLAUTH SETTINGS
# ============================================================================
# ALLAUTH settings are already correctly defined in settings.py
# We don't override them here to avoid conflicts

# ============================================================================
# PRODUCTION SECURITY
# ============================================================================
DEBUG = False

ALLOWED_HOSTS = [
    'advision-backend.onrender.com',
    'https://advision-backend-8u95.onrender.com',
    'advision-backend-8u95.onrender.com',
    '.onrender.com',
    'localhost',
    '127.0.0.1',
]

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Proxy settings for Render
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True

# ============================================================================
# DATABASE - PostgreSQL on Render
# ============================================================================
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# ============================================================================
# STATIC FILES (WhiteNoise)
# ============================================================================
if 'whitenoise.middleware.WhiteNoiseMiddleware' not in MIDDLEWARE:
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

os.makedirs(STATIC_ROOT, exist_ok=True)

# ============================================================================
# CORS
# ============================================================================
FRONTEND_URL = os.getenv('FRONTEND_URL', 'https://ad-vision-frontend.vercel.app/')

# Remove trailing slashes and filter valid URLs
def clean_url(url):
    """Remove trailing slash and ensure valid URL"""
    if url and url.startswith('http'):
        return url.rstrip('/')
    return None

CORS_ALLOWED_ORIGINS = list(set(filter(None, [
    clean_url(FRONTEND_URL),
    clean_url("https://advision-frontend.vercel.app"),
    clean_url("https://advision.vercel.app"),
])))

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

CSRF_TRUSTED_ORIGINS = list(set(filter(None, [
    clean_url(FRONTEND_URL),
    clean_url("https://ad-vision-frontend.vercel.app/"),
    clean_url("https://ad-vision-frontend-git-main-raghavs-projects-e83ddc80.vercel.app/"),
    clean_url("https://ad-vision-frontend-mkvkyh6xx-raghavs-projects-e83ddc80.vercel.app/"),
])))

# ============================================================================
# GOOGLE OAUTH SETTINGS
# ============================================================================
GOOGLE_OAUTH_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID', '')
GOOGLE_OAUTH_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET', '')

# ============================================================================
# API ENCRYPTION KEY
# ============================================================================
API_ENCRYPTION_KEY = os.getenv('API_ENCRYPTION_KEY', SECRET_KEY)

# ============================================================================
# CLOUDINARY CONFIGURATION
# ============================================================================
import cloudinary

cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET'),
    secure=True
)

USE_CLOUDINARY = True

# ============================================================================
# AI API KEYS
# ============================================================================
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '')
STABILITY_API_KEY = os.getenv('STABILITY_API_KEY', '')

# ============================================================================
# LOGGING
# ============================================================================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'core': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# ============================================================================
# REPORT STORAGE PATH
# ============================================================================
REPORT_STORAGE_PATH = os.path.join(BASE_DIR, 'reports')
os.makedirs(REPORT_STORAGE_PATH, exist_ok=True)