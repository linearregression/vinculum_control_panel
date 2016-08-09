# control_panel

## Getting Started

Make sure you are using a virtual environment of some sort (e.g. `virtualenv` or
`pyenv`).

```
pip install -r requirements.txt
./manage.py migrate
./manage.py loaddata sites
./manage.py runserver
```

## Creating Postgres Server configurations

    # create user vinculum_user with password '...';
    # create database vinculum owner vinculum_user;
    # alter user vinculum_user createdb;
    
Inside of the settings.py file create something like

    DB_PASSWORD = os.environ['DB_PASSWORD']

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'vinculum',
            'USER': 'vinculum_user',
            'PASSWORD': 'password',
            'HOST': 'localhost',
            'PORT': '',
        }
    }
    
