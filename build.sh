#!/bin/bash

# Build the project
python -m pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate