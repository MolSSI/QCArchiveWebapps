QCArchive Website
=================

A full featured flask website, built with Flask, SQLAlchemy, Alembic, and Dash

How to run
===========

Run in shell:

```
conda create -n qca_web pip
pip install -r requirements/dev.txt
conda activate qca_web
```

Create the environment-specific `.flaskenv` file, with key values that will be exported to the environment (dev, prod, etc). Use `.env` for private variables.

```
FLASK_APP=qcarchive_web.py
# any other customizations
```

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
