#!/bin/bash

service nginx start
python3 manage.py collectstatic --noinput
sleep 1
python3 manage.py migrate
sleep 1
python3 manage.py makemigrations
sleep 1
python3 manage.py migrate
sleep 1
python3 manage.py initadmin
sleep 1
python3 manage.py runserver
