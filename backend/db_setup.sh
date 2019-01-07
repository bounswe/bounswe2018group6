# Migrate models to defined db
env/bin/python manage.py migrate

# Load data 
env/bin/python manage.py loaddata dump.json
