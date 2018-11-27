# Cultidate Backend

## Initial Setup

Django REST Framework and various libraries defined in `requirements.txt` are utilized. Agents should have Python 3, pip and virtualenv initially.

- Create a virtual environment:

`virtualenv env`

- Activate the virtual environment:

`source env/bin/activate` or

`source env/Scripts/activate` for Windows

- Install dependencies from `requirements.txt`

`pip install -r requirements.txt`

- There should also be a `.env` file which some of Django parameters and API keys are kept. This file can be created manually with deployment specific variabled or gathered from the backend team.

## Running the Project

Check if Django configured correctly:

`./manage.py check`

Run local development server:

`./manage.py runserver 8000`

Make migration files:

`./manage.py makemigrations`

Migrate models to defined db:

`./manage.py migrate`

Use Django Shell:

`./manage.py shell`
