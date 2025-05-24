from pathlib import Path
from src.utils.env import ENV
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent/"db.sqlite3"

DATABASES = {
    "default": (
        {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": ENV['POSTGRES_NAME'],
            "USER": ENV['POSTGRES_USER'],
            "PASSWORD": ENV['POSTGRES_PASSWORD'],
            "HOST": ENV['POSTGRES_HOST'],
            "PORT": ENV['POSTGRES_PORT'],
        }
        if not int(ENV['DEBUG'])
        else {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR,
        }
    )
}
