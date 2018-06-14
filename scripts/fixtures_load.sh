#!/bin/sh

python manage.py loaddata fixtures/users.json
python manage.py loaddata expenses/fixtures/expenses.json
