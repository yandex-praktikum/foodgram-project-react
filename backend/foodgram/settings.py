import os

from dotenv import load_dotenv
from decouple import Csv, config

load_dotenv()


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.getenv(
    'SECRET_KEY',
    default='django-insecure-051ek9e6-u)7oq=(bws@q0f1=vg$n66w81zlye2&mmue!is5ni'
)
# SECRET_KEY = "django-insecure-051ek9e6-u)7oq=(bws@q0f1=vg$n66w81zlye2&mmue!is5ni"

DEBUG = os.getenv('DEBUG', default='True')
ALLOWED_HOSTS = ['*']
# ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="*", cast=Csv())

# CSRF_TRUSTED_ORIGINS = config(
    # "CSRF_TRUSTED_ORIGINS",
    # default="http://localhost, http://127.0.0.1",
    # cast=Csv(),
# )


# ALLOWED_HOSTS = []
# ALLOWED_HOSTS = ['130.193.53.39', 'devinse.ru']
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = False

# CSRF_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = [
    'http://localhost',
    'http://localhost:8000',
]

# CORS_ALLOWED_ORIGINS = [
    # 'http://localhost:8000',
# ]

# CORS_ALLOW_ALL_ORIGINS = False

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "django_filters",
    "rest_framework.authtoken",
    "djoser",
    "api",
    "recipes",
    "users",
    # "corsheaders",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]




ROOT_URLCONF = "foodgram.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "foodgram.wsgi.application"


DATABASES = {
    "default": {
        'ENGINE': os.getenv('DB_ENGINE', default='django.db.backends.sqlite3'),
        # "ENGINE": os.getenv("DB_ENGINE", default="django.db.backends.postgresql"),
        'NAME': os.getenv('DB_NAME',
                          default=os.path.join(BASE_DIR, 'db.sqlite3')),
        # "NAME": os.getenv("DB_NAME", default="postgres"),
        # "USER": os.getenv("POSTGRES_USER", default="postgres"),
        # "PASSWORD": os.getenv("POSTGRES_PASSWORD", default="postgres"),
        # "HOST": os.getenv("DB_HOST", default="db"),
        # "PORT": os.getenv("DB_PORT", default="5432"),
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PAGINATION_CLASS": "api.pagination.CustomPageNumberPagination",
    "PAGE_SIZE": 6,
}


AUTH_USER_MODEL = "users.User"


DJOSER = {
    "LOGIN_FIELD": "email",
    "PERMISSIONS": {
        "user": ["rest_framework.permissions.IsAuthenticated"],
        "user_list": ["rest_framework.permissions.AllowAny"],
    },
    "SERIALIZERS": {
        "user": "api.serializers.CustomUserSerializer",
        "current_user": "api.serializers.CustomUserSerializer",
    },
}
