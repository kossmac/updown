# UpDown

## Requirements

- python3, pip

## Installation

1. Unzip package

    ``unzip updown.zip``

2. install virtual environment

    ``python -m venv env``

3. activate virtual environment

    ``source env/bin/activate``

4. install python packages

    ``pip install -r requirements.txt``

5. migrate database initially

    ``python manage.py migrate``

6. load admin fixtures

    ``python manage.py loaddata updown/fixtures/admin``

7. start django

    ``python manage.py runserver``

## Users installed by fixtures

- admin / adminadmin
- admin2 / adminadmin
- normaluser / adminadmin
