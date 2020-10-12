# votepizza

[![Build Status](https://travis-ci.com/rozumalex/votepizza.svg?branch=main)](https://travis-ci.org/github/rozumalex/votepizza)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/rozumalex/votepizza/blob/master/LICENSE)
[![codecov](https://codecov.io/gh/rozumalex/votepizza/branch/main/graph/badge.svg)](https://codecov.io/gh/rozumalex/votepizza)

RESTful app for voting for the best pizza

---

## Installation Guide
To get a copy of votepizza app to your device, please follow next steps:

### Clone the project to your local machine
```
git clone https://github.com/rozumalex/votepizza
```

### Install poetry and dependencies
***Note:*** you should change the directory to project's folder to install dependencies

```
pip install poetry
poetry install
poetry shell
```

### Install PostgreSQL, then create database and user
```
sudo apt install postgresql libpq-dev python-dev
sudo -u postgres psql

CREATE DATABASE votepizza_db;
CREATE USER votepizza_user with encrypted password 'votepizza_pass';
GRANT ALL PRIVILEGES ON DATABASE votepizza_db TO votepizza_user;
```
***Note:*** then press Ctrl+D

### Create .env file
```
cd printacc
nano .env
```

### And insert following values:
```
DEBUG=True
SECRET_KEY="dev"
DATABASE_URL=psql://votepizza_user:votepizza_pass@127.0.0.1:5432/votepizza_db
```
***Note:*** then press Ctrl+X and save changes

### Apply migrations to database
```
python manage.py migrate
```

### Run server
```
python manage.py runserver
```

## License
This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/rozumalex/votepizza/blob/master/LICENSE) file for details.
