"""
Django settings for myproject project.
"""
import os
import cloudinary
import cloudinary.uploader
import cloudinary.api
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ===== ҚАУІПСІЗДІК =====
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-9pq5uc=y8ao-&dn2y1v^(^sr_6i8d$wo8qcqi@q1+_6w4r9s36')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = ['*']

# ===== ҚОСЫМШАЛАР =====
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary',           # ҚОСЫҢЫЗ
    'cloudinary_storage',   # ҚОСЫҢЫЗ
    'gallery',
]

# ===== MIDDLEWARE =====
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

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

WSGI_APPLICATION = 'myproject.wsgi.application'

# ===== ДЕРЕКҚОР =====
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ===== ҚҰПИЯ СӨЗДІ ТЕКСЕРУ =====
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ===== ТІЛДЕР =====
LANGUAGES = [
    ('kk', 'Қазақша'),
    ('ru', 'Русский'),
    ('en', 'English'),
]
LANGUAGE_CODE = 'kk'
TIME_ZONE = 'Asia/Almaty'
USE_I18N = True
USE_TZ = True

# ===== STATIC ЖӘНЕ MEDIA =====
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ===== CLOUDINARY =====
cloudinary.config(
    cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME', 'СІЗДІҢ_CLOUD_NAME'),
    api_key = os.environ.get('CLOUDINARY_API_KEY', 'СІЗДІҢ_API_KEY'),
    api_secret = os.environ.get('CLOUDINARY_API_SECRET', 'СІЗДІҢ_API_SECRET'),
    secure = True
)

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# ===== КІРУ/ШЫҒУ =====
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'gallery'
LOGOUT_REDIRECT_URL = 'login'

# ===== ФАЙЛ ЖҮКТЕУ ШЕКТЕУЛЕРІ =====
DATA_UPLOAD_MAX_NUMBER_FILES = 200
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10 MB