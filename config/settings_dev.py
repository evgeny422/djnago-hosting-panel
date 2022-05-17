import os

from config.settings import BASE_DIR

SECRET_KEY = 'django-insecure-oo7t92o#3q9o2$wblqa(^fuo*lnwr$*9w@z@8*94y_svn%3z_b'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

bash_dir_path = os.path.join(BASE_DIR, 'bash')

base_salt = 'DTLWPDgsge1g5_3'
