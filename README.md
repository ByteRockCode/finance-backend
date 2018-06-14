# ByteRock Finance Backend

[![Coverage Status](https://coveralls.io/repos/github/ByteRockCode/finance-backend/badge.svg?branch=master)](https://coveralls.io/github/ByteRockCode/finance-backend?branch=master)
[![Build Status](https://travis-ci.org/ByteRockCode/finance-backend.svg?branch=master)](https://travis-ci.org/ByteRockCode/finance-backend)

## Installation

```bash
mkdir -p ~/Dev/ByteRock
cd ~/Dev/ByteRock
git clone git@github.com:ByteRockCode/finance-backend.git

cd finance-backend
pipenv install --dev
sh scripts/database_build.sh
```


## Virtualenv

Create file `.env`

```
ALLOWED_HOSTS='*'
DATABASE_URL='postgres://postgres@localhost:5432/finance'
DJANGO_SETTINGS_MODULE='config.settings.development'
ENV='development'
SECRET_KEY='123456'
DEBUG_TOOLBAR=True
```


## Run server

```
pipenv run python manage.py runserver 0.0.0.0:8000
```
