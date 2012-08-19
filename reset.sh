#!/bin/bash

rm -rf media 
rm sqlite.db

python manage.py syncdb --migrate --noinput
python manage.py shell < _reset.input >> /dev/null
