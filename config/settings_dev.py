import os

from config.settings import BASE_DIR

SECRET_KEY = ''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

bash_dir_path = os.path.join(BASE_DIR, 'bash')

base_salt = ''
