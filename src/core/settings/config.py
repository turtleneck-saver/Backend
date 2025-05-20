SECRET_KEY = 'django-insecure-4g5w1%_u8uzrj*r&35&)+hna=xd%nvuhw4k8)h(kgnftdf-!4n'

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_CREDENTIALS = True

WSGI_APPLICATION = 'src.core.wsgi.application'

ROOT_URLCONF = 'core.urls'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
