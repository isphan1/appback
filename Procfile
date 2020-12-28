release: python manage.py migrate
web: gunicorn wapps.wsgi:application --log-file - --log-level debug
