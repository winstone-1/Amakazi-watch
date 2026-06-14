from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-change-me')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost 127.0.0.1').split()

INSTALLED_APPS = [
    'drf_yasg',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # Third-party
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'drf_spectacular',
    'cloudinary',
    'cloudinary_storage',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    # Local apps
    'users',
    'reports',
    'organisations',
    'content',
    'api',
    'safety',
    'vault',
    'peer_support',
    'legal_bot',
    'org_coordination',
    'campaigns',
    'workshops',
    'tips',
    'county_scorecard',
    'subscriptions',
    'intelligence',
    'notifications',
    'rosetta',
    'django_otp',
    'django_otp.plugins.otp_totp',
    'django_otp.plugins.otp_static',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django_otp.middleware.OTPMiddleware',
]

ROOT_URLCONF = 'amakaziwatch.urls'
AUTH_USER_MODEL = 'users.User'
SITE_ID = 1

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}]

WSGI_APPLICATION = 'amakaziwatch.wsgi.application'

# ── PostgreSQL Database ──────────────────────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME':     os.getenv('DB_NAME', 'amakaziwatch'),
        'USER':     os.getenv('DB_USER', 'amakaziwatch_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST':     os.getenv('DB_HOST', 'localhost'),
        'PORT':     os.getenv('DB_PORT', '5432'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en'

from django.utils.translation import gettext_lazy as _
LANGUAGES = [
    ('en', _('English')),
    ('sw', _('Swahili')),
]

LOCALE_PATHS = [BASE_DIR / 'locale']
TIME_ZONE = 'Africa/Nairobi'
USE_I18N = True
USE_L10N = True
USE_TZ = True


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ── Cloudinary ───────────────────────────────────────────────────────────────
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY':    os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# ── DRF ──────────────────────────────────────────────────────────────────────
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '30/hour',
        'user': '100/hour',
    },
}

# ── JWT ───────────────────────────────────────────────────────────────────────
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME':  timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

# ── Swagger ───────────────────────────────────────────────────────────────────
SPECTACULAR_SETTINGS = {
    'TITLE': 'AmakaziWatch API',
    'DESCRIPTION': 'Kenya first crowdsourced GBV awareness, reporting and prevention platform. Built with Django REST Framework, Groq AI, Africa Talking SMS, Cloudinary and Paystack.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': True,
    'COMPONENT_SPLIT_REQUEST': True,
    'SECURITY': [{'BearerAuth': []}],
    'SECURITY_SCHEMES': {
        'BearerAuth': {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'JWT',
        },
    },
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
        'displayOperationId': False,
        'defaultModelsExpandDepth': -1,
        'docExpansion': 'list',
        'filter': True,
        'showExtensions': True,
        'showCommonExtensions': True,
    },
    'TAGS': [
        {'name': 'Auth', 'description': 'Registration, login, JWT tokens, password reset and 2FA'},
        {'name': 'Reports', 'description': 'Anonymous incident reporting and heatmap data'},
        {'name': 'Organisations', 'description': 'NGO and county government directory'},
        {'name': 'Content', 'description': 'Education articles, guides and quizzes'},
        {'name': 'Donations', 'description': 'Paystack donations to verified organisations'},
        {'name': 'Analytics', 'description': 'Pandas CSV reports for NGO donor reporting'},
        {'name': 'Chat', 'description': 'Anonymous AI chatbot powered by Groq LLaMA'},
        {'name': 'Search', 'description': 'Search across organisations, content and quizzes'},
        {'name': 'Profile', 'description': 'User profile and bookmarks'},
    ],
}

# ── CORS ──────────────────────────────────────────────────────────────────────
CORS_ALLOWED_ORIGINS = os.getenv(
    'CORS_ALLOWED_ORIGINS', 'http://localhost:5173'
).split()

# ── Allauth ───────────────────────────────────────────────────────────────────
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
ACCOUNT_LOGIN_METHODS = {'username', 'email'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1*', 'password2*']
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.getenv('GOOGLE_CLIENT_ID'),
            'secret':    os.getenv('GOOGLE_CLIENT_SECRET'),
            'key': ''
        }
    }
}

# ── Africa's Talking ──────────────────────────────────────────────────────────
AT_API_KEY   = os.getenv('AT_API_KEY')
AT_USERNAME  = os.getenv('AT_USERNAME', 'sandbox')
AT_SENDER_ID = os.getenv('AT_SENDER_ID', 'AmakaziWatch')
AT_CALLER_ID = os.getenv('AT_CALLER_ID', '')

# ── M-Pesa Daraja ─────────────────────────────────────────────────────────────
MPESA_CONSUMER_KEY    = os.getenv('MPESA_CONSUMER_KEY')
MPESA_CONSUMER_SECRET = os.getenv('MPESA_CONSUMER_SECRET')
MPESA_SHORTCODE       = os.getenv('MPESA_SHORTCODE')
MPESA_PASSKEY         = os.getenv('MPESA_PASSKEY')
MPESA_CALLBACK_URL    = os.getenv('MPESA_CALLBACK_URL')
MPESA_ENV             = os.getenv('MPESA_ENV', 'sandbox')

# ── Google ────────────────────────────────────────────────────────────────────
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
YOUTUBE_API_KEY     = os.getenv('YOUTUBE_API_KEY')

# ── GROQ ─────────────────────────────────────────────────────────────────
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# ── Paystack ──────────────────────────────────────────────────────────────────
PAYSTACK_SECRET_KEY = os.getenv('PAYSTACK_SECRET_KEY')
PAYSTACK_PUBLIC_KEY = os.getenv('PAYSTACK_PUBLIC_KEY')

# ── Redis Cache ───────────────────────────────────────────────────────────────
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv("REDIS_URL", "redis://127.0.0.1:6379/1"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
CACHE_TTL = 60 * 5  # 5 minutes


# Media files for vault
MEDIA_URL = '/media/'
MEDIA_ROOT = '/secure_vault/'
# Add to amakaziwatch/settings.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_CACHE_RESPONSE': {
        'timeout': 300,  # 5 minutes
        'cache': 'default',
    },
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day'
    }
}
