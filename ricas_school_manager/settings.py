
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-integration-key-replace-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',     # For sites framework
    'django.contrib.sitemaps',  # For SEO sitemap generation

    # Third-party apps
    'crispy_forms',
    'crispy_bootstrap4',
    'mathfilters',
    'widget_tweaks',
    'tinymce',
    'django_apscheduler',  # For appointment scheduling

    # Shared utilities
    'shared_utils',  # Shared template tags and utilities

    # Website (DGMS) app
    'website',

    # SMS apps
    'users',
    'courses',
    'assignments',
    'attendance',
    'communications',
    'dashboard',
    'fees',
    'payroll',
    'appointments',  # Appointment booking system
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',  # Cache middleware (first)
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',  # Cache middleware (last)
]

ROOT_URLCONF = 'ricas_school_manager.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'website.context_processors.site_settings',
                'dashboard.context_processors.sidebar_context',
                'dashboard.context_processors.user_preferences',
                'dashboard.context_processors.notifications_context',
                'appointments.context_processors.appointment_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'ricas_school_manager.wsgi.application'


# Database - Using environment variables
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.getenv('DB_NAME', 'defaultdb'),
        'USER': os.getenv('DB_USER', 'your-db-user'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'your-db-password'),
        'HOST': os.getenv('DB_HOST', 'your-db-host'),
        'PORT': os.getenv('DB_PORT', '5432'),
        'OPTIONS': {
            'sslmode': 'require',
        },
        'CONN_MAX_AGE': 600,  # Connection pooling for performance
        'CONN_HEALTH_CHECKS': True,
    }
}

# Backup SQLite database for development/testing
DATABASES_BACKUP = {
    'sqlite': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3.backup',
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# =============================================================================
# STATIC AND MEDIA FILES CONFIGURATION
# =============================================================================

# Backblaze B2 Configuration - Using environment variables
B2_APPLICATION_KEY_ID = os.getenv('B2_APPLICATION_KEY_ID', 'your-b2-key-id')
B2_APPLICATION_KEY = os.getenv('B2_APPLICATION_KEY', 'your-b2-application-key')
B2_BUCKET_NAME = os.getenv('B2_BUCKET_NAME', 'your-media-bucket')
B2_STATIC_BUCKET_NAME = os.getenv('B2_STATIC_BUCKET_NAME', 'your-static-bucket')
B2_REGION = os.getenv('B2_REGION', 'us-west-000')
B2_ENDPOINT_URL = os.getenv('B2_ENDPOINT_URL', 'https://s3.us-west-000.backblazeb2.com')

# AWS S3 Compatible settings for B2
AWS_ACCESS_KEY_ID = B2_APPLICATION_KEY_ID
AWS_SECRET_ACCESS_KEY = B2_APPLICATION_KEY
AWS_STORAGE_BUCKET_NAME = B2_BUCKET_NAME
AWS_S3_REGION_NAME = B2_REGION
AWS_S3_ENDPOINT_URL = B2_ENDPOINT_URL
AWS_S3_CUSTOM_DOMAIN = None  # Set this if you have a custom domain
AWS_DEFAULT_ACL = 'public-read'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',  # 1 day cache
}
AWS_S3_FILE_OVERWRITE = False
AWS_QUERYSTRING_AUTH = False

# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files configuration - Backblaze B2
DEFAULT_FILE_STORAGE = 'shared_utils.storage_backends.B2MediaStorage'
MEDIA_URL = f'https://f000.backblazeb2.com/file/{B2_BUCKET_NAME}/'

# Local media fallback for development
if DEBUG:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Crispy Forms settings
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Default system name
DEFAULT_SCHOOL_NAME = 'Ricas School Manager'

# Use custom user model from SMS
AUTH_USER_MODEL = 'users.CustomUser'

# Authentication settings
LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'dashboard:index'
LOGOUT_REDIRECT_URL = 'website:home'

# Authentication backends
AUTHENTICATION_BACKENDS = [
    'users.auth_backends.FlexibleStudentBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Password reset settings
PASSWORD_RESET_TIMEOUT = 3600  # 1 hour
PASSWORD_RESET_DONE_REDIRECT_URL = 'users:password_reset_done'
PASSWORD_RESET_CONFIRM_TEMPLATE_NAME = 'users/password_reset_confirm.html'

# TinyMCE Configuration
TINYMCE_DEFAULT_CONFIG = {
    'height': 360,
    'width': '100%',
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'selector': 'textarea',
    'theme': 'silver',
    'plugins': '''
        textcolor save link image media preview codesample contextmenu
        table code lists fullscreen insertdatetime nonbreaking
        contextmenu directionality searchreplace wordcount visualblocks
        visualchars code fullscreen autolink lists charmap print hr
        anchor pagebreak
        ''',
    'toolbar1': '''
        fullscreen preview bold italic underline | fontselect,
        fontsizeselect | forecolor backcolor | alignleft alignright |
        aligncenter alignjustify | indent outdent | bullist numlist table |
        | link image media | codesample |
        ''',
    'toolbar2': '''
        visualblocks visualchars |
        charmap hr pagebreak nonbreaking anchor | code |
        ''',
    'contextmenu': 'formats | link image',
    'menubar': True,
    'statusbar': True,
}

# Academic years and terms (from SMS)
from datetime import datetime
CURRENT_YEAR = datetime.now().year
ACADEMIC_YEARS = [str(year) for year in range(CURRENT_YEAR - 1, CURRENT_YEAR + 5)]
ACADEMIC_TERMS = ["First Term", "Second Term", "Third Term"]

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'skillnetservices@gmail.com'
DEFAULT_FROM_EMAIL = 'skillnetservices@gmail.com'

# For security, set this in environment variable or local_settings.py
# EMAIL_HOST_PASSWORD = 'your-app-password-here'

# Try to import local settings if they exist
try:
    from .local_settings import *
except ImportError:
    pass

# Scheduler settings
RUN_SCHEDULER_IN_DEBUG = True  # Set to False to disable scheduler in debug mode

# =============================================================================
# CACHING CONFIGURATION
# =============================================================================

# Cache configuration - Redis for production, Database for development
if DEBUG and not os.getenv('REDIS_URL'):
    # Development: Use database cache when Redis is not available
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
            'LOCATION': 'cache_table',
            'TIMEOUT': 300,
            'OPTIONS': {
                'MAX_ENTRIES': 1000,
            }
        },
        'sessions': {
            'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
            'LOCATION': 'cache_table',
            'TIMEOUT': 86400,
        },
        'templates': {
            'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
            'LOCATION': 'cache_table',
            'TIMEOUT': 3600,
        }
    }
