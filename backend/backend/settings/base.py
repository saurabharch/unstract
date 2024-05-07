"""Django settings for backend project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path
from typing import Optional
from urllib.parse import quote_plus

from dotenv import find_dotenv, load_dotenv

missing_settings = []


def get_required_setting(
    setting_key: str, default: Optional[str] = None
) -> Optional[str]:
    """Get the value of an environment variable specified by the given key. Add
    missing keys to `missing_settings` so that exception can be raised at the
    end.

    Args:
        key (str): The key of the environment variable
        default (Optional[str], optional): Default value to return incase of
                                           env not found. Defaults to None.

    Returns:
        Optional[str]: The value of the environment variable if found,
                       otherwise the default value.
    """
    data = os.environ.get(setting_key, default)
    if not data:
        missing_settings.append(setting_key)
    return data


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load default log from env
DEFAULT_LOG_LEVEL = os.environ.get("DEFAULT_LOG_LEVEL", "INFO")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s] %(levelname)s %(name)s: %(message)s",
            "datefmt": "%d/%b/%Y %H:%M:%S",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": DEFAULT_LOG_LEVEL,  # Set the desired logging level here
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": DEFAULT_LOG_LEVEL,
        # Set the desired logging level here as well
    },
}


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

# Loading environment variables

WORKFLOW_ACTION_EXPIRATION_TIME_IN_SECOND = os.environ.get(
    "WORKFLOW_ACTION_EXPIRATION_TIME_IN_SECOND", 10800
)
WEB_APP_ORIGIN_URL = os.environ.get("WEB_APP_ORIGIN_URL", "http://localhost:3000")

LOGIN_NEXT_URL = os.environ.get("LOGIN_NEXT_URL", "http://localhost:3000/org")
LANDING_URL = os.environ.get("LANDING_URL", "http://localhost:3000/landing")
ERROR_URL = os.environ.get("ERROR_URL", "http://localhost:3000/error")

DJANGO_APP_BACKEND_URL = os.environ.get(
    "DJANGO_APP_BACKEND_URL", "http://localhost:8000"
)
INTERNAL_SERVICE_API_KEY = os.environ.get("INTERNAL_SERVICE_API_KEY")

GOOGLE_STORAGE_ACCESS_KEY_ID = os.environ.get("GOOGLE_STORAGE_ACCESS_KEY_ID")
GOOGLE_STORAGE_SECRET_ACCESS_KEY = os.environ.get("GOOGLE_STORAGE_SECRET_ACCESS_KEY")
UNSTRACT_FREE_STORAGE_BUCKET_NAME = os.environ.get(
    "UNSTRACT_FREE_STORAGE_BUCKET_NAME", "pandora-user-storage"
)
GOOGLE_STORAGE_BASE_URL = os.environ.get("GOOGLE_STORAGE_BASE_URL")
REDIS_USER = os.environ.get("REDIS_USER", "default")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", "")
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = os.environ.get("REDIS_PORT", "6379")
REDIS_DB = os.environ.get("REDIS_DB", "")
SESSION_EXPIRATION_TIME_IN_SECOND = os.environ.get(
    "SESSION_EXPIRATION_TIME_IN_SECOND", 3600
)
SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE", True)
CSRF_COOKIE_SECURE = os.environ.get("CSRF_COOKIE_SECURE", True)

PATH_PREFIX = os.environ.get("PATH_PREFIX", "api/v1").strip("/")
API_DEPLOYMENT_PATH_PREFIX = os.environ.get(
    "API_DEPLOYMENT_PATH_PREFIX", "deployment"
).strip("/")

DB_NAME = os.environ.get("DB_NAME", "unstract_db")
DB_USER = os.environ.get("DB_USER", "unstract_dev")
DB_HOST = os.environ.get("DB_HOST", "backend-db-1")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "unstract_pass")
DB_PORT = os.environ.get("DB_PORT", 5432)

DEFAULT_ORGANIZATION = "default_org"
FLIPT_BASE_URL = os.environ.get("FLIPT_BASE_URL", "http://localhost:9005")
PLATFORM_HOST = os.environ.get("PLATFORM_SERVICE_HOST", "http://localhost")
PLATFORM_PORT = os.environ.get("PLATFORM_SERVICE_PORT", 3001)
PROMPT_HOST = os.environ.get("PROMPT_HOST", "http://localhost")
PROMPT_PORT = os.environ.get("PROMPT_PORT", 3003)
PROMPT_STUDIO_FILE_PATH = os.environ.get(
    "PROMPT_STUDIO_FILE_PATH", "/app/prompt-studio-data"
)
X2TEXT_HOST = os.environ.get("X2TEXT_HOST", "http://localhost")
X2TEXT_PORT = os.environ.get("X2TEXT_PORT", 3004)
STRUCTURE_TOOL_IMAGE_URL = get_required_setting("STRUCTURE_TOOL_IMAGE_URL")
STRUCTURE_TOOL_IMAGE_NAME = get_required_setting("STRUCTURE_TOOL_IMAGE_NAME")
STRUCTURE_TOOL_IMAGE_TAG = get_required_setting("STRUCTURE_TOOL_IMAGE_TAG")
WORKFLOW_DATA_DIR = os.environ.get("WORKFLOW_DATA_DIR")
API_STORAGE_DIR = os.environ.get("API_STORAGE_DIR")
CACHE_TTL_SEC = os.environ.get("CACHE_TTL_SEC", 10800)

DEFAULT_AUTH_USERNAME = os.environ.get("DEFAULT_AUTH_USERNAME", "unstract")
DEFAULT_AUTH_PASSWORD = os.environ.get("DEFAULT_AUTH_PASSWORD", "unstract")
SYSTEM_ADMIN_USERNAME = get_required_setting("SYSTEM_ADMIN_USERNAME")
SYSTEM_ADMIN_PASSWORD = get_required_setting("SYSTEM_ADMIN_PASSWORD")
SYSTEM_ADMIN_EMAIL = get_required_setting("SYSTEM_ADMIN_EMAIL")
SESSION_COOKIE_AGE = int(get_required_setting("SESSION_COOKIE_AGE", "86400"))
ENABLE_LOG_HISTORY = get_required_setting("ENABLE_LOG_HISTORY")
LOG_HISTORY_CONSUMER_INTERVAL = int(
    get_required_setting("LOG_HISTORY_CONSUMER_INTERVAL", "60")
)
LOGS_BATCH_LIMIT = int(get_required_setting("LOGS_BATCH_LIMIT", "30"))

# Flag to Enable django admin
ADMIN_ENABLED = False

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_required_setting("DJANGO_SECRET_KEY")
ENCRYPTION_KEY = get_required_setting("ENCRYPTION_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]
CSRF_TRUSTED_ORIGINS = [WEB_APP_ORIGIN_URL]
CORS_ALLOW_ALL_ORIGINS = False


# Application definition
SHARED_APPS = (
    # Multitenancy
    "django_tenants",
    "corsheaders",
    # For the organization model
    "account",
    # Django apps should go below this line
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admindocs",
    # Third party apps should go below this line,
    "rest_framework",
    # Connector OAuth
    "connector_auth",
    "social_django",
    # Doc generator
    "drf_yasg",
    "docs",
    # Plugins
    "plugins",
    "feature_flag",
    "django_celery_beat",
)

TENANT_APPS = (
    # your tenant-specific apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "tenant_account",
    "project",
    "prompt",
    "connector",
    "adapter_processor",
    "file_management",
    "workflow_manager.endpoint",
    "workflow_manager.workflow",
    "tool_instance",
    "pipeline",
    "platform_settings",
    "api",
    "prompt_studio.prompt_profile_manager",
    "prompt_studio.prompt_studio",
    "prompt_studio.prompt_studio_core",
    "prompt_studio.prompt_studio_registry",
    "prompt_studio.prompt_studio_output_manager",
    "prompt_studio.prompt_studio_document_manager",
    "prompt_studio.prompt_studio_index_manager",
)

INSTALLED_APPS = list(SHARED_APPS) + [
    app for app in TENANT_APPS if app not in SHARED_APPS
]
DEFAULT_MODEL_BACKEND = "django.contrib.auth.backends.ModelBackend"
GOOGLE_MODEL_BACKEND = "social_core.backends.google.GoogleOAuth2"

AUTHENTICATION_BACKENDS = (
    DEFAULT_MODEL_BACKEND,
    GOOGLE_MODEL_BACKEND,
)

TENANT_MODEL = "account.Organization"
TENANT_DOMAIN_MODEL = "account.Domain"
AUTH_USER_MODEL = "account.User"
PUBLIC_ORG_ID = "public"

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django_tenants.middleware.TenantSubfolderMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "account.custom_auth_middleware.CustomAuthMiddleware",
    "middleware.exception.ExceptionLoggingMiddleware",
    "social_django.middleware.SocialAuthExceptionMiddleware",
    "middleware.remove_allow_header.RemoveAllowHeaderMiddleware",
]

PUBLIC_SCHEMA_URLCONF = "backend.public_urls"
ROOT_URLCONF = "backend.urls"
TENANT_SUBFOLDER_PREFIX = f"/{PATH_PREFIX}/unstract"
SHOW_PUBLIC_IF_NO_TENANT_FOUND = True

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

WSGI_APPLICATION = "backend.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django_tenants.postgresql_backend",
        "NAME": f"{DB_NAME}",
        "USER": f"{DB_USER}",
        "HOST": f"{DB_HOST}",
        "PASSWORD": f"{DB_PASSWORD}",
        "PORT": f"{DB_PORT}",
        "ATOMIC_REQUESTS": True,
    }
}

DATABASE_ROUTERS = ("django_tenants.routers.TenantSyncRouter",)

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SERIALIZER": "django_redis.serializers.json.JSONSerializer",
            "DB": REDIS_DB,
            "USERNAME": REDIS_USER,
            "PASSWORD": REDIS_PASSWORD,
        },
        "KEY_FUNCTION": "utils.redis_cache.custom_key_function",
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

RQ_QUEUES = {
    "default": {"USE_REDIS_CACHE": "default"},
}

# Used for asynchronous/Queued execution
# Celery based scheduler
CELERY_BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"

# CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:{REDIS_PORT}/1"
# Postgres as result backend
CELERY_RESULT_BACKEND = (
    f"db+postgresql://{DB_USER}:{quote_plus(DB_PASSWORD)}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"
CELERY_TASK_MAX_RETRIES = 3
CELERY_TASK_RETRY_BACKOFF = 60  # Time in seconds before retrying the task

# Feature Flag
FEATURE_FLAG_SERVICE_URL = {"evaluate": f"{FLIPT_BASE_URL}/api/v1/flags/evaluate/"}

SCHEDULER_KWARGS = {
    "coalesce": True,
    "misfire_grace_time": 300,
    "max_instances": 1,
    "replace_existing": True,
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation."
        "UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation." "MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation." "CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation." "NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_URL = f"/{PATH_PREFIX}/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [],  # TODO: Update once auth is figured
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    "EXCEPTION_HANDLER": "middleware.exception.drf_logging_exc_handler",
}

# These paths will work without authentication
WHITELISTED_PATHS_LIST = [
    "/login",
    "/home",
    "/callback",
    "/favicon.ico",
    "/logout",
    "/signup",
    "/static",
]
WHITELISTED_PATHS = [f"/{PATH_PREFIX}{PATH}" for PATH in WHITELISTED_PATHS_LIST]
# White lists workflow-api-deployment path
WHITELISTED_PATHS.append(f"/{API_DEPLOYMENT_PATH_PREFIX}")


# API Doc Generator Settings
# https://drf-yasg.readthedocs.io/en/stable/settings.html
REDOC_SETTINGS = {
    "PATH_IN_MIDDLE": True,
    "REQUIRED_PROPS_FIRST": True,
}

# Social Auth Settings
SOCIAL_AUTH_LOGIN_REDIRECT_URL = f"{WEB_APP_ORIGIN_URL}/oauth-status/?status=success"
SOCIAL_AUTH_LOGIN_ERROR_URL = f"{WEB_APP_ORIGIN_URL}/oauth-status/?status=error"
SOCIAL_AUTH_EXTRA_DATA_EXPIRATION_TIME_IN_SECOND = os.environ.get(
    "SOCIAL_AUTH_EXTRA_DATA_EXPIRATION_TIME_IN_SECOND", 3600
)
SOCIAL_AUTH_USER_MODEL = "account.User"
SOCIAL_AUTH_STORAGE = "connector_auth.models.ConnectorDjangoStorage"
SOCIAL_AUTH_JSONFIELD_ENABLED = True
SOCIAL_AUTH_URL_NAMESPACE = "social"
SOCIAL_AUTH_FIELDS_STORED_IN_SESSION = ["oauth-key", "connector-guid"]
SOCIAL_AUTH_TRAILING_SLASH = False

for key in [
    "GOOGLE_OAUTH2_KEY",
    "GOOGLE_OAUTH2_SECRET",
]:
    exec("SOCIAL_AUTH_{key} = os.environ.get('{key}')".format(key=key))

SOCIAL_AUTH_PIPELINE = (
    # Checks if user is authenticated
    "connector_auth.pipeline.common.check_user_exists",
    # Gets user details from provider
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    # Cache secrets and fields in redis
    "connector_auth.pipeline.common.cache_oauth_creds",
)

# Social Auth: Google OAuth2
# Default takes care of sign in flow which we don't need for connectors
SOCIAL_AUTH_GOOGLE_OAUTH2_IGNORE_DEFAULT_SCOPE = True
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/drive",
]
SOCIAL_AUTH_GOOGLE_OAUTH2_AUTH_EXTRA_ARGUMENTS = {
    "access_type": "offline",
    "include_granted_scopes": "true",
    "prompt": "consent",
}
SOCIAL_AUTH_GOOGLE_OAUTH2_USE_UNIQUE_USER_ID = True


# Always keep this line at the bottom of the file.
if missing_settings:
    ERROR_MESSAGE = "Below required settings are missing.\n" + ",\n".join(
        missing_settings
    )
    raise ValueError(ERROR_MESSAGE)
