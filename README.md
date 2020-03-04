[![Build Status](https://travis-ci.com/MolSSI/QCArchive_webapps.svg?token=66tFeohM6UiDzZMw65q9&branch=master)](https://travis-ci.com/MolSSI/QCArchive_webapps)
[![codecov](https://codecov.io/gh/MolSSI/QCArchive_webapps/branch/master/graph/badge.svg?token=xPgDkNsfxk)](https://codecov.io/gh/MolSSI/QCArchive_webapps)

QCArchive Website Webapps
========================

A full featured flask website, built with Flask, MongoDB, Alembic (if using SQL backend), and Dash.
This repository serves the Webapps on the [QCArchive](https://qcarchive.molssi.org) website.
Pull requests are welcome for bug fixes or small features!
If interested, please reach out to us on Slack or an Issue here before starting a new web application.

**Note:** This repository is built to be a QCArchive end product and is not suitable as a library or for replicating.

How to run and use for development:
===================================

### Install Python requiremets:

Run in shell, create python env, and install requirements:

```bash
conda create -n qca_web -c rdkit rdkit pip
conda activate qca_web
pip install -r requirements/dev.txt
```

Or use conda env:

```bash
conda env create -f environment.yml 
conda activate qca_env
```

### Install JavaScript requirements:

Next, install Node (front-end), and install JS requirements, 
which will be fetched from package.json automatically. In Ubuntu:

```bash
sudo apt-get install nodejs
cd QCArchive_webapps
npm install
```

Note that whenever you add a new JS library, you must add it to the node requirments
by using `npm install mypackage --save` in the root `QCArchive_webapps/` folder.

### Database setup

1. Install mongodb based on your operating system from 
https://docs.mongodb.com/guides/server/install/

2. Create a `QCArchive_webapps/.env` file, and add your DB URI to the config file:
```.env
MONGO_URI='mongodb://usr_username:user_password@localhost:27017/qca_apps_db_dev'
```

Replace `user_username` and `user_password` with your own values from your installation. 
You don't have to create a database after your install mongodb because the application will do it later.


Note: In the future when you need to, add PUBLICALLY shared environment attributes to `.flaskenv` file, with key values that will be exported to the environment (dev, prod, etc).
Use `.env` file for private variables that won't be shared or pushed to Github. Note that `.env` overrides `.flaskenv`, and both override `config.py`.


### DB migration init (You shouldn't do it, skip this step)
The migrations folder was created initially by the following command 
(you shouldn't create it again):

```bash
flask db init
```

Later, you can use migration commands, like `flask db migrate` to creare migrations.
 

### Creare your DB

To run the website, use upgrade command to create the DB if it doesn't exist and 
upgrade it:

```bash
flask db upgrade
# or even better (as more deployment commands added):
flask deploy
```

### Run the local server

To run the website locally, use: 

```bash
flask run
```


## More resources:

1. For Docker deployment config example, check this
https://www.digitalocean.com/community/tutorials/how-to-set-up-flask-with-mongodb-and-docker
