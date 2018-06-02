#!/bin/bash

echo "-----Apply database migrations-----"
python src/manage.py migrate

echo "-----Run tests-----"
python src/manage.py test

echo "-----Starting server-----"
python src/manage.py runserver 0.0.0.0:8000