else:
    # Production: Use Redis cache
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': os.getenv('REDIS_URL', 'redis://127.0.0.1:6379/1'),
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                'CONNECTION_POOL_KWARGS': {
                    'max_connections': 100,  # High connection pool for concurrent users
                    'retry_on_timeout': True,
                },
                'COMPRESSOR': 'django_redis.compressors.zlib.ZlibCompressor',
                'SERIALIZER': 'django_redis.serializers.json.JSONSerializer',
            },
            'TIMEOUT': 300,  # 5 minutes default
            'KEY_PREFIX': 'ricas_school',
            'VERSION': 1,
        },
        'sessions': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': os.getenv('REDIS_SESSIONS_URL', 'redis://127.0.0.1:6379/2'),
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                'CONNECTION_POOL_KWARGS': {
                    'max_connections': 50,
                    'retry_on_timeout': True,
                },
            },
            'TIMEOUT': 86400,  # 24 hours for sessions
            'KEY_PREFIX': 'ricas_sessions',
        },
        'templates': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': os.getenv('REDIS_TEMPLATES_URL', 'redis://127.0.0.1:6379/3'),
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                'CONNECTION_POOL_KWARGS': {
                    'max_connections': 30,
                    'retry_on_timeout': True,
                },
            },
            'TIMEOUT': 3600,  # 1 hour for templates
            'KEY_PREFIX': 'ricas_templates',
        }
    }

# Cache key prefix to avoid conflicts
CACHE_MIDDLEWARE_KEY_PREFIX = 'ricas_school'
CACHE_MIDDLEWARE_SECONDS = 600  # 10 minutes for page cache

# Session cache - Redis for high performance
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'sessions'
SESSION_COOKIE_AGE = 86400  # 24 hours
SESSION_SAVE_EVERY_REQUEST = False  # Only save when modified
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Template caching
TEMPLATE_CACHE_TIMEOUT = 3600  # 1 hour

# =============================================================================
# SEO CONFIGURATION
# =============================================================================

# Site information for SEO - Using environment variables
SITE_NAME = os.getenv('SITE_NAME', 'Deigratia Montessori School')
SITE_DESCRIPTION = os.getenv('SITE_DESCRIPTION', 'Comprehensive school management system for Deigratia Montessori School - managing students, teachers, courses, assignments, and more.')
SITE_KEYWORDS = os.getenv('SITE_KEYWORDS', 'school management, education, student portal, teacher portal, academic management, Ghana education, Deigratia Montessori School')
SITE_AUTHOR = 'Deigratia Montessori School'

# Social media and Open Graph settings
SOCIAL_MEDIA = {
    'facebook': os.getenv('FACEBOOK_URL', ''),
    'twitter': os.getenv('TWITTER_URL', ''),
    'linkedin': os.getenv('LINKEDIN_URL', ''),
    'instagram': os.getenv('INSTAGRAM_URL', ''),
}

# SEO Meta defaults
DEFAULT_META_DESCRIPTION = SITE_DESCRIPTION
DEFAULT_META_KEYWORDS = SITE_KEYWORDS
DEFAULT_OG_TYPE = 'website'
DEFAULT_OG_IMAGE = '/static/img/og-image.jpg'  # Add this image to your static files

# Canonical URL settings
CANONICAL_URL_BASE = os.getenv('CANONICAL_URL_BASE', 'http://localhost:8000')  # Update with your actual domain

# =============================================================================
# SECURITY AND PERFORMANCE SETTINGS
# =============================================================================

# Security headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Static files optimization
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# Compression settings (for production)
COMPRESS_ENABLED = not DEBUG
COMPRESS_OFFLINE = True

# Sites framework
SITE_ID = 1

# =============================================================================
# HIGH CONCURRENCY PERFORMANCE SETTINGS (2000 users)
# =============================================================================

# Database connection pooling
DATABASES['default']['CONN_MAX_AGE'] = 600  # 10 minutes
DATABASES['default']['CONN_HEALTH_CHECKS'] = True

# Template caching - only for production
if not DEBUG:
    TEMPLATES[0]['OPTIONS']['loaders'] = [
        ('django.template.loaders.cached.Loader', [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ]),
    ]
    # Remove APP_DIRS when using custom loaders
    TEMPLATES[0]['APP_DIRS'] = False

# Security settings for production
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

    # Session security
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    CSRF_COOKIE_HTTPONLY = True

# Logging configuration for production monitoring
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
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'maxBytes': 1024*1024*15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'ricas_school_manager': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
    },
}

# Create logs directory if it doesn't exist
import os
os.makedirs(BASE_DIR / 'logs', exist_ok=True)

