#!/bin/bash

rm game/migrations/0001_initial.py
rm member/migrations/0001_initial.py

python manage.py schemamigration game --init
python manage.py schemamigration member --init
