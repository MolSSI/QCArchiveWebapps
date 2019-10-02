[![Build Status](https://travis-ci.com/MolSSI/QCArchive_website.svg?token=66tFeohM6UiDzZMw65q9&branch=master)](https://travis-ci.com/MolSSI/QCArchive_website)
[![codecov](https://codecov.io/gh/MolSSI/QCArchive_website/branch/master/graph/badge.svg?token=xPgDkNsfxk)](https://codecov.io/gh/MolSSI/QCArchive_website)

QCArchive Website
=================

A full featured flask website, built with Flask, SQLAlchemy, Alembic, and Dash

How to run
===========

Run in shell:

```
conda create -n qca_web pip
conda activate qca_web
pip install -r requirements/dev.txt
sudo npm install -g less
```

Add environment-specific attributes to `.flaskenv` file, with key values that will be exported to the environment (dev, prod, etc). Use `.env` file for private variables.


Create the migrations folder if doesn't exists by: (usually not needed)
```
flask db init
```

Later, you can use migration commands, like `flask db migrate` to creare migrations.
 
Now, use upgrade command to create the DB if it doesn't exist and upgrade it if it exists:
```
flask db upgrade
```

To run the app, use: 
```
flask run
```
