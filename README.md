# PurBeurre V2
> OpenClassrooms project 11 - <a href="https://openclassrooms.com/fr/paths/68-developpeur-dapplication-python">Python app devloper</a>
> Tags : Python, Openfoodfacts

## Run
- After installation, in your virtual environment use this command line :
```shell
$ pip python manage.py runserver
```

## Installation

### Clone

- HTTP > Clone this repo to your local machine using `https://github.com/TheodoraxX/projet11.git`
- SSH  > Clone this repo to your local machine using `git@github.com:TheodoraxX/projet11.git`

### Auto setup

- You can use requirements.txt file
```shell
$ pip install -r requirements.txt
```

### Manual setup

- Activate veritual env
```shell
$ python3 -m venv venv
```

- Activate the virtual environment
```shell
$ source venv/bin/activate
```

- Install Django 2.2.1
```shell
$ pip install django==2.2.1
```

- Install PostgreSQL 2.2.1
```shell
$ pip install postgres==2.2.2
```

- Install Requests 2.21.0
```shell
$ pip install postgres==2.21.0
```

- Install django-crispy-forms 1.7.2
- For more informations :
https://django-crispy-forms.readthedocs.io/en/latest/install.html

```shell
$ pip install django-crispy-forms==1.7.2
```

- Install pillow 6.0.0
- For more informations :
https://pillow.readthedocs.io/en/stable/

```shell
$ pip install pillow==6.0.0
```

- Install social-auth-app-django 3.1.0
- For more informations :
https://pypi.org/project/social-auth-app-django/

```shell
$ pip install social-auth-app-django==3.1.0
```

- Install coverage 4.5.3
```shell
$ pip install coverage==4.5.3
```

## Configuration

### Collect static

```shell
$ python manage.py collectstatic
```

### Create Django superuser

Use this command line :
```shell
$ python manage.py createsuperuser
```

### Settings

Go to purbeurreV2/settings/common.py
```shell
$ vi purbeurreV2/settings/common.py
```

- In 'Internationalization' change settings
- For more informations : https://docs.djangoproject.com/en/2.2/topics/i18n/timezones/#timezone
```shell
LANGUAGE_CODE 'fr-FR' # Change to your settings
TIME_ZONE = 'Europe/Paris' # Change to your settings
```

### Database

This application we use PostgreSQL but you can use another database, just change settings.

(!) For postgresql command line : Go to https://gist.github.com/Kartones/dd3ff5ec5ea238d4c546

- Admin database connection
```shell
$ sudo -u postgres psql
```

- Create app database
```shell
postgres=# CREATE DATABASE dbname;
```

- Create an database user
```shell
postgres=# CREATE USER username WITH PASSWORD 'userpassword';
```

- Change configurations like Django recommendations
https://docs.djangoproject.com/en/1.11/ref/databases/

```shell
postgres=# ALTER ROLE username SET client_encoding TO 'utf8';
```
```shell
postgres=# ALTER ROLE username SET default_transaction_isolation TO 'read committed';
```
```shell
postgres=# ALTER ROLE username SET timezone TO 'Europe/Paris';
```

- Grant all privileges to your new user on your database
```shell
postgres=# GRANT ALL PRIVILEGES ON DATABASE dbname TO username;
```

- Update development/production settings files
```shell
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dbname', # Add your new database name
        'USER': 'username', # Add your new user name
        'PASSWORD': 'userPass', # Add your new user password
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

- Launch migrations from the application root
```shell
$ python manage.py migrate
```

### Social auth

- Google Authentication
Go to : https://console.developers.google.com/projectselector2/apis/library?supportedpurview=project
and select your project.

## Managments commands

- Import products to database
```shell
$ python manage.py products_import
```

## Product

