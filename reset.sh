#!/bin/bash

rm -rf data 
rm sqlite.db

python manage.py syncdb --migrate --noinput
python manage.py shell < reset.py >> /dev/null
