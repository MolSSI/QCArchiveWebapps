[![Build Status](https://travis-ci.com/MolSSI/QCArchive_website.svg?token=66tFeohM6UiDzZMw65q9&branch=master)](https://travis-ci.com/MolSSI/QCArchive_website)
[![codecov](https://codecov.io/gh/MolSSI/QCArchive_website/branch/master/graph/badge.svg?token=xPgDkNsfxk)](https://codecov.io/gh/MolSSI/QCArchive_website)

QCArchive Website
=================

A full featured flask website, built with Flask, SQLAlchemy, Alembic, and Dash

How to run and use for development:
===================================

Run in shell, create python env, and install requirements:

```bash
conda create -n qca_web pip
conda activate qca_web
pip install -r requirements/dev.txt
```

Next, install Node (front-end),and the install requirements, 
which will be fetched from package.json automatically:

```bash
sudo apt-get install nodejs
npm install

```

Note that whenever you add a new JS library, you must add it to the node requirments
by using `npm install mypackage --save`.

Add environment-specific attributes to `.flaskenv` file, with key values that will be exported to the environment (dev, prod, etc). Use `.env` file for private variables.


The migrations folder was created initially by the following command 
(you shouldn't create it again):

```bash
flask db init
```

Now, you can use migration commands, like `flask db migrate` to creare migrations.
 
To run the website, use upgrade command to create the DB if it doesn't exist and 
upgrade it:

```bash
flask db upgrade
# or even better (as more deployment commands added):
flask deploy
```

To run the website locally, use: 

```bash
flask run
```
