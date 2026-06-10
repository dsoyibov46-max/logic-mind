from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# Buni Railway Settings -> Variables qismiga qo'shib, bu yerda os.environ orqali olish xavfsizroq
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-*v%q(!=6@z)z@&wih^&jhbj@5_r&h$@(k-v3mgk(h^k(*b57og')

# Productionda har doim False bo'lishi kerak
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['*']

# ⚠️ Diqqat: Bu yerga Railway taqdim etgan hozirgi jonli domen manzilingizni yozing!
CSRF_TRUSTED_ORIGINS = [
    'https://logic-mind-production.up.railway.app', 
    'https://welcoming-fascination-production.up.railway.app' # Agar domen o'zgargan bo'lsa buni ham qo'shing
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',

    'main',
    'users',
    'classrooms',
    'game_app',
    'results',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Statik fayllar uchun
    'corsheaders.middleware.CorsMiddleware',       # ⬅️ MANA SHU QATOR QOLIB KETGAN EDI (Eng tepaga yaqin turishi shart)
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Railway PostgreSQL ulanishi uchun mukammal sozlama
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('PGDATABASE'),
        'USER': os.environ.get('PGUSER'),
        'PASSWORD': os.environ.get('PGPASSWORD'),
        'HOST': os.environ.get('PGHOST'),
        'PORT': os.environ.get('PGPORT', '5432'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator' },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Django 4.2+ va Django 6.0 uchun yangi standart statik fayllar ombori sozlamasi:
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'users.User'

CORS_ALLOW_ALL_ORIGINS = True

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/student/'
LOGOUT_REDIRECT_URL = '/login/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'