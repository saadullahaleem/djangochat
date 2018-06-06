# Django Channels Chat

A simple chat application made using Django channels. It has basic social authentication and a chat interface.

## Requirements

You'll need to have Redis and PostgreSQL installed for this app to work.

## Installation

- Install the necessary modules using pip.
```pip install -r requirements.txt```

- Add your PostgreSQL credentials to the settings file
    ```
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'chat_app',
            'USER': 'your_user',
            'PASSWORD': 'password',
            'PORT': 5432,
            'HOST': 'localhost'
        }
    }
    ```

- Run the migrations
```python manage.py migrate```

- Run the development server ```python manage.py runserver```