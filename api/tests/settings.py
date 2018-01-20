DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory',
    }
}

INSTALLED_APPS = (
    'api',
)

SECRET_KEY = 'dummy'
