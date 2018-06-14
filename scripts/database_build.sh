#!/bin/bash

python manage.py migrate
sh scripts/fixtures_load.sh
