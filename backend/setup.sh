# Create a virtual environment
virtualenv env

# Install dependencies from requirements.txt
env/bin/pip install -r requirements.txt


# Check if Django configured correctly
env/bin/python manage.py check

# Run tests
env/bin/python manage.py test

# Migrate models to defined db
env/bin/python manage.py migrate

# Load data 
env/bin/python manage.py loaddata dump.json

# Run the development server
env/bin/python manage.py runserver 8000
