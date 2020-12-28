release: python manage.py migrate
web: gunicorn dr.wsgi:application --log-file - --log-level debug
